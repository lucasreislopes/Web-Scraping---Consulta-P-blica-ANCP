from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
import time
import pandas as pd

from coleta_offline import coletar_informacoes

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.ancp.org.br/consultaTouro.php?iframe=true#")

time.sleep(2)

a = ActionChains(driver)

def press(key, times=1, delay=0.05):
    for _ in range(times):
        a.send_keys(key).perform()
        time.sleep(delay)

def press_filtro(key, times=1, delay=0.25):
    for _ in range(times):
        a.send_keys(key).perform()
        time.sleep(delay)

def press_shift_tab(delay=0.25):
    a.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT).perform()
    time.sleep(delay)

## sequências de teclas para selecionar o nelore
# sequência de teclas
press(Keys.TAB, 4)
press(Keys.ARROW_DOWN)
press(Keys.TAB, 3)
press(Keys.ENTER)
press(Keys.TAB)
press(Keys.ENTER)
press(Keys.TAB)
press(Keys.ENTER)
press(Keys.TAB)
press(Keys.ENTER)
press(Keys.TAB)
press(Keys.ENTER)
a.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT).perform()
press(Keys.ENTER)
press(Keys.TAB, 198)
press(Keys.TAB)
press(Keys.ENTER)

# tempo de espera
time.sleep(1) # 30

####
## sequencias de para coletar os animais
press(Keys.TAB, 1)
press(Keys.ENTER)
time.sleep(0.5)
# função para armazenar o HTML

def press_tabs_progressively(start=5, step=4, limit=40, delay=0.05):
    """
    Fluxo:
    1. Pressiona TAB duas vezes e ENTER (pré-inicialização)
    2. Depois envia TABs em progressão linear (5 -> 9 -> 13 ...)
       Sempre finalizando cada bloco com ENTER + delay.
    """
    
    # contar número de páginas
    def obter_total_paginas_selenium(driver):

        bloco = driver.find_element(By.ID, "pagina")
        texto = bloco.text.strip()

        # exemplo: "Pag. 1 / 1039\nTempo: 0,24 Segundos"
        partes = texto.split("/")
        total = partes[1].split()[0]

        return int(total)
    
    def pagina_atual(driver):
        
        bloco = driver.find_element(By.ID, "pagina")
        texto = bloco.text.strip()

        partes = texto.split("/")
        # A parte da esquerda contém algo como "Pag. 1"
        esquerda = partes[0]
        # Extrai apenas o número ao final do dicionário
        num = esquerda.split()[-1]

        return int(num)
        
    def ir_para_pagina(driver, numero):

        while True:
            try:
                # sempre reencontra o input (novo DOM)
                campo = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "id_ir_para"))
                )
                campo.clear()
                campo.send_keys(str(numero))

                # sempre reencontra o BOTÃO (novo DOM)
                botao = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[@onclick=\"ir('id_ir_para');\"]"))
                )

                botao.click()     # <<< AQUI OCORRIA O ERRO
                break             # se funcionou → sair do while

            except StaleElementReferenceException:
                print("Elemento stale → recarregando elementos… tentando novamente.")
                continue  # repete o while para recarregar o input e o botão

        # Agora aguarda a página nova carregar
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pagina"))
        )

    csv_path = "saida_touros.csv"

    # cria o csv vazio só uma vez
    import os

    # CAMINHO ABSOLUTO — GARANTE QUE O ARQUIVO APAREÇA NA PASTA DO PROJETO
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "saida_touros.csv")

    # criar CSV somente se ainda não existir OU estiver vazio
    def criar_csv_se_preciso(dados):
        if (not os.path.exists(csv_path)) or os.path.getsize(csv_path) == 0:
            print(">>> Criando CSV com cabeçalho real...")
            pd.DataFrame(columns=dados.keys()).to_csv(csv_path, index=False, sep=";")

    # 1) aperta tab 2 vezes
    press(Keys.TAB, 2)   # pressiona TAB duas vezes
    
    # 2) aperta enter
    press(Keys.ENTER)
    time.sleep(delay)

    # número de páginas a ser considerada
    total = obter_total_paginas_selenium(driver)

    # loop pelas páginas
    # Necessário atualizar a página caso o webdriver feche, recomendo que seja verificado no arquivo csv gerado e 
    # no site da ANCP para verificar em qual página está baseado no nome do animal e no seu valor de MGTe
    for pagina in range(1, total+1): 
        # --- Ciclo progressivo ---
        current = start
        
        pagina_esperada = pagina

        if pagina_atual(driver) != pagina_esperada:
            ir_para_pagina(driver, pagina_esperada)

            WebDriverWait(driver, 20).until(
                EC.text_to_be_present_in_element((By.ID, "pagina"), f"{pagina_esperada}")
            )

            time.sleep(1.5)
            
        while current <= limit:
          
            # 1) delay providencial
            time.sleep(delay)

            # 2) TAB x current
            press(Keys.TAB, current)

            # 3) ENTER
            press(Keys.ENTER)

            # 4) Delay providencial
            time.sleep(delay)
            time.sleep(0.5)

            # 5) função para armazenar o HTML ######
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            dados = coletar_informacoes(soup)

            time.sleep(0.5)

            # 2) --- AQUI entra a proteção do CSV ---
            if dados and len(dados.keys()) > 0:
                criar_csv_se_preciso(dados)   # <-- só cria 1 vez
            else:
                print("Aviso: dados vazios, pulando...")
                continue

            # # garantir que TEM AS MESMAS colunas do CSV
            df_temp = pd.DataFrame([dados])
            df_existente = pd.read_csv(csv_path, sep=";")
            df_unificado = pd.concat([df_existente, df_temp], axis = 0, ignore_index=True)
            df_unificado.to_csv(csv_path, index=False, sep= ";")
            # df_temp.to_csv(csv_path, mode = "a", header = False, index = False, sep = ";")

            # 6) aperta tab 2 vezes
            press(Keys.TAB, 2)   # pressiona TAB duas vezes
            
            # 7) aperta enter
            press(Keys.ENTER)

            # Aumenta a sequência
            current += step
        
        #####
        wait = WebDriverWait(driver, 20)

        try:
            botao_proxima = wait.until(
                EC.element_to_be_clickable((By.ID, "proxima_pagina"))
            )
            time.sleep(1) # 30
            botao_proxima.click()
            time.sleep(2) # 30


            # RECOMEÇA O TAB PARA A PRÓXIMA PÁGINA
            current = start
            
        except Exception as e:
            print("deu ruim, mas não tem como dar ruim")
            break

    # df_final.to_csv("saida_touros.csv",index=False, sep= ";")

press_tabs_progressively(
    start = 1, 
    step = 4,
    limit = 57,
    delay = 0.5
)

time.sleep(10)

# não fecha sozinho
input("Pressione ENTER para fechar...")
driver.quit()