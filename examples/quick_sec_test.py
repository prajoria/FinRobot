"""
Quick SEC EDGAR Import Test

This script tests the correct import paths for sec-edgar components.
Run this to verify the installation is working properly.
"""

import os
import sys
from pathlib import Path

# Add sec-edgar to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'external', 'sec-edgar'))

def test_imports():
    """Test all the necessary imports"""
    
    print("🧪 Testing SEC EDGAR Imports")
    print("=" * 40)
    
    try:
        print("📦 Testing base secedgar import...")
        import secedgar
        print(f"✅ secedgar version: {secedgar.__version__}")
        
        print("📦 Testing FilingType import...")
        from secedgar import FilingType
        print(f"✅ FilingType: {FilingType.FILING_10K}")
        
        print("📦 Testing filings function import...")
        from secedgar import filings
        print("✅ filings function imported")
        
        print("📦 Testing CompanyFilings import...")
        from secedgar import CompanyFilings
        print("✅ CompanyFilings imported")
        
        print("📦 Testing CIKLookup import...")
        from secedgar.cik_lookup import CIKLookup
        print("✅ CIKLookup imported")
        
        print("📦 Testing NetworkClient import...")
        from secedgar.client import NetworkClient
        print("✅ NetworkClient imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Run: ./setup_sec_edgar.sh")
        print("   2. Check if all dependencies are installed")
        print("   3. Make sure you're in the FinRobot root directory")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_basic_functionality():
    """Test basic CIK lookup functionality"""
    
    print("\n🔍 Testing Basic CIK Lookup")
    print("=" * 40)
    
    try:
        from secedgar.cik_lookup import CIKLookup
        
        print("🍎 Looking up Apple (AAPL) CIK...")
        user_agent = "FinRobot Test (test@finrobot.ai)"
        
        lookup = CIKLookup("AAPL", user_agent=user_agent)
        cik = lookup.ciks
        
        print(f"✅ AAPL CIK: {cik}")
        
        if cik and "AAPL" in cik:
            print(f"✅ Successfully found Apple's CIK: {cik['AAPL']}")
            return True
        else:
            print("❌ Could not retrieve Apple's CIK")
            return False
            
    except Exception as e:
        print(f"❌ Error during CIK lookup: {e}")
        print("\n💡 This might be due to:")
        print("   - Missing dependencies (aiohttp, requests, etc.)")
        print("   - Network connectivity issues")
        print("   - SEC rate limiting")
        return False

def main():
    """Main test function"""
    
    print("🚀 SEC EDGAR Quick Import Test")
    print("=" * 50)
    
    # Test 1: Imports
    imports_ok = test_imports()
    
    if not imports_ok:
        print("\n❌ Import test failed. Please run setup first:")
        print("   ./setup_sec_edgar.sh")
        return
    
    # Test 2: Basic functionality
    functionality_ok = test_basic_functionality()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    if imports_ok and functionality_ok:
        print("🎉 All tests passed! SEC EDGAR is ready to use.")
        print("\n📋 Next steps:")
        print("   1. Run: python examples/sec_edgar_fetcher.py")
        print("   2. Check the sec_filings/ directory for downloads")
    elif imports_ok:
        print("⚠️  Imports work, but functionality test failed.")
        print("   This might be a network issue. Try running the main script.")
    else:
        print("❌ Import test failed. Please check the setup.")

if __name__ == "__main__":
    main()