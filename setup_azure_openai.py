#!/usr/bin/env python3
"""
Azure OpenAI Environment Setup Script
=====================================

This script automatically configures OAI_CONFIG_LIST using environment variables
to keep your API keys secure and out of version control.
"""

import os
import json
from dotenv import load_dotenv

def setup_azure_openai_from_env():
    """
    Set up Azure OpenAI configuration from environment variables
    """
    print("🔧 Setting up Azure OpenAI from environment variables...")
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get Azure OpenAI credentials from environment
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
    
    # Get model deployment names
    gpt4_deployment = os.getenv('AZURE_OPENAI_GPT4_DEPLOYMENT', 'gpt-4o')
    gpt4_turbo_deployment = os.getenv('AZURE_OPENAI_GPT4_TURBO_DEPLOYMENT', 'gpt-4-turbo')
    gpt35_deployment = os.getenv('AZURE_OPENAI_GPT35_DEPLOYMENT', 'gpt-35-turbo')
    
    # Validate required credentials
    if not api_key or 'your_azure_openai_api_key_here' in api_key:
        print("❌ Azure OpenAI API key not found in environment")
        print("   Please set AZURE_OPENAI_API_KEY in your .env file")
        return False
    
    if not endpoint or 'your-resource-name' in endpoint:
        print("❌ Azure OpenAI endpoint not found in environment")
        print("   Please set AZURE_OPENAI_ENDPOINT in your .env file")
        return False
    
    # Create configuration
    config = [
        {
            "model": gpt4_deployment,
            "api_key": api_key,
            "base_url": endpoint,
            "api_type": "azure",
            "api_version": api_version
        },
        {
            "model": gpt4_turbo_deployment,
            "api_key": api_key,
            "base_url": endpoint,
            "api_type": "azure", 
            "api_version": api_version
        },
        {
            "model": gpt35_deployment,
            "api_key": api_key,
            "base_url": endpoint,
            "api_type": "azure",
            "api_version": api_version
        }
    ]
    
    # Write configuration to file
    try:
        with open('OAI_CONFIG_LIST', 'w') as f:
            json.dump(config, f, indent=4)
        
        print("✅ OAI_CONFIG_LIST updated successfully!")
        print(f"📋 Configured models:")
        for cfg in config:
            print(f"   - {cfg['model']}")
        print(f"🔗 Endpoint: {endpoint}")
        print(f"🔑 API Key: {api_key[:8]}...{api_key[-4:] if len(api_key) > 12 else '***'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing configuration: {e}")
        return False

def test_configuration():
    """
    Test the Azure OpenAI configuration
    """
    print("\n🧪 Testing configuration...")
    
    try:
        import autogen
        
        config_list = autogen.config_list_from_json("OAI_CONFIG_LIST")
        print(f"✅ Successfully loaded {len(config_list)} configurations")
        
        models = [config.get("model", "Unknown") for config in config_list]
        print(f"📋 Available models: {models}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """
    Main setup function
    """
    print("🤖 Azure OpenAI Environment Setup")
    print("=" * 50)
    
    # Setup configuration from environment
    setup_success = setup_azure_openai_from_env()
    
    if setup_success:
        # Test the configuration
        test_success = test_configuration()
        
        if test_success:
            print("\n🎉 Azure OpenAI setup completed successfully!")
            print("\nNext steps:")
            print("1. Run: python examples/azure_openai_test.py")
            print("2. Run: python examples/basic_usage_examples.py")
        else:
            print("\n⚠️  Configuration created but test failed")
            print("   Please check your Azure OpenAI deployment names")
    else:
        print("\n❌ Setup failed. Please check your .env file configuration")
        print("\nTo set up your .env file:")
        print("1. Edit /home/daaji/masterswork/git/FinRobot/.env")
        print("2. Replace 'your_azure_openai_api_key_here' with your actual API key")
        print("3. Replace 'your-resource-name' with your Azure resource name")
        print("4. Update model deployment names if needed")

if __name__ == "__main__":
    main()