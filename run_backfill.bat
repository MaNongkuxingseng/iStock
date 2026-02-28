@echo off
echo Executing historical data backfill...
echo Start time: %date% %time%

mysql -u root -p123456 mystock < "G:\openclaw\workspace\_system\agent-home\backfill_data.sql"

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Data backfill completed successfully!
    echo.
    echo Verification query:
    mysql -u root -p123456 -e "USE mystock; SELECT COUNT(*) as total_records, MIN(date) as earliest, MAX(date) as latest FROM cn_stock_indicators_sell;"
) else (
    echo.
    echo [ERROR] Data backfill failed!
)

echo End time: %date% %time%
pause
