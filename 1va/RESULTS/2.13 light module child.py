import random

class ChildAgent:
    def __init__(self):
        pass

    def choose_action(self, dirty):
        if dirty:
            return 'Suck'
        else:
            return random.choice(['Up', 'Down', 'Left', 'Right'])

# Função para simular o ambiente do aspirador de pó com obstáculos
def simulate_child_agent(size=(3, 3), time_steps=1000):
    environment = [[0 for _ in range(size[1])] for _ in range(size[0])]
    agent_position = [random.randint(0, size[0] - 1), random.randint(0, size[1] - 1)]

    performance_score = 0

    for _ in range(time_steps):
        dirty = environment[agent_position[0]][agent_position[1]] == 1

        # se houver crianças na sala, então cada quadrado limpo tem 10% de chance de se tornar sujo
        for i in range(size[0]):
            for j in range(size[1]):
                if environment[i][j] == 0 and random.uniform(0, 1) < 0.1:
                    environment[i][j] = 1

        # Imprime a matriz ambiente
        print("Ambiente com crianças:")
        for row in environment:
            print(row)

        action = ChildAgent().choose_action(dirty)

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
    total_scores_child = 0

    for _ in range(num_simulations):
        score_child = simulate_child_agent()
        total_scores_child += score_child
        print(f"Desempenho do agente reativo simples com obstáculos e crianças: {score_child}")

    average_score_child = total_scores_child / num_simulations
    print(f"Média de desempenho do agente reativo simples com obstáculos e crianças: {average_score_child}")
