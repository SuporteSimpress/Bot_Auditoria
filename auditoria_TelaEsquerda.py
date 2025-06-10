import pyautogui
import time
import sys
import webbrowser
import keyboard
from PIL import ImageGrab
from functools import partial
from screeninfo import get_monitors


ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)


#----------------------------------- FUNCTIONS ----------------------------------------------#
def construtor():
 global pedidosTravados 
 global larg
 larg = 0
 pedidosTravados = 0
 selecionaPedido('1')

def selecionaPedido(num):  
  global selecionaPed
  if num == '1':
    selecionaPed =  True
  else:
    selecionaPed =  False

def verificaMonitor():
 monitors = get_monitors()
 teste = False
 
 for monitor in monitors:
     if monitor.x < 0:
        teste = True        
 return teste


def barra_favoritos(verifica):   
   bar = str(verifica)
   global barra   
   if bar == '1':
     barra = 30     
   elif bar == '2':
     barra = 0    
   

def check_Tela(temp):
 global regiao  
 global monitor 
 global btmonitor
 global btaprova #serve para tirar a diferença de 1366 quando a tela estiver na esquerda
 global tela_selecionada 
 global monitor  # exemplo de monitor de 1366x768
 global monitor2  # exemplo de monitor de 1366x768
 global monitor3   # exemplo de monitor de 1366x768

 tela = str(temp)

 esq = verificaMonitor()
 if esq:
   btmonitor = -1366
   monitor1 = (0, 0, 1366, 768,)  
   monitor2 = (0, 0, 2732, 768)  
   monitor3 = (2732, 0, 1366, 768)    
 else:
   btmonitor =0
   monitor1 = (0, 0, 1366, 768,)  
   monitor2 = (0, 0, 1366, 768)  
   monitor3 = (1366, 0, 1366, 768)
   print('monitor da direita')

 if tela == '1':
  regiao  = monitor1
  monitor = -1366  
  btaprova = -1366
  tela_selecionada = 'Esquerda'
  
 elif tela == '2':
   regiao  = monitor2
   monitor = 0  
   btaprova = 0
   tela_selecionada = 'Central'   

 elif tela == '3':
  regiao  = monitor3
  monitor = 1366
  btaprova = 0
  tela_selecionada = 'Direita' 

 else:
   regiao  = monitor2
   monitor = 0
   btaprova = 0
   tela_selecionada = 'Central'


def check_travados(trav): 

 global pedidosTravados
 global larg
 travados = trav
 
 if travados =='0':
    pedidosTravados = 0
    larg =  0
 elif travados =='1':
    pedidosTravados = 20
    larg = -7
 elif travados =='2':
    pedidosTravados = 25
    larg = -7
 elif travados =='3':
    pedidosTravados = 30
    larg = -7
 elif travados =='4':
    pedidosTravados = 35
    larg = -7
 elif travados =='5':
    pedidosTravados = 40
    larg = -7
 elif travados =='6':
    pedidosTravados = 45
    larg = -7
 elif travados =='7':
    pedidosTravados = 50
    larg = -7
 elif travados =='8':
    pedidosTravados = 55
    larg = -7
 elif travados =='9':
    pedidosTravados = 60
    larg = -7
 elif travados =='10':
    pedidosTravados = 65
    larg = -7
 elif travados =='11':
    pedidosTravados = 70
    larg = -7
 elif travados =='12':
    pedidosTravados = 75
    larg = -7
 elif travados =='13':
    pedidosTravados = 80
    larg = -7
 elif travados =='14':
    pedidosTravados = 85
    larg = -7
 elif travados =='15':
    pedidosTravados = 90
    larg = -7
 elif travados =='16':
    pedidosTravados = 95
    larg = -7
 elif travados =='17':
    pedidosTravados = 100
    larg = -7
 elif travados =='18':
    pedidosTravados = 110
    larg = -7
 elif travados =='19':
    pedidosTravados = 115
    larg = -7
 elif travados =='20':
    pedidosTravados = 120
    larg = -7
 elif travados =='21':
    pedidosTravados = 125
    larg = -7
 elif travados =='22':
    pedidosTravados = 130
    larg = -7
 elif travados =='23':
    pedidosTravados = 135
    larg = -7
 elif travados =='24':
    pedidosTravados = 140
    larg = -7
 elif travados =='25':
    pedidosTravados = 145
    larg = -7
 elif travados =='26':
    pedidosTravados = 150
    larg = -7
 elif travados =='27':
    pedidosTravados = 155
    larg = -7
 elif travados =='28':
    pedidosTravados = 160
    larg = -7
 elif travados =='29':
    pedidosTravados = 165
    larg = -7
 elif travados =='30':
    pedidosTravados = 168
    larg = -7
 
def verificaPed(): 
 if pyautogui.locateOnScreen('img/SemPedidoTravado.jpg', region=regiao, confidence=0.85, grayscale=True):
  return 0
 else:
   print ('tem pedido travado') 
   return -16  
      
 
#Faz o teste da tela 
def VerificaTela():
 x , y = pyautogui.size()
 if ((x != 1366) | (y != 768)):
    pyautogui.alert(text='O programa será encerrado porque a resolução da tela não é 1366x768', title='ATENÇÃO', button='OK')
    finaliza()
 else:    
    pyautogui.alert(text='Para que o programa funcionar corretamente, coloque a pagina da tela de auditoria no monitor da esquerda!', title='ATENÇÃO', button='OK')

#Clica no botão de aprovar
def BtAprova():
  try:
   bt = pyautogui.locateOnScreen("img/btAprova2.png", region = regiao ,confidence=0.9, grayscale=True) 
   botao= pyautogui.center(bt)  

   pyautogui.click( btmonitor  + botao.x, botao.y + pedidosTravados)
   #pyautogui.click( btmonitor  + botao.x, barra + 365 + pedidosTravados)
   #pyautogui.click( btmonitor  + botao.x, barra + 383 + pedidosTravados)    

  except:
   pyautogui.alert("Não foi possível identificar o botão de aprovar na tela!", title='ERRO')
   
 
#clica no botão de aprovar orçamento
def BtAprovaOrcamento():   
 try:
  bt = pyautogui.locateOnScreen("btAprovaOrcamento2.png", region = regiao ,confidence=0.9, grayscale=True) 
  botao= pyautogui.center(bt)  
  pyautogui.click( btmonitor  + botao.x, barra + 365 + pedidosTravados)
  pyautogui.click( btmonitor  + botao.x, barra + 383 + pedidosTravados)  
 except:
   pyautogui.alert("!Não foi possível identificar o botão de aprovar na tela!", title='ERRO')

#clique no botão de reprovação
def BtReprova(): 
 try:
  bta = pyautogui.locateOnScreen("img/btReprova.png", region = regiao ,confidence=0.85, grayscale=True) 
  botaoR= pyautogui.center(bta)  
  pyautogui.click(btmonitor  + botaoR.x, botaoR.y + pedidosTravados)
  #pyautogui.click(btmonitor  + botaoR.x, barra + 383 + pedidosTravados) 
 except:
   pyautogui.alert("!Não foi possível identificar o botão de Reprovar na tela!", title='ERRO')
  

#clique no botão de relatório
def btRelatorio(): 
 try:
   bt = pyautogui.locateOnScreen("img/btRelatorio.png", region = regiao ,confidence=0.9, grayscale=True) 
   botao= pyautogui.center(bt)  
    
   pyautogui.click( btmonitor  + botao.x, botao.y + pedidosTravados)
   #pyautogui.click( btmonitor  + botao.x, barra + 384 + pedidosTravados)
   #pyautogui.click( btmonitor  + botao.x, barra + 388 + pedidosTravados)    

 except:
   pyautogui.alert("Não foi possível identificar o botão de aprovar na tela!", title='ERRO')


#clique no botão de cliente troca
def btClienteTroca():
 try:
  bt = pyautogui.locateOnScreen("img/btAprova2.png", region = regiao ,confidence=0.9, grayscale=True) 
  botao= pyautogui.center(bt)     
  pyautogui.click( btmonitor  + botao.x, botao.y + pedidosTravados) 
  
 except:
   pyautogui.alert("!Não foi possível identificar o botão de aprovar na tela!", title='ERRO')

#clique no botão de Kit Peça
def btkitpeca():
 try:
  bt = pyautogui.locateOnScreen("img/btAprova2.png", region = regiao ,confidence=0.9, grayscale=True) 
  botao= pyautogui.center(bt)     
  pyautogui.click( btmonitor  + botao.x, barra + 365 + pedidosTravados)
  pyautogui.click( btmonitor  + botao.x, barra + 383 + pedidosTravados) 
 except:
   pyautogui.alert("!Não foi possível identificar o botão de aprovar na tela!", title='ERRO')


 # Abre a pagina de relatório da OS
def VerRelatorio():   
 x , y = pyautogui.position()
 if VerificaImg('img/semPedidos.jpg'):
     pyautogui.alert('SEM PEDIDOS NA TELA DE AUDITORIA', title='ATENÇÃO', button='OK')
 else:    
    btRelatorio()
    time.sleep(1)     
    #pyautogui.click(30,200)
    pyautogui.hotkey('win', 'up')
   # time.sleep(2)
    #pyautogui.doubleClick(30,200)
    #time.sleep(1)
    #pyautogui.hotkey('ctrl', 'c')    
    pyautogui.moveTo(x, y)   

#Finaliza o programa   
def finaliza():
    sys.exit()

#metodo para aprovação orçamento
def aprovaOrcamento():  
  try: 
   x , y = pyautogui.position(); 
   cont=0
   if selecionaPed:
    BtAprovaOrcamento()
   while not VerificaImg("img/aprovaOrcamento.png"):  
    time.sleep(1)
    cont= cont+1
    if (cont>20):
     return      
   pyautogui.click(monitor + 220 , 274 + barra) #(-1119 , 283)
   keyboard.write("APROVADO!", 0.01)
   pyautogui.click(monitor + 396 , 340 + barra)
   pyautogui.moveTo(x, y)  
  except:
    while not VerificaImg("img/aprovaOrcamento3.png"):  
     time.sleep(1)
     cont= cont+1
    if (cont>20):
     return      
    pyautogui.click(monitor + 220 , 274 + barra) #(-1119 , 283)
    keyboard.write("APROVADO!", 0.01)
    pyautogui.click(monitor + 396 , 340 + barra)
    pyautogui.moveTo(x, y)  

#metodo para aprovação geral
def aprova( mensagem):  
 global selecionaPed
 x , y = pyautogui.position()
 cont=0  
 if selecionaPed:    
    BtAprova() 
 while not abriuPedido():  
    time.sleep(1)
    cont= cont+1       
    if (cont>20):
      return 
 if pyautogui.locateOnScreen("img/blockP.png", region=regiao, grayscale=True):
    pyautogui.alert("ATENÇÃO! TEM BLOCK P!!!")
 else:    
    pyautogui.click( monitor + 222 , 198 + barra)    
    pyautogui.click( monitor + 256 , 198 + barra)    
    pyautogui.click( monitor + 296 , 198 + barra) 
    pyautogui.click( monitor + 332 , 198 + barra)
    pyautogui.click( monitor + 247 , 283 + barra)
    time.sleep(0.3) 
    pyautogui.click( monitor + 230 , 345 + barra)
    pyautogui.click( monitor + 225 , 338 + barra)  
    time.sleep(0.5)   
    keyboard.write(mensagem, 0.01)
    time.sleep(0.1) 
    pyautogui.click( monitor + 390 , 407 + barra) 
 pyautogui.moveTo(x, y)     
   

# Atualiza a tela de auditoria
def atualiza():
  x , y = pyautogui.position()  
  pyautogui.click( monitor + 40 ,273 + barra) #clique no botão aprovação
  time.sleep(3)
  if pyautogui.locateAllOnScreen('img/atualizaTela.jpg', confidence= 0.7, region=regiao, grayscale=True):
     #pyautogui.click( monitor + 238 , 178 + barra)
     #time.sleep(2) 
     pyautogui.click( monitor + 755 , 225 + barra)
  else:    
    pyautogui.click( monitor + 753 , 279 + barra)
  pyautogui.moveTo(x, y)   

#Metodo para Aprovar o Kit Peça
def aprovaKitPeca():
 x , y = pyautogui.position()
 if selecionaPed:  
   btkitpeca()
 cont=0  
 while not abriuPedido():  
   time.sleep(0.5)
   cont= cont+1
   if (cont>20):
    return 
 if pyautogui.locateOnScreen("img/blockP.png", region=regiao,  confidence=0.9):
    pyautogui.alert("ATENÇÃO! TEM BLOCK P!!!")
 else:    
    pyautogui.click( monitor + 220 , 198 + barra)    
    pyautogui.click( monitor + 256 , 198 + barra)    
    pyautogui.click( monitor + 296 , 198 + barra) 
    pyautogui.click( monitor + 247 , 283 + barra)
    time.sleep(0.3) 
    pyautogui.click( monitor + 230 , 343 + barra)
    pyautogui.click( monitor + 217 , 336 + barra)  
    time.sleep(0.5)   
    keyboard.write('APROVADO!', 0.01)
    time.sleep(0.3) 
    pyautogui.click( monitor + 389 , 406 + barra)
 pyautogui.moveTo(x, y)   
        

#APROVAÇÃO COM O AVAL DO SUPORTE
def aprovaSuporte():
    msg= input('Digite a OS de liberação: ')
    aprova('LIBERADO PELO SUPORTE TECNICO MEDIANTE A OS :'+ msg)
    input("")

 #Metodo para aprovar Cliente Troca
def ClienteTroca1(mensagem):
    x , y = pyautogui.position()
    if selecionaPed:     
     btClienteTroca()     
    cont=0     
    while not abriuPedido():  
     time.sleep(0.5)
     cont= cont+1
     if (cont>20):
      return 
    if pyautogui.locateOnScreen("img/blockP.png", region=regiao, confidence=0.95):
     pyautogui.alert("ATENÇÃO! TEM BLOCK P!!!")
    else:     
      pyautogui.click( monitor + 220 , 198 + barra)    
      pyautogui.click( monitor + 256 , 198 + barra)    
      pyautogui.click( monitor + 296 , 198 + barra)
      pyautogui.click( monitor + 267, 288 + barra) #Clique no botão Motivo
      pyautogui.write('F')
      pyautogui.click( monitor + 294, 330 + barra)
      time.sleep(0.5)  
      keyboard.write(mensagem, 0.01)
      time.sleep(0.5)
      pyautogui.click( monitor + 385, 410 + barra)    
      pyautogui.click( monitor + 388, 415 + barra)
      pyautogui.click( monitor + 388, 471 + barra)
      pyautogui.click( monitor + 267, 288 + barra)
      pyautogui.write('F')
      pyautogui.click( monitor + 395, 478 + barra)     
    pyautogui.moveTo(x, y)     
   

#Cliente troca para reprovação
def ClienteTrocaReprova():
 x , y = pyautogui.position()
 #pyautogui.click( monitor + 941, 380 + barra)
 if selecionaPed:  
  btClienteTroca()
 cont=0
 while not abriuPedido():  
   time.sleep(0.5)
   cont= cont+1
   if (cont>20):
    return    
 pyautogui.click( monitor + 219,  431 + barra)   
 pyautogui.click( monitor + 220 , 198 + barra)    
 pyautogui.click( monitor + 256 , 198 + barra)    
 pyautogui.click( monitor + 296 , 198 + barra)
 time.sleep(1)
 pyautogui.click( monitor + 257,285 + barra)
 pyautogui.write('R')
 time.sleep(0.5)
 pyautogui.click( monitor + 310,331 + barra) 
 keyboard.write('Fora do prazo, sem evidencia', 0.01)
 pyautogui.click( monitor + 391, 411 + barra)
 pyautogui.click( monitor + 391, 420 + barra)  
 pyautogui.click( monitor + 389,472 + barra)
 pyautogui.moveTo(x, y)
 print("cliente troca reprova")

#Etacionar a OS
def aprovaPNR():
 x , y = pyautogui.position()
 if selecionaPed:
  global scrool 
  scrool= verificaScrool()
  ped = verificaPed() 
  pyautogui.click(ped + larg + scrool + monitor + 802, 380 + barra + pedidosTravados)
 time.sleep(4)
 pyautogui.click( monitor + 757 , 415 + barra)
 time.sleep(3)
 pyautogui.click( monitor + 803, 415 + barra)
 time.sleep(1)
 pyautogui.click( monitor + 1295,443 + barra)
 pyautogui.moveTo(x, y)   

 #Aprova pedido PRN
def reprovaPNR():
    x , y = pyautogui.position()
    if selecionaPed:
     global scrool 
     scrool= verificaScrool()
     ped = verificaPed() 
     pyautogui.click(ped + larg + scrool + monitor + 776 , 360 + barra + pedidosTravados)
    time.sleep(4)
    pyautogui.click( monitor + 248, 200 + barra)
    pyautogui.write('R')
    pyautogui.click( monitor + 226, 245 + barra)     
    keyboard.write('Fora do prazo sem o envio da pagina de suprimentos atraves dos canais oficiais de comunicacao.', 0.01)
    pyautogui.click( monitor + 396 ,410 + barra) 
    pyautogui.click( monitor + 394 ,413 + barra)  
    pyautogui.moveTo(x, y)   


#metodo para reprovação geral
def reprova( mensagem):   
    x , y = pyautogui.position()
    if selecionaPed:
     BtReprova()
    cont=0  
    while not abriuPedido():  
     time.sleep(1)
     cont= cont+1
     if (cont>20):
      return     
    pyautogui.click( monitor + 244,199 + barra)
    time.sleep(0.5)
    pyautogui.click( monitor + 242, 216 + barra)
    keyboard.write(mensagem, 0.01)
    time.sleep(0.5)
    pyautogui.click( monitor + 389,304 + barra )
    pyautogui.moveTo(x, y)   

def abriuPedido(): 
 if pyautogui.locateOnScreen("img/telaPedido.png", region=regiao, confidence=0.9):
  return True
 else:
   return False  

def verificaScrool(): 
 if pyautogui.locateOnScreen("img/reordenar.png", region=regiao, confidence=0.9):  
  return  0
 else:
   return -5  

def VerificaImg(imagem): 
 if pyautogui.locateOnScreen(imagem, region=regiao, confidence=0.8, grayscale=True):
  return True
 else:
   return False    

#####------------------------------------- PROGRAM ----------------------------------------------#####
construtor()
barra_favoritos('2')
check_Tela(2)