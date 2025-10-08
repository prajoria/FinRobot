"""
Simple SEC EDGAR Test Script

This script tests basic functionality of the sec-edgar library
and demonstrates fetching filings for major companies.

Run this after setting up sec-edgar with: ./setup_sec_edgar.sh
"""

import os
import sys
from datetime import date, timedelta
from pathlib import Path

# Add sec-edgar to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'external', 'sec-edgar'))

def test_sec_edgar_basic():
    """Test basic sec-edgar functionality"""
    
    print("🧪 Testing SEC EDGAR Basic Functionality")
    print("=" * 40)
    
    try:
        # Test imports
        print("📦 Testing imports...")
        import secedgar
        from secedgar import FilingType
        from secedgar.cik_lookup import CIKLookup
        
        print(f"✅ secedgar version: {secedgar.__version__}")
        print(f"✅ FilingType imported: {FilingType.FILING_10K}")
        
        # Test CIK lookup
        print("\n🔍 Testing CIK lookup...")
        user_agent = "FinRobot Test (test@finrobot.ai)"
        
        lookup = CIKLookup("AAPL", user_agent=user_agent)
        cik = lookup.ciks
        print(f"✅ AAPL CIK: {cik}")
        
        # Test multiple lookups
        lookup_multi = CIKLookup(["AAPL", "MSFT"], user_agent=user_agent)
        ciks = lookup_multi.ciks  
        print(f"✅ Multiple CIKs: {ciks}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_filing_urls():
    """Test getting filing URLs without downloading"""
    
    print("\n🔗 Testing Filing URL Retrieval")
    print("=" * 40)
    
    try:
        from secedgar import filings, FilingType
        
        user_agent = "FinRobot Test (test@finrobot.ai)"
        
        # Get recent 10-K URLs for Apple
        end_date = date.today()
        start_date = date(end_date.year - 1, 1, 1)
        
        print(f"📅 Date range: {start_date} to {end_date}")
        print("🍎 Getting Apple 10-K URLs...")
        
        my_filings = filings(
            cik_lookup="AAPL",
            filing_type=FilingType.FILING_10K,
            start_date=start_date,
            end_date=end_date,
            user_agent=user_agent
        )
        
        urls = my_filings.get_urls()
        
        print(f"✅ Found {len(urls)} filing URLs:")
        for i, url in enumerate(urls[:3], 1):  # Show first 3
            print(f"   {i}. {url}")
        
        if len(urls) > 3:
            print(f"   ... and {len(urls) - 3} more")
            
        return True
        
    except Exception as e:
        print(f"❌ Error getting URLs: {e}")
        return False

def test_small_download():
    """Test downloading a small number of filings"""
    
    print("\n💾 Testing Small Filing Download")
    print("=" * 40)
    
    try:
        from secedgar import filings, FilingType
        
        user_agent = "FinRobot Test (test@finrobot.ai)"
        
        # Create test download directory
        download_dir = Path("./test_sec_filings")
        download_dir.mkdir(exist_ok=True)
        
        # Get very recent 8-K filings (small files, frequent)
        end_date = date.today()
        start_date = end_date - timedelta(days=7)  # Last 7 days only
        
        print(f"📅 Date range: {start_date} to {end_date}")
        print("📰 Downloading recent 8-K filings for Apple...")
        
        my_filings = filings(
            cik_lookup="AAPL",
            filing_type=FilingType.FILING_8K,
            start_date=start_date,
            end_date=end_date,
            user_agent=user_agent,
            count=2  # Limit to 2 filings max
        )
        
        # Download
        my_filings.save(str(download_dir))
        
        # Check what was downloaded
        files = list(download_dir.glob("**/*"))
        print(f"✅ Downloaded {len(files)} files:")
        for f in files[:5]:  # Show first 5
            if f.is_file():
                size_kb = f.stat().st_size / 1024
                print(f"   📄 {f.name} ({size_kb:.1f} KB)")
        
        print(f"📁 Files saved to: {download_dir.absolute()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error downloading: {e}")
        return False

def main():
    """Main test function"""
    
    print("🚀 SEC EDGAR Test Suite for FinRobot")
    print("=" * 50)
    
    tests = [
        ("Basic Functionality", test_sec_edgar_basic),
        ("Filing URLs", test_filing_urls),
        ("Small Download", test_small_download)
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
    
    if passed == len(results):
        print("🎉 All tests passed! SEC EDGAR is ready for use.")
        print("\n📋 Next steps:")
        print("   1. Run the full example: python examples/sec_edgar_fetcher.py")
        print("   2. Integrate SEC data with FinRobot analysis tools")
    else:
        print("⚠️  Some tests failed. Check the setup and try again.")
        print("   💡 Tip: Make sure to run ./setup_sec_edgar.sh first")

if __name__ == "__main__":
    main()