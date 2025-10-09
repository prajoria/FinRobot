#!/usr/bin/env python3
"""
Update all edgartools notebooks to use SEC_IDENTITY from .env file

This script automatically updates all Jupyter notebooks in the edgartools directory
to load the SEC identity from the .env file instead of hardcoding email addresses.
"""

import os
import re
import json
from pathlib import Path

def update_notebook_identity(notebook_path):
    """Update a single notebook to use .env-based identity"""
    
    print(f"Processing: {notebook_path.name}")
    
    try:
        # Read the notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if notebook already uses environment variable approach
        if 'load_dotenv' in content and 'SEC_IDENTITY' in content:
            print(f"  ✅ Already updated: {notebook_path.name}")
            return True
        
        # Check if notebook has set_identity calls
        if 'set_identity' not in content:
            print(f"  ⏭️  No set_identity found: {notebook_path.name}")
            return True
        
        # Parse as JSON to work with notebook structure
        try:
            notebook = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"  ❌ JSON parse error in {notebook_path.name}: {e}")
            return False
        
        # Track if we made changes
        changed = False
        
        # Look for cells with set_identity
        for cell in notebook.get('cells', []):
            if cell.get('cell_type') == 'code':
                source = cell.get('source', [])
                if isinstance(source, list):
                    source_text = ''.join(source)
                else:
                    source_text = source
                
                # Check if this cell has set_identity
                if 'set_identity' in source_text:
                    print(f"  🔧 Updating cell with set_identity...")
                    
                    # Create new source with env loading
                    new_source = []
                    
                    # Add imports at the top
                    new_source.extend([
                        "import os\\n",
                        "from dotenv import load_dotenv\\n"
                    ])
                    
                    # Add existing imports (except duplicate os import)
                    for line in source if isinstance(source, list) else [source]:
                        if line.strip() and not line.startswith('set_identity') and 'import os' not in line:
                            if not any(imp in line for imp in ['from dotenv import load_dotenv']):
                                new_source.append(line)
                    
                    # Add environment loading
                    new_source.extend([
                        "\\n",
                        "# Load environment variables from .env file\\n",
                        "load_dotenv('/home/daaji/masterswork/git/FinRobot/.env')\\n",
                        "\\n",
                        "# Set identity from environment variable\\n",
                        "sec_identity = os.getenv('SEC_IDENTITY', 'default@example.com')\\n",
                        "set_identity(sec_identity)\\n"
                    ])
                    
                    # Update the cell source
                    cell['source'] = new_source
                    changed = True
        
        # Write back if changed
        if changed:
            with open(notebook_path, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=1, ensure_ascii=False)
            print(f"  ✅ Updated: {notebook_path.name}")
        else:
            print(f"  ⏭️  No changes needed: {notebook_path.name}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error processing {notebook_path.name}: {e}")
        return False

def main():
    """Main function to update all notebooks"""
    
    print("🚀 Updating EdgarTools Notebooks to Use .env Identity")
    print("=" * 60)
    
    # Define notebook directory
    notebooks_dir = Path("/home/daaji/masterswork/git/FinRobot/external/edgartools/notebooks")
    
    if not notebooks_dir.exists():
        print(f"❌ Notebooks directory not found: {notebooks_dir}")
        return
    
    # Find all notebook files
    notebook_files = list(notebooks_dir.glob("*.ipynb"))
    
    if not notebook_files:
        print(f"❌ No notebook files found in: {notebooks_dir}")
        return
    
    print(f"📚 Found {len(notebook_files)} notebook files")
    print()
    
    # Process each notebook
    success_count = 0
    for notebook_path in sorted(notebook_files):
        if update_notebook_identity(notebook_path):
            success_count += 1
        print()  # Add spacing between files
    
    # Summary
    print("=" * 60)
    print(f"📊 Summary: {success_count}/{len(notebook_files)} notebooks processed successfully")
    
    if success_count == len(notebook_files):
        print("🎉 All notebooks updated successfully!")
        print()
        print("📋 Next steps:")
        print("   1. Test a notebook: jupyter notebook external/edgartools/notebooks/Beginners-Guide.ipynb")
        print("   2. Verify SEC_IDENTITY is loaded from .env file")
        print("   3. Make sure python-dotenv is installed: pip install python-dotenv")
    else:
        print("⚠️  Some notebooks had issues. Please check the output above.")

if __name__ == "__main__":
    main()