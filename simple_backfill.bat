@echo off
echo Batch Data Backfill: 2026-02-14 to 2026-02-26
echo.

cd /d "G:\openclaw\workspace\projects\active\myStock\instock\job"

echo Current database records:
"C:\Program Files\MySQL\MySQL Server 9.4\bin\mysql.exe" -uroot -p785091 instockdb -e "SELECT date, COUNT(*) as records FROM cn_stock_indicators_sell GROUP BY date ORDER BY date DESC;" 2>nul

echo.
echo Starting backfill...
echo.

set success=0
set fail=0

for %%d in (
    2026-02-14
    2026-02-15
    2026-02-16
    2026-02-17
    2026-02-18
    2026-02-19
    2026-02-20
    2026-02-21
    2026-02-22
    2026-02-23
    2026-02-24
    2026-02-25
    2026-02-26
) do (
    echo Processing %%d...
    python strategy_data_daily_job.py --date %%d > backfill_%%d.log 2>&1
    if errorlevel 0 (
        echo   Success
        set /a success+=1
    ) else (
        echo   Failed
        set /a fail+=1
    )
    timeout /t 2 /nobreak > nul
)

echo.
echo Backfill completed:
echo   Success: %success%
echo   Failed: %fail%
echo   Total: 13

echo.
echo Final database status:
"C:\Program Files\MySQL\MySQL Server 9.4\bin\mysql.exe" -uroot -p785091 instockdb -e "SELECT date, COUNT(*) as records FROM cn_stock_indicators_sell GROUP BY date ORDER BY date DESC;" 2>nul

echo.
echo Log files saved in: G:\openclaw\workspace\projects\active\myStock\instock\job\