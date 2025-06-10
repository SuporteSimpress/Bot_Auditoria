import PySimpleGUI as sg
from auditoria_TelaEsquerda import *
from PySimpleGUI import ( Button, Radio, Checkbox , Combo,  Text, Input, Column, HSeparator, VSeparator, Push)
from PIL import ImageGrab
from functools import partial
import pyperclip
import csv
import os
import pandas as pd

ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
altura=0

tecnicos = []
mercantil =[]

#LEITURA DOS TECNICOS - O ARQUIVO PRECISA SER UTF-8
with open("./dados/tecnicos.csv", "r", encoding='utf-8') as arquivo:
    arquivo_csv = csv.reader(arquivo, delimiter=",")
    for i, linha in enumerate(arquivo_csv):
        if i == 0:
            print("Cabeçalho: " + str(linha))
        else:           
           tecnicos += linha

#LEITURA DO CLIENTE MERCANTIL - O ARQUIVO PRECISA SER UTF-8
with open("./dados/clientes.csv", "r", encoding='utf-8') as arquivo:
    arquivo_csv = csv.reader(arquivo, delimiter=",")
    for i, linha in enumerate(arquivo_csv):
        if i == 0:
            print("Cabeçalho: " + str(linha))
        else:           
           mercantil += linha

def lerClientes():
 file_id = "1_d-5B60n_gF4jxXSvmLGVmT3y734qjNd"
 url = f"https://drive.google.com/uc?id={file_id}"
 if not os.path.exists(url):
        print("Arquivo de técnicos clientes não encontrado.")
        return
 df = pd.read_csv(url)
 mercantil += df


layout_Esquerda= [
    [Text("Ver o relatório" , font=('Calibri', 14)), Push() , Button("    Ver     ", key='verRelatorio', button_color='#616161')],
    [Text("Atualizar a tela" , font=('calibri',14)), Push() , Button("Atualizar", key='atualiza' , button_color='#616161')],
   
    [Text("--------------------   APROVAÇÕES   --------------------------", font=('calibri', 17)), Push() ],
    [Text("Aprovação Suporte, OS:"), Input(key='os_Suporte', size=(18,0), do_not_clear=False ), Push(), Button("Aprovar", key='AprovaSuporte')],  
    [Text("Quebra Aleatória"), Push(), Combo(values=['QA - Quebra Aleatória','QA/ Atendimento B2C','QA - Peça com valor inferior a R$50.00'],size=(18,0) ,key='blockP', enable_events=True,  default_value='QA - Quebra Aleatória', font=('Calibri', 14),readonly=False) , Button("Aprovar", key='block')],  
    [Text("Unidade de imagem"), Push(), Combo(values=['Bolsão / Revisão Laboratório', 'Dentro do prazo', 'Impressões riscadas, claras ou manchadas ', 'Vazamento de revelador ', 'Alta área de cobertura ', 'Oxidação do rolo de carga ', 'Código de erro #31-007 ', 'Código de erro #C3-1315 ', 'Peça consumida com 80% de uso ', 'Ruído excessivo nas engrenagens, reciclagem travada '],size=(18,0) ,key='dentrodoprazo', enable_events=True,  default_value='Dentro do prazo ', font=('Calibri', 14),readonly=True) , Button("Aprovar", key='dentro')],
    [Text("Unidade de fusão"), Push(), Combo(values=['Dentro do prazo','Atolamento constante ','Erro de aquecimento ','Pelicula danificada ','Código de erro #02-001 '],size=(18,0) ,key='fuser', enable_events=True,  default_value='Erro de aquecimento ', font=('Calibri', 14),readonly=True) , Button("Aprovar", key='fusao')], 
    [Text("Cliente troca - UI"), Push(), Combo(values=['Bolsão / Revisão Laboratório', 'Dentro do prazo ', 'Impressões riscadas, claras ou manchadas ', 'Vazamento de revelador ', 'Alta área de cobertura ', 'Oxidação do rolo de carga ', 'Código de erro #31-007 ', 'Código de erro #C3-1315 ', 'Peça consumida com 80% de uso ', 'Ruído excessivo nas engrenagens, reciclagem travada '],size=(18,0) ,key='clientetrocaK', enable_events=True,  default_value='Dentro do prazo ', font=('Calibri', 14),readonly=True), Button("Aprovar", key='aprovaCliente')],  
    [Text("Cliente troca - fusão"), Push(), Combo(values=['Atolamento constante ','Erro de aquecimento ','Pelicula danificada ','Código de erro #02-001 '],size=(18,0) ,key='clientetrocafuserK', enable_events=True,  default_value='Erro de aquecimento ', font=('Calibri', 14),readonly=True) , Button("Aprovar", key='clientetrocafuser')], 
    
    [Text("--------------------  REPROVAÇÕES    -------------------------", font=('calibri', 17)), Push() ],        
    [Text("Recusar "), Push(), Combo(values=['Fora do prazo, sem evidência','Sem liberação do Suporte','Sem justificativa para liberação','Fora do prazo - Cliente Troca','Pedido Duplicado','Solicitado item incorreto','Não seguiu fluxo de orçamento','Quantidade acima do utilizado pelo equipamento','Solicitado consumível/acessório como peças','Venda Mercantil','Direcionado para troca técnica'],size=(18,0) ,key='recusak', enable_events=True,  default_value='Fora do prazo, sem evidência', font=('Calibri', 14),readonly=True) , Button("Recusar", key='recusa',button_color='brown')],  
]

layout_Direita = [
   [sg.Text(' TECNICOS DA LISTA  ', font=('calibri', 17))],
   [sg.Input(size=(36, 1), enable_events=True, key='combo-tecnico')],
   [sg.Listbox(values= tecnicos, size=(43, 7), enable_events=True, key='-LIST-TECNICO', font=('calibri',12))],
   [sg.Text('------------------------------------------------------------------------', font=('calibri', 17))],
   
   #LAYOUT DA CABEÇA TERMICA
   [sg.Text('CLIENTES - CABEÇA TÉRMICA', font=('calibri', 17))],
   [sg.Input(size=(36, 1), enable_events=True, key='combo-mercantil')],
   [sg.Listbox(values= mercantil, size=(43, 7), enable_events=True, key='-LIST-MERCANTIL', font=('calibri',12))],   
]

layout_monitor =  [ [Radio("Esq.", key='tela1', group_id='bt_Tela', enable_events=True ,  font=('calibri',12) ) ,Radio("Central", key='tela2', default=True,  group_id='bt_Tela', enable_events=True,  font=('calibri',13)), Radio("Direita", key='tela3',  group_id='bt_Tela', enable_events=True,  font=('calibri',13))]]
layout_barra = [[Checkbox('Barra de Fav.', key= '-barra-', default=False, enable_events=True,  font=('calibri',13) ), Checkbox('sel. Pedido', key= '-selecionaPedido-', default=True, enable_events=True,  font=('calibri',13) ), Text("Ped.Travado", font=('calibri',13)),Combo(values=['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30'],size=(3,1) ,key='-ped_travado-', enable_events=True, default_value='0',readonly=True,  font=('calibri',13))]]
Frame1 = [sg.Frame (' Localização do Monitor  ', layout_monitor, font=('calibri',9, "bold"), vertical_alignment='center') ]
Frame2 =  [sg.Frame('', layout_barra  , border_width=0)] 
Frame_Principal = [ Frame1, Frame2]

layout_cabecalho = [  
  [Text("                            BOT - AUDITORIA DE PEÇAS",font=("calibri", 24))],
  Frame2, Frame1 
]
 
#Layout principal
layout = [
    [ layout_cabecalho, Column(layout_Esquerda), VSeparator(), Column(layout_Direita) ]
]

janela = sg.Window("Tela de auditoria", size=(900, 670), layout=layout, margins=(0,2), resizable=True, font=('calibri',15,), relative_location= (-20,-50)  )


def verifica_Barra():
   
 if janela['-barra-'] == True:
      barra_favoritos('1')     
 if janela['-barra-'] == False:
      barra_favoritos('2')     

  
def change_radio_text_color(element, new_color, tamanho,  negrito):
    element.update(text_color=new_color)      
    element.Widget.config(font=('calibri', tamanho, negrito)) #o Widget.config serve para que a configuração seja usada sem um construtor.
 

while True: 
 eventos, valores = janela.read()
 if eventos == sg.WINDOW_CLOSED:
  finaliza()
 if valores['combo-tecnico'] != '': # if a keystroke entered in search field
    search = valores['combo-tecnico'].upper()
    new_values = [x for x in tecnicos if search in x]  # do the filtering
    janela['-LIST-TECNICO'].update(new_values)
    print(search)
    
 else:
    # display original unfiltered list
    janela['-LIST-TECNICO'].update(tecnicos)
    # if a list item is chosen
 if eventos == '-LIST-TECNICO' and len(valores['-LIST-TECNICO']):
    sg.popup('Selected ', valores['-LIST-TECNICO'])

 if valores['combo-mercantil'] != '':                         # if a keystroke entered in search field
    search = valores['combo-mercantil'].upper()
    new_values = [x for x in mercantil if search in x]  # do the filtering
    janela['-LIST-MERCANTIL'].update(new_values)
 else:
        # display original unfiltered list
        janela['-LIST-MERCANTIL'].update(mercantil)
    # if a list item is chosen
 if eventos == '-LIST-MERCANTIL' and len(valores['-LIST-MERCANTIL']):
        sg.popup('Selected ', valores['-LIST-MERCANTIL'])

 if eventos == 'verRelatorio':
   VerRelatorio()
 if eventos == 'atualiza':
   atualiza()
 if eventos == 'dentro':
  aprova(valores['dentrodoprazo'])
 if eventos == 'block':
  aprova(valores['blockP'])
 if eventos == 'AprovaSuporte':
  if valores['os_Suporte'] =="":
    pyautogui.alert("Insira a OS de suporte!")
  else:
   aprova("Liberado mediante  ação do Suporte na OS: " + valores['os_Suporte'] + " SEM BLOQ P")  
 if eventos == 'aprovaJustificativa':
    justificativa = valores['justifica']
    if justificativa == "":     
     aprova("Aprovado mediante justificativa do técnico na OS e/ou canais oficiais de comunicação.") 
    else:
     tamanho = len(justificativa)  
     if tamanho < 180:    
      aprova(justificativa)     
     else:     
      pyautogui.alert("Reduza o tamanho da justificativa!")        
  
 if eventos == 'aprovaCliente':
  ClienteTroca1(valores['clientetrocaK'])
 if eventos == 'fusao':
  aprova(valores['fuser'])
 if eventos == 'aprovaKit':
  aprovaKitPeca()
 if eventos == 'clientetrocafuser':
   ClienteTroca1(valores['clientetrocafuserK'])
 if eventos == 'recusa':
    if valores['recusak'] ==  'Fora do prazo - Cliente Troca':
       ClienteTrocaReprova()
       pyperclip.copy('Fora do prazo, sem evidência')
    else:
     reprova(valores['recusak'])
     if valores['recusak'] ==  'Fora do prazo, sem evidência':
      pyperclip.copy('Fora do prazo sem o envio da página de suprimentos através dos canais oficiais de comunicação ou evidência que justifique o pedido da peça.')
     elif valores['recusak'] ==  'Sem liberação do Suporte':
        pyperclip.copy('Sem a liberação do Suporte, pedido recusado')
     elif valores['recusak'] ==  'Sem justificativa para liberação':
       pyperclip.copy('Fora do prazo sem o envio da página de suprimentos através dos canais oficiais de comunicação ou evidência que justifique o pedido da peça.')
     elif valores['recusak'] ==  'Pedido Duplicado':
       pyperclip.copy('Pedido recusado porque encontra-se duplicado.')
     elif valores['recusak'] ==  'Solicitado item incorreto':
       pyperclip.copy('Pedido cancelado pois o item solicitado está incorreto.')
     elif valores['recusak'] ==  'Não seguiu fluxo de orçamento':
       pyperclip.copy('O fluxo de requisição de orçamento não foi realizado corretamente e a peça foi solicitada em garantia. Favor refazer o pedido da peça como orçamento.')
     elif valores['recusak'] ==  'Quantidade acima do utilizado pelo equipamento':
       pyperclip.copy('A quantidade de itens solicitados não compatível com o modelo do equipamento. Pedido recusado.')
     elif valores['recusak'] ==  'Solicitado consumível/acessório como peças':
       pyperclip.copy('O item solicitado não pode ser solicitado como peça. Pedido recusado.')
     elif valores['recusak'] ==  'Venda Mercantil':
       pyperclip.copy('A substituição das cabeças de impressão para os equipamentos térmicos ocorre via venda mercantil entre Cliente e Simpress, dessa forma, cancelamos a solicitação visto a troca deste item em garantia não ser contemplada em contrato. A solicitação pode ser feita via formulário BKS_022 - Solicitação de Venda Mercantil, sendo enviado (upload) no lugar do Termo de Ciência e disponível no Portal de Qualidade.')
     elif valores['recusak'] ==  'Direcionado para troca técnica':
       pyperclip.copy('O equipamento foi direcionado para troca técnica e por este motivo o pedido foi recusado.')
      

 
 
 if eventos == 'tela1':
   change_radio_text_color(janela['tela1'], 'LightGreen', 14,'bold')   
   change_radio_text_color(janela['tela2'], 'white', 14,'')  
   change_radio_text_color(janela['tela3'], 'white',14, '')  
   check_Tela('1')
  
 if eventos == 'tela2':
   change_radio_text_color(janela['tela1'], 'white',14,'')   
   change_radio_text_color(janela['tela2'], 'LightGreen', 14, 'bold')  
   change_radio_text_color(janela['tela3'], 'white',14,'')
   check_Tela('2')

 if eventos == 'tela3':
  change_radio_text_color(janela['tela1'], 'white',14,'')   
  change_radio_text_color(janela['tela2'], 'white',14,'')  
  change_radio_text_color(janela['tela3'], 'LightGreen', 14, 'bold')  
  check_Tela('3')
       
 if eventos =='-barra-' :   
     
    if janela['-barra-'] == True:
      barra_favoritos('1')
      print('barra = 30')
    if janela['-barra-'] == False:
      barra_favoritos('2')
      print('barra = 0')
    
    if janela["-barra-"].get() == True:
      barra_favoritos('1')          
      janela['-barra-'].Widget.config(font=('calibri', 14, 'bold')) 
    else:
      barra_favoritos('2')      
      janela['-barra-'].Widget.config(font=('calibri', 13)) 

 if eventos == '-selecionaPedido-':         
     if janela["-selecionaPedido-"].get() == True:        
      selecionaPedido('1')          
     if janela["-selecionaPedido-"].get() == False:        
      selecionaPedido('2') 
        
  
 if eventos == '-ped_travado-':    
   travados = valores['-ped_travado-']
   check_travados(travados)   