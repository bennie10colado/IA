import random

# Classe que simula o ambiente do aspirador de pó.
class VacuumCleanerEnvironment:
    def __init__(self, size=(1, 20)):
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
                print(".", end=" ")
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
            self.performance_score += 1

    def simulate(self):
        for _ in range(self.time_steps):
            self.get_performance_score()
            action = random.choice(['Left', 'Right', 'Suck'])
            self.perform_action(action)
        return self.performance_score

# Classe para o agente reativo
class ReactiveVacuumAgent:
    def __init__(self):
        self.actions = ['Suck', 'Left', 'Right']
        self.current_action_index = 0

    def select_action(self, percept):
        if percept[0] == 1:
            return 'Suck'
        else:
            action = self.actions[self.current_action_index]
            self.current_action_index = (self.current_action_index + 1) % len(self.actions)
            return action

# Função para executar a simulação com diferentes configurações iniciais sujas e posições iniciais do agente
def run_simulation():
    random.seed(0)
    scores = []
    environments = [(0, 0), (0, 1), (1, 0), (1, 1)]

    for env_state in environments:
        for pos in range(2):
            env = VacuumCleanerEnvironment()
            agent = ReactiveVacuumAgent()
            env.environment[0] = list(env_state)
            env.agent_position[1] = pos
            performance_score = 0

            for _ in range(env.time_steps):
                percept = [env.environment[env.agent_position[0]][env.agent_position[1]]]
                action = agent.select_action(percept)
                env.perform_action(action)
                performance_score = env.performance_score

            scores.append(performance_score)
            print(f"Ambiente: {env_state}, Posição inicial do agente: {pos + 1}, Pontuação: {performance_score}")

    average_score = sum(scores) / len(scores)
    print(f"Pontuação média global: {average_score}")

if __name__ == "__main__":
    run_simulation()
