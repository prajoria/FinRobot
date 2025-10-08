"""
SEC EDGAR Data Fetcher for Major Companies and ETFs

This script demonstrates how to use the sec-edgar library to fetch SEC filings
for major tech companies (AAPL, AMZN, MSFT, NVDA) and top S&P 500 ETFs.

Requirements:
- Install sec-edgar: pip install secedgar
- For Jupyter: pip install nest-asyncio

Author: FinRobot Team
Date: October 2025
"""

import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# Add the sec-edgar submodule to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'external', 'sec-edgar'))

# Import sec-edgar modules
from secedgar import filings, FilingType, CompanyFilings, CIKLookup
from secedgar.client import NetworkClient

# For Jupyter Notebook compatibility
try:
    import nest_asyncio
    nest_asyncio.apply()
    print("✅ nest_asyncio applied for Jupyter compatibility")
except ImportError:
    print("⚠️  nest_asyncio not installed. Install with: pip install nest_asyncio")

class SECDataFetcher:
    """SEC EDGAR data fetcher for companies and ETFs"""
    
    def __init__(self, user_agent="FinRobot SEC Fetcher (support@finrobot.ai)", download_dir="./sec_filings"):
        """
        Initialize the SEC data fetcher
        
        Args:
            user_agent (str): User agent for SEC requests (required by SEC fair access policy)
            download_dir (str): Directory to save downloaded filings
        """
        self.user_agent = user_agent
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)
        
        # Major tech companies
        self.tech_companies = {
            "AAPL": "Apple Inc.",
            "AMZN": "Amazon.com Inc.",
            "MSFT": "Microsoft Corporation", 
            "NVDA": "NVIDIA Corporation"
        }
        
        # Top S&P 500 ETFs
        self.sp500_etfs = {
            "SPY": "SPDR S&P 500 ETF Trust",
            "VOO": "Vanguard S&P 500 ETF",
            "IVV": "iShares Core S&P 500 ETF",
            "VTI": "Vanguard Total Stock Market ETF",
            "QQQ": "Invesco QQQ Trust"
        }
        
        print(f"🏢 SEC Data Fetcher initialized")
        print(f"📁 Download directory: {self.download_dir.absolute()}")
        print(f"👤 User agent: {self.user_agent}")
    
    def lookup_ciks(self, tickers):
        """Look up CIK numbers for given tickers"""
        print(f"\n🔍 Looking up CIK numbers for: {', '.join(tickers)}")
        
        try:
            cik_lookup = CIKLookup(tickers, user_agent=self.user_agent)
            cik_dict = cik_lookup.ciks
            
            print("📋 CIK Lookup Results:")
            for ticker, cik in cik_dict.items():
                print(f"   {ticker}: {cik}")
            
            return cik_dict
            
        except Exception as e:
            print(f"❌ Error looking up CIKs: {e}")
            return {}
    
    def fetch_10k_filings(self, tickers, years_back=2):
        """
        Fetch 10-K annual reports for specified companies
        
        Args:
            tickers (list): List of ticker symbols
            years_back (int): Number of years back to fetch filings
        """
        print(f"\n📊 Fetching 10-K filings for {len(tickers)} companies...")
        
        # Calculate date range
        end_date = date.today()
        start_date = date(end_date.year - years_back, 1, 1)
        
        print(f"📅 Date range: {start_date} to {end_date}")
        
        try:
            # Create filings object
            my_filings = filings(
                cik_lookup=tickers,
                filing_type=FilingType.FILING_10K,
                start_date=start_date,
                end_date=end_date,
                user_agent=self.user_agent
            )
            
            # Create company-specific download directory
            company_dir = self.download_dir / "10K_filings"
            company_dir.mkdir(exist_ok=True)
            
            print(f"💾 Saving 10-K filings to: {company_dir}")
            
            # Download filings
            my_filings.save(str(company_dir))
            
            print("✅ 10-K filings downloaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error fetching 10-K filings: {e}")
            return False
    
    def fetch_10q_filings(self, tickers, quarters_back=4):
        """
        Fetch 10-Q quarterly reports for specified companies
        
        Args:
            tickers (list): List of ticker symbols  
            quarters_back (int): Number of quarters back to fetch
        """
        print(f"\n📈 Fetching 10-Q filings for {len(tickers)} companies...")
        
        # Calculate date range (approximately quarters_back * 3 months)
        end_date = date.today()
        start_date = end_date - timedelta(days=quarters_back * 90)
        
        print(f"📅 Date range: {start_date} to {end_date}")
        
        try:
            # Create filings object
            my_filings = filings(
                cik_lookup=tickers,
                filing_type=FilingType.FILING_10Q,
                start_date=start_date,
                end_date=end_date,
                user_agent=self.user_agent
            )
            
            # Create company-specific download directory
            company_dir = self.download_dir / "10Q_filings"
            company_dir.mkdir(exist_ok=True)
            
            print(f"💾 Saving 10-Q filings to: {company_dir}")
            
            # Download filings
            my_filings.save(str(company_dir))
            
            print("✅ 10-Q filings downloaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error fetching 10-Q filings: {e}")
            return False
    
    def fetch_8k_filings(self, tickers, days_back=30):
        """
        Fetch 8-K current reports (material events) for specified companies
        
        Args:
            tickers (list): List of ticker symbols
            days_back (int): Number of days back to fetch filings
        """
        print(f"\n📰 Fetching 8-K filings for {len(tickers)} companies...")
        
        # Calculate date range
        end_date = date.today()
        start_date = end_date - timedelta(days=days_back)
        
        print(f"📅 Date range: {start_date} to {end_date}")
        
        try:
            # Create filings object
            my_filings = filings(
                cik_lookup=tickers,
                filing_type=FilingType.FILING_8K,
                start_date=start_date,
                end_date=end_date,
                user_agent=self.user_agent
            )
            
            # Create company-specific download directory  
            company_dir = self.download_dir / "8K_filings"
            company_dir.mkdir(exist_ok=True)
            
            print(f"💾 Saving 8-K filings to: {company_dir}")
            
            # Download filings
            my_filings.save(str(company_dir))
            
            print("✅ 8-K filings downloaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error fetching 8-K filings: {e}")
            return False
    
    def fetch_individual_company_filings(self, ticker, filing_types=None, years_back=1):
        """
        Fetch multiple filing types for a single company
        
        Args:
            ticker (str): Company ticker symbol
            filing_types (list): List of FilingType enums
            years_back (int): Number of years back to fetch
        """
        if filing_types is None:
            filing_types = [FilingType.FILING_10K, FilingType.FILING_10Q, FilingType.FILING_8K]
        
        print(f"\n🏢 Fetching multiple filings for {ticker}...")
        
        # Calculate date range
        end_date = date.today()
        start_date = date(end_date.year - years_back, 1, 1)
        
        for filing_type in filing_types:
            try:
                print(f"   📄 Fetching {filing_type.value} filings...")
                
                company_filings = CompanyFilings(
                    cik_lookup=ticker,
                    filing_type=filing_type,
                    start_date=start_date,
                    end_date=end_date,
                    user_agent=self.user_agent
                )
                
                # Create filing-type specific directory
                filing_dir = self.download_dir / f"{ticker}_{filing_type.value}"
                filing_dir.mkdir(exist_ok=True)
                
                # Download filings
                company_filings.save(str(filing_dir))
                
                print(f"   ✅ {filing_type.value} filings saved to {filing_dir}")
                
            except Exception as e:
                print(f"   ❌ Error fetching {filing_type.value} for {ticker}: {e}")
    
    def get_filing_urls_only(self, tickers, filing_type=FilingType.FILING_10K, years_back=1):
        """
        Get URLs of filings without downloading (useful for inspection)
        
        Args:
            tickers (list): List of ticker symbols
            filing_type: Type of filing to get URLs for
            years_back (int): Number of years back
        """
        print(f"\n🔗 Getting {filing_type.value} URLs for: {', '.join(tickers)}")
        
        # Calculate date range
        end_date = date.today()
        start_date = date(end_date.year - years_back, 1, 1)
        
        try:
            my_filings = filings(
                cik_lookup=tickers,
                filing_type=filing_type,
                start_date=start_date,
                end_date=end_date,
                user_agent=self.user_agent
            )
            
            urls = my_filings.get_urls()
            
            print(f"📋 Found {len(urls)} {filing_type.value} filings:")
            for i, url in enumerate(urls[:10], 1):  # Show first 10
                print(f"   {i}. {url}")
            
            if len(urls) > 10:
                print(f"   ... and {len(urls) - 10} more")
            
            return urls
            
        except Exception as e:
            print(f"❌ Error getting URLs: {e}")
            return []

def main():
    """Main execution function"""
    print("🚀 SEC EDGAR Data Fetcher - FinRobot Edition")
    print("=" * 50)
    
    # Initialize fetcher
    fetcher = SECDataFetcher()
    
    # Define companies and ETFs to analyze
    tech_tickers = list(fetcher.tech_companies.keys())
    etf_tickers = list(fetcher.sp500_etfs.keys())
    all_tickers = tech_tickers + etf_tickers
    
    print(f"\n🎯 Target Companies: {', '.join(tech_tickers)}")
    print(f"🎯 Target ETFs: {', '.join(etf_tickers)}")
    
    # Look up CIK numbers
    cik_results = fetcher.lookup_ciks(all_tickers)
    
    if not cik_results:
        print("❌ Could not lookup CIK numbers. Exiting.")
        return
    
    # Example 1: Get recent 10-K filings for tech companies
    print("\n" + "="*50)
    print("📊 EXAMPLE 1: Recent 10-K Annual Reports")
    print("="*50)
    
    fetcher.fetch_10k_filings(tech_tickers, years_back=2)
    
    # Example 2: Get recent 10-Q filings for all companies
    print("\n" + "="*50)
    print("📈 EXAMPLE 2: Recent 10-Q Quarterly Reports")
    print("="*50)
    
    fetcher.fetch_10q_filings(tech_tickers, quarters_back=4)
    
    # Example 3: Get recent 8-K filings (current events)
    print("\n" + "="*50)
    print("📰 EXAMPLE 3: Recent 8-K Current Reports")
    print("="*50)
    
    fetcher.fetch_8k_filings(tech_tickers, days_back=60)
    
    # Example 4: Deep dive into AAPL filings
    print("\n" + "="*50)
    print("🍎 EXAMPLE 4: Apple Inc. (AAPL) Deep Dive")
    print("="*50)
    
    fetcher.fetch_individual_company_filings("AAPL", years_back=1)
    
    # Example 5: Just get URLs for ETF filings (inspection only)
    print("\n" + "="*50)
    print("🔗 EXAMPLE 5: ETF Filing URLs (No Download)")
    print("="*50)
    
    fetcher.get_filing_urls_only(etf_tickers, FilingType.FILING_10K, years_back=1)
    
    # Summary
    print("\n" + "="*50)
    print("✅ SEC Data Fetching Complete!")
    print("="*50)
    
    print(f"📁 All filings saved to: {fetcher.download_dir.absolute()}")
    print("\n📋 Next Steps:")
    print("   1. Review downloaded filings in the sec_filings directory")
    print("   2. Use FinRobot's analysis tools to process the documents")
    print("   3. Extract financial metrics and insights")
    print("   4. Generate comprehensive reports")
    
    # List downloaded files
    if fetcher.download_dir.exists():
        print(f"\n📂 Downloaded Files Structure:")
        for item in fetcher.download_dir.iterdir():
            if item.is_dir():
                file_count = len(list(item.glob("**/*")))
                print(f"   📁 {item.name}/ ({file_count} files)")

if __name__ == "__main__":
    main()