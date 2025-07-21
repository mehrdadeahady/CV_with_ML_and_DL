For creating executable file from python apps there are a lot of options.
Main tool is pyinstaller but its ouput.exe file is very slow for unpacking and loading embedded resources.
So I used nuitka here. Below is a full command:
python -m nuitka --standalone \                      'Embedding all resources'
                 --include-module=_ctypes \          'Importing _ctypes'
                 --include-module=ctypes \           'Importing ctypes'
                 --include-package=ctypes \          'Importing ctypes'
                 --enable-plugin=pyqt6 \             'Adding pyqt6 support'
                 --include-data-dir=./icons=icons \  'Adding icons folder and its files'
                 --include-data-dir=./pages=pages \  'Adding pages folder and its files'
                 --windows-console-mode=disable \    'Disabilg console'
                 --onefile \                         'Putting all in one file'
                 ./app.py                            'Path to Main file (entry point)'