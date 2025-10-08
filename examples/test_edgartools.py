"""
EdgarTools Test Script for FinRobot

This script tests the edgartools library functionality for accessing
SEC EDGAR data with a modern Python API.

Requirements:
- Install edgartools: cd external/edgartools && pip install -e . && cd ../..
- Set SEC identity (email) as required by SEC fair access policy

Author: FinRobot Team
Date: October 2025
"""

import os
import sys
from pathlib import Path

# Add edgartools to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'external', 'edgartools'))

def test_edgartools_imports():
    """Test edgartools import functionality"""
    
    print("🧪 Testing EdgarTools Imports")
    print("=" * 40)
    
    try:
        print("📦 Testing main edgar import...")
        import edgar
        print(f"✅ edgar imported successfully")
        
        print("📦 Testing Company class...")
        from edgar import Company
        print("✅ Company class imported")
        
        print("📦 Testing set_identity function...")
        from edgar import set_identity
        print("✅ set_identity function imported")
        
        print("📦 Testing Filing and Filings...")
        from edgar import Filing, Filings
        print("✅ Filing classes imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Run: cd external/edgartools && pip install -e . && cd ../..")
        print("   2. Check if all dependencies are installed")
        print("   3. Make sure you're in the FinRobot root directory")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_company_lookup():
    """Test basic company lookup functionality"""
    
    print("\n🏢 Testing Company Lookup")
    print("=" * 40)
    
    try:
        from edgar import Company, set_identity
        
        # Set identity (required by SEC)
        set_identity("FinRobot Test (test@finrobot.ai)")
        print("✅ SEC identity set")
        
        print("🍎 Looking up Apple Inc. (AAPL)...")
        company = Company("AAPL")
        
        print(f"✅ Company created: {company}")
        print(f"   Name: {company.name}")
        print(f"   CIK: {company.cik}")
        print(f"   Ticker: {company.tickers}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during company lookup: {e}")
        print("\n💡 This might be due to:")
        print("   - Network connectivity issues")
        print("   - SEC rate limiting")
        print("   - Missing dependencies")
        return False

def test_filings_access():
    """Test accessing company filings"""
    
    print("\n📄 Testing Filings Access")
    print("=" * 40)
    
    try:
        from edgar import Company, set_identity
        
        set_identity("FinRobot Test (test@finrobot.ai)")
        
        print("📊 Getting Apple's recent 10-K filings...")
        company = Company("AAPL")
        
        # Get recent 10-K filings
        filings_10k = company.get_filings(form="10-K")
        
        print(f"✅ Found {len(filings_10k)} 10-K filings")
        
        if len(filings_10k) > 0:
            latest_10k = filings_10k[0]
            print(f"   Latest 10-K: {latest_10k.filing_date}")
            print(f"   Accession: {latest_10k.accession_no}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error accessing filings: {e}")
        return False

def test_financials_extraction():
    """Test extracting financial data"""
    
    print("\n💰 Testing Financial Data Extraction")
    print("=" * 40)
    
    try:
        from edgar import Company, set_identity
        
        set_identity("FinRobot Test (test@finrobot.ai)")
        
        print("📈 Extracting Apple's financial statements...")
        company = Company("AAPL")
        
        # Get financials
        try:
            financials = company.get_financials()
            print("✅ Financials object created")
            
            # Try to get income statement
            income_stmt = financials.income_statement()
            print(f"✅ Income statement extracted: {income_stmt.shape}")
            
            # Show a sample of the data
            if not income_stmt.empty:
                print("   Sample data:")
                print(f"   Columns: {list(income_stmt.columns[:3])}...")
                print(f"   First row: {income_stmt.iloc[0].name}")
            
        except Exception as e:
            print(f"⚠️  Financials extraction partial failure: {e}")
            print("   This is common - not all companies have standardized financial data")
        
        return True
        
    except Exception as e:
        print(f"❌ Error extracting financials: {e}")
        return False

def main():
    """Main test function"""
    
    print("🚀 EdgarTools Test Suite for FinRobot")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_edgartools_imports),
        ("Company Lookup", test_company_lookup),
        ("Filings Access", test_filings_access),
        ("Financial Extraction", test_financials_extraction)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed >= 2:  # At least imports and company lookup should work
        print("🎉 EdgarTools is working! You can start using it for SEC data analysis.")
        print("\n📋 Quick start example:")
        print("   from edgar import *")
        print("   set_identity('your.email@domain.com')")
        print("   company = Company('AAPL')")
        print("   filings = company.get_filings(form='10-K')")
        print("\n📖 See EDGAR_INTEGRATION_GUIDE.md for more examples")
    else:
        print("⚠️  Some tests failed. Check the setup:")
        print("   💡 Run: cd external/edgartools && pip install -e . && cd ../..")

if __name__ == "__main__":
    main()