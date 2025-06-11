from bs4 import BeautifulSoup
import os
import json

# === Caminho do diretório com os HTMLs ===
html_dir = 'data/raw/html'
html_files = [f for f in os.listdir(html_dir) if f.endswith('.html')]
if not html_files:
    raise FileNotFoundError(f"Nenhum arquivo HTML encontrado em: {html_dir}")

# Dicionário final por arquivo
dados_por_arquivo = {}

# Processar todos os arquivos HTML
for html_file in html_files:
    html_path = os.path.join(html_dir, html_file)
    with open(html_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    secoes_dict = {}

    # Encontrar todos os blocos de título
    divs_titulo = soup.find_all("div", id=lambda x: x and "_titulo" in x)

    for div in divs_titulo:
        id_titulo = div.get("id")
        id_base = id_titulo.replace("_titulo_completo", "").replace("_titulo", "")
        titulo = div.get_text(separator=" ", strip=True)

        if not titulo:
            continue

        if id_base not in secoes_dict:
            secoes_dict[id_base] = {
                "id": id_titulo,
                "titulo": titulo,
                "conteudo": ""
            }
        else:
            secoes_dict[id_base]["id"] = id_titulo
            secoes_dict[id_base]["titulo"] = titulo

    # Associar conteúdo
    for id_base in list(secoes_dict.keys()):
        div_conteudo = soup.find("div", id=f"{id_base}_conteudo")
        if div_conteudo:
            conteudo = div_conteudo.get_text(separator=" ", strip=True)
            if conteudo:
                secoes_dict[id_base]["conteudo"] = conteudo
            else:
                del secoes_dict[id_base]  # remover se conteúdo vazio
        else:
            del secoes_dict[id_base]  # remover se conteúdo ausente

    # Adicionar ao resultado final, se houver seções válidas
    secoes = list(secoes_dict.values())
    if secoes:
        nome_base = os.path.splitext(html_file)[0]  # nome do arquivo sem .html
        dados_por_arquivo[nome_base] = secoes

# === Exportar JSON final ===
output_dir = 'data/raw/json'
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'secoes_por_arquivo.json')

with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(dados_por_arquivo, json_file, ensure_ascii=False, indent=4)

print(f"✅ JSON salvo em: {output_path}")
