import random


# Classe que simula o ambiente do aspirador de pó.
class VacuumCleanerEnvironment:
    def __init__(self, size=(1, 2)):  # Reduzido para 2 espaços
        self.size = size
        self.environment = [[0 for _ in range(size[1])] for _ in range(size[0])]
        self.performance_score = 0
        self.agent_position = [0, 0]
        self.time_steps = 1000

    def print_guide(self):
        col_guide = "  " + " ".join(str(i + 1) for i in range(self.size[1]))
        print(col_guide)
        print("  " + "-" * (2 * self.size[1] - 1))
        for i in range(self.size[0]):
            print(f"{i + 1}|", end=" ")
            for j in range(self.size[1]):
                print("*" if self.environment[i][j] == 1 else ".", end=" ")
            print()

    def initialize_environment(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.environment[i][j] = random.randint(0, 1)

    def place_agent(self):
        self.agent_position = [random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1)]

    def get_performance_score(self):
        for row in self.environment:
            for cell in row:
                if cell == 0:
                    self.performance_score += 1

    def perform_action(self, action):
        if action == 'Left' and self.agent_position[1] > 0:
            self.agent_position[1] -= 1
        elif action == 'Right' and self.agent_position[1] < self.size[1] - 1:
            self.agent_position[1] += 1
        elif action == 'Suck':
            self.environment[self.agent_position[0]][self.agent_position[1]] = 0

    def simulate(self):
        for _ in range(self.time_steps):
            self.get_performance_score()
            action = random.choice(['Left', 'Right', 'Suck'])
            self.perform_action(action)
        return self.performance_score


# Classe para simular o ambiente com saída detalhada.
class VacuumCleanerEnvironmentSimulator(VacuumCleanerEnvironment):
    def is_dirty(self, position):
        return self.environment[position[0]][position[1]] == 1

    def clean(self, position):
        self.environment[position[0]][position[1]] = 0


# Classe que implementa o agente reativo com estado.
class ReactiveAgentWithState:
    def __init__(self, environment):
        self.environment = environment
        self.agent_position = [0, 0]
        self.performance_score = 0

    def move_left(self):
        if self.agent_position[1] > 0:
            self.agent_position[1] -= 1
            self.performance_score -= 1  # Penalização por movimento

    def move_right(self):
        if self.agent_position[1] < self.environment.size[1] - 1:
            self.agent_position[1] += 1
            self.performance_score -= 1  # Penalização por movimento

    def suck(self):
        if self.environment.is_dirty(self.agent_position):
            self.environment.clean(self.agent_position)
            self.performance_score += 1

    def perceive_and_act(self):
        if self.environment.is_dirty(self.agent_position):
            self.suck()
        else:
            if self.agent_position[1] == 0:
                self.move_right()
            else:
                self.move_left()


if __name__ == "__main__":
    random.seed(0)

    # Inicialize o ambiente e o agente
    vacuum_env_simulator = VacuumCleanerEnvironmentSimulator(size=(1, 2))
    vacuum_env_simulator.print_guide()
    vacuum_env_simulator.initialize_environment()
    vacuum_env_simulator.place_agent()

    # Execute a simulação com o agente reativo com estado
    vacuum_agent = ReactiveAgentWithState(vacuum_env_simulator)
    for _ in range(vacuum_env_simulator.time_steps):
        vacuum_agent.perceive_and_act()
        vacuum_env_simulator.print_guide()
        # Ao ativar essa linha 108, obtemos cada linha de código, sendo 2 prints para cada passo do codigo

    # Obtenha a pontuação de desempenho final do agente reativo com estado
    performance_score_agent = vacuum_agent.performance_score
    print(f"Pontuação de desempenho final do agente reativo com estado: {performance_score_agent}")
