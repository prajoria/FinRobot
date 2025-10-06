# Azure OpenAI Setup for FinRobot

## 🔧 Configuration Steps

### 1. Azure OpenAI Service Setup
First, you need to have Azure OpenAI service set up:
1. Go to [Azure Portal](https://portal.azure.com)
2. Create an Azure OpenAI resource
3. Deploy your models (e.g., GPT-4, GPT-3.5-turbo)
4. Get your API key and endpoint

### 2. Configure OAI_CONFIG_LIST

Replace the values in `/home/daaji/masterswork/git/FinRobot/OAI_CONFIG_LIST`:

```json
[
    {
        "model": "gpt-4o",
        "api_key": "your_actual_azure_api_key",
        "base_url": "https://your-resource-name.openai.azure.com/",
        "api_type": "azure",
        "api_version": "2024-02-15-preview"
    },
    {
        "model": "gpt-4-turbo", 
        "api_key": "your_actual_azure_api_key",
        "base_url": "https://your-resource-name.openai.azure.com/",
        "api_type": "azure",
        "api_version": "2024-02-15-preview"
    },
    {
        "model": "gpt-35-turbo",
        "api_key": "your_actual_azure_api_key",
        "base_url": "https://your-resource-name.openai.azure.com/",
        "api_type": "azure",
        "api_version": "2024-02-15-preview"
    }
]
```

### 3. Required Information

You need to replace:
- `your_actual_azure_api_key`: Your Azure OpenAI API key
- `your-resource-name`: Your Azure OpenAI resource name
- `model`: Must match your deployed model names in Azure

### 4. Find Your Azure OpenAI Details

**API Key:**
- Go to Azure Portal → Your OpenAI Resource → Keys and Endpoint
- Copy KEY 1 or KEY 2

**Endpoint:**
- Format: `https://your-resource-name.openai.azure.com/`
- Found in Keys and Endpoint section

**Model Names:**
- Go to Azure AI Studio → Deployments
- Use the exact deployment name as the "model" value

### 5. Model Deployment Names

Make sure your Azure OpenAI models are deployed with these names:
- `gpt-4o` (or whatever you named your GPT-4 deployment)
- `gpt-4-turbo` (or your GPT-4 Turbo deployment name)
- `gpt-35-turbo` (or your GPT-3.5 deployment name)

### 6. Test Configuration

After configuring, test with:
```bash
cd /home/daaji/masterswork/git/FinRobot
source finrobot_env/bin/activate
python examples/quick_start.py
```

## 🚀 Benefits of Azure OpenAI

1. **Enterprise Grade**: Better security and compliance
2. **Data Privacy**: Your data stays in your Azure tenant
3. **Regional Availability**: Choose data center location
4. **Integration**: Works seamlessly with other Azure services
5. **Cost Management**: Better cost controls and monitoring

## 🔍 Common Issues

**Issue**: Model not found
**Solution**: Check that model name in config matches deployment name in Azure

**Issue**: Authentication failed  
**Solution**: Verify API key and endpoint URL are correct

**Issue**: Rate limits
**Solution**: Check your Azure OpenAI quota and scaling settings

## 📝 Example Working Configuration

```json
[
    {
        "model": "my-gpt4-deployment",
        "api_key": "abcd1234567890efgh...",
        "base_url": "https://mycompany-openai.openai.azure.com/",
        "api_type": "azure",
        "api_version": "2024-02-15-preview"
    }
]
```

Remember: The `model` field should match your exact deployment name in Azure AI Studio!