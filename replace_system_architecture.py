#!/usr/bin/env python3
"""
Replace all current system_architecture.png files with System_Architecture_latest.png
"""

import os
import shutil
from pathlib import Path

def replace_system_architecture():
    """Replace all system_architecture.png files with the latest version."""
    
    source_file = "System_Architecture_latest.png"
    
    # Check if source file exists
    if not os.path.exists(source_file):
        print(f"❌ Error: {source_file} not found!")
        return False
    
    print("🔄 Replacing system architecture files...")
    print("=" * 60)
    
    # Get source file size for verification
    source_size = os.path.getsize(source_file)
    print(f"📁 Source: {source_file} ({source_size:,} bytes)")
    print()
    
    # List of target locations to replace
    target_locations = [
        "images/system_architecture.png",
        "figures/system_architecture.png", 
        "overleaf_package/figures/system_architecture.png"
    ]
    
    success_count = 0
    
    for target in target_locations:
        try:
            # Create directory if it doesn't exist
            target_dir = os.path.dirname(target)
            if target_dir and not os.path.exists(target_dir):
                os.makedirs(target_dir, exist_ok=True)
                print(f"📁 Created directory: {target_dir}")
            
            # Check if target exists (for backup info)
            if os.path.exists(target):
                old_size = os.path.getsize(target)
                print(f"🔄 Replacing: {target} ({old_size:,} bytes)")
            else:
                print(f"➕ Creating: {target}")
            
            # Copy the new file
            shutil.copy2(source_file, target)
            
            # Verify the copy
            if os.path.exists(target):
                new_size = os.path.getsize(target)
                if new_size == source_size:
                    print(f"   ✅ Success: {target} ({new_size:,} bytes)")
                    success_count += 1
                else:
                    print(f"   ⚠️  Warning: Size mismatch for {target}")
            else:
                print(f"   ❌ Failed: {target} not created")
                
        except Exception as e:
            print(f"   ❌ Error replacing {target}: {str(e)}")
        
        print()
    
    print("=" * 60)
    print(f"✅ Successfully replaced {success_count}/{len(target_locations)} files")
    
    return success_count == len(target_locations)

def update_overleaf_package():
    """Regenerate the Overleaf package with the new system architecture."""
    
    print("\n🔄 Updating Overleaf package...")
    
    try:
        # Import and run the package preparation
        import subprocess
        result = subprocess.run(['python', 'prepare_overleaf_package.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Overleaf package updated successfully!")
            return True
        else:
            print(f"❌ Error updating Overleaf package: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running package update: {str(e)}")
        return False

def verify_replacements():
    """Verify that all files have been replaced correctly."""
    
    print("\n🔍 Verifying replacements...")
    print("-" * 40)
    
    source_file = "System_Architecture_latest.png"
    source_size = os.path.getsize(source_file)
    
    target_locations = [
        "images/system_architecture.png",
        "figures/system_architecture.png", 
        "overleaf_package/figures/system_architecture.png"
    ]
    
    all_match = True
    
    for target in target_locations:
        if os.path.exists(target):
            target_size = os.path.getsize(target)
            if target_size == source_size:
                print(f"✅ {target}: {target_size:,} bytes (matches)")
            else:
                print(f"❌ {target}: {target_size:,} bytes (mismatch!)")
                all_match = False
        else:
            print(f"❌ {target}: File not found!")
            all_match = False
    
    print("-" * 40)
    if all_match:
        print("✅ All files verified successfully!")
    else:
        print("❌ Some files don't match - check for errors above")
    
    return all_match

def main():
    """Main function to replace system architecture files."""
    
    print("🔄 SYSTEM ARCHITECTURE REPLACEMENT")
    print("=" * 60)
    print("Replacing all system_architecture.png files with System_Architecture_latest.png")
    print()
    
    # Step 1: Replace all files
    if not replace_system_architecture():
        print("❌ File replacement failed!")
        return
    
    # Step 2: Update Overleaf package
    if not update_overleaf_package():
        print("⚠️  Overleaf package update failed, but files were replaced")
    
    # Step 3: Verify all replacements
    verify_replacements()
    
    print("\n" + "=" * 60)
    print("🎉 REPLACEMENT COMPLETE!")
    print()
    print("📋 What was updated:")
    print("• images/system_architecture.png")
    print("• figures/system_architecture.png") 
    print("• overleaf_package/figures/system_architecture.png")
    print("• overleaf_package.zip (regenerated)")
    print()
    print("🚀 Your paper now uses the latest system architecture diagram!")

if __name__ == "__main__":
    main()
