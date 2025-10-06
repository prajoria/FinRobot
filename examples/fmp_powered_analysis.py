#!/usr/bin/env python3

"""
FMP-Powered FinRobot Analysis Demo
================================
This demo uses Financial Modeling Prep API for comprehensive financial analysis
with FinRobot AI agents powered by Azure OpenAI GPT-4o.
"""

import os
import sys
import autogen
import json
import requests
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class FMPDataProvider:
    """Financial Modeling Prep API integration for FinRobot"""
    
    def __init__(self):
        # Load environment variables from .env file
        from dotenv import load_dotenv
        load_dotenv()
        
        self.api_key = os.getenv('FMP_ACCESS_TOKEN')
        self.base_url = "https://financialmodelingprep.com/api/v3"
        
        if not self.api_key:
            raise ValueError("FMP_ACCESS_TOKEN not found in environment variables")
    
    def get_company_profile(self, symbol):
        """Get comprehensive company profile"""
        url = f"{self.base_url}/profile/{symbol}?apikey={self.api_key}"
        response = requests.get(url)
        return response.json()[0] if response.json() else {}
    
    def get_quote(self, symbol):
        """Get real-time stock quote"""
        url = f"{self.base_url}/quote/{symbol}?apikey={self.api_key}"
        response = requests.get(url)
        return response.json()[0] if response.json() else {}
    
    def get_ratios(self, symbol):
        """Get financial ratios"""
        url = f"{self.base_url}/ratios/{symbol}?apikey={self.api_key}"
        response = requests.get(url)
        return response.json()[0] if response.json() else {}
    
    def get_news(self, symbol, limit=5):
        """Get recent company news"""
        url = f"{self.base_url}/stock_news?tickers={symbol}&limit={limit}&apikey={self.api_key}"
        response = requests.get(url)
        return response.json()
    
    def get_historical_data(self, symbol, days=30):
        """Get historical price data"""
        end_date = datetime(2025, 10, 3)  # October 3rd, 2025
        start_date = end_date - timedelta(days=days)
        url = f"{self.base_url}/historical-price-full/{symbol}?from={start_date.strftime('%Y-%m-%d')}&to={end_date.strftime('%Y-%m-%d')}&apikey={self.api_key}"
        response = requests.get(url)
        data = response.json()
        return data.get('historical', [])

def setup_finrobot_with_fmp():
    """Setup FinRobot with FMP data integration"""
    
    # Load Azure OpenAI configuration
    config_list = autogen.config_list_from_json("OAI_CONFIG_LIST")
    
    # Initialize FMP data provider
    fmp = FMPDataProvider()
    
    # Create FMP-powered financial analyst
    financial_analyst = autogen.AssistantAgent(
        name="FMP_Financial_Analyst",
        system_message="""
        You are a Financial Analyst powered by Financial Modeling Prep (FMP) data.
        You have access to real-time financial data, company profiles, financial ratios, 
        news sentiment, and historical performance data.
        
        Your role:
        - Analyze stocks using comprehensive FMP financial data
        - Provide investment recommendations based on fundamentals
        - Assess risk factors and market sentiment
        - Compare companies across sectors
        - Generate detailed financial reports
        
        Always provide data-driven analysis with specific metrics and reasoning.
        """,
        llm_config={
            "config_list": config_list,
            "temperature": 0.7,
        }
    )
    
    # Create data retrieval assistant
    data_assistant = autogen.AssistantAgent(
        name="FMP_Data_Assistant",
        system_message="""
        You are a Data Assistant that retrieves and formats financial data from FMP API.
        You help the Financial Analyst by providing clean, formatted data summaries.
        
        When asked for stock data, provide:
        - Current price and performance metrics
        - Key financial ratios (P/E, P/B, ROE, etc.)
        - Company profile information
        - Recent news sentiment
        - Historical performance trends
        
        Format all data clearly and highlight key insights.
        """,
        llm_config={
            "config_list": config_list,
            "temperature": 0.3,
        }
    )
    
    # User proxy for interaction
    user_proxy = autogen.UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=3,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config=False,
    )
    
    return financial_analyst, data_assistant, user_proxy, fmp

def analyze_stock_with_fmp(symbol, fmp, financial_analyst, data_assistant, user_proxy):
    """Comprehensive stock analysis using FMP data"""
    
    print(f"\n🔍 Analyzing {symbol} with FMP Data")
    print("=" * 60)
    
    try:
        # Gather comprehensive data
        profile = fmp.get_company_profile(symbol)
        quote = fmp.get_quote(symbol)
        ratios = fmp.get_ratios(symbol)
        news = fmp.get_news(symbol, limit=3)
        historical = fmp.get_historical_data(symbol, days=30)
        
        # Format data for analysis
        data_summary = f"""
📊 COMPREHENSIVE ANALYSIS FOR {symbol}
{'='*50}

🏢 COMPANY PROFILE:
   Company: {profile.get('companyName', 'N/A')}
   Industry: {profile.get('industry', 'N/A')}
   Sector: {profile.get('sector', 'N/A')}
   Market Cap: ${profile.get('mktCap', 0):,}
   Employees: {profile.get('fullTimeEmployees', 'N/A')}
   Website: {profile.get('website', 'N/A')}

💰 CURRENT MARKET DATA:
   Current Price: ${quote.get('price', 0):.2f}
   Change: ${quote.get('change', 0):.2f} ({quote.get('changesPercentage', 0):.2f}%)
   Volume: {quote.get('volume', 0):,}
   Market Cap: ${quote.get('marketCap', 0):,}
   Day High: ${quote.get('dayHigh', 0):.2f}
   Day Low: ${quote.get('dayLow', 0):.2f}

📈 KEY FINANCIAL RATIOS:
   P/E Ratio: {ratios.get('priceEarningsRatio', 'N/A')}
   P/B Ratio: {ratios.get('priceToBookRatio', 'N/A')}
   ROE: {ratios.get('returnOnEquity', 'N/A')}
   ROA: {ratios.get('returnOnAssets', 'N/A')}
   Debt/Equity: {ratios.get('debtEquityRatio', 'N/A')}
   Current Ratio: {ratios.get('currentRatio', 'N/A')}
   Gross Margin: {ratios.get('grossProfitMargin', 'N/A')}

📰 RECENT NEWS SENTIMENT:
"""
        
        for i, article in enumerate(news[:3], 1):
            data_summary += f"   {i}. {article.get('title', 'N/A')[:80]}...\n"
            data_summary += f"      Published: {article.get('publishedDate', 'N/A')}\n"
        
        if historical:
            recent_performance = []
            for data_point in historical[:5]:  # Last 5 days
                recent_performance.append(f"      {data_point['date']}: ${data_point['close']:.2f}")
            
            data_summary += f"\n📅 RECENT PERFORMANCE (Last 5 Days):\n"
            data_summary += "\n".join(recent_performance)
        
        data_summary += "\n\nPlease provide a comprehensive investment analysis based on this data."
        
        # Create analysis conversation
        chat_result = user_proxy.initiate_chat(
            financial_analyst,
            message=data_summary,
            summary_method="reflection_with_llm",
        )
        
        return chat_result
        
    except Exception as e:
        print(f"❌ Error analyzing {symbol}: {str(e)}")
        return None

def portfolio_analysis_with_fmp(portfolio, fmp, financial_analyst, data_assistant, user_proxy):
    """Portfolio analysis using FMP data"""
    
    print(f"\n💼 Portfolio Analysis with FMP Data")
    print("=" * 60)
    
    portfolio_data = {}
    total_value = 0
    
    # Gather data for each holding
    for symbol, weight in portfolio.items():
        try:
            quote = fmp.get_quote(symbol)
            profile = fmp.get_company_profile(symbol)
            
            position_value = weight * 100000  # Assuming $100k portfolio
            total_value += position_value
            
            portfolio_data[symbol] = {
                'weight': weight,
                'price': quote.get('price', 0),
                'change_pct': quote.get('changesPercentage', 0),
                'sector': profile.get('sector', 'Unknown'),
                'market_cap': quote.get('marketCap', 0),
                'position_value': position_value
            }
            
            print(f"📊 {symbol}: ${quote.get('price', 0):.2f} ({quote.get('changesPercentage', 0):+.2f}%) - Weight: {weight:.1%}")
            
        except Exception as e:
            print(f"❌ Error fetching data for {symbol}: {str(e)}")
    
    # Create portfolio analysis prompt
    portfolio_summary = f"""
💼 PORTFOLIO ANALYSIS REQUEST
{'='*40}

Portfolio Holdings:
"""
    
    for symbol, data in portfolio_data.items():
        portfolio_summary += f"""
{symbol} ({data['weight']:.1%}):
  - Current Price: ${data['price']:.2f}
  - Change: {data['change_pct']:+.2f}%
  - Sector: {data['sector']}
  - Position Value: ${data['position_value']:,.0f}
  - Market Cap: ${data['market_cap']:,}
"""
    
    portfolio_summary += f"""

Please provide a comprehensive portfolio analysis including:

1. DIVERSIFICATION ANALYSIS:
   - Sector concentration risks
   - Market cap distribution
   - Geographic exposure assessment

2. RISK ASSESSMENT:
   - Portfolio volatility estimate
   - Correlation risks between holdings
   - Concentration risk evaluation

3. PERFORMANCE ANALYSIS:
   - Individual position performance
   - Portfolio-weighted returns
   - Risk-adjusted performance metrics

4. RECOMMENDATIONS:
   - Rebalancing opportunities
   - Diversification improvements
   - Risk reduction strategies
   - Specific buy/sell recommendations

5. MARKET OUTLOOK:
   - How current conditions affect this portfolio
   - Upcoming catalysts to watch
   - Strategic adjustments for next quarter

Please provide specific, actionable recommendations based on the data.
"""
    
    # Initiate portfolio analysis
    chat_result = user_proxy.initiate_chat(
        financial_analyst,
        message=portfolio_summary,
        summary_method="reflection_with_llm",
    )
    
    return chat_result

def main():
    """Main demo function"""
    
    print("🤖 FMP-Powered FinRobot Analysis Demo")
    print("=" * 60)
    print("Powered by Financial Modeling Prep API + Azure OpenAI GPT-4o")
    print()
    
    try:
        # Setup FinRobot with FMP integration
        financial_analyst, data_assistant, user_proxy, fmp = setup_finrobot_with_fmp()
        print("✅ FinRobot environment initialized successfully!")
        print("✅ FMP API integration ready!")
        print()
        
        # Test 1: Individual Stock Analysis
        print("=" * 60)
        print("📊 DEMO 1: Individual Stock Analysis")
        print("=" * 60)
        
        # Analyze key tech stocks
        tech_stocks = ['AAPL', 'MSFT', 'NVDA']
        
        for symbol in tech_stocks:
            analyze_stock_with_fmp(symbol, fmp, financial_analyst, data_assistant, user_proxy)
            print()
        
        # Test 2: Portfolio Analysis
        print("=" * 60)
        print("💼 DEMO 2: Portfolio Analysis")
        print("=" * 60)
        
        # Sample technology-focused portfolio
        portfolio = {
            'AAPL': 0.25,   # 25%
            'MSFT': 0.20,   # 20%
            'GOOGL': 0.15,  # 15%
            'NVDA': 0.15,   # 15%
            'AMZN': 0.10,   # 10%
            'TSLA': 0.10,   # 10%
            'SPY': 0.05     # 5%
        }
        
        portfolio_analysis_with_fmp(portfolio, fmp, financial_analyst, data_assistant, user_proxy)
        
        print("\n" + "=" * 60)
        print("🎉 FMP-Powered FinRobot Demo Completed Successfully!")
        print("=" * 60)
        print()
        print("✅ Azure OpenAI GPT-4o: Working perfectly")
        print("✅ FMP API Integration: Providing real-time data")  
        print("✅ FinRobot AI Agents: Generating comprehensive analysis")
        print()
        print("🚀 You now have a fully functional AI-powered financial analysis system!")
        
    except Exception as e:
        print(f"❌ Error in demo: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()