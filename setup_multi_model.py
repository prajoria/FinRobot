#!/usr/bin/env python3
"""
Multi-Model Setup Script for FinRobot
=====================================

This script configures both Azure OpenAI (GPT-4o) and Anthropic Claude (Sonnet)
as primary models for FinRobot financial analysis.
"""

import os
import json
from dotenv import load_dotenv

def setup_multi_model_config():
    """
    Set up configuration with GPT-4o and Claude Sonnet as primary models
    """
    print("🔧 Setting up Multi-Model Configuration (GPT-4o + Claude Sonnet)...")
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get Azure OpenAI credentials
    azure_api_key = os.getenv('AZURE_OPENAI_API_KEY')
    azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    azure_api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
    gpt4_deployment = os.getenv('AZURE_OPENAI_GPT4_DEPLOYMENT', 'gpt-4o')
    
    # Get Anthropic credentials
    anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
    
    # Validate Azure OpenAI credentials
    azure_valid = True
    if not azure_api_key or 'your_azure_openai_api_key_here' in azure_api_key:
        print("⚠️  Azure OpenAI API key missing or placeholder")
        azure_valid = False
    
    if not azure_endpoint or 'your-resource-name' in azure_endpoint:
        print("⚠️  Azure OpenAI endpoint missing or placeholder")
        azure_valid = False
    
    # Validate Anthropic credentials
    anthropic_valid = True
    if not anthropic_api_key or 'your_anthropic_api_key_here' in anthropic_api_key:
        print("⚠️  Anthropic API key missing or placeholder")
        anthropic_valid = False
    
    # Create configuration with priority order: GPT-4o first, then Claude
    config = []
    
    # Primary Model 1: GPT-4o (Azure OpenAI)
    if azure_valid:
        config.append({
            "model": gpt4_deployment,
            "api_key": azure_api_key,
            "base_url": azure_endpoint,
            "api_type": "azure",
            "api_version": azure_api_version
        })
        print(f"✅ Added GPT-4o ({gpt4_deployment}) as primary model")
    else:
        print("❌ Cannot add GPT-4o - Azure OpenAI credentials missing")
    
    # Primary Model 2: Claude Sonnet
    if anthropic_valid:
        config.append({
            "model": "claude-3-5-sonnet-20241022",
            "api_key": anthropic_api_key
        })
        print("✅ Added Claude 3.5 Sonnet as secondary model")
    else:
        print("❌ Cannot add Claude Sonnet - Anthropic API key missing")
    
    # Add fallback models if Azure is configured
    if azure_valid:
        gpt4_turbo_deployment = os.getenv('AZURE_OPENAI_GPT4_TURBO_DEPLOYMENT', 'gpt-4-turbo')
        gpt35_deployment = os.getenv('AZURE_OPENAI_GPT35_DEPLOYMENT', 'gpt-35-turbo')
        
        config.extend([
            {
                "model": gpt4_turbo_deployment,
                "api_key": azure_api_key,
                "base_url": azure_endpoint,
                "api_type": "azure",
                "api_version": azure_api_version
            },
            {
                "model": gpt35_deployment,
                "api_key": azure_api_key,
                "base_url": azure_endpoint,
                "api_type": "azure",
                "api_version": azure_api_version
            }
        ])
        print(f"✅ Added fallback models: {gpt4_turbo_deployment}, {gpt35_deployment}")
    
    if not config:
        print("❌ No valid configurations found - please check your .env file")
        return False
    
    # Write configuration to file
    try:
        with open('OAI_CONFIG_LIST', 'w') as f:
            json.dump(config, f, indent=4)
        
        print(f"\n🎯 Configuration Summary:")
        print(f"   Total models configured: {len(config)}")
        print(f"   Primary models: GPT-4o {'✅' if azure_valid else '❌'}, Claude Sonnet {'✅' if anthropic_valid else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing configuration: {e}")
        return False

def test_configuration():
    """
    Test the multi-model configuration
    """
    print("\n🧪 Testing configuration...")
    
    try:
        import autogen
        
        config_list = autogen.config_list_from_json("OAI_CONFIG_LIST")
        print(f"✅ Successfully loaded {len(config_list)} configurations")
        
        models = [config.get("model", "Unknown") for config in config_list]
        print(f"📋 Available models (in priority order): {models}")
        
        # Test specific model loading
        try:
            # Try to get GPT-4o config
            gpt4_config = autogen.config_list_from_json(
                "OAI_CONFIG_LIST",
                filter_dict={"model": ["gpt-4o"]}
            )
            if gpt4_config:
                print("✅ GPT-4o configuration ready")
        except:
            print("⚠️  GPT-4o configuration issue")
        
        try:
            # Try to get Claude config
            claude_config = autogen.config_list_from_json(
                "OAI_CONFIG_LIST", 
                filter_dict={"model": ["claude-3-5-sonnet-20241022"]}
            )
            if claude_config:
                print("✅ Claude Sonnet configuration ready")
        except:
            print("⚠️  Claude Sonnet configuration issue")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """
    Main setup function
    """
    print("🤖 FinRobot Multi-Model Setup (GPT-4o + Claude Sonnet)")
    print("=" * 60)
    
    # Setup configuration
    setup_success = setup_multi_model_config()
    
    if setup_success:
        # Test the configuration
        test_success = test_configuration()
        
        if test_success:
            print("\n🎉 Multi-model setup completed successfully!")
            print("\n📖 Usage Notes:")
            print("   • GPT-4o will be used as the primary model")
            print("   • Claude Sonnet will be used as secondary/alternative")
            print("   • Fallback models available if needed")
            print("\n🚀 Next steps:")
            print("   1. Run: python examples/basic_usage_examples.py")
            print("   2. FinRobot will automatically use GPT-4o first, then Claude")
        else:
            print("\n⚠️  Configuration created but test failed")
            print("   Please check your model deployment names")
    else:
        print("\n❌ Setup failed. Please update your .env file:")
        print("\n📝 Required in .env file:")
        print("   AZURE_OPENAI_API_KEY=your_actual_azure_api_key")
        print("   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/")
        print("   ANTHROPIC_API_KEY=your_actual_anthropic_api_key")

if __name__ == "__main__":
    main()