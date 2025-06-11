<!-- @format -->

# Agrupamento de Acórdãos com BERTopic

Este repositório contém os experimentos realizados cujo objetivo é investigar a modelagem de tópicos em acórdãos trabalhistas utilizando o algoritmo BERTopic e embeddings jurídicos.

## Objetivo

O notebook `Agrupamento de acórdãos com BERTopic.ipynb` implementa um pipeline completo para:

- Pré-processamento de acórdãos trabalhistas;
- Extração de embeddings com modelos baseados em BERT (LegalBERT-pt);
- Modelagem de tópicos com o algoritmo BERTopic;
- Avaliação da coerência temática (coerência c_v);
- Análise do balanceamento entre os tópicos com base na proporção de documentos;
- Cálculo de métrica composta (score balanceado).

## Estrutura

```
├── Agrupamento de acórdãos com BERTopic.ipynb  # Notebook principal
├── content/acordaos/                           # Acórdãos trabalhistas em .html
├── stopword_extras.txt                         # Stopwords customizadas
```

> Os arquivos de entrada (`.html`) foram coletados do site do TRT-23.

## Requisitos

Instale os pacotes necessários com:

```bash
pip install -r requirements.txt
```

Pacotes principais:

- `bertopic`
- `sentence-transformers`
- `umap-learn`
- `nltk`
- `pandas`, `matplotlib`, `seaborn`
- `gensim`

## ▶️ Execução

1. Coloque os arquivos `.html` dos acórdãos no diretório `content/acordaos/`.
2. Abra o notebook:  
   `Agrupamento de acórdãos com BERTopic.ipynb`
3. Execute célula por célula para reproduzir o pipeline completo.

## Métricas

Além da coerência temática (c_v), foi proposto um **score balanceado**:

```
Diversidade = 1 − (Qtd. documentos no maior tópico / Qtd. total de documentos)
Score balanceado = Coerência_c_v × Diversidade
```

Essa métrica permite avaliar modelos que sejam semanticamente coerentes e distributivamente equilibrados.

## Licença

Este projeto está licenciado sob a licença MIT. Sinta-se à vontade para usar, modificar e citar este repositório, especialmente para fins acadêmicos.

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

### 1. Coletar Links

Execute o script `scraper.py` para buscar os links de "Inteiro Teor" no site do TRT23:

```bash
python src/scraper.py
```

Os links serão salvos no arquivo `data/raw/links_dispositivo_<filtro>.txt`.

### 2. Salvar HTMLs

Com os links coletados, execute o script `save_html.py` para salvar o conteúdo HTML de cada página:

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
