#!/usr/bin/env python3
"""
Script to update all edgartools notebooks to use relative paths for load_dotenv
instead of absolute paths.
"""

import os
import re
import glob

def update_notebook_dotenv_path(notebook_path):
    """Update a single notebook file to use relative path for load_dotenv"""
    
    # Read the notebook file
    with open(notebook_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match the absolute path load_dotenv line
    pattern = r'load_dotenv\(\'/home/daaji/masterswork/git/FinRobot/\.env\'\)'
    replacement = "load_dotenv('../../../.env')"
    
    # Check if the pattern exists
    if re.search(pattern, content):
        # Replace the pattern
        updated_content = re.sub(pattern, replacement, content)
        
        # Write back to file
        with open(notebook_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Updated: {os.path.basename(notebook_path)}")
        return True
    else:
        print(f"⏭️ Skipped: {os.path.basename(notebook_path)} (no absolute path found)")
        return False

def main():
    """Update all notebooks in the edgartools notebooks directory"""
    
    notebooks_dir = "external/edgartools/notebooks"
    notebook_pattern = os.path.join(notebooks_dir, "*.ipynb")
    
    print("🔄 Updating edgartools notebooks to use relative paths for load_dotenv...")
    print("=" * 70)
    
    updated_count = 0
    total_count = 0
    
    # Find all notebook files
    notebook_files = glob.glob(notebook_pattern)
    
    for notebook_path in sorted(notebook_files):
        total_count += 1
        if update_notebook_dotenv_path(notebook_path):
            updated_count += 1
    
    print("=" * 70)
    print(f"📊 Summary: Updated {updated_count} out of {total_count} notebooks")
    
    if updated_count > 0:
        print("🎉 All notebooks now use relative paths for load_dotenv!")
    else:
        print("ℹ️ No notebooks needed updating (all already use relative paths)")

if __name__ == "__main__":
    main()