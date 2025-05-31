#!/usr/bin/env python3
"""
Verify that all figures referenced in the LaTeX paper are present and accessible.
"""

import os
import re
from pathlib import Path

def extract_figure_references(tex_file):
    """Extract all figure references from the LaTeX file."""
    if not os.path.exists(tex_file):
        print(f"Error: {tex_file} not found")
        return []
    
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all \includegraphics commands
    pattern = r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}'
    matches = re.findall(pattern, content)
    
    return matches

def check_figure_exists(figure_path):
    """Check if a figure file exists."""
    # Try different extensions if no extension is provided
    if not os.path.splitext(figure_path)[1]:
        extensions = ['.png', '.jpg', '.jpeg', '.pdf', '.eps']
        for ext in extensions:
            if os.path.exists(figure_path + ext):
                return True, figure_path + ext
        return False, figure_path
    else:
        return os.path.exists(figure_path), figure_path

def main():
    """Main verification function."""
    print("=" * 70)
    print("PAPER FIGURE VERIFICATION")
    print("=" * 70)
    
    tex_file = "real_time_steering_paper.tex"
    
    # Extract figure references
    print(f"Analyzing {tex_file}...")
    figure_refs = extract_figure_references(tex_file)
    
    if not figure_refs:
        print("No figure references found in the LaTeX file.")
        return
    
    print(f"Found {len(figure_refs)} figure reference(s):")
    print()
    
    all_present = True
    
    for i, fig_path in enumerate(figure_refs, 1):
        exists, actual_path = check_figure_exists(fig_path)
        status = "✓ FOUND" if exists else "❌ MISSING"
        
        print(f"{i}. {fig_path}")
        print(f"   Status: {status}")
        if exists:
            print(f"   Path: {actual_path}")
            # Get file size
            try:
                size = os.path.getsize(actual_path)
                print(f"   Size: {size:,} bytes")
            except:
                print(f"   Size: Unable to determine")
        print()
        
        if not exists:
            all_present = False
    
    print("=" * 70)
    if all_present:
        print("✅ SUCCESS: All figures are present and accessible!")
        print()
        print("The paper is ready for compilation. You can:")
        print("1. Install LaTeX (e.g., TeX Live, MiKTeX)")
        print("2. Run: ./compile_paper.sh")
        print("3. Or manually compile with: pdflatex real_time_steering_paper.tex")
    else:
        print("❌ ERROR: Some figures are missing!")
        print()
        print("Missing figures need to be generated or downloaded.")
    
    print("=" * 70)
    
    # Additional information
    print("\nFIGURE DIRECTORY CONTENTS:")
    print("-" * 30)
    
    for directory in ['figures', 'images']:
        if os.path.exists(directory):
            print(f"\n{directory}/:")
            files = sorted(os.listdir(directory))
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf', '.eps')):
                    file_path = os.path.join(directory, file)
                    try:
                        size = os.path.getsize(file_path)
                        print(f"  {file} ({size:,} bytes)")
                    except:
                        print(f"  {file}")
        else:
            print(f"\n{directory}/: Directory not found")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
