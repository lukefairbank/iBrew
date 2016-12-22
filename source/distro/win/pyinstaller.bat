git clone https://github.com/pyinstaller/pyinstaller.git
cd pyinstaller\bootloader\
python .\waf distclean all
cd ..
python setup.py install
cd ..	
rmdir /s /q pyinstaller
