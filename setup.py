import sys
from cx_Freeze import setup, Executable

# no includes ficam todas as dependencias que o projeto precisa
# no include_files ficam todos as mídias necessárias para o projeto
build_exe_options = {"packages": ["pandas","os"], "includes": ["pyautogui", "PySimpleGUI", "PIL", "functools", "keyboard","pyperclip", "os", "requests", "time", "sys", "speech_recognition"], "include_files":["img/semPedidos.jpg", "img/icon.ico", "img/btAprova2.png", "img/btEstacionar.jpg", "img/btReprova.png" ]} 

# GUI applications require a different base on Windows (the default is for
# a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Bot Auditoria",
    version="3.0",
    description="Automatizador da tela de auditoria",
    options={"build_exe": build_exe_options},
    executables=[Executable(script="main.py", base=base, icon="img/icon.ico",)]
)
# Agora é só dar  o comando no terminal: python .\setup.py build

