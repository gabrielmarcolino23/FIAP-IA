# Banco de Dados e CRUD em Python

Este diretório contém o script `banco.py` para simular o armazenamento dos dados dos sensores em um banco SQLite, conforme o MER da Fase 2.

## Estrutura da Tabela
- **fosforo**: Presença (1) ou ausência (0) de fósforo
- **potassio**: Presença (1) ou ausência (0) de potássio
- **ph**: Valor analógico do pH (simulado)
- **umidade**: Valor da umidade do solo
- **irrigacao**: Status da bomba (1=ligada, 0=desligada)

## Operações CRUD
- Inserir nova leitura
- Consultar todas as leituras
- Atualizar uma leitura
- Remover uma leitura

Veja exemplos de uso no final do arquivo `banco.py`.

## Dashboard de Visualização
Agora você pode visualizar os dados de forma interativa usando o dashboard em Streamlit!

### Como rodar o dashboard:
1. Instale as dependências (se necessário):
   ```bash
   pip install streamlit pandas altair
   ```
2. Execute o dashboard:
   ```bash
   streamlit run dashboard.py
   ```
3. Acesse o endereço exibido no terminal para visualizar os gráficos e tabelas.

O dashboard mostra gráficos de umidade, pH, nutrientes e status da bomba, facilitando a análise dos dados coletados.

## Relação com o MER
A tabela `leituras` representa as medições feitas pelo sistema, conforme modelagem da Fase 2.

## Dados de Exemplo
Veja o arquivo `dados_exemplo.sql` para exemplos de inserção de dados. 