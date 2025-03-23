# FarmTech Solutions - Sistema de Gestão Agrícola

Este projeto foi desenvolvido para a FarmTech Solutions, uma empresa especializada em soluções tecnológicas para agricultura. O sistema gerencia dados de culturas agrícolas, permitindo o controle de áreas plantadas e insumos utilizados.

## Funcionalidades

### Gerenciamento de Culturas
- Suporte a duas culturas específicas:
  - Café
  - Soja
- Cálculo de área de plantio com três opções:
  - Retangular (largura × comprimento)
  - Circular (π × raio²)
  - Hexagonal (3√3/2 × lado²)
- Controle de ruas e comprimento de plantio

### Gerenciamento de Insumos
- Na entrada de dados:
  - Adição simples de insumos
  - Registro de quantidade por metro
- Na atualização:
  - Adição de novos insumos
  - Edição de insumos existentes
  - Remoção de insumos
  - Visualização detalhada

### Sistema de Menu
O sistema oferece um menu interativo com as seguintes opções:
1. Entrada de dados
   - Cadastro de nova cultura
   - Cálculo de área
   - Registro de insumos básico
2. Saída de dados
   - Listagem completa de culturas
   - Detalhes de área e insumos
3. Atualização de dados
   - Modificação de dados da cultura
   - Gerenciamento completo de insumos
4. Deletar dados
   - Remoção de culturas
5. Exportar dados para análise estatística
   - Gera arquivo CSV com dados formatados
6. Sair do programa

### Análise Estatística (R)
O sistema inclui um script R (`analise_estatistica.R`) que realiza análises estatísticas dos dados exportados:

#### Estatísticas Calculadas
- Por Cultura:
  - Média e desvio padrão da área
  - Média e desvio padrão do número de ruas
  - Média e desvio padrão do comprimento das ruas
- Por Insumo:
  - Média e desvio padrão das quantidades

#### Gráficos Gerados
1. `area_por_cultura.png`: Boxplot mostrando a distribuição de área por cultura
2. `quantidade_insumos.png`: Gráfico de barras mostrando quantidade de insumos por cultura

## Estrutura do Projeto

### Diretórios
- `fase1/cap1/data/`: Diretório onde são armazenados os arquivos CSV exportados
- `fase1/cap1/`: Diretório principal do projeto
  - `farmtech_solutions.py`: Sistema principal em Python
  - `analise_estatistica.R`: Script de análise estatística em R
  - `gerar_dados_teste.py`: Script para gerar dados de teste
  - `README.md`: Documentação do projeto

### Classes Principais
- `Cultura`: Representa uma cultura agrícola
  - Atributos: nome, área, número de ruas, comprimento da rua
  - Lista de insumos com nome e quantidade
- `SistemaAgricola`: Gerencia todas as operações
  - Lista de culturas
  - Cálculos de área
  - Operações CRUD (Criar, Ler, Atualizar, Deletar)
  - Exportação de dados para CSV

## Como Executar

### Sistema Python
1. Certifique-se de ter Python 3.6 ou superior instalado
2. Execute o arquivo `farmtech_solutions.py`:
   ```bash
   python fase1/cap1/farmtech_solutions.py
   ```
3. Siga as instruções do menu interativo

### Análise Estatística (R)
1. Certifique-se de ter R instalado
2. Instale as bibliotecas necessárias:
   ```R
   install.packages(c("tidyverse", "stats"))
   ```
3. Exporte os dados do sistema Python (opção 5 do menu)
4. Execute o script R:
   ```bash
   Rscript fase1/cap1/analise_estatistica.R
   ```

## Exemplo de Uso

### Cadastro de Nova Cultura
1. Selecione a opção 1 (Entrada de dados)
2. Escolha o tipo de cultura (1 para Café ou 2 para Soja)
3. Selecione o tipo de área (1-3)
4. Informe as dimensões conforme o tipo escolhido
5. Adicione insumos básicos (opcional)

### Atualização de Cultura
1. Selecione a opção 3 (Atualizar dados)
2. Escolha a cultura a ser atualizada
3. Modifique os dados necessários
4. Use o gerenciador de insumos para:
   - Adicionar novos insumos
   - Editar insumos existentes
   - Remover insumos

### Análise Estatística
1. Use a opção 5 do menu Python para exportar os dados (serão salvos em `fase1/cap1/data/`)
2. Execute o script R para gerar as análises
3. Verifique os resultados no terminal e os gráficos gerados

## Requisitos
- Python 3.6 ou superior
- R (para análise estatística)
- Módulos Python: math, typing, csv, datetime
- Pacotes R: tidyverse, stats

### Geração de Dados de Teste
O sistema inclui um script (`gerar_dados_teste.py`) para gerar dados de teste automaticamente:

1. Execute o script:
   ```bash
   python fase1/cap1/gerar_dados_teste.py
   ```

2. O script irá gerar:
   - 10 culturas aleatórias (Café e Soja)
   - Áreas entre 100 e 10000 m²
   - 5 a 50 ruas por cultura
   - Comprimento de ruas entre 10 e 100 m
   - 2 a 4 insumos aleatórios por cultura com quantidades realistas

3. Os dados serão exportados automaticamente para um arquivo CSV no diretório `fase1/cap1/data/` 