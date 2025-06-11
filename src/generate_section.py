from bs4 import BeautifulSoup
import json
import os

# Caminho do diretório com os HTMLs
html_dir = 'data/raw/html'
html_files = [f for f in os.listdir(html_dir) if f.endswith('.html')]
if not html_files:
    raise FileNotFoundError(f"Nenhum arquivo HTML encontrado em: {html_dir}")

# Abrir o primeiro HTML (você pode adaptar depois para processar todos)
html_path = os.path.join(html_dir, html_files[0])
with open(html_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parsear o HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Coletar os títulos das seções
titulos_info = []

# Encontrar todos os blocos com ID terminando em "_titulo_completo"
titulo_completo_divs = soup.find_all("div", id=lambda x: x and x.endswith("_titulo_completo"))

for div in titulo_completo_divs:
    id_original = div.get("id", None)
    titulo_texto = div.get_text(separator=" ", strip=True)
    
    # Apenas incluir se o título não estiver vazio
   
    titulos_info.append({
        "id": id_original,
        "titulo": titulo_texto
    })

# Exportar para JSON
json_output = json.dumps(titulos_info, ensure_ascii=False, indent=4)
output_dir = 'data/raw/json'
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'titulos.json')

with open(output_path, 'w', encoding='utf-8') as json_file:
    json_file.write(json_output)

print(f"✅ Títulos salvos em: {output_path}")
