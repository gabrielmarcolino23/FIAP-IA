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
5. Sair do programa

## Estrutura do Projeto

### Classes Principais
- `Cultura`: Representa uma cultura agrícola
  - Atributos: nome, área, número de ruas, comprimento da rua
  - Lista de insumos com nome e quantidade
- `SistemaAgricola`: Gerencia todas as operações
  - Lista de culturas
  - Cálculos de área
  - Operações CRUD (Criar, Ler, Atualizar, Deletar)

## Como Executar

1. Certifique-se de ter Python 3.6 ou superior instalado
2. Execute o arquivo `farmtech_solutions.py`:
   ```bash
   python fase1/cap1/farmtech_solutions.py
   ```
3. Siga as instruções do menu interativo

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

## Requisitos
- Python 3.6 ou superior
- Módulos padrão do Python (math, typing) 