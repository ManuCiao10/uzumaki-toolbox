VERSION="0.0.24"

VERSION_MAC="0.0.24."

#if windows
pyinstaller --onefile --console --icon icon.ico --name Uzumaki_$VERSION.exe Uzumaki.py

# if mac
pyinstaller --onefile Uzumaki.py --name Uzumaki_$VERSION_MAC


