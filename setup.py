import sys
from cx_Freeze import setup, Executable

# no includes ficam todas as dependencias que o projeto precisa
# no include_files ficam todos as mídias necessárias para o projeto
build_exe_options = {"packages": ["os"], "includes": ["pyautogui", "PySimpleGUI", "PIL", "functools", "keyboard"], "include_files":["img/semPedidos.jpg", "img/aprovaOrcamento.png", "img/telaPedido.png", "img/blockP.png", "img/atualizaTela.jpg", "img/icon.ico"]} 

# GUI applications require a different base on Windows (the default is for
# a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Bot Auditoria",
    version="2.1.3",
    description="Automatizador da tela de auditoria",
    options={"build_exe": build_exe_options},
    executables=[Executable(script="auditoria.py", base=base, icon="img/icon.ico",)]
)
# Agora é só dar  o comando no terminal: python .\setup.py build

