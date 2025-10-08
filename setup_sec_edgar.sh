#!/bin/bash

# SEC EDGAR Setup Script for FinRobot
# This script installs dependencies and sets up the sec-edgar submodule

echo "🚀 Setting up SEC EDGAR integration for FinRobot..."
echo "================================================="

# Check if we're in the FinRobot directory
if [ ! -d "external/sec-edgar" ]; then
    echo "❌ Error: Please run this script from the FinRobot root directory"
    echo "   Expected to find: external/sec-edgar/"
    exit 1
fi

echo "✅ Found sec-edgar submodule"

# Install sec-edgar and dependencies
echo "📦 Installing sec-edgar and dependencies..."

# First install the core dependencies
echo "📦 Installing core dependencies..."
pip install beautifulsoup4 aiohttp urllib3 requests lxml tqdm

# Install nest-asyncio for Jupyter compatibility
echo "📦 Installing Jupyter compatibility..."
pip install nest-asyncio

# Option 1: Install from the submodule (development version)
echo "📦 Installing sec-edgar from submodule..."
cd external/sec-edgar
pip install -e .
cd ../..

# Option 2: Alternative - install from PyPI (stable version)
# pip install secedgar

# Install additional dependencies (if not already installed)
echo "📦 Verifying additional dependencies..."
pip install --upgrade beautifulsoup4 aiohttp urllib3 requests lxml tqdm nest-asyncio

echo "✅ Installation complete!"

# Test the installation
echo "🧪 Testing SEC EDGAR installation..."
python -c "
try:
    import secedgar
    from secedgar import FilingType, CompanyFilings
    print('✅ SEC EDGAR imported successfully')
    print(f'   Version: {secedgar.__version__}')
except ImportError as e:
    print(f'❌ Import error: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo "🎉 SEC EDGAR setup completed successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Run the example script: python examples/sec_edgar_fetcher.py"
    echo "   2. Check the sec_filings/ directory for downloaded documents"
    echo "   3. Use FinRobot's analysis tools to process the SEC filings"
else
    echo "❌ Setup failed. Please check the error messages above."
    exit 1
fi