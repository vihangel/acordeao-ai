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
try:
    fechar_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//span[text()="FECHAR"]'))
    )
    fechar_btn.click()
except:
    print("⚠️ Pop-up 'FECHAR' não encontrado. Continuando...")

# === Preencher campo "Palavras no dispositivo (e)" ===
filtro = '"isto posto"'
campo_dispositivo = driver.find_element(By.ID, "filtrosEDispositivo")
campo_dispositivo.clear()
campo_dispositivo.send_keys(filtro)

# === Desmarcar checkbox "Todos" ===
label_todos_checkbox = driver.find_element(By.CSS_SELECTOR, 'label[for="mat-checkbox-2-input"]')
input_todos_checkbox = driver.find_element(By.ID, "mat-checkbox-2-input")

if input_todos_checkbox.get_attribute("aria-checked") == "true":
    label_todos_checkbox.click()

# === Marcar apenas "Acórdão" ===
label_acordao_checkbox = driver.find_element(By.CSS_SELECTOR, 'label[for="mat-checkbox-3-input"]')
input_acordao_checkbox = driver.find_element(By.ID, "mat-checkbox-3-input")

if input_acordao_checkbox.get_attribute("aria-checked") == "false":
    label_acordao_checkbox.click()

# === Clicar em "Pesquisar" ===
btn_pesquisar = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//span[contains(., "Pesquisar")]'))
)
btn_pesquisar.click()
time.sleep(3)

# === Coletar os links "Inteiro Teor" ===
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

# === Verificar se há próxima página ===
def ha_proxima_pagina():
    try:
        botao = driver.find_element(By.XPATH, '//button[@aria-label="Próxima página" and not(@disabled)]')
        return botao
    except:
        return None

# === Loop por todas as páginas e salvar tudo em um único arquivo ===
arquivo_saida = os.path.join(download_dir, f"links_dispositivo_{filtro.replace(' ', '_')}.txt")
pagina = 1
with open(arquivo_saida, "w") as f:
    while True:
        print(f"\n📄 Página {pagina}")
        links = coletar_links_teor()

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

print(f"\n✅ Todos os links foram salvos em: {arquivo_saida}")
driver.quit()
