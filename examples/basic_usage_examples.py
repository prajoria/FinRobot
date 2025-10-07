#!/usr/bin/env python3
"""
FinRobot Usage Examples
=======================

This file demonstrates practical usage of FinRobot for various financial analysis tasks.
Make sure you have configured OAI_CONFIG_LIST and config_api_keys before running.

Author: AI Assistant
Date: October 2025
"""

import autogen
import os
import sys
from datetime import datetime, timedelta
from textwrap import dedent

# Add the parent directory to Python path to import finrobot
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from finrobot.utils import get_current_date, register_keys_from_json
from finrobot.agents.workflow import SingleAssistant, SingleAssistantShadow

def setup_environment():
    """Set up the basic environment for FinRobot"""
    print("🚀 Setting up FinRobot environment...")
    
    # Check if config files exist
    config_files = {
        "OAI_CONFIG_LIST": "OAI_CONFIG_LIST",
        "config_api_keys": "config_api_keys"
    }
    
    for name, path in config_files.items():
        if not os.path.exists(path):
            print(f"❌ Missing {name} file at {path}")
            print(f"Please copy {name}_sample to {name} and configure it")
            return False
    
    # Basic LLM configuration - supports both OpenAI and Azure OpenAI
    try:
        # Try to load config and filter for available models
        config_list = autogen.config_list_from_json("OAI_CONFIG_LIST")
        
        # Check what models are available
        available_models = [config.get("model", "") for config in config_list]
        print(f"📋 Available models: {available_models}")
        
        # Prefer GPT-4o as primary model, with Azure OpenAI fallbacks
        preferred_models = ["gpt-4o", "gpt-4-turbo", "gpt-4-0125-preview", "gpt-35-turbo"]
        selected_model = None
        
        for model in preferred_models:
            if model in available_models:
                selected_model = model
                break
        
        if not selected_model:
            selected_model = available_models[0] if available_models else "gpt-4o"
        
        print(f"🎯 Using model: {selected_model}")
        
        llm_config = {
            "config_list": autogen.config_list_from_json(
                "OAI_CONFIG_LIST",
                filter_dict={"model": [selected_model]},
            ),
            "timeout": 120,
            "temperature": 0,
        }
    except Exception as e:
        print(f"❌ Error loading model config: {e}")
        print("💡 Make sure OAI_CONFIG_LIST is properly configured")
        return False
    
    # Register API keys
    try:
        register_keys_from_json("config_api_keys")
        print("✅ API keys registered successfully")
    except Exception as e:
        print(f"❌ Error registering API keys: {e}")
        return False
    
    print("✅ Environment setup complete!")
    return llm_config

def example_1_market_analysis():
    """
    Example 1: Market Analysis and Stock Prediction
    
    This example shows how to use the Market_Analyst agent to:
    - Analyze a specific stock (NVDA)
    - Get current market data and news
    - Generate price prediction with supporting analysis
    """
    print("\n" + "="*60)
    print("📊 EXAMPLE 1: Market Analysis and Stock Prediction")
    print("="*60)
    
    llm_config = setup_environment()
    if not llm_config:
        return
    
    # Choose a stock to analyze
    company = "NVDA"  # NVIDIA
    
    # Create Market Analyst agent
    market_analyst = SingleAssistant(
        "Market_Analyst",
        llm_config,
        human_input_mode="NEVER",  # Fully automated
    )
    
    # Prepare analysis prompt
    analysis_prompt = f"""
    Use all the tools provided to retrieve information available for {company} upon {get_current_date()}.
    
    Please perform a comprehensive analysis including:
    1. Current financial metrics and recent performance
    2. Recent news sentiment and market developments
    3. Technical indicators and price trends
    4. Risk factors and potential concerns
    
    Then provide:
    - A rough prediction (e.g. up/down by X%) for next week
    - Confidence level (High/Medium/Low)
    - Key supporting factors for your prediction
    - Main risks to watch
    
    Keep the analysis concise but thorough.
    """
    
    print(f"🔍 Analyzing {company} stock...")
    print(f"📅 Analysis date: {get_current_date()}")
    print("\n🤖 Market Analyst is working...")
    
    try:
        # Run the analysis
        result = market_analyst.chat(analysis_prompt)
        print("\n✅ Analysis completed!")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")

def example_2_equity_research_report():
    """
    Example 2: Equity Research Report Generation
    
    This example demonstrates how to:
    - Generate a professional equity research report
    - Analyze SEC filings (10-K reports)
    - Create charts and visualizations
    - Generate PDF output
    """
    print("\n" + "="*60)
    print("📋 EXAMPLE 2: Equity Research Report Generation")
    print("="*60)
    
    llm_config = setup_environment()
    if not llm_config:
        return
    
    # Report parameters
    company = "Microsoft"
    fyear = "2023"
    
    # Create work directory for reports
    work_dir = "../reports"
    os.makedirs(work_dir, exist_ok=True)
    
    # Create Expert Investor agent (Shadow version has enhanced capabilities)
    expert_investor = SingleAssistantShadow(
        "Expert_Investor",
        llm_config,
        max_consecutive_auto_reply=None,
        human_input_mode="TERMINATE",
    )
    
    # Prepare report generation prompt
    report_prompt = dedent(f"""
        Create a comprehensive annual report for {company}'s {fyear} 10-K filing.
        
        Please follow this structure:
        1. Executive Summary
        2. Company Overview and Business Model
        3. Financial Performance Analysis
        4. Risk Assessment
        5. Financial Visualizations (charts and graphs)
        6. Investment Recommendation
        
        Requirements:
        - Use the tools available to gather SEC filings and financial data
        - Each section should be 400-450 words
        - Include relevant charts and visualizations
        - Generate a professional PDF report
        - Save all files in "{work_dir}"
        - Display any generated images in the chat
        
        Please explain your working plan before starting.
    """)
    
    print(f"📊 Generating equity research report for {company} ({fyear})")
    print(f"📁 Reports will be saved in: {work_dir}")
    print("\n🤖 Expert Investor is working...")
    
    try:
        # Generate the report
        result = expert_investor.chat(
            report_prompt, 
            use_cache=True, 
            max_turns=50,
            summary_method="last_msg"
        )
        print("\n✅ Report generation completed!")
        print(f"📁 Check {work_dir} for generated files")
        
    except Exception as e:
        print(f"❌ Error during report generation: {e}")

def example_3_custom_analysis():
    """
    Example 3: Custom Financial Analysis
    
    This example shows how to:
    - Create custom analysis queries
    - Use specific financial tools
    - Get targeted insights
    """
    print("\n" + "="*60)
    print("🎯 EXAMPLE 3: Custom Financial Analysis")
    print("="*60)
    
    llm_config = setup_environment()
    if not llm_config:
        return
    
    # Create Market Analyst for custom analysis
    analyst = SingleAssistant(
        "Market_Analyst",
        llm_config,
        human_input_mode="NEVER",
    )
    
    # Example custom analyses
    custom_analyses = [
        {
            "title": "Technology Sector Comparison",
            "prompt": """
            Compare the following technology stocks: AAPL, MSFT, GOOGL, NVDA.
            
            For each stock, provide:
            1. Current price and recent performance (1 month)
            2. Key financial metrics (P/E, revenue growth)
            3. Recent news sentiment
            4. Risk assessment
            
            Then rank them by investment attractiveness and explain your reasoning.
            """,
        },
        {
            "title": "Dividend Analysis",
            "prompt": """
            Analyze dividend-paying stocks: JNJ, PG, KO, MCD.
            
            For each stock, examine:
            1. Current dividend yield
            2. Dividend growth history
            3. Payout ratio sustainability
            4. Business stability
            
            Recommend the best dividend stock for long-term income investors.
            """,
        },
        {
            "title": "Market Sentiment Analysis",
            "prompt": """
            Analyze current market sentiment for the following themes:
            1. Artificial Intelligence stocks (NVDA, AMD, INTC)
            2. Electric Vehicle market (TSLA, F, GM)
            3. Cloud Computing (AMZN, MSFT, CRM)
            
            Identify which theme has the most positive outlook based on recent news and data.
            """,
        }
    ]
    
    # Run custom analyses
    for i, analysis in enumerate(custom_analyses, 1):
        print(f"\n🔍 Running Analysis {i}: {analysis['title']}")
        print("-" * 50)
        
        try:
            result = analyst.chat(analysis['prompt'])
            print(f"✅ {analysis['title']} completed!")
            
        except Exception as e:
            print(f"❌ Error in {analysis['title']}: {e}")

def example_4_portfolio_analysis():
    """
    Example 4: Portfolio Analysis
    
    This example demonstrates:
    - Portfolio composition analysis
    - Risk assessment
    - Performance evaluation
    - Rebalancing recommendations
    """
    print("\n" + "="*60)
    print("💼 EXAMPLE 4: Portfolio Analysis")
    print("="*60)
    
    llm_config = setup_environment()
    if not llm_config:
        return
    
    # Create Market Analyst for portfolio analysis
    portfolio_analyst = SingleAssistant(
        "Market_Analyst",
        llm_config,
        human_input_mode="NEVER",
    )
    
    # Sample portfolio
    portfolio = {
        "AAPL": 25,  # 25% allocation
        "MSFT": 20,  # 20% allocation
        "GOOGL": 15, # 15% allocation
        "AMZN": 15,  # 15% allocation
        "TSLA": 10,  # 10% allocation
        "NVDA": 10,  # 10% allocation
        "SPY": 5,    # 5% allocation (ETF for diversification)
    }
    
    # Portfolio analysis prompt
    portfolio_prompt = f"""
    Analyze the following portfolio composition:
    {chr(10).join([f'- {stock}: {allocation}%' for stock, allocation in portfolio.items()])}
    
    Please provide:
    
    1. PORTFOLIO OVERVIEW:
       - Total number of holdings
       - Sector diversification analysis
       - Geographic exposure
    
    2. RISK ANALYSIS:
       - Concentration risk assessment
       - Sector concentration
       - Correlation between holdings
       - Overall portfolio volatility estimate
    
    3. PERFORMANCE ANALYSIS:
       - Recent performance (1 month, 3 months)
       - Individual stock contributions
       - Compare vs benchmark (S&P 500)
    
    4. RECOMMENDATIONS:
       - Rebalancing suggestions
       - Risk reduction opportunities
       - Diversification improvements
       - Specific buy/sell recommendations
    
    5. MARKET OUTLOOK:
       - How current market conditions affect this portfolio
       - Upcoming earnings or events to watch
       - Suggested adjustments for next quarter
    
    Use all available tools to gather current data for each holding.
    """
    
    print("💼 Analyzing portfolio composition...")
    print("Holdings:", list(portfolio.keys()))
    print("\n🤖 Portfolio Analyst is working...")
    
    try:
        result = portfolio_analyst.chat(portfolio_prompt)
        print("\n✅ Portfolio analysis completed!")
        
    except Exception as e:
        print(f"❌ Error during portfolio analysis: {e}")

def main():
    """
    Main function to run FinRobot examples
    """
    print("🤖 FinRobot Usage Examples")
    print("=" * 60)
    print("This script demonstrates various ways to use FinRobot for financial analysis.")
    print("\nAvailable examples:")
    print("1. Market Analysis and Stock Prediction")
    print("2. Equity Research Report Generation") 
    print("3. Custom Financial Analysis")
    print("4. Portfolio Analysis")
    print("\n" + "=" * 60)
    
    # Check environment first
    if not os.path.exists("OAI_CONFIG_LIST"):
        print("❌ Please set up OAI_CONFIG_LIST file first")
        print("   Copy OAI_CONFIG_LIST_sample to OAI_CONFIG_LIST and add your OpenAI API key")
        return
    
    if not os.path.exists("config_api_keys"):
        print("❌ Please set up config_api_keys file first")
        print("   Copy config_api_keys_sample to config_api_keys and add your API keys")
        return
    
    # Run examples
    try:
        # Example 1: Market Analysis
        example_1_market_analysis()
        
        # Example 2: Report Generation (commented out as it takes longer)
        # example_2_equity_research_report()
        
        # Example 3: Custom Analysis
        example_3_custom_analysis()
        
        # Example 4: Portfolio Analysis
        example_4_portfolio_analysis()
        
        print("\n" + "=" * 60)
        print("🎉 All examples completed successfully!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n⚡ Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")

if __name__ == "__main__":
    main()