# FinRobot Setup and Usage Guide

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Dependencies
```bash
cd /home/daaji/masterswork/git/FinRobot

# Install FinRobot in development mode
pip install -e .

# Or install from PyPI
pip install finrobot
```

### Step 2: Configure API Keys

#### OpenAI Configuration
```bash
# Copy the sample file
cp OAI_CONFIG_LIST_sample OAI_CONFIG_LIST

# Edit OAI_CONFIG_LIST and add your OpenAI API key:
```
```json
[
    {
        "model": "gpt-4-0125-preview",
        "api_key": "your-openai-api-key-here"
    }
]
```

#### Financial Data APIs
```bash
# Copy the sample file  
cp config_api_keys_sample config_api_keys

# Edit config_api_keys and add your API keys:
```
```json
{
    "FINNHUB_API_KEY": "your-finnhub-key-here",
    "FMP_API_KEY": "oTP74s9TxGsnRjac3xRBn3JQcP5qvYwQ",
    "SEC_API_KEY": "your-sec-api-key-here",
    "REDDIT_CLIENT_ID": "your-reddit-client-id",
    "REDDIT_CLIENT_SECRET": "your-reddit-client-secret"
}
```

> **Note**: You already have an FMP API key configured. You can get free API keys from:
> - [Finnhub](https://finnhub.io/) - Free tier available
> - [SEC API](https://sec-api.io/) - Free tier available

### Step 3: Test Installation
```bash
python examples/quick_start.py
```

---

## 💡 Usage Examples

### Example 1: Simple Stock Analysis
```python
import autogen
from finrobot.utils import get_current_date, register_keys_from_json
from finrobot.agents.workflow import SingleAssistant

# Setup
llm_config = {
    "config_list": autogen.config_list_from_json("OAI_CONFIG_LIST"),
    "timeout": 120,
    "temperature": 0,
}
register_keys_from_json("config_api_keys")

# Create analyst agent
analyst = SingleAssistant("Market_Analyst", llm_config, human_input_mode="NEVER")

# Analyze a stock
result = analyst.chat(f"""
Analyze NVDA stock for {get_current_date()}. 
Provide price prediction and key insights.
""")
```

### Example 2: Generate Investment Report
```python
from finrobot.agents.workflow import SingleAssistantShadow

# Create expert investor agent
investor = SingleAssistantShadow("Expert_Investor", llm_config)

# Generate comprehensive report
report = investor.chat(f"""
Create annual report for Microsoft 2023 10-K filing.
Include comprehensive analysis and PDF generation.
""")
```

### Example 3: Multi-Agent Investment Committee
```python
from finrobot.experiments.investment_group import group_config
from finrobot.agents.workflow import MultiAssistantWithLeader

# Create investment committee
committee = MultiAssistantWithLeader(group_config, llm_config)

# Collaborative analysis
decision = committee.chat("""
Evaluate Q4 2024 portfolio rebalancing strategy.
Consider market outlook and risk parameters.
""")
```

---

## 🎯 Real-World Use Cases

### 1. Daily Market Analysis
```python
# Monitor top 10 stocks
stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "CRM", "ORCL"]

for stock in stocks:
    analysis = analyst.chat(f"Quick analysis of {stock} - price movement and news sentiment")
    print(f"{stock}: {analysis}")
```

### 2. Earnings Season Preparation
```python
# Analyze companies before earnings
earnings_calendar = ["AAPL", "MSFT", "GOOGL"]  # Companies reporting this week

for company in earnings_calendar:
    report = investor.chat(f"""
    Pre-earnings analysis for {company}:
    1. Historical earnings performance
    2. Analyst expectations vs reality
    3. Key metrics to watch
    4. Potential price impact scenarios
    """)
```

### 3. Portfolio Health Check
```python
# Analyze your current portfolio
portfolio = {
    "AAPL": 25, "MSFT": 20, "GOOGL": 15, 
    "AMZN": 15, "TSLA": 10, "NVDA": 10, "SPY": 5
}

portfolio_analysis = analyst.chat(f"""
Analyze this portfolio allocation: {portfolio}

Provide:
- Risk assessment
- Diversification analysis  
- Rebalancing recommendations
- Market outlook impact
""")
```

### 4. Sector Rotation Analysis
```python
# Compare different sectors
sectors = {
    "Technology": ["AAPL", "MSFT", "GOOGL"],
    "Healthcare": ["JNJ", "PFE", "UNH"], 
    "Finance": ["JPM", "BAC", "WFC"],
    "Energy": ["XOM", "CVX", "COP"]
}

for sector, stocks in sectors.items():
    analysis = analyst.chat(f"""
    Analyze {sector} sector momentum:
    Stocks: {stocks}
    
    Provide sector outlook and best picks.
    """)
```

---

## 🔧 Advanced Configuration

### Custom Agent Creation
```python
# Create custom agent with specific tools
from finrobot.data_source import YFinanceUtils, FMPUtils
from finrobot.agents.workflow import FinRobot

custom_agent_config = {
    "name": "Options_Trader",
    "profile": "Expert in options trading and volatility analysis",
    "toolkits": [
        YFinanceUtils.get_stock_data,
        FMPUtils.get_financial_metrics,
        # Add custom options tools here
    ]
}

options_trader = FinRobot(custom_agent_config, llm_config=llm_config)
```

### Multi-Model Setup
```python
# Use different models for different tasks
llm_configs = {
    "analysis": {
        "config_list": [{"model": "gpt-4-0125-preview", "api_key": "your-key"}],
        "temperature": 0,
    },
    "creative": {
        "config_list": [{"model": "gpt-4-0125-preview", "api_key": "your-key"}],
        "temperature": 0.7,
    }
}

# Use appropriate config for each task
analyst = SingleAssistant("Market_Analyst", llm_configs["analysis"])
writer = SingleAssistant("Expert_Investor", llm_configs["creative"])
```

---

## 📊 Data Sources Available

| Source | Purpose | Free Tier |
|--------|---------|-----------|
| **FMP** | SEC filings, fundamentals, target prices | ✅ 250 calls/day |
| **Yahoo Finance** | Stock prices, financial statements | ✅ Unlimited |
| **Finnhub** | Real-time data, news, profiles | ✅ 60 calls/minute |
| **SEC API** | Official regulatory filings | ✅ 10 calls/second |
| **Reddit** | Social sentiment analysis | ✅ With account |

---

## 🎓 Learning Resources

### Beginner Tutorials
- `tutorials_beginner/agent_fingpt_forecaster.ipynb` - Stock prediction
- `tutorials_beginner/agent_annual_report.ipynb` - Report generation
- `tutorials_beginner/agent_rag_qa.ipynb` - Document Q&A

### Advanced Tutorials  
- `tutorials_advanced/agent_trade_strategist.ipynb` - Trading strategies
- `tutorials_advanced/lmm_agent_mplfinance.ipynb` - Advanced charting
- `tutorials_advanced/agent_openbb.ipynb` - OpenBB integration

### Example Scripts
- `examples/quick_start.py` - Basic usage
- `examples/basic_usage_examples.py` - Comprehensive examples
- `experiments/portfolio_optimization.py` - Multi-agent workflows

---

## 🔍 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Install missing dependencies
pip install pyautogen finnhub-python yfinance reportlab
```

**2. API Key Errors**
```bash
# Check your API keys are correctly formatted in config_api_keys
# Ensure no extra quotes or spaces
```

**3. Model Timeout**
```python
# Increase timeout in llm_config
llm_config = {
    "config_list": [...],
    "timeout": 300,  # 5 minutes
    "temperature": 0,
}
```

**4. Rate Limiting**
```python
# Add delays between API calls
import time
time.sleep(1)  # Wait 1 second between requests
```

### Getting Help
- Check the [GitHub Issues](https://github.com/AI4Finance-Foundation/FinRobot/issues)
- Join the [Discord Community](https://discord.gg/trsr8SXpW5)
- Review the [Documentation](https://github.com/AI4Finance-Foundation/FinRobot)

---

## 🚀 Next Steps

1. **Start Simple**: Run `examples/quick_start.py` to verify setup
2. **Explore Notebooks**: Try the Jupyter tutorials in `tutorials_beginner/`
3. **Build Custom Agents**: Create agents for your specific use cases
4. **Scale Up**: Implement multi-agent workflows for complex analysis
5. **Integrate**: Connect FinRobot to your existing trading/analysis systems

Happy Financial AI! 🤖📈