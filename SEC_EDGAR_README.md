# SEC EDGAR Integration for FinRobot

This document explains how to use the SEC EDGAR integration to fetch financial filings for companies and ETFs.

## Overview

The SEC EDGAR integration allows you to:
- Download SEC filings (10-K, 10-Q, 8-K, etc.) for any publicly traded company
- Fetch filings for multiple companies at once
- Get filings for major tech companies: Apple (AAPL), Amazon (AMZN), Microsoft (MSFT), NVIDIA (NVDA)
- Retrieve filings for top S&P 500 ETFs: SPY, VOO, IVV, VTI, QQQ
- Process and analyze SEC documents using FinRobot's AI capabilities

## Quick Setup

### 1. Install Dependencies

Run the setup script:
```bash
./setup_sec_edgar.sh
```

Or install manually:
```bash
# Install from submodule (development version)
cd external/sec-edgar
pip install -e .
cd ../..

# Install additional dependencies
pip install nest-asyncio beautifulsoup4 aiohttp urllib3 requests lxml tqdm
```

### 2. Test Installation

```bash
python examples/test_sec_edgar.py
```

### 3. Run Full Example

```bash
python examples/sec_edgar_fetcher.py
```

## Usage Examples

### Basic Company Filing Fetch

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'external', 'sec-edgar'))

from secedgar import filings, FilingType
from datetime import date

# Fetch Apple's recent 10-K annual reports
my_filings = filings(
    cik_lookup="AAPL",
    filing_type=FilingType.FILING_10K,
    start_date=date(2022, 1, 1),
    end_date=date.today(),
    user_agent="Your Name (your.email@domain.com)"
)

# Save to directory
my_filings.save('./sec_filings/apple_10k')
```

### Multiple Companies

```python
# Fetch 10-Q filings for multiple tech companies
tech_companies = ["AAPL", "MSFT", "AMZN", "NVDA"]

my_filings = filings(
    cik_lookup=tech_companies,
    filing_type=FilingType.FILING_10Q,
    start_date=date(2023, 1, 1),
    user_agent="Your Name (your.email@domain.com)"
)

my_filings.save('./sec_filings/tech_10q')
```

### ETF Filings

```python
# Fetch filings for top S&P 500 ETFs
sp500_etfs = ["SPY", "VOO", "IVV", "VTI", "QQQ"]

my_filings = filings(
    cik_lookup=sp500_etfs,
    filing_type=FilingType.FILING_10K,
    start_date=date(2023, 1, 1),
    user_agent="Your Name (your.email@domain.com)"
)

my_filings.save('./sec_filings/etf_10k')
```

### Get URLs Only (No Download)

```python
# Just get filing URLs for inspection
my_filings = filings(
    cik_lookup="AAPL",
    filing_type=FilingType.FILING_8K,
    start_date=date(2024, 1, 1),
    user_agent="Your Name (your.email@domain.com)"
)

urls = my_filings.get_urls()
print(f"Found {len(urls)} filings")
for url in urls:
    print(url)
```

## Supported Filing Types

The integration supports all major SEC filing types:

### Annual Reports
- **10-K**: Annual report with comprehensive company information
- **10-K/A**: Amended annual report

### Quarterly Reports  
- **10-Q**: Quarterly financial report
- **10-Q/A**: Amended quarterly report

### Current Reports
- **8-K**: Report of major corporate events or changes

### Proxy Statements
- **DEF 14A**: Definitive proxy statement
- **DEFA14A**: Additional definitive proxy soliciting materials

### Registration Statements
- **S-1**: Registration statement for new securities
- **S-3**: Registration statement for experienced issuers

### And many more... (see `FilingType` enum for complete list)

## Companies and ETFs Covered

### Major Tech Companies
- **AAPL**: Apple Inc.
- **AMZN**: Amazon.com Inc.
- **MSFT**: Microsoft Corporation
- **NVDA**: NVIDIA Corporation

### Top S&P 500 ETFs
- **SPY**: SPDR S&P 500 ETF Trust
- **VOO**: Vanguard S&P 500 ETF
- **IVV**: iShares Core S&P 500 ETF
- **VTI**: Vanguard Total Stock Market ETF
- **QQQ**: Invesco QQQ Trust

## Advanced Usage

### Custom Date Ranges

```python
from datetime import date, timedelta

# Last 6 months
end_date = date.today()
start_date = end_date - timedelta(days=180)

my_filings = filings(
    cik_lookup="AAPL",
    filing_type=FilingType.FILING_8K,
    start_date=start_date,
    end_date=end_date,
    user_agent="Your Name (your.email@domain.com)"
)
```

### Limit Number of Filings

```python
# Get only the 5 most recent filings
my_filings = filings(
    cik_lookup="AAPL",
    filing_type=FilingType.FILING_10Q,
    count=5,
    user_agent="Your Name (your.email@domain.com)"
)
```

### Company-Specific Deep Dive

```python
from secedgar import CompanyFilings

# Get comprehensive filings for a single company
company_filings = CompanyFilings(
    cik_lookup="AAPL",
    filing_type=FilingType.FILING_10K,
    start_date=date(2020, 1, 1),
    end_date=date.today(),
    user_agent="Your Name (your.email@domain.com)"
)

company_filings.save('./apple_comprehensive')
```

## Integration with FinRobot Analysis

Once you've downloaded SEC filings, you can use FinRobot's analysis capabilities:

```python
# Example: Analyze downloaded 10-K filings
from finrobot.functional.analyzer import ReportAnalysisUtils

# Analyze income statement from 10-K filing
analyzer = ReportAnalysisUtils()
income_analysis = analyzer.analyze_income_stmt(
    ticker_symbol="AAPL",
    fyear="2023",
    save_path="./analysis/aapl_income_analysis.txt"
)

print(income_analysis)
```

## SEC Fair Access Policy

**Important**: The SEC requires a proper User-Agent header for all requests. Always provide:
- Your name or organization
- Contact email
- Purpose of access

Example: `"FinRobot Analysis (support@finrobot.ai)"`

## File Organization

Downloaded filings are organized as:
```
sec_filings/
├── 10K_filings/
│   ├── AAPL/
│   ├── MSFT/
│   └── ...
├── 10Q_filings/
│   ├── AAPL/
│   └── ...
└── 8K_filings/
    └── ...
```

## Troubleshooting

### Import Errors
If you get import errors:
1. Run `./setup_sec_edgar.sh`
2. Ensure you're in the FinRobot root directory
3. Check that the submodule was properly initialized

### Network Issues
- Ensure stable internet connection
- The SEC may rate-limit requests
- Use appropriate `user_agent` header

### Large Downloads
- SEC filings can be large (MB-GB per company)
- Use date ranges and count limits to manage download size
- Monitor disk space

### Jupyter Notebook Issues
For Jupyter notebooks, add at the start:
```python
import nest_asyncio
nest_asyncio.apply()
```

## Next Steps

1. **Download filings** using the example scripts
2. **Analyze content** with FinRobot's AI-powered tools
3. **Extract insights** about financial performance, risks, and opportunities
4. **Generate reports** combining multiple data sources
5. **Automate workflows** for regular financial analysis

## Resources

- [SEC EDGAR Database](https://www.sec.gov/edgar.shtml)
- [SEC Filing Types Guide](https://www.sec.gov/forms)
- [FinRobot Documentation](../README.md)
- [sec-edgar Library Documentation](https://sec-edgar.github.io/sec-edgar/)