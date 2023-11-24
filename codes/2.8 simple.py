import itertools
import random


# Classe que simula o ambiente do aspirador de po.
class VacuumCleanerEnvironment:
    # Inicializacao do ambiente com definicao de tamanho e variaveis iniciais.
    def __init__(self, size=(1, 2)):  # Apenas dois espaços conforme a figura 2.2
        self.size = size
        self.environment = [[0 for _ in range(size[1])] for _ in range(size[0])]
        self.performance_score = 0
        self.agent_position = [0, 0]
        self.time_steps = 1000

    # Atualiza a pontuacao de desempenho baseada no numero de quadrados limpos.
    def get_performance_score(self):
        self.performance_score += sum(cell == 0 for row in self.environment for cell in row)

    # Define as acoes do agente: mover para esquerda/direita ou aspirar.
    def perform_action(self, action):
        if action == 'Left':
            self.agent_position[1] = max(self.agent_position[1] - 1, 0)
        elif action == 'Right':
            self.agent_position[1] = min(self.agent_position[1] + 1, self.size[1] - 1)
        elif action == 'Suck':
            if self.environment[self.agent_position[0]][self.agent_position[1]] == 1:
                self.environment[self.agent_position[0]][self.agent_position[1]] = 0

    # Executa a simulacao com acoes baseadas no estado do ambiente.
    def simulate(self):
        for _ in range(self.time_steps):
            # Verifica se o quadrado atual está sujo e aspira se estiver.
            if self.environment[self.agent_position[0]][self.agent_position[1]] == 1:
                self.perform_action('Suck')
            else:
                self.perform_action(random.choice(['Left', 'Right']))
            self.get_performance_score()
        return self.performance_score


random.seed(0)  # Garante a reproducao dos resultados.
scores = []

# Todas as possíveis configurações iniciais sujas para um ambiente com dois espaços
for initial_dirt in itertools.product([0, 1], repeat=2):
    # Para cada posição inicial do agente nos dois espaços
    for initial_position in range(2):
        # Inicializa o ambiente e o agente
        env = VacuumCleanerEnvironment()
        env.environment[0] = list(initial_dirt)
        env.agent_position[1] = initial_position
        score = env.simulate()
        scores.append(score)
        print(
            f"Ambiente inicial: {initial_dirt}, Posição inicial do agente: {initial_position + 1}, Pontuação: {score}")

# Calcula a média das pontuações
average_score = sum(scores) / len(scores)
print(f"Pontuação média global: {average_score}")

#o print sugere que caso na geografia de (0,1), se o agente estive na posicao 1, ele nao limpa o segundo quadro no primeiro movimento, como a contabilização dos movimentos é medida após suas ações pelos passos de tempo, temos 2000 quando está tudo limpo ou o aspirador está em cima da uma sujeira existente
# para 1995, é caso o aspirador esteja em um ponto, e a sujeira em outra, logo sua soma da pontuacao antes de se movimentar eh contabilizada, e menor que 2000
# para 1999 ou 1998, conta ponto por ele ter limpado, entao conseguiu uma pontuacao maior que 1995