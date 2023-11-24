# Implementação do exercício 2.13 com um agente que opera em um ambiente estocástico
import random

class StochasticVacuumCleanerEnvironment:
    def __init__(self, size=(1, 20), dirt_rate=0.1, suck_failure_rate=0.1, children_rate=0.05):
        self.size = size
        self.environment = [[0 for _ in range(size[1])] for _ in range(size[0])]
        self.performance_score = 0
        self.agent_position = [0, 0]
        self.time_steps = 1000
        self.cleaned_positions = set()
        # Taxas estocásticas adicionadas
        self.dirt_rate = dirt_rate
        self.suck_failure_rate = suck_failure_rate
        self.children_rate = children_rate

    def initialize_environment(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.environment[i][j] = random.randint(0, 1)

    def place_agent(self):
        self.agent_position = [random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1)]

    def perform_action(self, action):
        x, y = self.agent_position
        if action == 'Left' and y > 0:
            self.agent_position[1] -= 1
        elif action == 'Right' and y < self.size[1] - 1:
            self.agent_position[1] += 1
        elif action == 'Suck':
            # Incorpora falha na ação de aspirar
            if random.random() > self.suck_failure_rate:
                self.environment[x][y] = 0
                self.cleaned_positions.add((x, y))
            else:
                # A ação de aspirar falha e potencialmente suja o local novamente
                self.environment[x][y] = random.randint(0, 1)

    def simulate(self):
        for t in range(self.time_steps):
            # Adiciona sujeira aleatoriamente no ambiente com base na taxa de crianças
            if random.random() < self.children_rate:
                x, y = random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1)
                self.environment[x][y] = 1

            # Se a posição atual já foi limpa, evita limpar novamente
            if tuple(self.agent_position) in self.cleaned_positions:
                action = random.choice(['Left', 'Right'])
            else:
                action = random.choice(['Left', 'Right', 'Suck'])

            self.perform_action(action)

            # Atualiza a pontuação de desempenho
            self.performance_score = sum(cell == 0 for row in self.environment for cell in row)

        return self.performance_score

# Executando a simulação
if __name__ == "__main__":
    random.seed(0)
    stochastic_vacuum_env = StochasticVacuumCleanerEnvironment()
    stochastic_vacuum_env.initialize_environment()
    stochastic_vacuum_env.place_agent()
    performance_score_stochastic = stochastic_vacuum_env.simulate()
    print(f"Pontuação de desempenho final em ambiente estocástico: {performance_score_stochastic}")
