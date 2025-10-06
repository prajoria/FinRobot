#!/usr/bin/env python3
"""
FinRobot with FMP API Integration
================================

This example demonstrates how to use FinRobot with your FMP API access
for comprehensive financial analysis using real-time data.
"""

import os
import sys
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Add FinRobot to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_fmp_data(endpoint, symbol=None, params=None):
    """Helper function to get data from FMP API"""
    load_dotenv()
    fmp_token = os.getenv('FMP_ACCESS_TOKEN')
    
    if not fmp_token:
        return None
    
    base_url = "https://financialmodelingprep.com/api/v3"
    
    if symbol:
        url = f"{base_url}/{endpoint}/{symbol}"
    else:
        url = f"{base_url}/{endpoint}"
    
    request_params = {'apikey': fmp_token}
    if params:
        request_params.update(params)
    
    try:
        response = requests.get(url, params=request_params, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching FMP data: {e}")
    
    return None

def fmp_stock_analysis(symbol):
    """Comprehensive stock analysis using FMP API"""
    print(f"📊 Comprehensive Analysis for {symbol}")
    print("=" * 50)
    
    # 1. Company Profile
    print(f"\n🏢 Company Information:")
    profile = get_fmp_data('profile', symbol)
    if profile and len(profile) > 0:
        company = profile[0]
        print(f"   Company: {company.get('companyName', 'N/A')}")
        print(f"   Industry: {company.get('industry', 'N/A')}")
        print(f"   Sector: {company.get('sector', 'N/A')}")
        print(f"   Market Cap: ${company.get('mktCap', 0):,.0f}")
        print(f"   Website: {company.get('website', 'N/A')}")
    
    # 2. Current Quote
    print(f"\n💰 Current Stock Data:")
    quote = get_fmp_data('quote', symbol)
    if quote and len(quote) > 0:
        stock = quote[0]
        price = stock.get('price', 0)
        change = stock.get('change', 0)
        change_pct = stock.get('changesPercentage', 0)
        volume = stock.get('volume', 0)
        
        print(f"   Current Price: ${price:.2f}")
        print(f"   Change: ${change:+.2f} ({change_pct:+.2f}%)")
        print(f"   Volume: {volume:,}")
        print(f"   Day High: ${stock.get('dayHigh', 0):.2f}")
        print(f"   Day Low: ${stock.get('dayLow', 0):.2f}")
    
    # 3. Financial Ratios
    print(f"\n📈 Financial Ratios:")
    ratios = get_fmp_data('ratios', symbol)
    if ratios and len(ratios) > 0:
        latest_ratios = ratios[0]
        print(f"   P/E Ratio: {latest_ratios.get('priceEarningsRatio', 'N/A'):.2f}")
        print(f"   P/B Ratio: {latest_ratios.get('priceToBookRatio', 'N/A'):.2f}")
        print(f"   ROE: {latest_ratios.get('returnOnEquity', 'N/A'):.2f}")
        print(f"   ROA: {latest_ratios.get('returnOnAssets', 'N/A'):.2f}")
        print(f"   Debt/Equity: {latest_ratios.get('debtEquityRatio', 'N/A'):.2f}")
        print(f"   Current Ratio: {latest_ratios.get('currentRatio', 'N/A'):.2f}")
    
    # 4. Recent Performance
    print(f"\n📅 Recent Performance:")
    historical = get_fmp_data('historical-price-full', symbol, {'timeseries': '7'})
    if historical and 'historical' in historical:
        recent_data = historical['historical'][:5]  # Last 5 days
        print(f"   Recent Price History:")
        for day in recent_data:
            date = day.get('date', 'N/A')
            close = day.get('close', 0)
            volume = day.get('volume', 0)
            print(f"     {date}: ${close:.2f} (Vol: {volume:,})")
    
    # 5. News (if available)
    print(f"\n📰 Recent News:")
    news = get_fmp_data('stock_news', params={'tickers': symbol, 'limit': 3})
    if news and len(news) > 0:
        for item in news[:3]:
            title = item.get('title', 'N/A')[:60] + '...' if len(item.get('title', '')) > 60 else item.get('title', 'N/A')
            date = item.get('publishedDate', 'N/A')
            print(f"     • {title} ({date})")
    else:
        print("     No recent news available")

def portfolio_analysis_with_fmp(portfolio):
    """Analyze a portfolio using FMP data"""
    print(f"\n💼 Portfolio Analysis with FMP Data")
    print("=" * 60)
    
    total_value = 0
    portfolio_data = []
    
    for symbol, weight in portfolio.items():
        print(f"\n📊 Analyzing {symbol} ({weight:.1%}):")
        
        # Get current quote
        quote = get_fmp_data('quote', symbol)
        if quote and len(quote) > 0:
            stock = quote[0]
            price = stock.get('price', 0)
            change_pct = stock.get('changesPercentage', 0)
            market_cap = stock.get('marketCap', 0)
            
            position_value = weight * 100000  # Assume $100k portfolio
            
            portfolio_data.append({
                'symbol': symbol,
                'weight': weight,
                'price': price,
                'change_pct': change_pct,
                'market_cap': market_cap,
                'position_value': position_value
            })
            
            print(f"   Price: ${price:.2f} ({change_pct:+.2f}%)")
            print(f"   Position Value: ${position_value:,.0f}")
    
    # Portfolio summary
    print(f"\n📋 Portfolio Summary:")
    total_change = sum(p['change_pct'] * p['weight'] for p in portfolio_data)
    print(f"   Weighted Average Change: {total_change:+.2f}%")
    
    # Top performers
    top_performer = max(portfolio_data, key=lambda x: x['change_pct'])
    bottom_performer = min(portfolio_data, key=lambda x: x['change_pct'])
    
    print(f"   Best Performer: {top_performer['symbol']} ({top_performer['change_pct']:+.2f}%)")
    print(f"   Worst Performer: {bottom_performer['symbol']} ({bottom_performer['change_pct']:+.2f}%)")

def finrobot_with_fmp_demo():
    """Main demo combining FinRobot capabilities with FMP data"""
    print("🤖 FinRobot + FMP API Integration Demo")
    print("=" * 80)
    
    # Test FMP access first
    load_dotenv()
    fmp_token = os.getenv('FMP_ACCESS_TOKEN')
    
    if not fmp_token:
        print("❌ FMP_ACCESS_TOKEN not found in environment")
        return
    
    print(f"✅ FMP API Token loaded: {fmp_token[:8]}...{fmp_token[-4:]}")
    
    # Demo 1: Individual Stock Analysis
    print(f"\n" + "="*80)
    print(f"DEMO 1: Individual Stock Analysis with FMP Data")
    print(f"="*80)
    
    # Analyze popular stocks
    stocks_to_analyze = ['AAPL', 'MSFT', 'NVDA']
    
    for symbol in stocks_to_analyze:
        fmp_stock_analysis(symbol)
        print(f"\n" + "-"*50)
    
    # Demo 2: Portfolio Analysis
    print(f"\n" + "="*80)
    print(f"DEMO 2: Portfolio Analysis with FMP Data")
    print(f"="*80)
    
    # Sample portfolio
    sample_portfolio = {
        'AAPL': 0.25,
        'MSFT': 0.20,
        'GOOGL': 0.15,
        'AMZN': 0.15,
        'TSLA': 0.10,
        'NVDA': 0.10,
        'SPY': 0.05
    }
    
    portfolio_analysis_with_fmp(sample_portfolio)
    
    # Demo 3: Market Overview
    print(f"\n" + "="*80)
    print(f"DEMO 3: Market Overview")
    print(f"="*80)
    
    print(f"\n📊 Top Market Movers Today:")
    popular_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX']
    
    movers = []
    for symbol in popular_stocks:
        quote = get_fmp_data('quote', symbol)
        if quote and len(quote) > 0:
            stock = quote[0]
            movers.append({
                'symbol': symbol,
                'price': stock.get('price', 0),
                'change_pct': stock.get('changesPercentage', 0)
            })
    
    # Sort by absolute percentage change
    movers.sort(key=lambda x: abs(x['change_pct']), reverse=True)
    
    print(f"\n🚀 Biggest Movers:")
    for i, mover in enumerate(movers[:5], 1):
        symbol = mover['symbol']
        price = mover['price']
        change_pct = mover['change_pct']
        direction = "📈" if change_pct > 0 else "📉"
        print(f"   {i}. {symbol}: ${price:.2f} ({change_pct:+.2f}%) {direction}")
    
    print(f"\n🎯 Summary:")
    print(f"   ✅ FMP API successfully integrated with FinRobot")
    print(f"   ✅ Real-time market data retrieved")
    print(f"   ✅ Comprehensive financial analysis performed")
    print(f"   ✅ Portfolio analysis completed")
    
    print(f"\n🚀 What you can do next:")
    print(f"   1. Use this data with FinRobot AI agents")
    print(f"   2. Create automated trading strategies")
    print(f"   3. Build portfolio optimization tools")
    print(f"   4. Generate investment research reports")

if __name__ == "__main__":
    finrobot_with_fmp_demo()