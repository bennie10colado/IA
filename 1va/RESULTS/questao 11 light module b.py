import random

class RandomAgent:
    def __init__(self):
        pass

    def choose_action(self): #random
        return random.choice(['Up', 'Down', 'Left', 'Right', 'Suck'])

# Função para simular o ambiente do aspirador de pó
def simulate_random_agent(size=(3, 3), dirt_probability=0.2, time_steps=1000):
    environment = [[0 for _ in range(size[1])] for _ in range(size[0])]
    agent_position = [random.randint(0, size[0] - 1), random.randint(0, size[1] - 1)]

    for i in range(size[0]):
        for j in range(size[1]):
            if random.uniform(0, 1) < dirt_probability:
                environment[i][j] = 1

    performance_score = 0

    for _ in range(time_steps):
        action = RandomAgent().choose_action()

        if action == 'Up' and agent_position[0] > 0: #agent position verifica que nao ira quebrar o código, como percorrer valores negativos da matriz
            agent_position[0] -= 1
        elif action == 'Down' and agent_position[0] < size[0] - 1:
            agent_position[0] += 1
        elif action == 'Left' and agent_position[1] > 0:
            agent_position[1] -= 1
        elif action == 'Right' and agent_position[1] < size[1] - 1:
            agent_position[1] += 1
        elif action == 'Suck' and environment[agent_position[0]][agent_position[1]] == 1:
            environment[agent_position[0]][agent_position[1]] = 0
            performance_score += 1

    return performance_score

# Simule o agente aleatório em diferentes ambientes
total_scores_random = 0
num_simulations = 10

for _ in range(num_simulations):
    score_random = simulate_random_agent()
    total_scores_random += score_random
    print(f"Desempenho do agente aleatório: {score_random}")

average_score_random = total_scores_random / num_simulations
print(f"Média de desempenho do agente aleatório: {average_score_random}")
