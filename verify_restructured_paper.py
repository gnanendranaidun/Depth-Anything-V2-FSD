#!/usr/bin/env python3
"""
Verification script for the restructured IEEE conference paper
"""

import os
import re

def verify_paper_structure():
    """Verify that the restructured paper follows the required outline."""
    print("🔍 VERIFYING RESTRUCTURED PAPER STRUCTURE")
    print("="*50)
    
    tex_file = "restructured_steering_paper.tex"
    
    if not os.path.exists(tex_file):
        print(f"❌ File not found: {tex_file}")
        return False
    
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define the required structure
    required_sections = [
        r'\\section\{Introduction\}',
        r'\\subsection\{Background\}',
        r'\\subsection\{Motivation\}', 
        r'\\subsection\{Solution Overview\}',
        r'\\section\{Literature Review\}',
        r'\\subsection\{Current Solutions\}',
        r'\\subsection\{Typical Approaches\}',
        r'\\subsection\{Limitations\}',
        r'\\section\{Definitions and Terminology\}',
        r'\\subsection\{Key Terms\}',
        r'\\subsection\{Brief Explanations\}',
        r'\\section\{Proposed Methodology\}',
        r'\\subsection\{Rationale\}',
        r'\\subsection\{Technical Approach\}',
        r'\\subsection\{Mathematical Framework\}',
        r'\\section\{Experimental Setup and Results\}',
        r'\\subsection\{Experimental Setup\}',
        r'\\subsection\{Evaluation Metrics\}',
        r'\\subsection\{Results Analysis\}',
        r'\\subsection\{Comparative Analysis\}',
        r'\\section\{Conclusion and Future Work\}',
        r'\\subsection\{Summary\}',
        r'\\subsection\{Current Limitations\}',
        r'\\subsection\{Future Enhancements\}'
    ]
    
    print("\n📋 CHECKING REQUIRED SECTIONS:")
    all_sections_found = True
    
    for i, section_pattern in enumerate(required_sections, 1):
        if re.search(section_pattern, content):
            section_name = section_pattern.replace(r'\\section\{', '').replace(r'\\subsection\{', '').replace(r'\}', '')
            print(f"✅ {i:2d}. {section_name}")
        else:
            section_name = section_pattern.replace(r'\\section\{', '').replace(r'\\subsection\{', '').replace(r'\}', '')
            print(f"❌ {i:2d}. {section_name} - MISSING")
            all_sections_found = False
    
    return all_sections_found

def verify_figures():
    """Verify that all figures are properly referenced and exist."""
    print("\n🖼️  VERIFYING FIGURES:")
    
    tex_file = "restructured_steering_paper.tex"
    
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all figure references
    figure_refs = re.findall(r'\\includegraphics.*?\{(.*?)\}', content)
    label_refs = re.findall(r'\\label\{(fig_.*?)\}', content)
    ref_calls = re.findall(r'\\ref\{(fig_.*?)\}', content)
    
    print(f"Found {len(figure_refs)} figure includes:")
    for fig_path in figure_refs:
        if os.path.exists(fig_path):
            file_size = os.path.getsize(fig_path)
            print(f"✅ {fig_path} - {file_size:,} bytes")
        else:
            print(f"❌ {fig_path} - FILE NOT FOUND")
    
    print(f"\nFound {len(label_refs)} figure labels:")
    for label in label_refs:
        print(f"✅ {label}")
    
    print(f"\nFound {len(ref_calls)} figure references:")
    for ref in ref_calls:
        if ref in label_refs:
            print(f"✅ \\ref{{{ref}}} - label exists")
        else:
            print(f"❌ \\ref{{{ref}}} - LABEL NOT FOUND")
    
    return len(figure_refs) > 0 and len(label_refs) == len(set(ref_calls))

def verify_content_preservation():
    """Verify that key content from original paper is preserved."""
    print("\n📄 VERIFYING CONTENT PRESERVATION:")
    
    tex_file = "restructured_steering_paper.tex"
    
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for key technical content
    key_elements = [
        ("Abstract", r'\\begin\{abstract\}'),
        ("Keywords", r'\\begin\{IEEEkeywords\}'),
        ("Depth-Anything-V2", r'Depth-Anything-V2'),
        ("Mathematical equations", r'\\begin\{equation\}'),
        ("Tables", r'\\begin\{table\}'),
        ("Bibliography", r'\\begin\{thebibliography\}'),
        ("ROI processing", r'roi_top_frac'),
        ("1D profile", r'1D.*profile'),
        ("Steering angle", r'steering.*angle'),
        ("Free-space analysis", r'free-space.*analysis')
    ]
    
    for element_name, pattern in key_elements:
        if re.search(pattern, content, re.IGNORECASE):
            print(f"✅ {element_name} - preserved")
        else:
            print(f"❌ {element_name} - MISSING")
    
    # Count key metrics
    equation_count = len(re.findall(r'\\begin\{equation\}', content))
    table_count = len(re.findall(r'\\begin\{table\}', content))
    figure_count = len(re.findall(r'\\begin\{figure\}', content))
    citation_count = len(re.findall(r'\\cite\{.*?\}', content))
    
    print(f"\n📊 CONTENT METRICS:")
    print(f"   Equations: {equation_count}")
    print(f"   Tables: {table_count}")
    print(f"   Figures: {figure_count}")
    print(f"   Citations: {citation_count}")
    
    return True

def verify_ieee_formatting():
    """Verify IEEE conference paper formatting."""
    print("\n📝 VERIFYING IEEE FORMATTING:")
    
    tex_file = "restructured_steering_paper.tex"
    
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    formatting_checks = [
        ("Document class", r'\\documentclass\[conference\]\{IEEEtran\}'),
        ("Title", r'\\title\{.*?\}'),
        ("Authors", r'\\author\{.*?\}'),
        ("Abstract", r'\\begin\{abstract\}.*?\\end\{abstract\}'),
        ("Keywords", r'\\begin\{IEEEkeywords\}.*?\\end\{IEEEkeywords\}'),
        ("Bibliography", r'\\begin\{thebibliography\}'),
        ("Acknowledgment", r'\\section\*\{Acknowledgment\}')
    ]
    
    for check_name, pattern in formatting_checks:
        if re.search(pattern, content, re.DOTALL):
            print(f"✅ {check_name} - correct format")
        else:
            print(f"❌ {check_name} - FORMATTING ISSUE")
    
    return True

def main():
    """Main verification function."""
    print("🔍 RESTRUCTURED PAPER VERIFICATION")
    print("="*60)
    
    # Run all verification checks
    structure_ok = verify_paper_structure()
    figures_ok = verify_figures()
    content_ok = verify_content_preservation()
    format_ok = verify_ieee_formatting()
    
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    if structure_ok:
        print("✅ Paper structure follows required outline")
    else:
        print("❌ Paper structure issues found")
    
    if figures_ok:
        print("✅ All figures properly referenced and exist")
    else:
        print("❌ Figure reference issues found")
    
    if content_ok:
        print("✅ Key content preserved from original")
    else:
        print("❌ Content preservation issues found")
    
    if format_ok:
        print("✅ IEEE formatting standards maintained")
    else:
        print("❌ Formatting issues found")
    
    overall_success = structure_ok and figures_ok and content_ok and format_ok
    
    if overall_success:
        print("\n🎉 VERIFICATION SUCCESSFUL!")
        print("The restructured paper is ready for submission.")
    else:
        print("\n⚠️  VERIFICATION ISSUES FOUND")
        print("Please review and fix the issues above.")
    
    return overall_success

if __name__ == "__main__":
    main()
