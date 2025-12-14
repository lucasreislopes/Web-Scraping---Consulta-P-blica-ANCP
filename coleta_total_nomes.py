from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

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

def coletar_nomes(driver):

    fonts = driver.find_elements(By.CSS_SELECTOR, 'font[color="#000000"][size="-2"]')

    nomes = []

    for f in fonts:
        links = f.find_elements(By.CSS_SELECTOR, 'a[href="#"]')
        for link in links:
            nome = link.text.strip()
            if nome:
                nomes.append(nome)
    
    return nomes

def coletar_linha(driver):
    linhas = driver.find_elements(By.CSS_SELECTOR, "tr.textinho")

    dados = []

    for linha in linhas:
        colunas = linha.find_elements(By.CSS_SELECTOR, "td font[color='#000000'][size='-2'] a")
        valores = []

        for c in colunas:
            texto = c.text.strip()
            texto = " ".join(texto.split())
            valores.append(texto)

        while len(valores) < 4:
            valores.append("")

        dados.append(valores[:4])
    
    return dados

def contar_nomes(driver):
    return len(driver.find_elements(
        By.CSS_SELECTOR,
        'font[color="#000000"][size="-2"] a[href="#"]'
    ))

# contar número de páginas
def obter_total_paginas_selenium(driver):

    bloco = driver.find_element(By.ID, "pagina")
    texto = bloco.text.strip()
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

def salvar_nomes(pagina, nomes):

    if not nomes:
        return
    
    df_existente = pd.read_csv(csv_path, sep=";")

    df_novos = pd.DataFrame(
        [{"pagina": pagina, "nome": nome} for nome in nomes]
    )

    df_final = pd.concat([df_existente, df_novos], ignore_index=True)
    df_final.to_csv(csv_path, index=False, sep=";")

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
press(Keys.ARROW_DOWN, 5) # 5
press(Keys.TAB)
press(Keys.ENTER)

# tempo de espera
time.sleep(35) # 30


total = obter_total_paginas_selenium(driver)

import os
# cria arquivo
csv_path = "coleta_animais.csv"

# CAMINHO ABSOLUTO — GARANTE QUE O ARQUIVO APAREÇA NA PASTA DO PROJETO
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "coleta_animais.csv")

# criar CSV somente se ainda não existir OU estiver vazio
if (not os.path.exists(csv_path)) or os.path.getsize(csv_path) == 0:
    # pd.DataFrame(columns=["nome"]).to_csv(csv_path, index=False, sep=";")
    pd.DataFrame(columns=["Nome_animal", "Série", "RGN", "RGD"]).to_csv(csv_path, index=False, sep=";")

# for pagina in range(1, total+1):
for pagina in range(0, total+1): 

    # current = start
    pagina_esperada = pagina

    if pagina_atual(driver) != pagina_esperada:
            ir_para_pagina(driver, pagina_esperada)

            time.sleep(35) # 35
            WebDriverWait(driver, 20).until(
                EC.text_to_be_present_in_element((By.ID, "pagina"), f"{pagina_esperada}")
            )

            # Aguarda a presença de pelo menos 1 nome na tabela
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'font[color="#000000"][size="-2"] a[href="#"]'))
            )

            nomes_coletados = coletar_linha(driver) # coletar_nomes
            time.sleep(0.5) # 35

            # df_temp = pd.DataFrame({"nome": nomes_coletados})
            df_temp = pd.DataFrame(nomes_coletados, columns=["Nome_animal", "Série", "RGN", "RGD"])
            write_header = (not os.path.exists(csv_path)) or os.path.getsize(csv_path) == 0
            df_temp.to_csv(csv_path, mode = "a", header = write_header, index = False, sep = ";")
