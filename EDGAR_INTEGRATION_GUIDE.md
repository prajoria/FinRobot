# Dual SEC EDGAR Integration for FinRobot

FinRobot now includes **two powerful SEC EDGAR libraries** to provide comprehensive access to SEC filings and financial data:

## 📚 Available Libraries

### 1. **sec-edgar** - Bulk Filing Downloads
**Location**: `external/sec-edgar/`  
**Best for**: Downloading large numbers of filings, historical data collection

**Key Features**:
- Bulk download of 10-K, 10-Q, 8-K filings
- Historical filing retrieval
- Multiple companies at once
- File-based storage

### 2. **edgartools** - Modern API & Data Analysis  
**Location**: `external/edgartools/`  
**Best for**: Real-time data access, financial analysis, AI/LLM integration

**Key Features**:
- Clean Python API with pandas integration
- Instant access to company financials  
- XBRL data parsing
- LLM-ready text extraction
- Insider trading data
- Fund holdings analysis

## 🚀 Quick Start Guide

### Setup Both Libraries

```bash
# Run the existing setup for sec-edgar
./setup_sec_edgar.sh

# Install edgartools
cd external/edgartools
pip install -e .
cd ../..
```

### Using sec-edgar for Bulk Downloads

```python
import sys
import os
sys.path.insert(0, './external/sec-edgar')

from secedgar import filings, FilingType
from datetime import date

# Download recent 10-K filings for tech companies
tech_companies = ["AAPL", "MSFT", "AMZN", "NVDA"]
my_filings = filings(
    cik_lookup=tech_companies,
    filing_type=FilingType.FILING_10K,
    start_date=date(2022, 1, 1),
    user_agent="FinRobot Analysis (support@finrobot.ai)"
)
my_filings.save('./sec_filings/bulk_10k')
```

### Using edgartools for Financial Analysis

```python
import sys
import os
sys.path.insert(0, './external/edgartools')

from edgar import *

# Set identity (required by SEC)
set_identity("your.email@domain.com")

# Get Apple's latest financials in one line
company = Company("AAPL")
financials = company.get_financials()

# Extract specific financial statements
income_statement = financials.income_statement()
balance_sheet = financials.balance_sheet()
cash_flow = financials.cash_flow()

print(income_statement.head())
```

## 💡 Recommended Usage Patterns

### For Historical Research & Bulk Analysis
Use **sec-edgar** when you need to:
- Download filings for multiple years
- Collect data for large company sets
- Perform historical trend analysis
- Store filings locally for offline processing

```python
# Example: Download 5 years of quarterly reports for S&P 500 companies
sp500_companies = ["AAPL", "MSFT", "AMZN", "GOOGL", "TSLA", ...]
quarterly_filings = filings(
    cik_lookup=sp500_companies,
    filing_type=FilingType.FILING_10Q,
    start_date=date(2019, 1, 1),
    user_agent="FinRobot Historical Analysis"
)
quarterly_filings.save('./historical_research')
```

### For Real-time Analysis & AI Integration
Use **edgartools** when you need to:
- Access latest financial data quickly
- Integrate with pandas/numpy workflows
- Prepare data for LLM analysis
- Get structured financial metrics

```python
# Example: Real-time competitive analysis
companies = ["AAPL", "MSFT", "GOOGL"]
comparison_data = []

for ticker in companies:
    company = Company(ticker)
    latest_10k = company.get_filings(form="10-K").latest()
    
    # Extract key metrics
    financials = company.get_financials()
    revenue = financials.income_statement()['Revenues'].iloc[0]
    
    comparison_data.append({
        'company': ticker,
        'revenue': revenue,
        'filing_date': latest_10k.filing_date
    })

df = pd.DataFrame(comparison_data)
```

## 🔄 Integration with FinRobot Analysis

### Combined Workflow Example

```python
# Step 1: Use sec-edgar for bulk historical downloads
from secedgar import filings, FilingType

# Download 3 years of filings
historical_filings = filings(
    cik_lookup=["AAPL", "MSFT"],
    filing_type=FilingType.FILING_10K,
    start_date=date(2021, 1, 1),
    user_agent="FinRobot Combined Analysis"
)
historical_filings.save('./analysis_data/historical')

# Step 2: Use edgartools for latest financial data
from edgar import *
set_identity("analyst@finrobot.ai")

for ticker in ["AAPL", "MSFT"]:
    company = Company(ticker)
    
    # Get latest financials
    current_financials = company.get_financials()
    
    # Use FinRobot's analysis tools
    from finrobot.functional.analyzer import ReportAnalysisUtils
    analyzer = ReportAnalysisUtils()
    
    # Analyze the financial data
    analysis = analyzer.analyze_income_stmt(
        ticker_symbol=ticker,
        fyear="2024",
        save_path=f"./analysis_results/{ticker}_analysis.txt"
    )
```

## 📊 Feature Comparison

| Feature | sec-edgar | edgartools |
|---------|-----------|------------|
| **Bulk Downloads** | ✅ Excellent | ❌ Not designed for this |
| **Real-time Access** | ❌ Complex | ✅ Excellent |
| **Financial Data Parsing** | ❌ Raw files only | ✅ Automatic parsing |
| **Pandas Integration** | ❌ Manual | ✅ Built-in |
| **Historical Coverage** | ✅ 1994+ | ✅ 1994+ |
| **Rate Limiting** | ⚠️ Manual handling | ✅ Automatic |
| **XBRL Support** | ❌ No | ✅ Yes |
| **LLM Integration** | ⚠️ Text processing needed | ✅ LLM-ready |
| **Learning Curve** | ⚠️ Moderate | ✅ Easy |

## 🛠️ Setup Instructions

### Quick Setup for Both Libraries

1. **Install sec-edgar dependencies**:
   ```bash
   ./setup_sec_edgar.sh
   ```

2. **Install edgartools**:
   ```bash
   cd external/edgartools
   pip install -e .
   cd ../..
   ```

3. **Test both libraries**:
   ```bash
   python examples/quick_sec_test.py  # Test sec-edgar
   python examples/test_edgartools.py  # Test edgartools (to be created)
   ```

## 📈 Next Steps

1. **Choose the right tool** for your specific use case
2. **Combine both libraries** for comprehensive SEC data analysis
3. **Integrate with FinRobot's AI agents** for automated financial analysis
4. **Build custom workflows** that leverage the strengths of both libraries

The dual integration provides the best of both worlds: powerful bulk data collection with sec-edgar and modern, AI-ready analysis capabilities with edgartools! 🎉