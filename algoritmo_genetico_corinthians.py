import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Carregar e padronizar os dados
df = pd.read_excel('arquivos\Corinthians_2025_dados.xlsx')
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.normalize('NFKD')
    .str.encode('ascii', errors='ignore')
    .str.decode('utf-8')
)

# Configurar o gráfico ao vivo da atualização do fitness
sns.set(style="whitegrid")
plt.ion()
fig, ax = plt.subplots(figsize=(10, 5))
linha, = ax.plot([], [], marker='o', color='royalblue', label='Fitness por Geração')
ax.set_title('Evolução do Fitness em Tempo Real')
ax.set_xlabel('Geração')
ax.set_ylabel('Fitness')
ax.legend()

# Parâmetros
tamanho_populacao = 100
taxa_mutacao = 0.3
num_geracoes = 50
formacao = random.randint(1, 3)

# Gerar um indivíduo válido
def Gerar_individuo(df):
    global formacao, time

    formacao
    time = []

    # Separar por posição
    goleiros    = df[df["posicao"] == "G"]
    zagueiros   = df[df["posicao"] == "ZG"]
    laterais    = df[df["posicao"] == "LT"]
    volantes    = df[df["posicao"] == "VOL"]
    meias       = df[df["posicao"] == "MEI"]
    atacantes   = df[df["posicao"] == "AT"]

    if formacao == 1:  # 4-3-3
        config = {"G":1, "ZG":2, "LT":2, "VOL":2, "MEI":1, "AT":3}
    elif formacao == 2:  # 4-4-2
        config = {"G":1, "ZG":2, "LT":2, "VOL":3, "MEI":1, "AT":2}
    else:  # 3-5-2
        config = {"G":1, "ZG":3, "LT":1, "VOL":3, "MEI":1, "AT":2}

    try:
        time += random.sample(goleiros['jogador'].tolist(), config["G"])
        time += random.sample(zagueiros['jogador'].tolist(), config["ZG"])
        time += random.sample(laterais['jogador'].tolist(), config["LT"])
        time += random.sample(volantes['jogador'].tolist(), config["VOL"])
        time += random.sample(meias['jogador'].tolist(), config["MEI"])
        time += random.sample(atacantes['jogador'].tolist(), config["AT"])
    except ValueError as e:
        raise ValueError(f"Erro ao gerar time: {e}")

    assert len(set(time)) == 11, "Há jogadores repetidos na escalação!"

    return (formacao, time)

# Avaliação (Fitness) de cada indivíduo
def Avaliar_individuos(individuo, df):
    _, time = individuo
    fitness = 0

    for nome in time:
        linha = df[df["jogador"] == nome]
        if linha.empty:
            continue
        jogador = linha.iloc[0]
        pos = jogador["posicao"]

        if pos == 'G':
            fitness += (jogador["minutos_em_campo"] * 0.25 + 
                        jogador["defesas"] * 3 - 
                        jogador["gols_sofridos"] * 1.5 - 
                        jogador["gols_sofridos_por_jogo"])
        elif pos == "ZG":
            fitness += (jogador["minutos_em_campo"] * 0.25 - 
                        jogador["cartao_amarelo"] * 1.2 - 
                        jogador["cartao_vermelho"] * 3 + 
                        jogador["divididas_ganhas"] * 1.5 + 
                        jogador["desarmes"] * 2 + 
                        jogador["bloqueios"] * 1.5 + 
                        jogador["interceptacoes"] * 1.5)
        elif pos == "LT":
            fitness += (jogador["minutos_em_campo"] * 0.25 - 
                        jogador["cartao_amarelo"] * 1.2 - 
                        jogador["cartao_vermelho"] * 3 + 
                        jogador["divididas_ganhas"] * 1.5 + 
                        jogador["desarmes"] * 1.5 + 
                        jogador["bloqueios"] * 1.5 + 
                        jogador["interceptacoes"] * 1.5 + 
                        jogador["assistencias"] * 2 +
                        jogador["gols"] * 2 +
                        jogador["conducoes_relevantes"] * 1.5 +
                        jogador["passes_relevantes"] * 1.5)
        elif pos == "VOL":
            fitness += (jogador["minutos_em_campo"] * 0.25 - 
                        jogador["cartao_amarelo"] * 1.2 - 
                        jogador["cartao_vermelho"] * 3 + 
                        jogador["divididas_ganhas"] * 1.5 + 
                        jogador["desarmes"] * 3 + 
                        jogador["bloqueios"] * 1.5 + 
                        jogador["interceptacoes"] * 1.5 + 
                        jogador["assistencias"] * 2.5 +
                        jogador["gols"] * 2 +
                        jogador["conducoes_relevantes"] * 1.5 +
                        jogador["passes_relevantes"] * 1.5)
        elif pos == "MEI":
            fitness += (jogador["minutos_em_campo"] * 0.25 - 
                        jogador["cartao_amarelo"] * 1.2 - 
                        jogador["cartao_vermelho"] * 3 + 
                        jogador["assistencias"] * 2.5 +
                        jogador["gols"] * 2 +
                        jogador["conducoes_relevantes"] * 1.75 +
                        jogador["passes_relevantes"] * 2)
        elif pos == "AT":
            fitness += (jogador["minutos_em_campo"] * 0.25 - 
                        jogador["cartao_amarelo"] * 1.2 - 
                        jogador["cartao_vermelho"] * 3 + 
                        jogador["assistencias"] * 2 +
                        jogador["gols"] * 3 +
                        jogador["conducoes_relevantes"] * 1.75)
    return fitness

# Gerar a população de acordo com os parâmetros definidos
def Gerar_populacao_inicial(df):
    return [Gerar_individuo(df) for _ in range(tamanho_populacao)]

# Avaliar todos os indivíduos da população
def Avaliar_populacao(populacao, df):
    return [(ind, Avaliar_individuos(ind, df)) for ind in populacao]

# Selecionar os melhores avaliados
def Selecionar_melhores(avaliados, k=10):
    avaliados.sort(key=lambda x: x[1], reverse=True)
    return [ind for ind, _ in avaliados[:k]]

# Crossover respeitando posições e formações iguais
def Crossover(pai1, pai2):
    form1, time1 = pai1
    form2, time2 = pai2
    if form1 != form2:
        return pai1, pai2

    def posicoes_do_time(time):
        return {j: df[df["jogador"] == j]["posicao"].values[0] for j in time}

    pos1 = posicoes_do_time(time1)
    pos2 = posicoes_do_time(time2)

    filho1, filho2 = [], []
    for p in ["G", "ZG", "LT", "VOL", "MEI", "AT"]:
        j1 = [j for j in time1 if pos1[j] == p]
        j2 = [j for j in time2 if pos2[j] == p]
        if len(j1) == len(j2):
            ponto = random.randint(1, len(j1)) if len(j1) > 1 else 1
            f1 = j1[:ponto] + [j for j in j2 if j not in j1[:ponto]]
            f2 = j2[:ponto] + [j for j in j1 if j not in j2[:ponto]]
            filho1.extend(f1[:len(j1)])
            filho2.extend(f2[:len(j2)])
        else:
            filho1.extend(j1)
            filho2.extend(j2)

    return (form1, filho1), (form2, filho2)

# Mutação
def Mutar(individuo, df):
    formacao, time = individuo
    novo_time = time[:]
    i = random.randint(0, 10)
    jogador_antigo = novo_time[i]
    posicao = df[df["jogador"] == jogador_antigo]["posicao"].values[0]
    candidatos = df[(df["posicao"] == posicao) & (~df["jogador"].isin(novo_time))]

    if not candidatos.empty:
        novo_time[i] = random.choice(candidatos["jogador"].tolist())

    return (formacao, novo_time)

# Exibir a melhor escalação
def Exibir_melhor_indivíduo(historico):
    melhor_individuo, melhor_fitness = historico[-1]
    formacao, escalação = melhor_individuo

    print(f"\nMelhor Time da Última Geração:")
    print(f"Formação: {formacao}")
    print(f"Fitness: {melhor_fitness:.2f}\n")
    print("Jogadores escalados:")

    for jogador in escalação:
        posicao = df[df["jogador"] == jogador]["posicao"].values[0]
        print(f"{posicao}: {jogador}")

# Seleção por torneio (Evita convergência prematura)
def selecionar_por_torneio(avaliados, tamanho_torneio=3, numero_selecionados=4):
    selecionados = []
    for _ in range(numero_selecionados):
        torneio = random.sample(avaliados, tamanho_torneio)
        melhor = max(torneio, key=lambda x: x[1])
        selecionados.append(melhor[0])
    return selecionados

# Exibir um gráfico em tempo real com a evolução do Fitness
def Grafico_tempo_real(historico):
        fitness_por_geracao = [fit for (_, fit) in historico]
        linha.set_data(range(len(fitness_por_geracao)), fitness_por_geracao)
        ax.relim()
        ax.autoscale_view()
        plt.pause(0.1)

# Exibir a escalação em um gráfico
def exibir_escalacao_real(formacao, jogadores_nomeados, df):
    if formacao == 1:  # 4-3-3
        posicoes = [
            (5, 0), 
            (20, 10), 
            (20, -10), 
            (20, 20), 
            (20, -20),
            (40, 0), 
            (60, 11), 
            (60, -11),
            (80, 20), 
            (85, 0), 
            (80, -20)
        ]
    elif formacao == 2:  # 4-4-2
        posicoes = [
            (5, 0), 
            (20, 10), 
            (20, -10), 
            (20, 20), 
            (20, -20),
            (40, 10), 
            (40, -10), 
            (60, 15), 
            (60, -15),
            (80, 10), 
            (80, -10)
        ]
    elif formacao == 3:  # 3-5-2
        posicoes = [
            (5, 0), 
            (20, 0), 
            (20, 10), 
            (20, -10), 
            (40, 20),
            (40, -20), 
            (40, 0), 
            (60, 10), 
            (60, -10),
            (80, 10), 
            (80, -10)
        ]
    else:
        raise ValueError("Formação inválida.")

    if len(jogadores_nomeados) != len(posicoes):
        raise ValueError("Número de jogadores não corresponde à formação definida.")

    # Mapeia a posição real do jogador para cor e código
    def info_por_jogador(nome):
        linha = df[df["jogador"] == nome]
        if linha.empty:
            return '???', 'gray'
        pos = linha.iloc[0]["posicao"]
        if pos == "G":
            return "G", "yellow"
        elif pos == "ZG":
            return "ZG", "blue"
        elif pos == "LT":
            return "LT", "blue"
        elif pos == "VOL":
            return "VOL", "green"
        elif pos == "MEI":
            return "MEI", "green"
        elif pos == "AT":
            return "AT", "red"
        else:
            return pos, "gray"

    # Carrega o fundo da imagem do campo
    img = mpimg.imread(f'imagens\imagem_do_campo_de_futebol.jpeg')

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(img, extent=[0, 100, -30, 30], aspect='auto')  # fundo com as mesmas dimensões do campo
    ax.set_xlim(0, 100)
    ax.set_ylim(-30, 30)
    ax.axis('off')

    # Plotar jogadores
    for nome, (x, y) in zip(jogadores_nomeados, posicoes):
        pos_codigo, cor = info_por_jogador(nome)

        # Bolinha com cor
        ax.scatter(x, y, s=800, color=cor, edgecolor='white', linewidth=2, zorder=2)

        # Texto dentro da bolinha = posição
        ax.text(x, y, pos_codigo, ha='center', va='center', fontsize=10, color='black' if cor == "yellow" else 'white',
                weight='bold', zorder=2)

        # Nome do jogador abaixo da bolinha
        ax.text(x, y-4, nome, ha='center', va='center', fontsize=9, color='white', zorder=3)

    plt.title('Escalação - Formação ' + ('4-3-3' if formacao == 1 else '4-4-2' if formacao == 2 else '3-5-2'),
              fontsize=14, color='white', weight='bold')
    plt.show()

# Algoritmo genético principal
def Algoritmo_genetico(df):
    populacao = Gerar_populacao_inicial(df)
    historico = []

    for geracao in range(num_geracoes):
        avaliados = Avaliar_populacao(populacao, df)
        # melhores = Selecionar_melhores(avaliados, k=10)
        melhores = selecionar_por_torneio(avaliados, tamanho_torneio=3, numero_selecionados=5)
        nova_pop = melhores[:]

        while len(nova_pop) < tamanho_populacao:
            pai1, pai2 = random.sample(melhores, 2)
            filho1, filho2 = Crossover(pai1, pai2)
            if random.random() < taxa_mutacao:
                filho1 = Mutar(filho1, df)
            if random.random() < taxa_mutacao:
                filho2 = Mutar(filho2, df)
            nova_pop += [filho1, filho2]

        populacao = nova_pop[:tamanho_populacao]
        melhor = max(avaliados, key=lambda x: x[1])

        historico.append(melhor)
        Grafico_tempo_real(historico)


        print(f"Geração {geracao+1:03} | Fitness: {melhor[1]:.2f}")

    formacao, jogadores = historico[-1][0]
    exibir_escalacao_real(formacao, jogadores, df)
    plt.ioff()
    plt.show()
    Exibir_melhor_indivíduo(historico)

    return historico




# Executar
historico = Algoritmo_genetico(df)
