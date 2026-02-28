@echo off
echo Starting historical data backfill...
echo.

cd /d "G:\openclaw\workspace\projects\active\myStock\instock\job"

echo Backfilling data for 2026-02-14...
python strategy_data_daily_job.py --date 2026-02-14 > backfill_2026-02-14.log 2>&1
if %errorlevel% equ 0 (
    echo   Success: 2026-02-14
) else (
    echo   Failed: 2026-02-14
    type backfill_2026-02-14.log
)

echo.
echo Checking database records...
"C:\Program Files\MySQL\MySQL Server 9.4\bin\mysql.exe" -uroot -p785091 instockdb -e "SELECT date, COUNT(*) as records FROM cn_stock_indicators_sell GROUP BY date ORDER BY date DESC;" 2>nul

echo.
echo Backfill process started.
echo Log files saved in current directory.