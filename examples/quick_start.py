#!/usr/bin/env python3
"""
FinRobot Quick Start Example
============================

A simple example to get started with FinRobot for stock analysis.

Before running this script:
1. Copy OAI_CONFIG_LIST_sample to OAI_CONFIG_LIST and add your OpenAI API key
2. Copy config_api_keys_sample to config_api_keys and add your FMP API key
3. Install FinRobot: pip install -e .

Usage:
    python quick_start.py

Author: AI Assistant  
Date: October 2025
"""

import os
import sys

def check_setup():
    """Check if FinRobot is properly configured"""
    print("🔍 Checking FinRobot setup...")
    
    # Check config files
    if not os.path.exists("../OAI_CONFIG_LIST"):
        print("❌ Missing OAI_CONFIG_LIST file")
        print("   → Copy OAI_CONFIG_LIST_sample to OAI_CONFIG_LIST")
        print("   → Add your OpenAI API key")
        return False
    
    if not os.path.exists("../config_api_keys"):
        print("❌ Missing config_api_keys file") 
        print("   → Copy config_api_keys_sample to config_api_keys")
        print("   → Add your FMP_API_KEY")
        return False
    
    # Try importing FinRobot
    try:
        import autogen
        from finrobot.utils import get_current_date, register_keys_from_json
        from finrobot.agents.workflow import SingleAssistant
        print("✅ FinRobot imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   → Install FinRobot: pip install -e .")
        print("   → Install dependencies: pip install -r requirements.txt")
        return False

def simple_stock_analysis():
    """Run a simple stock analysis example"""
    
    if not check_setup():
        return
    
    # Import after checking setup
    import autogen
    from finrobot.utils import get_current_date, register_keys_from_json
    from finrobot.agents.workflow import SingleAssistant
    
    print("\n🚀 Starting FinRobot Stock Analysis")
    print("=" * 50)
    
    # Setup configuration
    llm_config = {
        "config_list": autogen.config_list_from_json(
            "../OAI_CONFIG_LIST",
            filter_dict={"model": ["gpt-4-0125-preview"]},
        ),
        "timeout": 120,
        "temperature": 0,
    }
    
    # Register API keys
    try:
        register_keys_from_json("../config_api_keys")
        print("✅ API keys registered")
    except Exception as e:
        print(f"❌ API key error: {e}")
        return
    
    # Choose stock to analyze
    stock_symbol = "AAPL"  # Change this to analyze different stocks
    
    print(f"📊 Analyzing {stock_symbol} stock...")
    print(f"📅 Date: {get_current_date()}")
    
    # Create Market Analyst agent
    analyst = SingleAssistant(
        "Market_Analyst",
        llm_config,
        human_input_mode="NEVER",
    )
    
    # Simple analysis prompt
    prompt = f"""
    Analyze {stock_symbol} stock and provide:
    
    1. Current stock price and recent performance
    2. Key financial metrics (P/E ratio, market cap, etc.)
    3. Recent company news and developments
    4. Short-term outlook (next 1-2 weeks)
    5. Your recommendation (Buy/Hold/Sell) with reasoning
    
    Keep the analysis concise and actionable.
    """
    
    print("\n🤖 Market Analyst is working...")
    print("-" * 30)
    
    try:
        # Run the analysis
        result = analyst.chat(prompt)
        print(f"\n✅ Analysis for {stock_symbol} completed!")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        print("\nTroubleshooting tips:")
        print("- Check your OpenAI API key in OAI_CONFIG_LIST")
        print("- Verify FMP API key in config_api_keys")
        print("- Ensure you have internet connection")

def main():
    """Main function"""
    print("🤖 FinRobot Quick Start")
    print("=" * 30)
    print("This example demonstrates basic stock analysis using FinRobot.")
    print()
    
    simple_stock_analysis()
    
    print("\n" + "=" * 50)
    print("🎯 Next Steps:")
    print("1. Try changing the stock_symbol variable to analyze different stocks")
    print("2. Explore basic_usage_examples.py for more advanced examples")
    print("3. Check tutorials_beginner/ folder for Jupyter notebooks")
    print("4. Review the documentation for multi-agent workflows")

if __name__ == "__main__":
    main()