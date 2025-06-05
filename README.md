UNIVERSIDADE FEDERAL DE MINAS GERAIS

Instituto de Ciências Exatas -- Departamento de Ciência da Computação

DCC207 -- Algoritmos 2 -- Prof. Renato Vimieiro

<h1>Trabalho Prático 1 – Geometria Computacional</h1>
<b>Alunos:</b> Christian Rodrigues e Chrystian Melo
<h2>Objetivos</h2>
Nesse trabalho, serão abordados os aspectos práticos dos algoritmos de geometria
computacional. Especificamente, serão explorados aspectos de implementação de
árvores k-dimensionais para realização de busca ortogonal em conjuntos de pontos.

O objetivo secundário é fixar o conteúdo e mostra sua aplicabilidade em contextos
práticos mais realistas. Entende-se que ao implementar a estrutura o aluno conseguirá
compreender melhor os conceitos explorados. Dessa forma, o conteúdo teórico será
melhor absorvido e fixado. Além disso, os alunos terão a oportunidade de ver
conceitos não abordados na disciplina, no caso específico, bibliotecas para
manipulação e plotagem de mapas e dados geográficos.

<h2>Tarefas</h2>
Os alunos deverão implementar um sistema para consulta ortogonal de
estabelecimento comerciais dentro de uma área retangular à escolha do usuário a
partir de um mapa interativo. Especificamente, os alunos deverão criar um sistema
interativo para visualizar os bares e restaurantes registrados na base de dados da
Prefeitura de Belo Horizonte (PBH). O sistema deve exibir os estabelecimentos
comerciais como pinos de localização no mapa da cidade. Informações
complementares dos estabelecimentos também deverão ser exibidas em uma tabela
abaixo do mapa. Além disso, o sistema deverá permitir aos usuários filtrar os
estabelecimentos que queiram exibir informações na tabela através de uma
ferramenta de seleção retangular no mapa. Essa consulta deverá ser feita com o
suporte de uma árvore k-dimensional usando as coordenadas geográficas (longitude,
latitude) como dimensões da árvore.

Os alunos devem implementar as funcionalidades para exibir e interação com os
mapas, toda a estrutura da árvore k-dimensional, e o algoritmo de busca ortogonal. A
implementação deverá ser feita obrigatoriamente em Python. O sistema deverá ser
efetivamente interativo. O produto final deverá ser uma página interativa que permite
a visualização dos dados, filtragem e eventuais resets dos filtros. As páginas serão
hospedadas no Github Pages.

Os dados para realização do trabalho estão disponíveis em
https://dados.pbh.gov.br/dataset/atividades-economicas1. A prefeitura disponibiliza
os dados em formato CSV atualizados (quase) mensalmente. Dessa forma, para fixar
um conjunto de dados, usaremos os dados disponibilizados em 2025-04-01. Uma
descrição dos atributos desses dados está disponível no link.

Um ponto de atenção em relação aos dados é que eles contêm estabelecimentos de
diferentes atividades econômicas. Dessa forma, será necessário realizar um préprocessamento
para manter somente aqueles referentes a bares e restaurantes. O
filtro deverá ser feito sobre a descrição da CNAE principal. Deverão ser mantidos todos
os estabelecimentos que tenham qualquer um dos termos em sua descrição.

A segunda observação a se fazer diz respeito à localização geográfica dos
estabelecimentos. A base de dados acima apresenta apenas o endereço através da
composição do tipo de logradouro, nome, número, complemento e bairro. Os alunos
deverão fazer a conversão desses para coordenadas geográficas. Para isso, poderão
ser usadas ferramentas e bibliotecas que acessem a API do OpenStreetMaps. As
coordenadas deverão ser incluídas nos dados originais.

Após a filtragem e obtenção das coordenadas, deverão ser mantidos apenas os
seguintes atributos para exibição na tabela mencionada anteriormente: a data de
início das atividades, se a empresa possui alvará de funcionamento, o endereço
(formatado) e o nome (ou nome fantasia).
A construção do mapa interativo será feita com o auxílio da biblioteca dash-leaflet.
Essa biblioteca possibilita o uso dos recursos de duas outras bibliotecas: Plotly|Dash e
Leaflet. Para plotar o mapa de Belo Horizonte, pode ser necessário recuperar as
coordenadas a partir do site da PBH, em particular, caso queira mostrar o contorno
dos bairros. Veja uma discussão sobre isso em https://medium.com/starschemablog/
draw-a-map-of-the-districts-of-budapest-using-the-overpass-api-ofopenstreetmap-
and-python-bd0417469935 e
https://forum.jornalismodedados.org/t/geojson-nao-funciona-no-folium-python/467.
Um exemplo de sincronização entre o mapa e a tabela pode ser visto na galeria de
exemplos do Plotly.

Como atividade extra (valendo pontos adicionais), você poderá cruzar os dados dos
estabelecimentos do portal da PBH com aqueles participantes do festival Comida di
Buteco. Nesse caso, você deverá implementar uma funcionalidade extra (hover) que,
ao passar o mouse sobre um bar participante, serão exibidas informações sobre o
prato concorrente em 2025 desse estabelecimento. A avaliação dos pontos extras será
feita com base na completude e qualidade dessa funcionalidade adicional.

Finalmente, os alunos deverão preparar um relatório final em que descrevem
textualmente sua implementação bem como o problema abordado no trabalho.
Deverão ser descritos todos os passos da implementação, descrevendo as decisões
tomadas e a exibição de exemplos ilustrando o resultado ou mecanismo
implementado. Também deverão ser dados exemplos de funcionamento do sistema. O
nível de elaboração do texto e qualidade das descrições serão critérios de avaliação.
Em outras palavras, o mesmo cuidado com a implementação deverá ser observado no
relatório produzido. O relatório deverá ser publicado junto com o código em
repositório aberto no GitHub.

O trabalho poderá ser feito em grupos de até três alunos. Recomenda-se fortemente
que o trabalho seja realizado em grupo.

O uso de qualquer biblioteca adicional ou código de terceiros deverá ser discutido com
o professor.

<h2>O que entregar?</h2>
Deverá ser entregue um repositório no GitHub contendo todos os arquivos criados na
implementação da ferramenta. O link para o repositório deverá ser postado no
Moodle. O repositório deverá ser mantido privado até 3 dias após a data de entrega.
Então, o repositório deverá ser tornado público. Caso o repositório não esteja aberto
ou o link postado não funcione a partir do 4º dia após a data de entrega, o trabalho
será considerado não entregue e receberá nota nula.

<h2>Política de Plágio</h2>
Os alunos podem, e devem, discutir soluções sempre que necessário. Dito isso,
há uma diferença bem grande entre implementação de soluções similares e cópia
integral de ideias. Trabalhos copiados na íntegra ou em partes de outros alunos
e/ou da internet serão prontamente anulados. Caso haja dois trabalhos copiados
por alunos/grupos diferentes, ambos serão anulados.

<h2>Datas</h2>
<b>Entrega: 08/06/2025 às 23h59</b>

<h2>Política de atraso</h2>
Haverá tolerância de 30min na entrega dos trabalhos. Submissões feitas depois
do intervalo de tolerância serão penalizados, incluindo mudanças no repositório.

• Atraso de 1 dia: 30%

• Atraso de 2 dias: 50%

• Atraso de 3+ dias: não aceito

Serão considerados atrasos de 1 dia aqueles feitos após as 0h30 do dia seguinte à
entrega (sexta-feira). A partir daí serão contados o número de dias passados da data
de entrega.