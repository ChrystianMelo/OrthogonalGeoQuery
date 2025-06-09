# Trabalho Prático 1 - Geometria Computacional

**Universidade Federal de Minas Gerais**

**Instituto de Ciências Exatas - Departamento de Ciência da Computação**

**Disciplina: DCC207 - Algoritmos 2**

**Professor: Renato Vimieiro**

## Integrantes

* Christian Rodrigues
* Chrystian Melo

## Visão Geral do Projeto

Este projeto consiste em um sistema de visualização de dados geográficos que permite a consulta interativa de bares e restaurantes em Belo Horizonte. Utilizando uma base de dados pública da prefeitura, a aplicação processa, filtra e exibe os estabelecimentos em um mapa interativo. A funcionalidade central é a busca ortogonal (retangular) otimizada por uma **árvore k-dimensional (k-d tree)**, permitindo que o usuário selecione uma área no mapa e visualize, em tempo real, os pontos de interesse contidos naquela região e seus detalhes em uma tabela.

## Arquitetura e Fluxo de Dados

O projeto é dividido em duas etapas principais: um pipeline de pré-processamento de dados e a aplicação web interativa.

1. **Pré-processamento (`main.py` e `filtrar_csv.py`):**

   * **Coleta:** O script `main.py` baixa o conjunto de dados original da PBH.

   * **Filtragem:** O `filtrar_csv.py` é chamado para limpar os dados, mantendo apenas estabelecimentos cujo CNAE e descrição se relacionam com "bares" ou "restaurantes". Endereços são padronizados e formatados.

   * **Geocodificação:** A biblioteca `geopy` é utilizada em `utils.py` para converter os endereços formatados em coordenadas geográficas (latitude e longitude), lidando com limites de requisição da API Nominatim (OpenStreetMap).

   * **Geração de Artefatos:** O processo gera três arquivos principais na pasta `data/`: um CSV com os dados filtrados (`atividade_economica_filtrada.csv`), um CSV apenas com as coordenadas (`cordenadas_bares_restaurantes.csv`) e um arquivo final `bares_restaurantes.geojson`, que consolida todas as informações e é otimizado para ser consumido pela interface web.

2. **Aplicação Web (`app.py`):**

   * **Carregamento:** A aplicação Dash carrega o `bares_restaurantes.geojson`.

   * **Estrutura de Dados:** Uma árvore k-dimensional é construída em memória com as coordenadas de todos os estabelecimentos para otimizar as consultas espaciais.

   * **Interface:** Utilizando `Dash` e `Dash-Leaflet`, a aplicação renderiza um mapa com os pontos agrupados (clustering) e uma tabela com os detalhes.

   * **Interação:** O usuário pode desenhar um retângulo no mapa. As coordenadas desse retângulo são capturadas e usadas como entrada para o algoritmo de busca na k-d tree.

   * **Visualização:** Os resultados da busca (os estabelecimentos dentro do retângulo) são usados para atualizar o conteúdo da tabela de forma dinâmica.

## Detalhes Técnicos da Implementação

### Busca Ortogonal com k-d tree (`range_search`)

Para atender ao requisito de consulta em uma área retangular, a **árvore k-dimensional** foi a estrutura de dados escolhida. A principal vantagem de uma k-d tree sobre uma busca linear (que verificaria todos os pontos) é sua eficiência em podar grandes porções do espaço de busca. Para N pontos, uma busca em um conjunto de dados bem distribuído tem complexidade média próxima a **O(√N + k)**, onde k é o número de pontos reportados, em contraste com a complexidade **O(N)** da força bruta.

A nossa implementação, localizada em `utils.py`, segue o algoritmo canônico:

1. **Construção (`build_kd`):** A árvore é construída recursivamente. Em cada nível, os pontos são ordenados por uma dimensão (alternando entre longitude e latitude) e divididos pela mediana.

2. **Busca (`range_search`):** A função de busca recebe a raiz da árvore e um retângulo de busca (`bounding box`). Ela navega pela árvore e, em cada nó, decide se:

   * O ponto do nó atual está dentro do retângulo (e deve ser adicionado aos resultados).

   * A busca deve continuar na sub-árvore esquerda, direita, ou ambas. A busca só continua em uma sub-árvore se a região que ela representa intercepta o retângulo de busca. É essa verificação que permite a "poda" e garante a eficiência do algoritmo.

### Tecnologias e Deploy

* **Linguagem:** Python 3

* **Análise de Dados:** Pandas, GeoPandas, Shapely

* **Geocodificação:** Geopy, OSMnx

* **Interface Web:** Dash, Dash-Bootstrap-Components

* **Mapas:** Dash-Leaflet

* **Servidor de Produção:** Gunicorn

* **Hospedagem (Deploy):** A aplicação está publicada e rodando na plataforma **Render.com**, que se integra diretamente ao repositório do GitHub para deploy contínuo.

## Desafios e Decisões de Projeto

1. **Lentidão no Pré-processamento:** A etapa de geocodificação é o principal gargalo. Cada endereço exige uma chamada de API à Nominatim, que impõe um limite de 1 requisição por segundo. Para processar milhares de endereços, isso levaria muito tempo. A solução foi implementar um **pipeline de dados desacoplado (`main.py`)**, que gera os arquivos processados uma única vez. A aplicação web (`app.py`) apenas consome o resultado final (`.geojson`), garantindo um carregamento rápido para o usuário.

2. **Performance do Mapa:** Renderizar milhares de marcadores individuais em um mapa Leaflet trava o navegador. Para resolver isso, utilizamos a funcionalidade de **clustering do lado do cliente** (`superClusterOptions` no `dl.GeoJSON`). Os pontos próximos são agrupados em um único círculo, e apenas os marcadores na área visível são renderizados, garantindo uma experiência de navegação fluida.


## Estrutura do Projeto

```
.
├── data/
│   ├── atividade_economica_filtrada.csv
│   ├── bares_restaurantes.geojson
│   └── cordenadas_bares_restaurantes.csv
├── app.py              # Código principal da interface interativa
├── main.py             # Script para baixar e processar dados iniciais
├── filtrar_csv.py      # Script para filtrar e formatar os dados CSV originais
├── utils.py            # Funções utilitárias para geocodificação e árvore k-d
├── requirements.txt    # Dependências necessárias para executar o projeto
├── setup.sh/setup.bat  # Scripts para configurar o ambiente
├── run.sh/run.bat      # Scripts para executar a aplicação
└── README.md           # Documentação completa do projeto
```

## Como Executar Localmente

Siga os passos abaixo para configurar e executar o projeto em sua máquina local.

### Para Linux (ou Windows com WSL)

1. **Configurar o ambiente (apenas uma vez):**

   * No terminal, dê permissão de execução aos scripts: `chmod +x setup.sh run.sh`

   * Execute o script de setup: `./setup.sh`

2. **Executar a aplicação:**

   * A cada vez que for rodar o projeto, execute: `./run.sh`

### Para Windows

1. **Configurar o ambiente (apenas uma vez):**

   * Dê um duplo clique no arquivo `setup.bat`.

2. **Executar a aplicação:**

   * A cada vez que for rodar o projeto, dê um duplo clique em `run.bat`.

## Deploy (Publicação Online)

A aplicação foi publicada utilizando o serviço **Render.com** e está disponível publicamente no seguinte endereço:

[**https://tp01-alg02-20251.onrender.com/**](https://tp01-alg02-20251.onrender.com/)
