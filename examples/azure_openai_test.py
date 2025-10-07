#!/usr/bin/env python3
"""
Azure OpenAI Connection Test for FinRobot
=========================================

This script tests your Azure OpenAI configuration before running FinRobot examples.
"""

import json
import os
import sys

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_azure_openai_config():
    """Test Azure OpenAI configuration"""
    print("🔍 Testing Azure OpenAI Configuration")
    print("=" * 50)
    
    # Check if config file exists
    config_path = "OAI_CONFIG_LIST"
    if not os.path.exists(config_path):
        print("❌ OAI_CONFIG_LIST file not found")
        return False
    
    # Load and validate configuration
    try:
        with open(config_path, 'r') as f:
            configs = json.load(f)
        
        print(f"✅ Found {len(configs)} model configurations")
        
        azure_configs = []
        openai_configs = []
        
        for i, config in enumerate(configs):
            model_name = config.get("model", "Unknown")
            api_type = config.get("api_type", "openai")
            
            if api_type == "azure":
                azure_configs.append(config)
                print(f"   🔷 Azure OpenAI: {model_name}")
                
                # Validate Azure-specific fields
                required_fields = ["api_key", "base_url", "api_version"]
                missing_fields = []
                
                for field in required_fields:
                    if not config.get(field) or "your_" in str(config.get(field, "")):
                        missing_fields.append(field)
                
                if missing_fields:
                    print(f"      ⚠️  Missing/placeholder values: {missing_fields}")
                else:
                    print(f"      ✅ Configuration looks complete")
                    
            else:
                openai_configs.append(config)
                print(f"   🔶 OpenAI: {model_name}")
        
        print(f"\n📊 Summary:")
        print(f"   Azure OpenAI models: {len(azure_configs)}")
        print(f"   OpenAI models: {len(openai_configs)}")
        
        if azure_configs:
            print(f"\n🎯 Recommended: Use Azure OpenAI for enterprise features")
            return True
        elif openai_configs:
            print(f"\n💡 Using OpenAI models (consider Azure for enterprise)")
            return True
        else:
            print(f"\n❌ No valid configurations found")
            return False
            
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in config file: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading config file: {e}")
        return False

def test_simple_autogen_import():
    """Test if autogen can import and use the config"""
    print("\n🔍 Testing AutoGen Integration")
    print("=" * 50)
    
    try:
        import autogen
        print("✅ AutoGen imported successfully")
        
        # Try to load config with autogen
        config_list = autogen.config_list_from_json("OAI_CONFIG_LIST")
        print(f"✅ AutoGen loaded {len(config_list)} configurations")
        
        # Show available models
        models = [config.get("model", "Unknown") for config in config_list]
        print(f"📋 Available models: {models}")
        
        return True
        
    except Exception as e:
        print(f"❌ AutoGen integration error: {e}")
        return False

def provide_setup_instructions():
    """Provide setup instructions for Azure OpenAI"""
    print(f"\n📝 Azure OpenAI Setup Instructions")
    print("=" * 50)
    print(f"""
To configure Azure OpenAI:

1. 🔑 Get your Azure OpenAI credentials:
   - Go to Azure Portal → Your OpenAI Resource
   - Copy the API Key from "Keys and Endpoint"
   - Copy the Endpoint URL

2. 📝 Update OAI_CONFIG_LIST:
   Replace these values in /home/daaji/masterswork/git/FinRobot/OAI_CONFIG_LIST:
   
   - "your_azure_openai_api_key_here" → Your actual API key
   - "your-resource-name" → Your Azure resource name
   - Model names should match your deployments in Azure AI Studio

3. 🧪 Test configuration:
   cd /home/daaji/masterswork/git/FinRobot
   source finrobot_env/bin/activate
   python examples/azure_openai_test.py

4. 🚀 Run FinRobot examples:
   python examples/basic_usage_examples.py

📚 For detailed instructions, see: AZURE_OPENAI_SETUP.md
""")

def main():
    """Main test function"""
    print("🤖 FinRobot Azure OpenAI Configuration Test")
    print("=" * 60)
    
    config_ok = test_azure_openai_config()
    autogen_ok = test_simple_autogen_import()
    
    print(f"\n🎯 Test Results:")
    print(f"   Configuration: {'✅ PASS' if config_ok else '❌ FAIL'}")
    print(f"   AutoGen Integration: {'✅ PASS' if autogen_ok else '❌ FAIL'}")
    
    if config_ok and autogen_ok:
        print(f"\n🎉 Azure OpenAI configuration looks good!")
        print(f"   You can now run: python examples/basic_usage_examples.py")
    else:
        provide_setup_instructions()

if __name__ == "__main__":
    main()