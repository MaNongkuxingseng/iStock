@echo off
echo Installing mystock dependencies...

pip install tornado --target="D:\Program Files\Python\Lib\site-packages"
pip install pymysql --target="D:\Program Files\Python\Lib\site-packages"
pip install sqlalchemy --target="D:\Program Files\Python\Lib\site-packages"
pip install pandas --target="D:\Program Files\Python\Lib\site-packages"
pip install numpy --target="D:\Program Files\Python\Lib\site-packages"
pip install talib --target="D:\Program Files\Python\Lib\site-packages"
pip install requests --target="D:\Program Files\Python\Lib\site-packages"
pip install beautifulsoup4 --target="D:\Program Files\Python\Lib\site-packages"
pip install lxml --target="D:\Program Files\Python\Lib\site-packages"
pip install tqdm --target="D:\Program Files\Python\Lib\site-packages"
pip install py_mini_racer --target="D:\Program Files\Python\Lib\site-packages"

echo.
echo Dependencies installation completed.
echo.