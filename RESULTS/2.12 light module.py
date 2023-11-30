import random

class SimpleReactiveAgent:
    def __init__(self):
        pass

    def choose_action(self, dirty):
        if dirty:
            return 'Suck'
        else:
            return random.choice(['Up', 'Down', 'Left', 'Right'])

# Função para simular o ambiente do aspirador de pó com obstáculos
def simulate_simple_reactive_agent(size=(3, 3), dirt_probability=0.2, obstacle_probability=0.1, time_steps=1000):
    environment = [[0 for _ in range(size[1])] for _ in range(size[0])]
    agent_position = [random.randint(0, size[0] - 1), random.randint(0, size[1] - 1)]

    # Coloca sujeira no ambiente
    for i in range(size[0]):
        for j in range(size[1]):
            if random.uniform(0, 1) < dirt_probability:
                environment[i][j] = 1

    # Coloca obstáculos no ambiente
    for i in range(size[0]):
        for j in range(size[1]):
            if random.uniform(0, 1) < obstacle_probability:
                environment[i][j] = 'X'  # Use 'X' para representar obstáculos

    # Imprime a matriz ambiente
    print("Ambiente com obstáculos:")
    for row in environment:
        print(row)

    performance_score = 0

    for _ in range(time_steps):
        dirty = environment[agent_position[0]][agent_position[1]] == 1

        if environment[agent_position[0]][agent_position[1]] == 'X':
            # Se o agente encontrar um obstáculo, ele se move aleatoriamente
            action = random.choice(['Up', 'Down', 'Left', 'Right'])
        else:
            action = SimpleReactiveAgent().choose_action(dirty)

        if action == 'Up' and agent_position[0] > 0:
            agent_position[0] -= 1
        elif action == 'Down' and agent_position[0] < size[0] - 1:
            agent_position[0] += 1
        elif action == 'Left' and agent_position[1] > 0:
            agent_position[1] -= 1
        elif action == 'Right' and agent_position[1] < size[1] - 1:
            agent_position[1] += 1
        elif action == 'Suck' and dirty:
            environment[agent_position[0]][agent_position[1]] = 0
            performance_score += 1

    return performance_score

if __name__ == "__main__":
    # Simule o agente reativo simples em diferentes ambientes com obstáculos
    num_simulations = 10
    total_scores_simple = 0

    for _ in range(num_simulations):
        score_simple = simulate_simple_reactive_agent()
        total_scores_simple += score_simple
        print(f"Desempenho do agente reativo simples com obstáculos: {score_simple}")

    average_score_simple = total_scores_simple / num_simulations
    print(f"Média de desempenho do agente reativo simples com obstáculos: {average_score_simple}")
