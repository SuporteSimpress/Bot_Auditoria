# bot_unificado.py
# Arquivo unificado: juntei as funcionalidades do seu app principal + auditoria + tela esquerda
# Implementação de "segure para falar" no botão -LISTEN- usando bind de mouse (ButtonPress / ButtonRelease)
# Atenção: pyautogui.locateOnScreen depende de imagens em pasta img/ e resolução/região correta.

import PySimpleGUI as sg
import speech_recognition as sr
import pyautogui
import pyperclip
import time
import threading
import sys
import keyboard
import csv
import pandas as pd
import webbrowser
from PIL import ImageGrab
from functools import partial
from screeninfo import get_monitors

# Força captura de todas as telas com PIL (mesma lógica que você tinha)
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

# ----------------------------- VARIÁVEIS GLOBAIS -----------------------------
# Valores iniciais (ajuste se necessário)
barra = 38           # offset da barra de favoritos (ajustado para matching com auditoria_TelaEsquerda)
monitor = 0
monitor_telaprincipal = 0
btmonitor = 0
btaprova = 0
regiao = (0, 0, 1366, 768)
tela_selecionada = "Central"

# Flags / controles microfone
mic_stop_event = None
mic_thread = None

# Variáveis de auditoria / listas
tecnicos = []
mercantil = []
analista_selecionado = ""
pedirNome = ""

# Variáveis de pedidos travados (TelaEsquerda)
pedidosTravados = 0
larg = 0
selecionaPed = True

# ----------------------------- CARREGA LISTAS (tecnicos / clientes) -----------------------------
# Tenta ler dos urls; se falhar usa arquivos locais
try:
    clientes_url = "https://raw.githubusercontent.com/SuporteSimpress/Bot_Auditoria/main/dados/clientes.csv"
    tecnicos_url = "https://raw.githubusercontent.com/SuporteSimpress/Bot_Auditoria/main/dados/tecnicos.csv"
    analistas_url = "https://raw.githubusercontent.com/SuporteSimpress/Bot_Auditoria/main/dados/analistas.csv"

    df = pd.read_csv(clientes_url, encoding='utf-8')
    mercantil = [", ".join(map(str, linha)) for linha in df.values.tolist()]

    dftecnicos = pd.read_csv(tecnicos_url, encoding='utf-8')
    tecnicos = [", ".join(map(str, linha)) for linha in dftecnicos.values.tolist()]

    dfanalistas = pd.read_csv(analistas_url, encoding='utf-8')
    analistas = [", ".join(map(str, linha)) for linha in dfanalistas.values.tolist()]

except Exception:
    # fallback para arquivos locais
    try:
        with open("./dados/tecnicos.csv", "r", encoding='utf-8') as arquivo:
            arquivo_csv = csv.reader(arquivo, delimiter=",")
            for i, linha in enumerate(arquivo_csv):
                if i == 0:
                    pass
                else:
                    tecnicos += linha
    except Exception:
        tecnicos = []

    try:
        with open("./dados/clientes.csv", "r", encoding='utf-8') as arquivo:
            arquivo_csv = csv.reader(arquivo, delimiter=",")
            for i, linha in enumerate(arquivo_csv):
                if i == 0:
                    pass
                else:
                    mercantil += linha
    except Exception:
        mercantil = []

    try:
        with open("./dados/analistas.csv", "r", encoding='utf-8') as arquivo:
            arquivo_csv = csv.reader(arquivo, delimiter=",")
            for i, linha in enumerate(arquivo_csv):
                if i == 0:
                    pass
                else:
                    analistas += linha
    except Exception:
        analistas = []

# ----------------------------- FUNÇÕES REUTILIZÁVEIS -----------------------------

def alternar(janela_atual, outra_janela):
    """Esconde a janela atual e mostra a outra."""
    try:
        janela_atual.hide()
        outra_janela.un_hide()
    except Exception:
        pass

def selecionaPedido(num):
    """Define se seleciona pedido (usado na tela de auditoria)."""
    global selecionaPed
    selecionaPed = True if str(num) == '1' else False

def construtor():
    """Inicializações da TelaEsquerda (mantive o que existia)."""
    global pedidosTravados, larg
    larg = 0
    pedidosTravados = 0
    selecionaPedido('1')

def verificaMonitor():
    monitors = get_monitors()
    teste = False
    for m in monitors:
        if m.x < 0:
            teste = True
    return teste

def barra_favoritos(verifica):
    """Define valor de 'barra' (offset) com base na escolha."""
    global barra
    if str(verifica) == '1':
        barra = 38
    else:
        barra = 0

def check_Tela(temp):
    """Define regiao/offsets de monitor conforme seleção."""
    global regiao, monitor, btmonitor, btaprova, tela_selecionada
    tela = str(temp)
    esq = verificaMonitor()
    if esq:
        btmonitor = -1366
        monitor1 = (0, 0, 1366, 768)
        monitor2 = (0, 0, 2732, 768)
        monitor3 = (2732, 0, 1366, 768)
    else:
        btmonitor = 0
        monitor1 = (0, 0, 1366, 768)
        monitor2 = (0, 0, 1366, 768)
        monitor3 = (1366, 0, 1366, 768)

    if tela == '1':
        regiao = monitor1
        monitor = -1366
        btaprova = -1366
        tela_selecionada = 'Esquerda'
    elif tela == '2':
        regiao = monitor2
        monitor = 0
        btaprova = 0
        tela_selecionada = 'Central'
    elif tela == '3':
        regiao = monitor3
        monitor = 1366
        btaprova = 0
        tela_selecionada = 'Direita'
    else:
        regiao = monitor2
        monitor = 0
        btaprova = 0
        tela_selecionada = 'Central'

def check_travados(trav):
    """Define offsets para pedidos travados (valor usado em VerRelatorio/aprova)."""
    global pedidosTravados, larg
    try:
        n = int(trav)
    except Exception:
        n = 0
    pedidosTravados = n * 60
    larg = -7 if n > 0 else 0

# ----------------------------- FUNÇÕES DE AUDITORIA (pyautogui) -----------------------------

def VerificaImg(imagem):
    """Procura imagem na tela dentro da região definida. Retorna True/False."""
    try:
        found = pyautogui.locateOnScreen(imagem, region=regiao, confidence=0.9, grayscale=True)
        return bool(found)
    except Exception:
        return False

def VerRelatorio():
    """Clica no relatório e tenta copiar informações (baseado no seu antigo código)."""
    x, y = pyautogui.position()
    try:
        pyautogui.click(monitor + 195, 400 + pedidosTravados + barra)
        cont = 0
        while not VerificaImg("img/relatorio.jpg"):
            time.sleep(1)
            cont += 1
            if cont > 10:
                return
        pyautogui.doubleClick(monitor + 265, 598 + barra)
        pyautogui.hotkey('ctrl', 'c')
        pyautogui.keyDown('shift')
        pyautogui.scroll(-2000, x=pyautogui.position()[0], y=pyautogui.position()[1])
        pyautogui.keyUp('shift')
        time.sleep(1)
        pyautogui.scroll(-500)
    finally:
        pyautogui.moveTo(x, y)

def aprova(mensagem):
    """Realiza processo de aprovação escrevendo texto no campo identificado."""
    x, y = pyautogui.position()
    try:
        bt = pyautogui.locateOnScreen("img/btEstacionar.jpg", region=regiao, confidence=0.9, grayscale=True)
        if bt:
            botao = pyautogui.center(bt)
            pyautogui.click(btmonitor + botao.x, botao.y)
            time.sleep(0.5)
            keyboard.write(mensagem, 0.01)
            time.sleep(0.5)
            pyautogui.click(btmonitor + botao.x, botao.y)
            time.sleep(1)
            pyautogui.hotkey('Enter')
            print("Achou o botão de estacionar")
            print(btmonitor + botao.x, botao.y)
            return
        # fallback 1
        bt = pyautogui.locateOnScreen("img/btAprova2.png", region=regiao, confidence=0.9, grayscale=True)
        if bt:
            botao = pyautogui.center(bt)
            pyautogui.click(btmonitor + botao.x, botao.y)
            time.sleep(0.5)
            keyboard.write(mensagem, 0.01)
            time.sleep(0.5)
            pyautogui.click(btmonitor + botao.x, botao.y)
            time.sleep(1)
            pyautogui.hotkey('Enter')
            print("Achou o botão de aprova2")
            print(btmonitor + botao.x, botao.y)
            return
        # fallback 2: rolar e tentar localizar novamente
        pyautogui.click(monitor + 195, 400 + pedidosTravados + barra)
        time.sleep(1)
        pyautogui.scroll(-800)
        time.sleep(1)
        bt = pyautogui.locateOnScreen("img/btAprova2.png", region=regiao, confidence=0.9, grayscale=True)
        if bt:
            botao = pyautogui.center(bt)
            pyautogui.click(btmonitor + botao.x, botao.y)
            time.sleep(0.5)
            keyboard.write(mensagem, 0.01)
            time.sleep(0.5)
            pyautogui.click(btmonitor + botao.x, botao.y)
            time.sleep(1)
            pyautogui.hotkey('Enter')
            print("Achou o botão de aprova3")
            print(btmonitor + botao.x, botao.y)
            return
        bt = pyautogui.locateOnScreen("img/btAprova3.png", region=regiao, confidence=0.9, grayscale=True)
        if bt:
            botao = pyautogui.center(bt)
            pyautogui.click(btmonitor + botao.x, botao.y)
            time.sleep(0.5)
            keyboard.write(mensagem, 0.01)
            time.sleep(0.5)
            pyautogui.click(btmonitor + botao.x, botao.y)
            time.sleep(1)
            pyautogui.hotkey('Enter')
            print("Achou o botão de aprova4")
            print(btmonitor + botao.x, botao.y)
            return
        bt = pyautogui.locateOnScreen("img/btAprova4.png", region=regiao, confidence=0.9, grayscale=True)
        if bt:
            botao = pyautogui.center(bt)
            pyautogui.click(btmonitor + botao.x, botao.y)
            time.sleep(0.5)
            keyboard.write(mensagem, 0.01)
            time.sleep(0.5)
            pyautogui.click(btmonitor + botao.x, botao.y)
            time.sleep(1)
            pyautogui.hotkey('Enter')
            print("Achou o botão de aprova4")
            print(btmonitor + botao.x, botao.y)
            return

        pyautogui.alert("Não foi possível identificar o botão de Aprovar na tela!", title='ERRO')
        pyperclip.copy(mensagem)
    except Exception:
        pyautogui.alert("Erro ao executar rotina de aprovar.", title='ERRO')
        pyperclip.copy(mensagem)
    finally:
        pyautogui.moveTo(x, y)

def reprova(mensagem):
    x, y = pyautogui.position()
    try:
        bt = pyautogui.locateOnScreen("img/btReprova.png", region=regiao, confidence=0.9, grayscale=True)
        if bt:
            botao = pyautogui.center(bt)
            pyautogui.click(btmonitor + botao.x, botao.y)
            time.sleep(0.5)
            keyboard.write(mensagem, 0.01)
            time.sleep(0.5)
            pyautogui.click(btmonitor + botao.x, botao.y)
            time.sleep(1)
            pyautogui.hotkey('Enter')
            return
        # fallback: rolar e tentar encontrar
        pyautogui.click(monitor + 195, 400 + pedidosTravados + barra)
        time.sleep(1)
        pyautogui.scroll(-800)
        time.sleep(1)
        bt = pyautogui.locateOnScreen("img/btReprova.png", region=regiao, confidence=0.9, grayscale=True)
        if bt:
            botao = pyautogui.center(bt)
            pyautogui.click(btmonitor + botao.x, botao.y)
            time.sleep(0.5)
            keyboard.write(mensagem, 0.01)
            time.sleep(0.5)
            pyautogui.click(btmonitor + botao.x, botao.y)
            time.sleep(1)
            pyautogui.hotkey('Enter')
            return
        pyautogui.alert("Não foi possível identificar o botão de Reprovar na tela!", title='ERRO')
        pyperclip.copy(mensagem)
    except Exception:
        pyautogui.alert("Erro ao executar rotina de reprovar.", title='ERRO')
        pyperclip.copy(mensagem)
    finally:
        pyautogui.moveTo(x, y)

def atualiza():
    x, y = pyautogui.position()
    try:
        pyautogui.click(monitor + 80, 290 + barra)
        time.sleep(3)
        pyautogui.click(monitor + 1185, 250 + barra)
    finally:
        pyautogui.moveTo(x, y)

def aprovaSuporte():
    msg = input('Digite a OS de liberação: ')
    aprova('LIBERADO PELO SUPORTE TECNICO MEDIANTE A OS :' + msg)
    input("")

def VerificaTela():
    x, y = pyautogui.size()
    if (x != 1366) or (y != 768):
        pyautogui.alert(text='O programa será encerrado porque a resolução da tela não é 1366x768',
                        title='ATENÇÃO', button='OK')
        finaliza()
    else:
        pyautogui.alert(text='Para que o programa funcionar corretamente, coloque a pagina da tela de auditoria no monitor da esquerda!',
                        title='ATENÇÃO', button='OK')

def finaliza():
    sys.exit()

# ----------------------------- FUNÇÕES DE VOZ (THREAD) -----------------------------
def ouvir_microfone(window):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    # Mostra contagem regressiva na interface
    

    window['-INPUT-'].update("Pode falar agora!")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        while window['-LISTEN-'].metadata:  # Enquanto o botão estiver "pressionado"
            try:
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=20)
                texto = recognizer.recognize_google(audio, language='pt-BR')
                texto = acentuacao(texto) #trata acentuação da fala
                window['-INPUT-'].update(texto)
            except sr.UnknownValueError:
                window['-INPUT-'].update("Não entendi, fale novamente...")
            except sr.RequestError:
                window['-INPUT-'].update("Erro na conexão com o serviço de reconhecimento.")


def acentuacao(frase):
      fas1 = frase.replace("ponto de interrogação", "?")
      fas2 = fas1.replace("Ponto de interrogação", "?")
      fas3 = fas2.replace("Ponto Final", ". ")
      fas4 = fas3.replace("ponto final", ". ")
      fas5 = fas4.replace("vírgula", ", ")
      fas6 = fas5.replace("virgula", ", ")
      return fas6



def ouvir_microfone_thread(window_write_event, stop_event):
    """
    Thread de captura de áudio que envia eventos à janela principal.
    Envia:
      - '-MIC-COUNTDOWN-' : int (3..1)
      - '-MIC-STATUS-' : str ("Pode falar agora!")
      - '-RECOG-' : str (texto reconhecido) or None (não entendeu)
      - '-RECOG-ERROR-' : str (mensagem de erro)
    """
    try:
        recognizer = sr.Recognizer()
        try:
            mic = sr.Microphone()
        except Exception as e:
            # Microfone não disponível / driver faltando
            window_write_event('-RECOG-ERROR-', f'Erro ao acessar microfone: {e}')
            return

        # Contagem regressiva
        for i in range(3, 0, -1):
            if stop_event.is_set():
                return
            window_write_event('-MIC-COUNTDOWN-', i)
            time.sleep(1)

        window_write_event('-MIC-STATUS-', "Pode falar agora!")

        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            while not stop_event.is_set():
                try:
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
                    texto = recognizer.recognize_google(audio, language='pt-BR')
                    window_write_event('-RECOG-', texto)
                except sr.UnknownValueError:
                    window_write_event('-RECOG-', None)  # não entendeu
                except sr.RequestError as e:
                    window_write_event('-RECOG-ERROR-', f'Erro no serviço de reconhecimento: {e}')
                except Exception as e:
                    # Erros inesperados do listen/recognize (timeout etc.)
                    # continuamos o loop para permitir nova tentativa, mas logamos
                    window_write_event('-RECOG-ERROR-', f'Erro interno de áudio: {e}')
                    continue
    except Exception as e:
        # Qualquer outro erro que não tenha sido capturado
        try:
            window_write_event('-RECOG-ERROR-', f'Erro fatal no thread de áudio: {e}')
        except Exception:
            print('Erro ao enviar evento de erro do thread:', e)

# ----------------------------- FUNÇÃO DE ENVIO (pyautogui + clipboard) -----------------------------
def enviar_texto(texto):
    """Copia texto para clipboard, clica na posição prevista e envia Enter."""
    x, y = pyautogui.position()
    if texto and texto.strip():
        pyperclip.copy(texto)
        time.sleep(0.15)
        try:
            pyautogui.click(monitor_telaprincipal + 400, barra + 610)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')            
        except Exception as e:
            sg.popup(f'Erro ao enviar texto via pyautogui: {e}')
        pyautogui.moveTo(x, y)

# ----------------------------- LAYOUTS (unificados) -----------------------------
layout_monitor = [
    [sg.Radio("Esq.", key='tela1', group_id='bt_Tela', enable_events=True, font=('calibri', 12), ),
     sg.Radio("Central", key='tela2', default=True, group_id='bt_Tela', enable_events=True, font=('calibri', 13)),
     sg.Radio("Direita", key='tela3', group_id='bt_Tela', enable_events=True, font=('calibri', 13)), 
     sg.Text("Analista:"), sg.Combo(values=analistas,
                                                     size=(14, 0), key='analista_selecionado', enable_events=True,  font=('Calibri', 14), readonly=False),   
    ], 
    [sg.Button('Ir para tela de auditoria', key='Tela_auditoria', visible=True, tooltip='Abre a tela de auditoria de peças'), sg.Button('Sair') , ],

]  
    
    

layout_Texto = [
    [sg.Multiline(size=(40, 8), key='-INPUT-', enter_submits=True, pad=0, font=('calibri', 12))],
    [sg.Button('Enviar'), ]
]

layoutSaudacao = [
    [sg.Button('Saudação', key='Saudação', tooltip=f'Olá, bem vindo ao suporte, eu sou o {analista_selecionado}. Por gentileza me informe {pedirNome}o motivo do contato.'),
     sg.Checkbox('Pedir nome', key='-pedirNome-', default=False, enable_events=True, font=('calibri', 9)),
      ],
    [sg.Button('Espera', key='Espera', tooltip='Aguarde um momento por favor.')],
    [sg.Button('Espera Liberação', key='Espera Liberação', tooltip='Aguarde um momento, estou realizando a liberação para você.')],
    [sg.Button('Codigo de peça', key='codigo_peca', tooltip="Para acesso ao codigo da peça, acesse o site https://partsurfer.hp.com/ , digite o numero de serie e vc tera a acesso aos codigos das pecas do equipamento. Voce tambem pode acessar o site da universidade: https://simuniversidade.com.br e procurar o catalogo de peças. No WhatsApp do suporte também tem a opção de consultar peças. No menu inicial tem a opção: CONSULTA DE CÓDIGOS DE PEÇAS. Selecione ela, coloque o modelo do eqiupamento e o  sistema retornará os códigos das peças.")],
    [sg.Button('Despedida', key='Despedida', tooltip='Por nada. Agradecemos o seu contato. Tenha um ótimo dia!')]
]

layoutProcedimentos = [
    [sg.Button('Procedimentos realizados', key='Procedimentos realizados', tooltip='Quais procedimentos foram realizados no equipamento?')],
    [sg.Button('Mau uso', key='Mau uso', tooltip='Foi verificado algum indicio de mau uso no equipamento?')],
    [sg.Button('Foto do defeito:', key='Foto do defeito:', tooltip='Por favor, envie uma foto do defeito apresentado no equipamento.')],
    [sg.Button('Log de erros', key='log_erro', tooltip='Me envie por favor a pagina de erros do equipamento para análise do defeito.')],
    [sg.Button('Rede elétrica', key='Rede elétrica', tooltip='Me informe os valores da rede eletrica por favor. Fase + neutro, fase + terra e neutro + terra.')],
]

layoutVoz = [
    # O botão -LISTEN- terá bind para detectar PRESS/RELEASE e assim funcionar "segure para falar"
    [sg.Button("Segure para Falar", key='-LISTEN-', button_color=('white', 'blue'), size=(15, 1)),
     sg.Button('Enviar Audio', key='Enviar_Audio', size=(10, 1))]
]

layoutPBA = [
    [sg.Button('Tensão na PBA', key='tensão_PBA',tooltip='Quais os valores de Tensao de saida da fonte ate a placa principal?')],
    [sg.Button('Conector amassado', key='conector_amassado_PBA', tooltip='Os conectores da entrada de  rede estao amassados ou tortos? Poderia me enviar uma foto por favor?')],    
    [sg.Button('Pagina de configuração', key='pagina_PBA', tooltip='Por favor, acesse a pagina de configuração do equipamento e me envie para analise do defeito.')],
    [sg.Button('Atualizar o firmware', key='firmware_PBA', tooltip='Eu te recomendo a atualizar o firmware para a versão mais atualizada para o reparar o equipamento')],
    #[sg.Button('Espera-Liberacao', key='Espera_Liberacao_PBA' tooltip='Vou realizar a liberação da placa. Aguarde um momento por favor.')],
]

layoutFonte = [
    [sg.Button('Tensão de saida', key='tensão_Fonte', tooltip= 'Quais os valores de Tensao de saida da fonte que vão para a placa principal?')],
    [sg.Button('Capacitores estufados', key='capacitor_estufado', tooltip='Os capacitores estao estufados ou vazando? Poderia me enviar uma foto por favor?')],
    [sg.Button('Foto da Fonte', key='foto_fonte', tooltip= 'Por favor, envie uma foto da fonte do equipamento.')],
    #[sg.Button('Mau uso', key='mau_uso_fonte', tooltip= 'Foi identificado algum indicio de mau uso na rede eletrica? surto eletrico ou ligacao em 220v?')],
    [sg.Button('Rede elétrica', key='rede_eletrica_fonte', tooltip='Me informe os valores da rede eletrica por favor. Fase + neutro, fase + terra e neutro + terra.')]
]

layoutScanner = [
    [sg.Button('Foto defeito', key='foto_defeito_scanner', tooltip='Por favor, envie uma foto do defeito apresentado no scanner.')],
    #[sg.Button('Relatório de erros', key='relatorio_erros_scanner', tooltip= 'Me envie por favor o relatório de erros do equipamento para análise do defeito.')],
    [sg.Button('Troca dos roletes', key='troca_roletes_scanner', tooltip= 'Os roletes do ADF foram trocados recentemente?')],
    [sg.Button('Foto fonte - SCB', key='foto_fonte_scb', tooltip= 'Esse defeito pode estar associado a placa do scanner ou a fonte do equipamento. Por favor, envie uma foto da placa fonte para análise.')],
    [sg.Button('Video do defeito', key='video_defeito_scanner', tooltip= 'Por favor, envie um vídeo do defeito apresentado no scanner para análise.')]
]

layout_PC = [
    [sg.Button('Reset elétrico', key='reset_eletrico_pc', tooltip='Realize um reset elétrico no equipamento por favor.')],
    [sg.Button('Atualizar Bios', key='bios_pc', tooltip= 'Atualize a BIOS do equipamento para a versão mais recente disponível no site do fabricante.')],
    [sg.Button('Atualiza driver', key='atualiza_driver_pc', tooltip= 'Atualize os drivers do equipamento por favor' )],
    [sg.Button('Foto Placa mãe', key='foto_pc', tooltip='Me envie uma foto da placa mãe do equipamento para análise.')],
    
]

FrameTexto = [sg.Frame(' Digite seu texto ', layout_Texto, font=('calibri', 9, "bold"), vertical_alignment='center')]
FrameSaudacao = [sg.Frame('Saudação ', layoutSaudacao, font=('calibri', 9, "bold"), vertical_alignment='center')]
FrameProcedimentos = [sg.Frame(' Procedimentos ', layoutProcedimentos, font=('calibri', 9, "bold"), vertical_alignment='center')]
FrameVoz = [sg.Frame(' Transcrição de Voz', layoutVoz, font=('calibri', 9, "bold"), vertical_alignment='center')]
FramePBA = [sg.Frame(' Placa principal ', layoutPBA, font=('calibri', 9, "bold"))]
FrameFonte = [sg.Frame(' Placa fonte ', layoutFonte, font=('calibri', 9, "bold"), vertical_alignment='top')]
FrameScanner = [sg.Frame(' Scanner ', layoutScanner, font=('calibri', 9, "bold"), vertical_alignment='top')]
FramePC = [sg.Frame(' PC ', layout_PC, font=('calibri', 9, "bold"), vertical_alignment='top')]
Frame1 = [sg.Frame(' Localização do Monitor  ', layout_monitor, font=('calibri', 9, "bold"), vertical_alignment='center')]

layout = [
    [sg.Text("OS de Suporte: ", font=13),
     sg.Combo(values=['Peça', 'Placa Fonte', 'Placa Principal', 'Placa Formatter', 'ADF','SCB',  'Placa mãe', 'Placa do Painel', 'Painel de operações', 'HVPS', 'DC controller', 'Placa IOD'],
              size=(18, 0), key='Peca_Liberada', enable_events=True, default_value='Peça', font=('Calibri', 12),readonly=False),
     sg.Input(key='os_Suporte', size=(18, 0), do_not_clear=True), sg.Button("Aprovar", key='AprovaSuporte')],
    [sg.Column([FrameTexto]), sg.VSeparator(), sg.Column([FrameSaudacao]), sg.VSeparator(), sg.Column([FrameProcedimentos])],
    [FrameVoz],
    [sg.Column([FramePBA]), sg.VSeparator(), sg.Column([FrameFonte]), sg.VSeparator(), sg.Column([FrameScanner]), sg.VSeparator(), sg.Column([FramePC])]
]

layout_cabecalho = [
    [sg.Text("                          AUTOMAÇÃO DO SERVICE NOW", font=("calibri", 24))],
    Frame1
]

layoutPrincipal = [layout_cabecalho, layout]

# ----------------------------- JANELAS -----------------------------
window = sg.Window('App Automação com Atalhos', layout=layoutPrincipal, size=(900, 690),
                   font=('calibri', 13), resizable=True, relative_location=(-30, -50), finalize=True)

window['-LISTEN-'].bind('<ButtonPress-1>', '+PRESS')
window['-LISTEN-'].bind('<ButtonRelease-1>', '+RELEASE')

###########################################################################################################
###########################################################################################################
##################################    LAYOUT DA AUDITORIA     #############################################
layout_Esquerda = [
    [sg.Text("Ver o relatório", font=('Calibri', 14)), sg.Push(), sg.Button("    Ver     ", key='verRelatorio', button_color='#616161')],
    [sg.Text("Atualizar a tela", font=('calibri', 14)), sg.Push(), sg.Button("Atualizar", key='atualiza', button_color='#616161')],
    [sg.Text("--------------------   APROVAÇÕES   --------------------------", font=('calibri', 17)), sg.Push()],
    [sg.Text("Dentro do prazo", font=('calibri', 14)), sg.Push(), sg.Button("Aprovar", key='dentroprazo', button_color='green')],
    [sg.Text("Aprovação Suporte, OS:"), sg.Input(key='os_Suporte_AUD', size=(18, 0), do_not_clear=True), sg.Push(), sg.Button("Aprovar", key='AprovaSuporte_AUD')],
    [sg.Text("Quebra Aleatória"), sg.Push(), sg.Combo(values=['QA - Quebra Aleatória', 'Reposição de pedido devido ocorrência de transportes.', 'QA/ Atendimento B2C', 'QA - Peça com valor inferior a R$50.00'],
                                                     size=(18, 0), key='blockP', enable_events=True, default_value='QA - Quebra Aleatória', font=('Calibri', 14), readonly=False), sg.Button("Aprovar", key='block')],
    [sg.Text("Unidade de imagem"), sg.Push(), sg.Combo(values=['Bolsão / Revisão Laboratório', 'Dentro do prazo', 'Impressões riscadas, claras ou manchadas', 'Vazamento de revelador ', 'Alta área de cobertura ', 'Oxidação do rolo de carga ',
                                                              'Código de erro #31-007 ', 'Código de erro #C3-1315 ', 'Reposição de pedido devido ocorrência de transportes.', 'Peça consumida com 80% de uso ', 'Ruído excessivo nas engrenagens, reciclagem travada '],
                                                    size=(18, 0), key='dentrodoprazo', enable_events=True, default_value='Impressões riscadas, claras ou manchadas', font=('Calibri', 14), readonly=True), sg.Button("Aprovar", key='dentro')],
    [sg.Text("Unidade de fusão"), sg.Push(), sg.Combo(values=['Dentro do prazo', 'Atolamento constante ', 'Erro de aquecimento ', 'Pelicula danificada ', 'Código de erro #02-001 '],
                                                   size=(18, 0), key='fuser', enable_events=True, default_value='Erro de aquecimento ', font=('Calibri', 14), readonly=True), sg.Button("Aprovar", key='fusao')],
    [sg.Text("--------------------  REPROVAÇÕES    -------------------------", font=('calibri', 17)), sg.Push()],
    [sg.Text("Recusar "), sg.Push(),
     sg.Combo(values=['Fora do prazo, sem evidência', 'Sem liberação do Suporte', 'Sem justificativa para liberação', 'Fora do prazo - Cliente Troca', 'Pedido Duplicado', 'Solicitado item incorreto', 'Não seguiu fluxo de orçamento', 'Quantidade acima do utilizado pelo equipamento', 'Solicitado consumível/acessório como peças', 'Venda Mercantil', 'Direcionado para troca técnica'],
              size=(18, 0), key='recusak', enable_events=True, default_value='Fora do prazo, sem evidência', font=('Calibri', 14), readonly=True), sg.Button("Recusar", key='recusa', button_color='brown')],
    [sg.Text("Sem liberação do Suporte "),sg.Push(), sg.Button("Recusar", key='semliberacao', button_color='brown')],
]

layout_Direita = [
    [sg.Text(' TECNICOS DA LISTA  ', font=('calibri', 17))],
    [sg.Input(size=(36, 1), enable_events=True, key='combo-tecnico')],
    [sg.Listbox(values=tecnicos, size=(43, 7), enable_events=True, key='-LIST-TECNICO', font=('calibri', 12))],
    [sg.Text('------------------------------------------------------------------------', font=('calibri', 17))],
    [sg.Text('CLIENTES - CABEÇA TÉRMICA', font=('calibri', 17))],
    [sg.Input(size=(36, 1), enable_events=True, key='combo-mercantil')],
    [sg.Listbox(values=mercantil, size=(43, 7), enable_events=True, key='-LIST-MERCANTIL', font=('calibri', 12))]
]

layout_m = [
    [sg.Radio("Esq.", key='tela1_AUD', group_id='bt_Tela_AUD', enable_events=True, font=('calibri', 12)),
     sg.Radio("Central", key='tela2_AUD', default=True, group_id='bt_Tela_AUD', enable_events=True, font=('calibri', 13)),
     sg.Radio("Direita", key='tela3_AUD', group_id='bt_Tela_AUD', enable_events=True, font=('calibri', 13)),
    sg.Button('Ir pra tela inicial', key='Tela_inicial', visible=True, font=('calibri', 12),tooltip='Volta para a tela inicial')]
]

layout0_barra = [[sg.Checkbox('Barra de Fav.', key='-barra-AUD-', default=True, enable_events=True, font=('calibri', 13)),
                  sg.Checkbox('sel. Pedido', key='-selecionaPedido-', default=True, enable_events=True, font=('calibri', 13)),
                  sg.Text("Ped.Travado", font=('calibri', 13)),
                  sg.Combo(values=[str(i) for i in range(0, 31)], size=(3, 1), key='-ped_travado-', enable_events=True, default_value='0', readonly=True, font=('calibri', 13))]]

Frame01 = [sg.Frame(' Localização do Monitor  ', layout_m, font=('calibri', 9, "bold"), vertical_alignment='center')]
Frame02 = [sg.Frame('', layout0_barra, border_width=0)]

layout0_cabecalho = [
    [sg.Text("                            BOT - AUDITORIA DE PEÇAS", font=("calibri", 24))],
    Frame02, Frame01
]

layout0 = [
    [layout0_cabecalho, sg.Column(layout_Esquerda), sg.VSeparator(), sg.Column(layout_Direita)]
]

janela = sg.Window("Tela de auditoria", size=(900, 690), layout=layout0, margins=(0, 2), resizable=True, font=('calibri', 15,), relative_location=(-30, -50), finalize=True)
# inicialmente escondida
janela.hide()

# ----------------------------- INICIALIZAÇÕES -----------------------------
construtor()
barra_favoritos('1')
check_Tela(2)

# ----------------------------- BIND DO BOTÃO -LISTEN- (PRESS + RELEASE) -----------------------------
# Precisamos do widget finalizado para fazer bind de eventos mouse.
# Event names serão: '-LISTEN-+PRESS' e '-LISTEN-+RELEASE'
window['-LISTEN-'].bind('<ButtonPress-1>', 'PRESS')
window['-LISTEN-'].bind('<ButtonRelease-1>', 'RELEASE')

# ----------------------------- FUNÇÃO AUXILIAR PARA ENVIAR EVENTOS DO THREAD -----------------------------
def send_to_window(event_key, value):
    """Wrapper para enviar eventos do thread para a janela principal."""
    window.write_event_value(event_key, value)

# ----------------------------- LOOP PRINCIPAL (único) -----------------------------
#########################################################################################################
#########################################################################################################
##############################   LOOPING DA TELA INICIAL     ############################################
while True:
    event, values = window.read(timeout=100)

    # Eventos de fechamento
    if event == sg.WINDOW_CLOSED or event == 'Sair':
        break

    # ------------------ Tratamento de eventos normais da janela principal ------------------
    if event == 'analista_selecionado':
       analista_selecionado = values['analista_selecionado'].strip()       
    if event == 'Tela_auditoria':
        alternar(window, janela)

    # Saudações / atalhos
    if event == 'Saudação':
        if analista_selecionado == '':            
            sg.popup('Por favor, selecione o seu nome na lista de analistas antes de enviar a saudação.') 
        else:  
         enviar_texto(f'Olá, bem vindo ao suporte, eu sou o {analista_selecionado}. Por gentileza me informe {pedirNome}o motivo do contato.')
    if event == 'Espera':
        enviar_texto('Aguarde um momento por favor.')
    if event == 'Espera Liberação':
        enviar_texto('Aguarde um momento, estou realizando a liberação para você.')
    if event == 'codigo_peca':
        enviar_texto("Para acesso ao codigo da peça, acesse o site https://partsurfer.hp.com/ , digite o numero de serie e vc tera a acesso aos codigos das pecas do equipamento. Voce tambem pode acessar o site da universidade: https://simuniversidade.com.br e procurar o catalogo de peças. No WhatsApp do suporte também tem a opção de consultar peças. No menu inicial tem a opção: CONSULTA DE CÓDIGOS DE PEÇAS. Selecione ela, coloque o modelo do eqiupamento e o  sistema retornará os códigos das peças.")
    if event == 'Despedida':
        enviar_texto('Por nada. Agradecemos o seu contato. Tenha um ótimo dia!')

    # Procedimentos
    if event == 'Procedimentos realizados':
        enviar_texto('Quais procedimentos foram realizados no equipamento?')
    if event == 'Mau uso':
        enviar_texto('Foi verificado algum indicio de mau uso no equipamento?')
    if event == 'Foto do defeito:':
        enviar_texto('Por favor, envie uma foto do defeito apresentado no equipamento.')
    if event == 'Rede elétrica':
        enviar_texto('Me informe os valores da rede eletrica por favor. Fase + neutro, fase + terra e neutro + terra.')
    if event == 'log_erro':
        enviar_texto('Me envie por favor a pagina de erros do equipamento para análise do defeito.')
    
    if event == 'Enviar_Audio':
        texto_audio = values['-INPUT-'].strip()
        if texto_audio:
            enviar_texto(texto_audio)            
            window['-INPUT-'].update('')  # Limpa a caixa
    # Se pressionou Enter dentro da caixa ou clicou em Enviar
    if event == '-INPUT-' or event == 'Enviar':
        texto = values['-INPUT-'].strip()
        if texto:
            enviar_texto(texto)            
            window['-INPUT-'].update('')  # Limpa a caixa      
    elif event == '-LISTEN-':
        # Alterna estado do botão
        if not window['-LISTEN-'].metadata:
            window['-LISTEN-'].metadata = True
            threading.Thread(target=ouvir_microfone, args=(window,), daemon=True).start()
            window['-LISTEN-'].update("Clique para Parar", button_color=('white', 'red'))
        else:
            window['-LISTEN-'].metadata = False
            window['-LISTEN-'].update("Clique para Falar", button_color=('white', 'blue'))
    
    # Aprovação via botão na janela principal
    if event == 'AprovaSuporte':
        peca = values['Peca_Liberada'].strip()
        os_texto = values['os_Suporte'].strip()
        if os_texto:
            enviar_texto(f'{peca} liberado mediante ação do suporte. Protocolo de liberação: {os_texto}')
        else:
            sg.popup('Por favor, insira o número da OS antes de aprovar.')
        window['os_Suporte'].update(value='') # Limpa o campo após envio

    # Placa principal / Fonte / Scanner (mesmos textos)
    if event == 'tensão_PBA':
        enviar_texto('Quais os valores de Tensao de saida da fonte ate a placa principal?')
    if event == 'conector_amassado_PBA':
        enviar_texto('Os conectores da entrada de  rede estao amassados ou tortos? Poderia me enviar uma foto por favor?')
    if event == 'pagina_PBA':
        enviar_texto('Por favor, acesse a pagina de configuração do equipamento e me envie para analise do defeito.')    
    if event == 'firmware_PBA':
        enviar_texto('Eu te recomendo a atualizar o firmware para a versão mais atualizada para o reparar o equipamento') 
    if event == 'Espera_Liberacao_PBA':
        enviar_texto('Vou realizar a liberação da placa. Aguarde um momento por favor.')

    if event == 'tensão_Fonte':
        enviar_texto('Quais os valores de Tensao de saida da fonte que vão para a placa principal?')
    if event == 'capacitor_estufado':
        enviar_texto('Os capacitores estao estufados ou vazando? Poderia me enviar uma foto por favor?')
    if event == 'foto_fonte':
        enviar_texto('Por favor, envie uma foto da fonte do equipamento.')
    if event == 'mau_uso_fonte':
        enviar_texto('Foi identificado algum indicio de mau uso na rede eletrica? surto eletrico ou ligacao em 220v?')
    if event == 'rede_eletrica_fonte':
        enviar_texto('Me informe os valores da rede eletrica por favor. Fase + neutro, fase + terra e neutro + terra.')

    if event == 'foto_defeito_scanner':
        enviar_texto('Por favor, envie uma foto do defeito apresentado no scanner.')
    if event == 'relatorio_erros_scanner':
        enviar_texto('Me envie por favor o relatório de erros do equipamento para análise do defeito.')
    if event == 'troca_roletes_scanner':
        enviar_texto('Os roletes do ADF foram trocados recentemente?')
    if event == 'foto_fonte_scb':
        enviar_texto('Esse defeito pode estar associado a placa do scanner ou a fonte do equipamento. Por favor, envie uma foto da placa fonte para análise.')
    if event == 'video_defeito_scanner':
        enviar_texto('Por favor, envie um vídeo do defeito apresentado no scanner para análise.')


    if event == 'reset_eletrico_pc':
        enviar_texto('Realize um reset elétrico no equipamento por favor.')
    if event == 'bios_pc':
        enviar_texto('Atualize a BIOS do equipamento para a versão mais recente disponível no site do fabricante.')
    if event == 'atualiza_driver_pc':
        enviar_texto('Atualize os drivers do equipamento por favor') 
    if event == 'foto_pc':
        enviar_texto('Me envie uma foto da placa mãe do equipamento para análise.')
    # Configurações de tela / barra
    if event == 'tela1':
        monitor_telaprincipal = -1366
       
    if event == 'tela2':
        monitor_telaprincipal = 0
       
    if event == 'tela3':
        monitor_telaprincipal = 1366
       
    if event == '-barra-':
        if values['-barra-'] == True:
            barra_favoritos('1')
            
        else:
            barra_favoritos('2')
    
    if event == '-pedirNome-':
        if values['-pedirNome-'] == True:
            pedirNome = 'seu nome e '
        else:
            pedirNome = ''
           

    # ------------------ Eventos gerados pelo thread de voz ------------------
    if event == '-MIC-COUNTDOWN-':
        cnt = values[event]
        window['-INPUT-'].update(f"Iniciando em {cnt}...")
    if event == '-MIC-STATUS-':
        window['-INPUT-'].update(values[event])
    if event == '-RECOG-':
        texto_rec = values[event]
        if texto_rec:
            window['-INPUT-'].update(texto_rec)
        else:
            window['-INPUT-'].update("Não entendi, fale novamente...")
    if event == '-RECOG-ERROR-':
        window['-INPUT-'].update(values[event])

    ######################################################################################################
    ######################################################################################################
    ################################   LOOPING DA AUDITORIA     ##########################################
    try:
        eventos, valores = janela.read(timeout=10)
    except Exception:
        eventos, valores = (None, None)

    if eventos == sg.WINDOW_CLOSED or eventos == 'Fechar':
        janela.hide()
        window.un_hide()

    if eventos == 'Tela_inicial':
        alternar(janela, window)

    # Auditoria: filtragem listas e botões
    if valores:
        try:
            if valores.get('combo-tecnico', '') != '':
                search = valores['combo-tecnico'].upper()
                new_values = [x for x in tecnicos if search in x]
                janela['-LIST-TECNICO'].update(new_values)
            else:
                janela['-LIST-TECNICO'].update(tecnicos)

            if valores.get('combo-mercantil', '') != '':
                search = valores['combo-mercantil'].upper()
                new_values = [x for x in mercantil if search in x]
                janela['-LIST-MERCANTIL'].update(new_values)
            else:
                janela['-LIST-MERCANTIL'].update(mercantil)
        except Exception:
            pass

    if eventos == '-LIST-TECNICO' and valores and len(valores.get('-LIST-TECNICO', [])):
        sg.popup('Selected ', valores['-LIST-TECNICO'])
    if eventos == '-LIST-MERCANTIL' and valores and len(valores.get('-LIST-MERCANTIL', [])):
        sg.popup('Selected ', valores['-LIST-MERCANTIL'])

    if eventos == 'verRelatorio':
        VerRelatorio()
    if eventos == 'atualiza':
        atualiza()
    if eventos == 'dentro':
        aprova(valores.get('dentrodoprazo', 'Dentro do prazo'))
    if eventos == 'dentroprazo':
        aprova('Dentro do prazo')
    if eventos == 'block':
        aprova(valores.get('blockP', 'QA - Quebra Aleatória'))
    if eventos == 'AprovaSuporte_AUD':
        if valores.get('os_Suporte_AUD', "") == "":
            pyautogui.alert("Insira a OS de suporte!")
        else:
            aprova("Liberado mediante  ação do Suporte na OS: " + valores.get('os_Suporte_AUD', "") + " SEM BLOQ P")
            janela['os_Suporte_AUD'].update(value='')  # Limpa o campo após envio   
    if eventos == 'aprovaJustificativa':
        justificativa = valores.get('justifica', "")
        if justificativa == "":
            aprova("Aprovado mediante justificativa do técnico na OS e/ou canais oficiais de comunicação.")
        else:
            tamanho = len(justificativa)
            if tamanho < 180:
                aprova(justificativa)
            else:
                pyautogui.alert("Reduza o tamanho da justificativa!")
    if eventos == 'fusao':
        aprova(valores.get('fuser', ''))
    if eventos == 'recusa':
        reprova(valores.get('recusak', ''))
        # Copia texto pra clipboard conforme seleção (mantive os textos do seu código)
        k = valores.get('recusak', '')
        if k == 'Fora do prazo, sem evidência':
            pyperclip.copy('Fora do prazo sem o envio da página de suprimentos através dos canais oficiais de comunicação ou evidência que justifique o pedido da peça.')
        elif k == 'Sem liberação do Suporte':
            pyperclip.copy('Sem a liberação do Suporte, pedido recusado')
        elif k == 'Sem justificativa para liberação':
            pyperclip.copy('Fora do prazo sem o envio da página de suprimentos através dos canais oficiais de comunicação ou evidência que justifique o pedido da peça.')
        elif k == 'Pedido Duplicado':
            pyperclip.copy('Pedido recusado porque encontra-se duplicado.')
        elif k == 'Solicitado item incorreto':
            pyperclip.copy('O item solicitado não pode ser solicitado como peça. Pedido recusado.')
        elif k == 'Não seguiu fluxo de orçamento':
            pyperclip.copy('O fluxo de requisição de orçamento não foi realizado corretamente e a peça foi solicitada em garantia. Favor refazer o pedido da peça como orçamento.')
        elif k == 'Quantidade acima do utilizado pelo equipamento':
            pyperclip.copy('A quantidade de itens solicitados não compatível com o modelo do equipamento. Pedido recusado.')
        elif k == 'Solicitado consumível/acessório como peças':
            pyperclip.copy('O item solicitado não pode ser solicitado como peça. Pedido recusado.')
        elif k == 'Venda Mercantil':
            pyperclip.copy('A substituição das cabeças de impressão para os equipamentos térmicos ocorre via venda mercantil entre Cliente e Simpress, dessa forma, cancelamos a solicitação visto a troca deste item em garantia não ser contemplada em contrato. A solicitação pode ser feita via formulário BKS_022 - Solicitação de Venda Mercantil, sendo enviado (upload) no lugar do Termo de Ciência e disponível no Portal de Qualidade.')
        elif k == 'Direcionado para troca técnica':
            pyperclip.copy('O equipamento foi direcionado para troca técnica e por este motivo o pedido foi recusado.')
    if eventos == 'semliberacao':
        reprova('Sem liberação do Suporte')  
        pyperclip.copy('Sem a liberação do Suporte, pedido recusado')
    # Interações de tela na janela de auditoria (radios / checkbox)
    if eventos == 'tela1_AUD':
        # muda cor do radio (função change_radio_text_color foi simplificada; Tk widget pode ser ajustado)
        check_Tela('1')
    if eventos == 'tela2_AUD':
        check_Tela('2')
    if eventos == 'tela3_AUD':
        check_Tela('3')
    if eventos == '-barra-AUD-':
        if valores.get('-barra-AUD-') == True:
            barra_favoritos('1')
        else:
            barra_favoritos('2')
    if eventos == '-selecionaPedido-':
        if janela['-selecionaPedido-'].get():
            selecionaPedido('1')
        else:
            selecionaPedido('2')
    if eventos == '-ped_travado-':
        check_travados(valores.get('-ped_travado-', '0'))

# ----------------------------- FINALIZAÇÃO -----------------------------
# garante parada do thread e fechamento de janelas
if mic_thread and mic_thread.is_alive():
    try:
        mic_stop_event.set()
        mic_thread.join(timeout=1)
    except Exception:
        pass

window.close()
try:
    janela.close()
except Exception:
    pass

