For creating executable file from python apps there are a lot of options.
Main tool is pyinstaller but its ouput.exe file is very slow for unpacking and loading embedded resources.
Other option is nuitka tool, that is compatible with python 3.4 to 3.12, so if main python version is different, 
install a compatible version separately and run that version by pointing to its path.
Below is a full command:
python -m nuitka --standalone                      'Embedding all resources'                 
                 --include-module=_ctypes          'Importing _ctypes'                       
                 --include-module=ctypes           'Importing ctypes'                        
                 --include-package=ctypes          'Importing ctypes'                        
                 --enable-plugin=pyqt6             'Adding pyqt6 support'                   
                 --include-data-dir=./icons=icons  'Adding icons folder and its files'       
                 --include-data-dir=./pages=pages  'Adding pages folder and its files'       
                 --windows-console-mode=disable    'Disabilg console'                        
                 --onefile                         'Putting all in one file'                 
                 ./app.py                          'Path to Main file (entry point)'

#python -m nuitka --standalone --include-module=_ctypes --include-module=ctypes --include-package=ctypes  --enable-plugin=pyqt6 --windows-console-mode=disable --onefile ./app.py