@echo off
REM Wikipedia Language Equity Analysis - Installation Script for Windows
REM Run this to install all required packages

echo Installing required Python packages...
echo.

pip install requests
pip install pandas
pip install openpyxl
pip install plotly
pip install pyarrow

echo.
echo Installation complete!
echo.
echo Optional: Install kaleido for static image export
echo   pip install kaleido
echo.
echo You can now run the analysis:
echo   python wikipedia_analyzer_enhanced.py
echo.
pause
