from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

from coleta_offline import coletar_informacoes # type: ignore


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.ancp.org.br/consultaTouro.php?iframe=true#")

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "coleta_faltando.txt")

dados = []

with open(csv_path, newline="", encoding="utf-8-sig") as f:
    for linha in f:
        linha = linha.strip()  # remove espaços e quebras de linha
        partes = linha.split(",")  # divide pelos campos
        dados.append(partes)

time.sleep(2)

a = ActionChains(driver)

def press(key, times=1, delay=0.5):
    for _ in range(times):
        a.send_keys(key).perform()
        time.sleep(delay)

def selecionar_nome(lista): # adicionar loop para repetir

    # Série
    campo_serie = driver.find_element(By.ID, 'FILTRO_IDENTIFICACAO_SERIE')
    campo_serie.click()
    campo_serie.clear()
    campo_serie.send_keys(lista[1])

    # RGN
    campo_rgn = driver.find_element(By.ID, 'FILTRO[IDENTIFICACAO][RGN]')
    campo_rgn.click()
    campo_rgn.clear()
    campo_rgn.send_keys(lista[2])

    # RGD
    campo_rgd = driver.find_element(By.ID, 'FILTRO[IDENTIFICACAO][RGD]')
    campo_rgd.click()
    campo_rgd.clear()
    campo_rgd.send_keys(lista[3])

def selecionar_animal(nome):
    nome_limpo = nome.replace(" ", "").upper()

    bloco = driver.find_elements(By.CSS_SELECTOR, 'font[color="#000000"][size="-2"] a[href="#"]')
    
    for elemento in bloco:
        texto = elemento.text.strip().replace(" ", "").upper()

        if texto == nome_limpo:
            press(Keys.TAB)
            press(Keys.ENTER)
            time.sleep(0.5)
            return True

def selecionar_animal(nome):
    # nome_limpo = nome.replace(" ", "").upper()
    nome_limpo = nome[0].replace(" ", "").upper()

    try:
        bloco = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'font[color="#000000"][size="-2"] a[href="#"]')
            )
        )
    except Exception as e:
        print("Erro ao carregar lista de animais:", e)
        return False

    for elemento in bloco:
        texto = elemento.text.strip().replace(" ", "").upper()
        if texto == nome_limpo:
            driver.execute_script("arguments[0].click();", elemento)
            time.sleep(1)
            return True

    print("Animal não encontrado:", nome)
    return False


def aba1(driver):
    aba = driver.find_element(By.CSS_SELECTOR, 'a[href="#aba1"]')   
    aba.click()
    time.sleep(2)
       
# # # sequências de teclas para selecionar o nelore
# # sequência de teclas
press(Keys.TAB, 4)
press(Keys.ARROW_DOWN)

aba1(driver)
time.sleep(0.05)

# cria arquivo
csv_path = "animais_corrigidos.csv"

# CAMINHO ABSOLUTO — GARANTE QUE O ARQUIVO APAREÇA NA PASTA DO PROJETO
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "animais_corrigidos.csv")

# criar CSV somente se ainda não existir OU estiver vazio
if (not os.path.exists(csv_path)) or os.path.getsize(csv_path) == 0:
    df_vazio = pd.DataFrame().to_csv(csv_path, index=False, sep=";") #index true
    df_vazio.to_csv(csv_path, index=False, sep = ";")

if not os.path.exists(csv_path):
    open(csv_path, "W", encoding="utf-8").close

# for nomes in dados:
for nomes in dados[1:]:
    
    selecionar_nome(nomes)
    press(Keys.ENTER)

    time.sleep(3) # 2 ou 3 sec 

    press(Keys.TAB)
    press(Keys.ENTER)      

    time.sleep(1) # 2 ou 3 sec        
    selecionar_animal(nomes)

    # time.sleep(1) # 2 ou 3 sec        
    # 5) função para armazenar o HTML ######
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    resultados = coletar_informacoes(soup)
    df_temp = pd.DataFrame([resultados])

    try: 
        df_existente = pd.read_csv(csv_path, sep=";")
        df_unificado = pd.concat([df_existente, df_temp], axis=0, ignore_index=True)
    except:
        df_unificado = df_temp.copy()

    df_unificado.to_csv(csv_path, index=False, sep= ";")

    time.sleep(1.5)
    aba1(driver)
    time.sleep(0.05)

input("Pressione ENTER para fechar...")