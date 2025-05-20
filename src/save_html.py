from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time

# python src/save_html.py

# Caminhos
links_file = "data/raw/links_dispositivo_isto_posto.txt"
output_dir = "data/raw/html"
os.makedirs(output_dir, exist_ok=True)

# Configura navegador
options = Options()
options.add_argument("--window-size=1560,901")
# options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

# Lê os links
with open(links_file, "r") as f:
    links = [line.strip() for line in f if line.strip()]

# Verifica quais arquivos já existem
arquivos_existentes = set(os.listdir(output_dir))
ids_existentes = {arquivo.replace(".html", "") for arquivo in arquivos_existentes}

# Filtra links restantes
links_faltando = [link for link in links if link.strip().split("/")[-1] not in ids_existentes]
print(f"🔗 Total de links: {len(links)} | Já salvos: {len(ids_existentes)} | Faltando: {len(links_faltando)}")

# Aba original
original_window = driver.current_window_handle

# Processa somente os que ainda não foram salvos
for i, link in enumerate(links_faltando, 1):
    try:
        id_doc = link.strip().split("/")[-1]
        print(f"➡️ Acessando {id_doc} ({i}/{len(links_faltando)})")

        # Abre nova aba
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(link)

        # Espera carregar conteúdo relevante
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(translate(text(), "Isto posto", "Isto posto"), "Isto posto")]'))
        )

        # Salva HTML
        filename = os.path.join(output_dir, f"{id_doc}.html")
        with open(filename, "w", encoding="utf-8") as f_out:
            f_out.write(driver.page_source)

        print(f"✅ Salvo: {filename}")

        # Fecha aba e volta
        driver.close()
        driver.switch_to.window(original_window)

    except Exception as e:
        print(f"❌ Erro ao acessar {link}: {e}")
        driver.switch_to.window(original_window)

driver.quit()
print("🏁 Fim do processo.")
