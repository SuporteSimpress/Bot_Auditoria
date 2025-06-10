import pandas as pd
import os


def lerClientes():
 file_id = "1_d-5B60n_gF4jxXSvmLGVmT3y734qjNd"
 url = f"https://drive.google.com/uc?id={file_id}"
 if not os.path.exists(url):
        print("Arquivo de técnicos clientes não encontrado.")
        return
 df = pd.read_csv(url)

def lerTecnicos():
 file_id = "1jHA03Me2wtgW6Py9zY8yxBBl6ndFQ0Rz"
 url = f"https://drive.google.com/uc?id={file_id}"
 if not os.path.exists(url):
        print("Arquivo de técnicos não encontrado.")
        return
 df = pd.read_csv(url)


def lerGit():
 url = "https://raw.githubusercontent.com/usuario/repositorio/main/arquivo.csv"
 df = pd.read_csv(url)


def lerLocal():
    url = "D:/Users/samue/Samuel/PROGRAMAÇÃO/Python/_PROJETOS/Auditoria de peças/Bot_Auditoria - clique 2.1.3/dados1/clientes.csv"
    df = pd.read_csv(url)
    print(df)

  


lerClientes()