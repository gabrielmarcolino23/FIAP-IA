# Script de Análise Estatística para Dados Agrícolas
# Este script analisa os dados exportados pelo sistema Python

# Carrega as bibliotecas necessárias
library(tidyverse)
library(stats)

# Função para criar diretórios necessários
criar_diretorios <- function() {
  # Define os diretórios
  data_dir <- "fase1/cap1/data"
  graphs_dir <- file.path(data_dir, "graphs")
  
  # Cria os diretórios se não existirem
  dir.create(data_dir, showWarnings = FALSE)
  dir.create(graphs_dir, showWarnings = FALSE)
  
  return(graphs_dir)
}

# Função para ler o arquivo CSV mais recente
ler_dados_mais_recentes <- function() {
  # Define o diretório de dados
  data_dir <- "fase1/cap1/data"
  
  # Lista todos os arquivos CSV que começam com "dados_agricolas_"
  arquivos <- list.files(data_dir, pattern = "^dados_agricolas_.*\\.csv$", full.names = TRUE)
  
  if (length(arquivos) == 0) {
    stop("Nenhum arquivo de dados encontrado no diretório fase1/cap1/data!")
  }
  
  # Pega o arquivo mais recente
  arquivo_mais_recente <- arquivos[which.max(file.mtime(arquivos))]
  
  # Lê o arquivo CSV
  dados <- read.csv(arquivo_mais_recente, fileEncoding = "UTF-8")
  
  # Renomeia as colunas para evitar problemas com caracteres especiais
  colnames(dados) <- c("Cultura", "Area", "Numero_Ruas", "Comprimento_Rua", "Insumo", "Quantidade")
  
  return(dados)
}

# Função para calcular estatísticas
calcular_estatisticas <- function(dados) {
  # Estatísticas por cultura
  estatisticas_cultura <- dados %>%
    group_by(Cultura) %>%
    summarise(
      media_area = mean(as.numeric(Area)),
      sd_area = sd(as.numeric(Area)),
      media_ruas = mean(as.numeric(Numero_Ruas)),
      sd_ruas = sd(as.numeric(Numero_Ruas)),
      media_comprimento = mean(as.numeric(Comprimento_Rua)),
      sd_comprimento = sd(as.numeric(Comprimento_Rua))
    )
  
  # Estatísticas por insumo
  estatisticas_insumos <- dados %>%
    filter(Insumo != "") %>%
    group_by(Cultura, Insumo) %>%
    summarise(
      media_quantidade = mean(as.numeric(Quantidade)),
      sd_quantidade = sd(as.numeric(Quantidade))
    )
  
  return(list(
    cultura = estatisticas_cultura,
    insumos = estatisticas_insumos
  ))
}

# Tema personalizado para os gráficos
tema_farmtech <- function() {
  theme_minimal() +
    theme(
      plot.title = element_text(
        size = 16, 
        face = "bold",
        color = "#2C3E50",
        margin = margin(b = 20)
      ),
      plot.subtitle = element_text(
        size = 12,
        color = "#7F8C8D",
        margin = margin(b = 15)
      ),
      axis.title = element_text(
        size = 11,
        color = "#2C3E50",
        face = "bold"
      ),
      axis.text = element_text(
        size = 10,
        color = "#34495E"
      ),
      legend.title = element_text(
        size = 11,
        face = "bold",
        color = "#2C3E50"
      ),
      legend.text = element_text(
        size = 10,
        color = "#34495E"
      ),
      legend.position = "right",
      panel.grid.major = element_line(
        color = "#ECF0F1",
        size = 0.2
      ),
      panel.grid.minor = element_blank(),
      plot.margin = margin(20, 20, 20, 20)
    )
}

# Paleta de cores personalizada
cores_insumos <- c(
  "Fertilizante NPK" = "#3498DB",  # Azul
  "Fungicida" = "#2ECC71",         # Verde
  "Herbicida" = "#E74C3C",         # Vermelho
  "Inseticida" = "#F1C40F"         # Amarelo
)

# Função para gerar gráficos
gerar_graficos <- function(dados) {
  # Gráfico de área por cultura
  p1 <- ggplot(dados, aes(x = Cultura, y = as.numeric(Area))) +
    geom_boxplot(fill = "#3498DB", alpha = 0.7, color = "#2C3E50") +
    labs(
      title = "Distribuição de Área por Cultura",
      subtitle = "Análise da variação de área em diferentes culturas",
      y = "Área (m²)",
      x = "Tipo de Cultura"
    ) +
    tema_farmtech()
  
  # Gráfico de quantidade de insumos
  p2 <- dados %>%
    filter(Insumo != "") %>%
    ggplot(aes(x = Cultura, y = as.numeric(Quantidade), fill = Insumo)) +
    geom_bar(stat = "identity", position = position_dodge(width = 0.9), alpha = 0.8) +
    scale_fill_manual(values = cores_insumos) +
    labs(
      title = "Quantidade de Insumos por Cultura",
      subtitle = "Comparação do uso de diferentes insumos entre culturas",
      y = "Quantidade (L/m)",
      x = "Tipo de Cultura",
      fill = "Tipo de Insumo"
    ) +
    tema_farmtech()
  
  return(list(area = p1, insumos = p2))
}

# Função principal
main <- function() {
  tryCatch({
    # Cria diretórios necessários
    graphs_dir <- criar_diretorios()
    
    # Lê os dados
    cat("Lendo dados...\n")
    dados <- ler_dados_mais_recentes()
    
    # Calcula estatísticas
    cat("Calculando estatísticas...\n")
    estatisticas <- calcular_estatisticas(dados)
    
    # Mostra resultados
    cat("\nEstatísticas por Cultura:\n")
    print(estatisticas$cultura)
    
    cat("\nEstatísticas por Insumo:\n")
    print(estatisticas$insumos)
    
    # Gera e salva gráficos
    cat("\nGerando gráficos...\n")
    graficos <- gerar_graficos(dados)
    
    # Salva os gráficos com melhor resolução
    ggsave(
      file.path(graphs_dir, "area_por_cultura.png"),
      graficos$area,
      width = 10,
      height = 6,
      dpi = 300,
      bg = "white"
    )
    
    ggsave(
      file.path(graphs_dir, "quantidade_insumos.png"),
      graficos$insumos,
      width = 12,
      height = 7,
      dpi = 300,
      bg = "white"
    )
    
    cat("\nAnálise concluída com sucesso!\n")
    cat("Gráficos salvos no diretório:", graphs_dir, "\n")
    
  }, error = function(e) {
    cat("Erro durante a execução:", e$message, "\n")
  })
}

# Executa o programa
main() 