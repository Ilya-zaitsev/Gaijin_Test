import os
import importlib.util
import subprocess
import sys

def find_python_files(directory_path):
    all_py_files = []
    for address, dirs, files in os.walk(directory_path):
        for name in files:
            file = os.path.join(address, name)
            if file.endswith('.py'):
                all_py_files.append(file)

    return sorted(all_py_files, key=str.lower)


def extract_cmds_from_file(file_path):
    spec = importlib.util.spec_from_file_location("module", file_path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        cmds = getattr(module, 'CMDS', None)
        if isinstance(cmds, list):
            return cmds
        else:
            print(f'Ошибка при извлечении команд из файла {file_path}: CMDS не список!')
            return []
    except Exception as e:
        print(f'Ошибка при извлечении команд из файла {file_path}: {e}')
        return []


def execute_commands(cmds):
    executed_commands = []

    for cmd in cmds:
        if cmd not in executed_commands:
            try:
                subprocess.run(cmd, shell=True, check=True)
                executed_commands.append(cmd)
            except subprocess.CalledProcessError as e:
                print(f'Ошибка при выполнении команды "{cmd}": {e}')
        else:
            print(f'Команда "{cmd}" уже была выполнена, пропускаем.')


def main(directory):
    all_cmds = []
    python_files = find_python_files(directory)

    for file in python_files:
        cmds = extract_cmds_from_file(file)
        all_cmds.extend(cmds)
    # print(all_cmds)

    execute_commands(all_cmds)

def Error(Er_str):
    print(Er_str)
    input("Нажмите ENTER для выхода")
    sys.exit(-1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        Error("Не передан путь к директории!")
    directory_path = sys.argv[1]

    if not (os.path.exists(directory_path)) or not os.path.isdir(directory_path):
        Error("Путь до директории не правильный!")
    else:
        main(directory_path)