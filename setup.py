import sys
from cx_Freeze import setup, Executable

build_exe_options = dict(
    compressed = True,
    includes = ['urllib', 'urllib.request', 're', 'csv', 'bs4', 'selenium', 'xlsxwriter'],
    include_files = ['./chromedriver']
)



setup( name = "crawler",
       version = '1.0',
       description = "crawler",
       author = "Heoju",
       options = {"build_ext":build_exe_options},
       executables = [Executable("main.py")])
