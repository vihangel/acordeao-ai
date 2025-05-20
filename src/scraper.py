from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import time

# python src/scraper.py


# === Configurar pasta de download ===
download_dir = os.path.abspath("data/raw")
os.makedirs(download_dir, exist_ok=True)

prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}

# === Configurar navegador ===
options = Options()
options.add_argument("--window-size=1560,901")
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=options)

# === Acessar página ===
driver.get("https://pje.trt23.jus.br/jurisprudencia/")
time.sleep(5)

# === Fechar pop-up de cookies ===
fechar_btn = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, '//span[text()="FECHAR"]'))
)
fechar_btn.click()


# === 1. Digitar "isto posto" no campo de palavras-chave ===
campo_palavras = driver.find_element(By.ID, "filtrosE")
campo_palavras.clear()
campo_palavras.send_keys("isto posto")

# === 2. Desmarcar todos os checkboxes ===
label_todos_checkbox = driver.find_element(By.CSS_SELECTOR, 'label[for="mat-checkbox-2-input"]')
input_todos_checkbox = driver.find_element(By.ID, "mat-checkbox-2-input")

if input_todos_checkbox.get_attribute("aria-checked") == "true":
    label_todos_checkbox.click()

# === 3. Marcar apenas "Acórdão" ===
label_acordao_checkbox = driver.find_element(By.CSS_SELECTOR, 'label[for="mat-checkbox-3-input"]')
input_acordao_checkbox = driver.find_element(By.ID, "mat-checkbox-3-input")

if input_acordao_checkbox.get_attribute("aria-checked") == "false":
    label_acordao_checkbox.click()


# === 4. Preencher data de assinatura (campo início) ===
campo_data_inicio = driver.find_element(By.ID, "mat-input-5")
campo_data_inicio.clear()
campo_data_inicio.send_keys("01/01/2024")
campo_data_inicio.send_keys(Keys.TAB)

# === 5. Clicar no botão "Pesquisar" ===
btn_pesquisar = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//span[contains(., "Pesquisar")]'))
)
btn_pesquisar.click()
time.sleep(3)

# === Função para salvar todos os arquivos da página ===

def coletar_links_teor():
    base_url = "https://pje.trt23.jus.br"
    links = []

    elementos = driver.find_elements(By.XPATH, '//a[contains(@aria-label, "Inteiro teor")]')
    print(f"🔎 {len(elementos)} links de 'Inteiro Teor' encontrados.")

    for el in elementos:
        href = el.get_attribute("href")
        if href:
            full_url = href if href.startswith("http") else base_url + href
            links.append(full_url)
            print(f"🔗 {full_url}")

    return links


# === Função para verificar se há próxima página ===
def ha_proxima_pagina():
    try:
        botao = driver.find_element(By.XPATH, '//button[@aria-label="Próxima página" and not(@disabled)]')
        return botao
    except:
        return None


# === Loop de paginação ===
todos_links = []
pagina = 1

while True:
    print(f"\n📄 Página {pagina}")
    links = coletar_links_teor()
    todos_links.extend(links)

    # Salva links desta página individualmente
    with open(f"data/raw/links_pagina_{pagina}.txt", "w") as f:
        for link in links:
            f.write(link + "\n")

    botao_proximo = ha_proxima_pagina()
    if botao_proximo:
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", botao_proximo)
            ActionChains(driver).move_to_element(botao_proximo).pause(0.2).click(botao_proximo).perform()
            pagina += 1
            time.sleep(3)
        except Exception as e:
            print(f"⚠️ Erro ao tentar ir para a próxima página: {e}")
            break
    else:
        print("🚩 Última página alcançada.")
        break


# === Finaliza ===
driver.quit()
