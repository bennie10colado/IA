import os
import random

TAMANHO_POPULACAO = 100
PROBABILIDADE_MUTACAO = 0.01
NUMERO_GERACOES = 100
TAMANHO_TORNEIO = 5

# definir funções para gerar um indivíduo,
# calcular a aptidão de um indivíduo, mutar um gene e processar a entrada e saída.
def gerar_individuo(equipamentos, alunos):
    """
    Gera um indivíduo (solução) para o problema de alocação de equipamentos de academia.
    Um indivíduo é uma lista de listas, onde cada sublista representa a agenda de um equipamento.
    Cada sublista contém tuples de (nome do aluno, equipamento), representando uma alocação.
    
    :param equipamentos: Lista de equipamentos disponíveis.
    :param alunos: Dicionário com alunos e o número de vezes que cada um deve utilizar os equipamentos.
    :return: Um indivíduo representando uma solução para o problema de alocação.
    """
    individuo = []
    for equipamento in equipamentos:
        agenda = []
        for aluno, num_usos in alunos.items():
            for _ in range(num_usos):
                agenda.append((aluno, equipamento))
        random.shuffle(agenda) 
        individuo.append(agenda)
    return individuo

def calcular_aptidao(individuo):
    pass

def mutar_gene(gene):
    pass

def processar_entrada(entrada):
    pass

def alocar_tempo(dados, solucao):
    pass

def gerar_saida(horarios):
    pass

def salvar_saida(saida, nome_arquivo_saida):
    pass

def gerar_populacao_inicial():
    return [gerar_individuo() for _ in range(TAMANHO_POPULACAO)]

def avaliar_aptidao(individuo):
    return calcular_aptidao(individuo)

def selecionar_pais(populacao):
    return [torneio(populacao) for _ in range(TAMANHO_POPULACAO)]

def crossover(pai1, pai2):
    ponto_corte = random.randint(1, len(pai1)-1)
    filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
    filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
    return filho1, filho2

def mutacao(individuo):
    if random.random() < PROBABILIDADE_MUTACAO:
        ponto_mutacao = random.randint(0, len(individuo)-1)
        individuo[ponto_mutacao] = mutar_gene(individuo[ponto_mutacao])
    return individuo

def selecionar_sobreviventes(populacao, descendentes):
    populacao.extend(descendentes)
    populacao.sort(key=avaliar_aptidao, reverse=True)
    return populacao[:TAMANHO_POPULACAO]

def checar_criterio_parada(geracao_atual):
    return geracao_atual >= NUMERO_GERACOES

def torneio(populacao):
    competidores = random.sample(populacao, TAMANHO_TORNEIO)
    competidores.sort(key=avaliar_aptidao, reverse=True)
    return competidores[0]

def main():
    input_directory = '../entrada_50'
    output_directory = '../saida_50'
    os.makedirs(output_directory, exist_ok=True)
    
    # inicialização da população
    populacao = gerar_populacao_inicial()
    geracao_atual = 0
    
    while not checar_criterio_parada(geracao_atual):
        aptidoes = [avaliar_aptidao(ind) for ind in populacao]
        
        pais = selecionar_pais(populacao)
        
        # recombinação e mutação
        descendentes = []
        for _ in range(len(populacao) // 2):
            pai1, pai2 = random.sample(pais, 2)
            filho1, filho2 = crossover(pai1, pai2)
            descendentes.append(mutacao(filho1))
            descendentes.append(mutacao(filho2))
        
        populacao = selecionar_sobreviventes(populacao, descendentes)
        geracao_atual += 1
    
    melhor_solucao = populacao[0]
    
    # processamento de entradas e saídas com a melhor solução encontrada
    for nome_arquivo_entrada in os.listdir(input_directory):
        if nome_arquivo_entrada.endswith('.txt'):
            caminho_completo_entrada = os.path.join(input_directory, nome_arquivo_entrada)
            nome_arquivo_saida = f"{output_directory}/saida_{nome_arquivo_entrada.split('_')[-1]}"

            with open(caminho_completo_entrada, 'r', encoding='ISO-8859-1') as f:
                entrada = f.read()

            dados = processar_entrada(entrada)
            horarios = alocar_tempo(dados, melhor_solucao)  # modificado para usar a melhor solução
            saida = gerar_saida(horarios)
            salvar_saida(saida, nome_arquivo_saida)

            print(f"O arquivo de saída '{nome_arquivo_saida}' foi gerado com sucesso.")

if __name__ == "__main__":
    main()
