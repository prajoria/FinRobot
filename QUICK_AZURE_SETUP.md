# 🔐 Secure Azure OpenAI Setup Instructions

## Step 1: Add Your Credentials to .env

Edit the file `/home/daaji/masterswork/git/FinRobot/.env` and replace these values:

```bash
# Replace these with your actual Azure OpenAI credentials:
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/

# Update these with your actual deployment names:
AZURE_OPENAI_GPT4_DEPLOYMENT=gpt-4o
AZURE_OPENAI_GPT4_TURBO_DEPLOYMENT=gpt-4-turbo  
AZURE_OPENAI_GPT35_DEPLOYMENT=gpt-35-turbo
```

## Step 2: What You Need to Replace

### API Key
- Replace `your_azure_openai_api_key_here` with your actual Azure OpenAI API key
- Example: `abcd1234567890efghijklmnop1234567890`

### Endpoint
- Replace `your-resource-name` with your Azure OpenAI resource name
- Example: If your resource is called "mycompany-openai", then:
  `https://mycompany-openai.openai.azure.com/`

### Model Deployment Names
- Replace the deployment names with your actual model deployments from Azure AI Studio
- Go to Azure AI Studio → Deployments to see your exact deployment names

## Step 3: Run the Setup Script

After updating your .env file, run:

```bash
cd /home/daaji/masterswork/git/FinRobot
source finrobot_env/bin/activate
python setup_azure_openai.py
```

This will automatically:
1. Read your credentials from the .env file
2. Create the OAI_CONFIG_LIST file with your settings
3. Test the configuration

## Step 4: Test Your Setup

```bash
# Test the Azure OpenAI connection
python examples/azure_openai_test.py

# Run FinRobot examples
python examples/basic_usage_examples.py
```

## 🔒 Security Benefits

✅ **API keys stay in .env file** (never committed to git)  
✅ **No credentials in code** - loaded from environment  
✅ **Easy to update** - just edit .env file  
✅ **Secure by default** - .env is in .gitignore  

## ❓ Need Help?

If you have your Azure OpenAI API key and endpoint ready, just:

1. Edit `.env` file with your credentials
2. Run `python setup_azure_openai.py`
3. You're ready to use FinRobot with Azure OpenAI!

The script will show exactly what needs to be configured if anything is missing.