<!-- @format -->

# Acordeão Scrapper

Este projeto utiliza **Selenium** para automatizar a coleta de dados de jurisprudência no site do TRT23 e salvar os resultados em arquivos HTML. Ele é dividido em dois scripts principais:

1. **`scraper.py`**: Realiza a busca no site, coleta os links de "Inteiro Teor" e salva em um arquivo de texto.
2. **`save_html.py`**: Lê os links coletados e salva o conteúdo HTML de cada página.

## Estrutura do Projeto

```
acordeao-ai/
├── data/
│   └── raw/                # Diretório onde os dados coletados serão salvos
├── src/
│   ├── scraper.py          # Script para coletar links
│   ├── save_html.py        # Script para salvar HTMLs
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação do projeto
```

## Pré-requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- [ChromeDriver](https://chromedriver.chromium.org/downloads) compatível com sua versão do Chrome

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/acordeao-ai.git
   cd acordeao-ai
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

## Como Rodar

Antes de executar os scripts, instale as dependências:

```bash
pip install -r requirements.txt
```

### 1. Coletar Links

Execute o script `scraper.py` para buscar os links de "Inteiro Teor" no site do TRT23:

**No Linux/Mac:**

```bash
python3 src/scraper.py
```

**No Windows:**

```bash
python src/scraper.py
```

Os links serão salvos no arquivo `data/raw/links_dispositivo_<filtro>.txt`.

### 2. Salvar HTMLs

Com os links coletados, execute o script `save_html.py` para salvar o conteúdo HTML de cada página:

**No Linux/Mac:**

```bash
python3 src/save_html.py
```

**No Windows:**

```bash
python src/save_html.py
```

Os arquivos HTML serão salvos no diretório `data/raw/html`.

## Observações

- Certifique-se de que o ChromeDriver está no PATH ou no mesmo diretório do projeto.
- Caso o site do TRT23 mude, os seletores utilizados no Selenium podem precisar de ajustes.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
