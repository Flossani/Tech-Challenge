# Tech-Challenge
Tech Challenge - fase 2

# Algoritmo Genético para Escalação Otimizada do Corinthians (2025)
Este projeto implementa um algoritmo genético para encontrar a melhor escalação possível do time do Corinthians em 2025, com base em estatísticas reais dos jogadores. O algoritmo considera diferentes formações táticas (4-3-3, 4-4-2, 3-5-2), calcula o fitness de cada jogador por posição e utiliza operadores genéticos como seleção por torneio, crossover posicional e mutação controlada para otimizar a escalação.

Além disso, o projeto conta com visualizações interativas e estatísticas em tempo real!

# Funcionalidades
- Leitura e limpeza automática dos dados do Excel.

- Geração de populações com formações táticas válidas.

- Avaliação de fitness baseada em estatísticas específicas por posição.

- Seleção por torneio para evitar convergência prematura.

- Crossover com preservação de posições e formações.

- Mutação seletiva por posição.

- Gráfico de evolução do fitness em tempo real.

- Visualização gráfica da escalação final com imagem de fundo de campo.

- Anotações com nomes, posições e cores diferenciadas por função.

#  Organização do Código
`Gerar_individuo`: Cria um time válido com base na formação escolhida.

`Avaliar_individuos`: Calcula o fitness de um time com base nas estatísticas dos jogadores.

`Selecionar_por_torneio`: Seleciona os melhores indivíduos para reprodução com um elemento de aleatoriedade.

`Crossover`: Gera filhos a partir de dois pais mantendo coerência posicional.

`Mutar`: Substitui aleatoriamente um jogador mantendo sua posição.

`exibir_escalacao_real`: Gera o gráfico com a escalação no campo com visual agradável.

`Algoritmo_genetico`: Função principal que executa todas as etapas por várias gerações.

# Visualizações
Gráfico de evolução do fitness: Plota em tempo real a melhora da população.

Escalação final: Cada jogador é plotado com uma cor conforme sua posição:

🟡 Goleiro: Amarelo

🔵 Defensores: Azul

🟢 Meios-campistas: Verde

🔴 Atacantes: Vermelho

# Exemplo de Execução

`python algoritmo_genetico_corinthians.py`

Durante a execução, você verá no console o progresso das gerações, seguido pela exibição gráfica do time com maior fitness encontrado.

# Requisitos
`Python 3.8+`

Bibliotecas:

`pandas`

`matplotlib`

`seaborn`

`openpyxl`

Instale os requisitos via:


`pip install pandas matplotlib seaborn openpyxl`

# Dados Utilizados
O projeto utiliza uma planilha `Corinthians_2025_dados.xlsx`, contendo estatísticas detalhadas dos jogadores como:

Minutos em campo

Gols, assistências

Interceptações, desarmes

Cartões

E outras métricas específicas por posição

Os dados são tratados automaticamente pelo script.

# Exemplos Visuais
### Evolução do Fitness
O gráfico se atualiza a cada geração.

### Escalação Gráfica Final
Visualização do time otimizado em campo.


# Oportunidades de Expansão
Simulação de partidas entre dois times gerados.

Geração de logs dos eventos da partida (ex: gols, cartões).

Adição de parâmetros personalizáveis (formações, pesos de estatísticas).

Exportação dos resultados para CSV/Excel ou HTML.

# Contribuição
Pull Requests são bem-vindos! Se você tiver ideias para melhorias, novas formações, operadores genéticos, ou melhorias visuais, sinta-se livre para contribuir.

# Licença
Este projeto está licenciado sob a MIT License.
