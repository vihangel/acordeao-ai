from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# python src/save_html.py

# Caminhos
links_file = "data/raw/links_dispositivo_isto_posto.txt"
output_dir = "data/raw/html"
os.makedirs(output_dir, exist_ok=True)

# Configura navegador
options = Options()
options.add_argument("--window-size=1560,901")


driver = webdriver.Chrome(options=options)

# Lê os links
with open(links_file, "r") as f:
    links = [line.strip() for line in f if line.strip()]

print(f"🔗 {len(links)} links encontrados.")

# Abre nova aba para cada link, salva HTML e volta
original_window = driver.current_window_handle

for i, link in enumerate(links, 1):
    try:
        # Abre nova aba
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(link)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(translate(text(), "EMENTA", "ementa"), "ementa")]'))
        )

        # Salva HTML
        id_doc = link.strip().split("/")[-1]
        filename = os.path.join(output_dir, f"{id_doc}.html")
        with open(filename, "w", encoding="utf-8") as f_out:
            f_out.write(driver.page_source)

        print(f"✅ ({i}) salvo: {filename}")

        # Fecha aba e volta à original
        driver.close()
        driver.switch_to.window(original_window)

    except Exception as e:
        print(f"❌ Erro ao acessar {link}: {e}")
        driver.switch_to.window(original_window)

driver.quit()
print("✅ Fim do processo.")
