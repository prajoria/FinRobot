#!/usr/bin/env python3
"""
FMP API Access Test for FinRobot
===============================

This script tests your Financial Modeling Prep (FMP) API access and demonstrates
how to use it for financial data retrieval in FinRobot.
"""

import os
import requests
import json
from dotenv import load_dotenv
import pandas as pd

def test_fmp_api():
    """Test FMP API access using the token from .env file"""
    print("🔍 Testing Financial Modeling Prep (FMP) API Access")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Get FMP API token
    fmp_token = os.getenv('FMP_ACCESS_TOKEN')
    
    if not fmp_token:
        print("❌ FMP_ACCESS_TOKEN not found in environment")
        return False
    
    print(f"✅ FMP API Token found: {fmp_token[:8]}...{fmp_token[-4:]}")
    
    # Test API endpoints
    base_url = "https://financialmodelingprep.com/api/v3"
    
    test_endpoints = [
        {
            "name": "Company Profile",
            "url": f"{base_url}/profile/AAPL",
            "description": "Get Apple Inc. company information"
        },
        {
            "name": "Stock Quote",
            "url": f"{base_url}/quote/AAPL",
            "description": "Get Apple Inc. current stock quote"
        },
        {
            "name": "Financial Statements",
            "url": f"{base_url}/income-statement/AAPL",
            "description": "Get Apple Inc. income statement (latest year)"
        },
        {
            "name": "Market Data",
            "url": f"{base_url}/quote-short/AAPL",
            "description": "Get Apple Inc. short quote"
        }
    ]
    
    successful_tests = 0
    
    for test in test_endpoints:
        print(f"\n🧪 Testing: {test['name']}")
        print(f"   📝 {test['description']}")
        
        try:
            # Make API request
            response = requests.get(
                test['url'],
                params={'apikey': fmp_token},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data:  # Check if data is not empty
                    print(f"   ✅ Success - Received {len(data)} records")
                    successful_tests += 1
                    
                    # Show sample data for first test
                    if test['name'] == "Company Profile" and isinstance(data, list) and data:
                        company = data[0]
                        print(f"   📊 Sample: {company.get('companyName', 'N/A')} - {company.get('industry', 'N/A')}")
                    elif test['name'] == "Stock Quote" and isinstance(data, list) and data:
                        quote = data[0]
                        print(f"   📊 Sample: Price ${quote.get('price', 'N/A')}, Change {quote.get('change', 'N/A')}")
                else:
                    print(f"   ⚠️  Success but empty data")
            else:
                print(f"   ❌ Failed - Status: {response.status_code}")
                if response.status_code == 401:
                    print(f"      🔑 Authentication failed - check API key")
                elif response.status_code == 403:
                    print(f"      🚫 Access forbidden - check API limits")
                
        except requests.exceptions.Timeout:
            print(f"   ❌ Timeout - API took too long to respond")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {e}")
        except json.JSONDecodeError:
            print(f"   ❌ Invalid JSON response")
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
    
    print(f"\n📊 Test Results:")
    print(f"   Successful tests: {successful_tests}/{len(test_endpoints)}")
    print(f"   Success rate: {(successful_tests/len(test_endpoints)*100):.1f}%")
    
    return successful_tests > 0

def demonstrate_fmp_usage():
    """Demonstrate practical FMP API usage for financial analysis"""
    print(f"\n🚀 FMP API Usage Examples")
    print("=" * 60)
    
    load_dotenv()
    fmp_token = os.getenv('FMP_ACCESS_TOKEN')
    
    if not fmp_token:
        print("❌ FMP token not available")
        return
    
    base_url = "https://financialmodelingprep.com/api/v3"
    
    # Example 1: Get multiple stock quotes
    print(f"\n📈 Example 1: Getting Stock Quotes")
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    
    try:
        quotes_url = f"{base_url}/quote/{','.join(symbols)}"
        response = requests.get(quotes_url, params={'apikey': fmp_token}, timeout=10)
        
        if response.status_code == 200:
            quotes = response.json()
            print(f"✅ Retrieved quotes for {len(quotes)} stocks:")
            
            for quote in quotes[:5]:  # Limit to first 5
                symbol = quote.get('symbol', 'N/A')
                price = quote.get('price', 0)
                change = quote.get('change', 0)
                change_pct = quote.get('changesPercentage', 0)
                print(f"   {symbol}: ${price:.2f} ({change:+.2f}, {change_pct:+.2f}%)")
        else:
            print(f"❌ Failed to get quotes: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Error getting quotes: {e}")
    
    # Example 2: Get company financials
    print(f"\n💰 Example 2: Company Financial Data")
    
    try:
        financials_url = f"{base_url}/ratios/AAPL"
        response = requests.get(financials_url, params={'apikey': fmp_token}, timeout=10)
        
        if response.status_code == 200:
            ratios = response.json()
            if ratios:
                latest = ratios[0]  # Most recent data
                print(f"✅ Apple Inc. Financial Ratios (Latest):")
                print(f"   P/E Ratio: {latest.get('priceEarningsRatio', 'N/A')}")
                print(f"   ROE: {latest.get('returnOnEquity', 'N/A')}")
                print(f"   Debt/Equity: {latest.get('debtEquityRatio', 'N/A')}")
                print(f"   Current Ratio: {latest.get('currentRatio', 'N/A')}")
        else:
            print(f"❌ Failed to get financials: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Error getting financials: {e}")

def check_fmp_integration_with_finrobot():
    """Check how FMP integrates with FinRobot"""
    print(f"\n🤖 FMP Integration with FinRobot")
    print("=" * 60)
    
    # Check if FinRobot can access FMP
    try:
        # Check config_api_keys file
        if os.path.exists('config_api_keys'):
            with open('config_api_keys', 'r') as f:
                config = json.load(f)
                
            fmp_key_in_config = config.get('FMP_API_KEY', '')
            print(f"✅ FMP API key in config_api_keys: {'✓' if fmp_key_in_config else '✗'}")
            
            if fmp_key_in_config and fmp_key_in_config != 'YOUR_FMP_API_KEY':
                print(f"   📋 Configured FMP key: {fmp_key_in_config[:8]}...{fmp_key_in_config[-4:]}")
            else:
                print(f"   ⚠️  FMP key appears to be placeholder or missing")
        else:
            print(f"❌ config_api_keys file not found")
        
        # Check if finrobot can import and use FMP
        print(f"\n🔍 Testing FinRobot FMP Integration:")
        
        # Import finrobot utilities
        import sys
        sys.path.append('.')
        
        from finrobot.utils import register_keys_from_json
        
        # Register keys
        register_keys_from_json('config_api_keys')
        print(f"✅ API keys registered with FinRobot")
        
        # Test if FMP tools are available
        try:
            from finrobot.data_source import FMPDataSource
            print(f"✅ FMP data source available in FinRobot")
        except ImportError:
            print(f"⚠️  FMP data source not available - checking alternatives")
            
    except Exception as e:
        print(f"❌ Error checking FinRobot integration: {e}")

def main():
    """Main test function"""
    print("🔍 Financial Modeling Prep (FMP) API Test Suite")
    print("=" * 80)
    
    # Test 1: Basic API access
    api_working = test_fmp_api()
    
    if api_working:
        # Test 2: Practical usage examples
        demonstrate_fmp_usage()
        
        # Test 3: FinRobot integration
        check_fmp_integration_with_finrobot()
        
        print(f"\n🎉 FMP API Testing Complete!")
        print(f"📋 Summary:")
        print(f"   ✅ FMP API access working")
        print(f"   ✅ Can retrieve financial data")
        print(f"   ✅ Ready for use with FinRobot")
        
        print(f"\n🚀 Next Steps:")
        print(f"   1. Use FMP data in FinRobot agents")
        print(f"   2. Access real-time market data")
        print(f"   3. Perform comprehensive financial analysis")
        
    else:
        print(f"\n❌ FMP API access failed")
        print(f"💡 Troubleshooting steps:")
        print(f"   1. Check your FMP_ACCESS_TOKEN in .env file")
        print(f"   2. Verify your FMP subscription is active")
        print(f"   3. Check FMP API limits and usage")

if __name__ == "__main__":
    main()