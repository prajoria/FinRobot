# API Configuration Setup Guide

This document explains how to set up the API configuration files for FinRobot.

## Quick Setup

1. **Copy the sample files:**
   ```bash
   cp OAI_CONFIG_LIST_sample OAI_CONFIG_LIST
   cp config_api_keys_sample config_api_keys
   ```

2. **Edit the configuration files with your actual API keys:**

### OAI_CONFIG_LIST
Update the Azure OpenAI configuration:
- Replace `YOUR_AZURE_OPENAI_API_KEY` with your actual Azure OpenAI API key
- Replace `https://your-resource-name.openai.azure.com/` with your Azure OpenAI endpoint URL

### config_api_keys
Update with your API keys for various financial data services:
- `FMP_API_KEY`: Your Financial Modeling Prep API key
- `FINNHUB_API_KEY`: Your Finnhub API key  
- `SEC_API_KEY`: Your SEC API key
- `REDDIT_CLIENT_ID` & `REDDIT_CLIENT_SECRET`: For Reddit data access
- `TWITTER_BEARER_TOKEN`: For Twitter/X data access

## Security Notes

⚠️ **Important**: Never commit the actual configuration files (`OAI_CONFIG_LIST` and `config_api_keys`) to git. They contain sensitive API keys and are automatically ignored via `.gitignore`.

✅ **Safe to commit**: Only the `*_sample` files should be committed to version control as they contain placeholder values.

## Getting API Keys

- **Azure OpenAI**: [Azure Portal](https://portal.azure.com) → AI + Machine Learning → Azure OpenAI
- **Financial Modeling Prep**: [FMP API](https://financialmodelingprep.com/developer/docs)
- **Finnhub**: [Finnhub API](https://finnhub.io/docs/api)
- **SEC API**: [SEC API](https://sec-api.io/)