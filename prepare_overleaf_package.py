#!/usr/bin/env python3
"""
Prepare a clean Overleaf-ready package for the IEEE conference paper.
This script creates a directory with only the essential files needed for Overleaf compilation.
"""

import os
import shutil
from pathlib import Path

def create_overleaf_package():
    """Create a clean directory structure for Overleaf upload."""
    
    # Define the package directory
    package_dir = "overleaf_package"
    
    # Remove existing package directory if it exists
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    # Create the package directory
    os.makedirs(package_dir)
    print(f"Created directory: {package_dir}/")
    
    # Essential files to include
    essential_files = [
        "real_time_steering_paper.tex",  # Main LaTeX file
    ]
    
    # Figure files to include
    figure_files = [
        "images/system_architecture.png",
        "figures/free_space_profile.png", 
        "figures/depth_comparison.png",
        "figures/environments.png"
    ]
    
    # Copy main LaTeX file
    print("\nCopying essential files:")
    for file in essential_files:
        if os.path.exists(file):
            shutil.copy2(file, package_dir)
            print(f"  ✓ {file}")
        else:
            print(f"  ❌ {file} (not found)")
    
    # Create figures subdirectory in package
    figures_dir = os.path.join(package_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)
    
    # Copy figure files
    print(f"\nCopying figures to {figures_dir}/:")
    for fig_file in figure_files:
        if os.path.exists(fig_file):
            # Get just the filename for the destination
            filename = os.path.basename(fig_file)
            dest_path = os.path.join(figures_dir, filename)
            shutil.copy2(fig_file, dest_path)
            print(f"  ✓ {fig_file} → figures/{filename}")
        else:
            print(f"  ❌ {fig_file} (not found)")
    
    return package_dir

def update_tex_file_for_overleaf(package_dir):
    """Update the LaTeX file to use the correct figure paths for Overleaf."""
    
    tex_file = os.path.join(package_dir, "real_time_steering_paper.tex")
    
    if not os.path.exists(tex_file):
        print("❌ LaTeX file not found in package directory")
        return
    
    print(f"\nUpdating figure paths in {tex_file}...")
    
    # Read the original file
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update figure paths to use the figures/ directory
    replacements = [
        ("images/system_architecture.png", "figures/system_architecture.png"),
        ("figures/free_space_profile.png", "figures/free_space_profile.png"),
        ("figures/depth_comparison.png", "figures/depth_comparison.png"),
        ("figures/environments.png", "figures/environments.png")
    ]
    
    for old_path, new_path in replacements:
        if old_path in content:
            content = content.replace(old_path, new_path)
            print(f"  ✓ Updated: {old_path} → {new_path}")
    
    # Write the updated content
    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(content)

def create_readme_for_overleaf(package_dir):
    """Create a README file with Overleaf instructions."""
    
    readme_content = """# Overleaf Package: Real-Time Steering Angle Estimation Paper

## Files Included

### Main Document
- `real_time_steering_paper.tex` - Main LaTeX paper file

### Figures
- `figures/system_architecture.png` - System architecture flowchart
- `figures/free_space_profile.png` - 1D free-space analysis visualization
- `figures/depth_comparison.png` - Depth map comparison across model variants
- `figures/environments.png` - System performance in different environments

## How to Use with Overleaf

### Method 1: Upload ZIP File
1. Create a ZIP file of this entire directory
2. Go to Overleaf.com and create a new project
3. Choose "Upload Project" and select your ZIP file
4. Overleaf will automatically extract and set up the project

### Method 2: Manual Upload
1. Create a new blank project in Overleaf
2. Upload `real_time_steering_paper.tex` as the main file
3. Create a `figures/` folder in Overleaf
4. Upload all PNG files to the `figures/` folder
5. Set `real_time_steering_paper.tex` as the main document

## Compilation
- The paper uses the `IEEEtran` document class
- Overleaf should automatically detect this and compile correctly
- If needed, set the compiler to `pdfLaTeX`

## Paper Details
- **Title**: Real-Time Steering Angle Estimation via Monocular Depth Profiling and 1D Free-Space Analysis
- **Format**: IEEE Conference Paper
- **Document Class**: IEEEtran
- **Figures**: 4 high-resolution PNG images (300 DPI)

## Troubleshooting
- If figures don't appear, check that they're in the `figures/` directory
- Ensure the main document is set to `real_time_steering_paper.tex`
- All figure paths use forward slashes: `figures/filename.png`

## File Sizes
- Total package size: ~3-4 MB
- All figures are optimized for academic publication
- High resolution (300 DPI) suitable for print and digital publication
"""
    
    readme_path = os.path.join(package_dir, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"  ✓ Created {readme_path}")

def create_zip_package(package_dir):
    """Create a ZIP file of the Overleaf package."""
    
    zip_filename = f"{package_dir}.zip"
    
    # Remove existing ZIP if it exists
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
    
    # Create ZIP file
    shutil.make_archive(package_dir, 'zip', package_dir)
    
    if os.path.exists(zip_filename):
        size = os.path.getsize(zip_filename)
        print(f"  ✓ Created {zip_filename} ({size:,} bytes)")
        return zip_filename
    else:
        print(f"  ❌ Failed to create {zip_filename}")
        return None

def main():
    """Main function to prepare Overleaf package."""
    
    print("=" * 70)
    print("PREPARING OVERLEAF PACKAGE")
    print("=" * 70)
    
    # Create the package directory and copy files
    package_dir = create_overleaf_package()
    
    # Update LaTeX file for Overleaf
    update_tex_file_for_overleaf(package_dir)
    
    # Create README
    print(f"\nCreating documentation:")
    create_readme_for_overleaf(package_dir)
    
    # Create ZIP package
    print(f"\nCreating ZIP package:")
    zip_file = create_zip_package(package_dir)
    
    # Final summary
    print("\n" + "=" * 70)
    print("✅ OVERLEAF PACKAGE READY!")
    print("=" * 70)
    
    print(f"\nPackage Directory: {package_dir}/")
    print(f"ZIP File: {package_dir}.zip")
    
    print(f"\nContents of {package_dir}/:")
    for root, dirs, files in os.walk(package_dir):
        level = root.replace(package_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                print(f"{subindent}{file} ({size:,} bytes)")
            except:
                print(f"{subindent}{file}")
    
    print(f"\n📋 INSTRUCTIONS FOR OVERLEAF:")
    print("1. Go to overleaf.com and create a new project")
    print("2. Choose 'Upload Project' and select the ZIP file:")
    print(f"   {package_dir}.zip")
    print("3. Overleaf will automatically extract and set up the project")
    print("4. Set 'real_time_steering_paper.tex' as the main document")
    print("5. Compile with pdfLaTeX")
    
    print(f"\n🎯 Alternative: Manual upload individual files from {package_dir}/")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
