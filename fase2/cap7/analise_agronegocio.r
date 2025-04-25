# Análise exploratória de uma variável quantitativa (Num_Bovinos) e uma variável qualitativa (Regiao)

# Carregar pacotes
library(readxl)
library(ggplot2)

# 1. Carregar dados
df <- read_excel("Dados_Agronegocio.csv")

# 2. Medidas de Tendência Central para Num_Bovinos
media <- mean(df$Num_Bovinos)
mediana <- median(df$Num_Bovinos)
moda <- as.numeric(names(sort(table(df$Num_Bovinos), decreasing=TRUE)[1]))

# 3. Medidas de Dispersão
variancia <- var(df$Num_Bovinos)
desvio_padrao <- sd(df$Num_Bovinos)
coef_variacao <- desvio_padrao / media * 100

# 4. Medidas Separatrizes
quartis <- quantile(df$Num_Bovinos, probs = c(0.25, 0.5, 0.75))
percentis <- quantile(df$Num_Bovinos, probs = c(0.1, 0.9))

# 5. Análise Gráfica Quantitativa
hist(df$Num_Bovinos, main = "Histograma de Número de Bovinos",
     xlab = "Número de Bovinos")
boxplot(df$Num_Bovinos, main = "Boxplot de Número de Bovinos",
        ylab = "Número de Bovinos")

# 6. Análise Gráfica Qualitativa
ggplot(df, aes(x = Regiao)) +
  geom_bar(fill = "steelblue") +
  ggtitle("Contagem de Fazendas por Região") +
  xlab("Região") + ylab("Contagem")
