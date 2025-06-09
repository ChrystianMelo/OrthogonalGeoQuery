# Trabalho Prático 1 - Geometria Computacional

**Universidade Federal de Minas Gerais**
**Instituto de Ciências Exatas - Departamento de Ciência da Computação**
**Disciplina: DCC207 - Algoritmos 2**
**Professor: Renato Vimieiro**

## Integrantes

* Christian Rodrigues
* Chrystian Melo

## Objetivo

Este projeto visa explorar a implementação prática de algoritmos de geometria computacional, especificamente árvores k-dimensionais para realizar buscas ortogonais em conjuntos de pontos georreferenciados.

O trabalho busca fixar conteúdos teóricos e demonstrar sua aplicabilidade em contextos práticos reais, permitindo aos alunos aprofundar o entendimento de estruturas complexas como as árvores k-dimensionais (k-d trees), além de utilizar bibliotecas avançadas para manipulação e visualização de dados geográficos.

## Descrição do Projeto

O sistema desenvolvido permite consultas interativas e ortogonais sobre estabelecimentos comerciais (bares e restaurantes) em Belo Horizonte. O usuário pode selecionar uma área retangular no mapa interativo, obtendo instantaneamente os estabelecimentos localizados nessa área, visualizados através de pinos no mapa e listados detalhadamente em uma tabela.

## Funcionalidades Principais

### Pré-processamento dos Dados

* Os dados originais da Prefeitura de Belo Horizonte são obtidos em formato CSV.
* Uma filtragem inicial é aplicada com base no código CNAE, mantendo apenas estabelecimentos com descrição associada a bares ou restaurantes.
* Os endereços são geocodificados utilizando a API OpenStreetMap (via `osmnx` e `geopy`), adicionando coordenadas geográficas (latitude e longitude).

### Estrutura de Dados

* Implementação de uma árvore k-dimensional (`k-d tree`) para armazenar as coordenadas geográficas e permitir buscas eficientes.
* O algoritmo de busca ortogonal permite recuperar rapidamente os estabelecimentos dentro de uma área retangular selecionada pelo usuário.

### Interface Interativa

* Desenvolvida usando `Dash` e `Dash-Leaflet` para interação e visualização.
* Permite desenhar retângulos no mapa, acionando automaticamente a busca ortogonal.
* Resultados exibidos dinamicamente na forma de pinos no mapa e detalhados em uma tabela interativa com informações como nome, endereço, alvará e início das atividades.

## Tecnologias Utilizadas

* **Python** para toda a implementação.
* **Dash** e **Dash-Leaflet** para a interface web interativa.
* **Pandas** para manipulação e pré-processamento dos dados.
* **Geopy e OSMnx** para geocodificação e interação com a API OpenStreetMap.
* **Matplotlib e Geopandas** para validação e visualização auxiliar dos dados.

## Otimizações Realizadas

* Implementação eficiente de buscas utilizando k-d trees reduzindo significativamente o tempo de consulta.
* Pré-processamento inteligente de endereços para minimizar chamadas à API de geocodificação, armazenando resultados intermediários.
* Interface leve e responsiva, com clustering de pontos para visualização mais clara e rápida no mapa.

## Estrutura do Projeto

```
.
├── data/                                # Diretório com dados CSV e GeoJSON processados
├── app.py                               # Código principal da interface interativa
├── main.py                              # Script para baixar e processar dados iniciais
├── filtrar_csv.py                       # Script para filtrar e formatar os dados CSV originais
├── utils.py                             # Funções utilitárias para geocodificação e árvore k-d
├── requirements.txt                     # Dependências necessárias para executar o projeto
└── README.md                            # Documentação completa do projeto
```

## Considerações Finais

Este projeto consolida conhecimentos práticos e teóricos sobre algoritmos geométricos, manejo eficiente de dados geográficos e desenvolvimento web interativo, destacando a importância da integração de técnicas computacionais avançadas em contextos reais.
