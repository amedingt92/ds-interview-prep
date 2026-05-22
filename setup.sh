#!/usr/bin/env bash
# setup.sh — run this once after cloning, or any time you want a clean slate
# Usage: bash setup.sh

set -e

echo ""
echo "── ds-interview-prep setup ─────────────────────────────────────────────"
echo ""

# Check Python version
PYTHON=$(python3 --version 2>&1)
echo "  Python: $PYTHON"

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "  Creating virtual environment..."
    python3 -m venv venv
else
    echo "  Virtual environment already exists — skipping creation"
fi

# Activate
source venv/bin/activate

# Install dependencies
echo "  Installing dependencies..."
pip install -r requirements.txt -q

# Generate data
echo "  Generating dataset..."
python data/generate.py

echo ""
echo "── Setup complete ───────────────────────────────────────────────────────"
echo ""
echo "  To activate your venv in the future:"
echo "    source venv/bin/activate        (Mac/Linux)"
echo "    venv\\Scripts\\activate           (Windows)"
echo ""
echo "  To start:"
echo "    python sql/lesson-01-select-filtering/lesson.py"
echo ""
