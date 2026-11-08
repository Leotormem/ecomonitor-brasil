# Escolha do Modelo LLM — EcoMonitor Brasil

## Tarefa escolhida

A tarefa definida para o TP4 é a classificação temática de textos ambientais.

O modelo deverá receber um texto ambiental e classificá-lo em uma das seguintes categorias:

- queimada;
- desmatamento;
- clima;
- biodiversidade;
- poluição;
- monitoramento ambiental.

## Critérios de avaliação

Os modelos serão avaliados considerando:

- desempenho no banco de provas do próprio projeto;
- tempo médio de processamento;
- consumo aproximado de memória;
- compatibilidade com execução local;
- facilidade de download e uso offline;
- licença e acessibilidade.

## Banco de provas

O banco de provas está localizado em:

`data/analisador/banco_de_provas.csv`

Ele contém 30 exemplos rotulados manualmente, distribuídos igualmente entre as seis categorias.

Os rótulos foram definidos antes da execução dos modelos para reduzir viés durante a avaliação.

## Modelo escolhido

A definição do modelo será realizada após os testes comparativos.

## Plano B

Também será registrado um modelo alternativo caso o modelo principal apresente custo computacional elevado ou incompatibilidade com o ambiente local.

## Primeiro modelo avaliado

### mDeBERTa multilingual zero-shot

Modelo:

`MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`

Tipo de tarefa:

Classificação zero-shot de textos ambientais.

Resultados no banco de provas do EcoMonitor Brasil:

- exemplos avaliados: 30;
- acertos: 24;
- erros: 6;
- acurácia: 80,00%;
- tempo médio por texto: 3,58 segundos;
- tempo de carregamento: 4,01 segundos.

O resultado foi considerado positivo, pois o modelo conseguiu classificar corretamente a maior parte dos textos ambientais sem treinamento adicional específico para o projeto.

O modelo será comparado com outras alternativas antes da escolha final.

## Segundo modelo avaliado

### Qwen2.5-1.5B-Instruct

Modelo:

`Qwen/Qwen2.5-1.5B-Instruct`

Tipo de tarefa:

Geração de texto utilizada para classificação temática através de prompt.

Resultados no banco de provas do EcoMonitor Brasil:

- exemplos avaliados: 30;
- acertos: 12;
- erros: 18;
- respostas sem categoria válida: 2;
- acurácia: 40,00%;
- tempo médio por texto: 6,39 segundos;
- tempo de carregamento: 5,58 segundos.

O modelo conseguiu executar a tarefa localmente, porém apresentou desempenho inferior ao mDeBERTa no banco de provas do projeto.

Além disso, por ser um modelo gerador, em alguns casos produziu texto adicional mesmo quando solicitado que retornasse apenas o nome da categoria.

Esse comportamento exigiria tratamento adicional da resposta antes de sua utilização pela API.

## Comparação parcial

| Modelo | Acertos | Acurácia | Tempo médio | Carregamento |
|---|---:|---:|---:|---:|
| mDeBERTa multilingual zero-shot | 24/30 | 80,00% | 3,58 s | 4,01 s |
| Qwen2.5-1.5B-Instruct | 12/30 | 40,00% | 6,39 s | 5,58 s |

Até este momento, o mDeBERTa apresenta melhor desempenho e menor tempo médio de processamento para a tarefa escolhida.

## Custo computacional do mDeBERTa

O modelo mDeBERTa avaliado possui aproximadamente:

- 278.811.651 parâmetros;
- 531,79 MB de memória para armazenamento dos parâmetros;
- aproximadamente 0,52 GB.

A medição foi realizada localmente utilizando o tamanho dos parâmetros carregados pelo PyTorch.

Além do consumo de memória, também foram observados:

- tempo médio de processamento: 3,58 segundos por texto;
- tempo de carregamento: 4,01 segundos.

Considerando o desempenho de 80,00% no banco de provas e o consumo aproximado de 0,52 GB, o modelo apresenta uma relação adequada entre desempenho e custo computacional para execução local no projeto.

## Modelo escolhido

Após os testes comparativos, o modelo escolhido para o TP4 foi:

`MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`

### Justificativa da escolha

A escolha foi baseada nos três critérios principais exigidos pelo TP4:

#### Desempenho

No banco de provas do EcoMonitor Brasil, com 30 exemplos rotulados manualmente, o mDeBERTa apresentou:

- 24 acertos;
- 6 erros;
- 80,00% de acurácia.

O Qwen2.5-1.5B-Instruct, utilizado como alternativa de comparação, apresentou:

- 12 acertos;
- 18 erros;
- 2 respostas sem categoria válida;
- 40,00% de acurácia.

O mDeBERTa apresentou desempenho significativamente superior para a tarefa de classificação temática escolhida.

#### Custo computacional local

O mDeBERTa apresentou:

- aproximadamente 278,8 milhões de parâmetros;
- aproximadamente 531,79 MB de memória para os parâmetros;
- cerca de 0,52 GB;
- tempo médio de 3,58 segundos por texto;
- tempo de carregamento de 4,01 segundos.

Esses resultados indicam que o modelo possui custo computacional compatível com execução local no ambiente utilizado durante o desenvolvimento.

#### Acessibilidade local

O modelo pode ser carregado através da biblioteca Transformers da Hugging Face e executado localmente após o download.

Isso permite que a aplicação realize a classificação sem depender de uma API externa de IA durante a inferência.

### Decisão final

O mDeBERTa foi escolhido por apresentar a melhor relação entre:

- desempenho;
- tempo de processamento;
- consumo de memória;
- facilidade de integração com Transformers;
- execução local.

## Plano B

O modelo alternativo avaliado foi:

`Qwen/Qwen2.5-1.5B-Instruct`

Apesar de possuir capacidade de geração de texto, ele apresentou menor desempenho no banco de provas e maior tempo médio de processamento para a tarefa de classificação temática.

Por esse motivo, ele não foi escolhido como modelo principal do TP4.