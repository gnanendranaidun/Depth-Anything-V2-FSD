#!/bin/bash
# Script to compile the IEEE conference paper

# Check if pdflatex is installed
if ! command -v pdflatex &> /dev/null; then
    echo "Error: pdflatex is not installed or not in PATH."
    echo "Please install a LaTeX distribution (e.g., TeX Live, MiKTeX) and try again."
    exit 1
fi

# Check if bibtex is installed
if ! command -v bibtex &> /dev/null; then
    echo "Error: bibtex is not installed or not in PATH."
    echo "Please install a LaTeX distribution (e.g., TeX Live, MiKTeX) and try again."
    exit 1
fi

# Check if the paper file exists
if [ ! -f "real_time_steering_paper.tex" ]; then
    echo "Error: real_time_steering_paper.tex not found."
    exit 1
fi

# Compile the paper
echo "Compiling the paper..."
pdflatex real_time_steering_paper.tex
bibtex real_time_steering_paper
pdflatex real_time_steering_paper.tex
pdflatex real_time_steering_paper.tex

# Check if the PDF was generated
if [ -f "real_time_steering_paper.pdf" ]; then
    echo "Paper compiled successfully: real_time_steering_paper.pdf"
    
    # Open the PDF if possible
    if command -v open &> /dev/null; then
        echo "Opening the PDF..."
        open real_time_steering_paper.pdf
    elif command -v xdg-open &> /dev/null; then
        echo "Opening the PDF..."
        xdg-open real_time_steering_paper.pdf
    else
        echo "PDF viewer not found. Please open real_time_steering_paper.pdf manually."
    fi
else
    echo "Error: Failed to generate real_time_steering_paper.pdf"
    exit 1
fi
