#!/bin/bash

# arXiv Build Script
# This script creates a clean arXiv submission package from the main paper directory
# Usage: ./arxiv_build.sh

set -e  # Exit on any error

echo "🚀 Building arXiv submission package..."

# Create temporary directory
TEMP_DIR="arxiv_temp_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$TEMP_DIR"

echo "📁 Copying essential files..."
# Copy only essential files for arXiv submission
cp ml_ucb.tex "$TEMP_DIR/"
cp mybib.bib "$TEMP_DIR/"
cp *.png "$TEMP_DIR/" 2>/dev/null || echo "⚠️  No PNG files found"

# Change to temp directory and build
cd "$TEMP_DIR"

echo "🔨 Compiling LaTeX..."
# Full LaTeX build cycle
pdflatex ml_ucb.tex > build.log 2>&1
bibtex ml_ucb >> build.log 2>&1
pdflatex ml_ucb.tex >> build.log 2>&1
pdflatex ml_ucb.tex >> build.log 2>&1

# Check if PDF was created successfully
if [[ ! -f ml_ucb.pdf ]]; then
    echo "❌ Error: PDF compilation failed. Check build.log"
    cat build.log
    exit 1
fi

echo "🧹 Cleaning auxiliary files..."
# Remove auxiliary files that arXiv doesn't need
rm -f *.aux *.log *.out *.bbl *.blg *.toc *.lof *.lot *.fls *.fdb_latexmk *.synctex.gz
rm -f build.log

# Create archive
cd ..
ARCHIVE_NAME="ml_ucb_arxiv_$(date +%Y%m%d_%H%M%S).tar.gz"
tar -czf "$ARCHIVE_NAME" -C "$TEMP_DIR" .

# Clean up temp directory
rm -rf "$TEMP_DIR"

echo "✅ arXiv submission package created: $ARCHIVE_NAME"
echo "📊 Archive size: $(du -h "$ARCHIVE_NAME" | cut -f1)"
echo ""
echo "📋 Next steps:"
echo "1. Upload $ARCHIVE_NAME to arXiv"
echo "2. Select subject categories (likely cs.LG - Machine Learning)"
echo "3. Review the rendered PDF on arXiv's system"
echo "4. Submit for processing"