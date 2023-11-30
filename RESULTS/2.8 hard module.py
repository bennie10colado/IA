import random


# Classe que simula o ambiente do aspirador de po.
# E modular e permite alteracoes nos sensores, atuadores e caracteristicas do ambiente.
class VacuumCleanerEnvironment:
    # Inicializacao do ambiente com definicao de tamanho e variaveis iniciais. Considerando a figura 2.2,
    # temos 2 ou 20 espaços em que o aspirador se move, mas podemos aumentar o eixo y para que se tenha mais colunas,
    # e assim o aspirador se mova mais vezes para a esquerda e direita, visualmente.
    def __init__(self, size=(1, 20)):
        self.size = size
        self.environment = [[0 for _ in range(size[1])] for _ in range(size[0])]
        self.performance_score = 0
        self.agent_position = [0, 0]
        self.time_steps = 1000

    # Metodo para imprimir a matriz com guia de linhas e colunas.
    def print_guide(self):
        # Imprime os numeros das colunas como guia.
        col_guide = "  " + " ".join(str(i + 1) for i in range(self.size[1]))
        print(col_guide)
        # Imprime a linha divisoria.
        print("  " + "-" * (2 * self.size[1] - 1))
        for i in range(self.size[0]):
            print(f"{i + 1}|", end=" ")
            for j in range(self.size[1]):
                print(".", end=" ")
            print()

    # Inicializa o estado do ambiente com sujeira distribuida aleatoriamente.
    def initialize_environment(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.environment[i][j] = random.randint(0, 1)

    # Posiciona o agente em uma localizacao aleatoria no inicio da simulacao.
    def place_agent(self):
        self.agent_position = [random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1)]

    # Atualiza a pontuacao de desempenho baseada no numero de quadrados limpos.
    def get_performance_score(self):
        for row in self.environment:
            for cell in row:
                if cell == 0:
                    self.performance_score += 1
                    # Como cada operação ocorre a 100 passos de tempo, por exemplo: se tivermos 10 quadrados limpos,
                    # após 100 passos de tempo, 1000 pontos terão sido adicionados para o performance_score => 10
                    # quadrados limpos x 100 passos = 1000 pontos

    # Define as acoes do agente: mover para esquerda/direita ou aspirar.
    def perform_action(self, action):
        if action == 'Left' and self.agent_position[1] > 0:
            self.agent_position[1] -= 1
        elif action == 'Right' and self.agent_position[1] < self.size[1] - 1:
            self.agent_position[1] += 1
        elif action == 'Suck':
            self.environment[self.agent_position[0]][self.agent_position[1]] = 0

    # Executa a simulacao, chamando as acoes de forma aleatoria e calculando a pontuacao.
    def simulate(self):
        for _ in range(self.time_steps):
            self.get_performance_score()
            action = random.choice(['Left', 'Right', 'Suck'])
            self.perform_action(action)
        return self.performance_score


# Classe para simular o ambiente com saida detalhada.
class VacuumCleanerEnvironmentSimulator(VacuumCleanerEnvironment):
    # Imprime o estado do ambiente e a pontuacao durante a simulacao.
    def print_environment(self):
        for row in self.environment:
            print(' '.join(['*' if cell == 1 else '.' for cell in row]))
        # Ajusta a impressao da posicao do agente para ser base 1 em vez de base 0.
        adjusted_position = [self.agent_position[0] + 1, self.agent_position[1] + 1]
        print(f"Posicao do agente: {adjusted_position}")
        print(f"Pontuacao de desempenho: {self.performance_score}\n")

    # Executa a simulacao com saida detalhada.
    def simulate(self):
        for t in range(self.time_steps):
            if t % 100 == 0:
                print(f"Passo de tempo: {t}")
                self.print_environment()
            self.get_performance_score()
            action = random.choice(['Left', 'Right', 'Suck'])
            self.perform_action(action)
        print("Estado final do ambiente:")
        self.print_environment()
        return self.performance_score


if __name__ == "__main__":
    random.seed(0)
    vacuum_env_simulator = VacuumCleanerEnvironmentSimulator()
    vacuum_env_simulator.print_guide()
    vacuum_env_simulator.initialize_environment()
    vacuum_env_simulator.place_agent()
    performance_score_simulator = vacuum_env_simulator.simulate()
    print(f"Pontuacao de desempenho final: {performance_score_simulator}")
