# Sistema de Sensores e Controle com ESP32

Bem-vindo à implementação do sistema de sensores e controle para irrigação inteligente! Aqui você encontra o código para simular o funcionamento do projeto usando ESP32, conforme proposto na Fase 3 do desafio.

## O que você vai encontrar aqui?
- Código comentado em C++ para ESP32
- Explicação dos sensores simulados e da lógica de irrigação
- Instruções simples para rodar e testar o sistema

## Componentes Simulados
- **Botão 1:** Fósforo (P)
- **Botão 2:** Potássio (K)
- **LDR:** pH (valor analógico)
- **DHT22:** Umidade do solo
- **Relé:** Bomba d'água
- **LED:** Status da bomba

## Como funciona a irrigação?
A lógica é simples e pode ser adaptada conforme sua criatividade! No exemplo, a bomba de irrigação é ativada quando:
- A umidade do solo está abaixo de 60%
- Há presença de fósforo e potássio
- O valor do pH (simulado pelo LDR) está acima de um valor mínimo

Você pode ajustar esses critérios no código para experimentar diferentes estratégias de irrigação.

## Como testar?
1. Monte o circuito no Wokwi (ou apenas simule os sensores conforme descrito acima).
2. Compile e envie o código para o ESP32 usando PlatformIO.
3. Acompanhe as leituras e o status da irrigação pelo monitor serial.

 