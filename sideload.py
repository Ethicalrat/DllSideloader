import os
import sys
import uuid
import shutil
import pefile
import pathlib
import subprocess

#Read target dll from sys arg
target_dll = sys.argv[1]

#Copy dll to current folder with a random name

current_dir = os.getcwd()
random_name = str(uuid.uuid4())
random_name_dll = random_name + ".dll"
shutil.copy(target_dll, os.path.join(current_dir, random_name_dll))


#Generate exports for the target dll. Code taken from

dll_path = pathlib.Path(random_name_dll)
dll = pefile.PE(dll_path)

original_stdout = sys.stdout

def_file = random_name + ".def"
with open(def_file, 'w') as f:
    sys.stdout = f
    print("EXPORTS")
    for export in dll.DIRECTORY_ENTRY_EXPORT.symbols:
        if export.name:
            print(f"\t{export.name.decode()}={dll_path.stem}.{export.name.decode()} @{export.ordinal}")
sys.stdout = original_stdout

#compile c++ dll source code with gcc

cpp_file = "dllmain.cpp"
out_file = target_dll
compile_command = f"gcc -shared -o {out_file} {cpp_file} {def_file} -s"
result = subprocess.run(compile_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if result.returncode == 0:
    print("Compilation successful")
else:
    print("Compilation failed")
    print("Error:", result.stderr.decode('utf-8'))
