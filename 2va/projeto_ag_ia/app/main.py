import os
import random
from collections import defaultdict

#codigo descartado por obter taxas de resposta muito baixas. 
# no final eu e neto discutimos em ligação e em código fomos aprimorando até que obtivessemos uma taxa de accuracy alta, 
# chegando até 88% de acerto registrado com leitura quase perfeita

TAMANHO_POPULACAO = 250  
PROBABILIDADE_MUTACAO = 0.1 
NUMERO_GERACOES = 300 

def processar_entrada(entrada):
    linhas = entrada.strip().split('\n')
    dados = {}
    for linha in linhas:
        equipamento, alunos_str = linha.split(':')
        alunos = alunos_str.split(';')[:-1]
        dados[equipamento.strip()] = {aluno.split('=')[0]: int(aluno.split('=')[1]) for aluno in alunos}
    return dados

def gerar_individuo(equipamentos, alunos):
    individuo = []
    for equipamento in equipamentos:
        agenda = [(aluno, equipamento) for aluno in alunos for _ in range(alunos[aluno])]
        random.shuffle(agenda)
        individuo.append(agenda[:12]) 
    return individuo

def calcular_aptidao(individuo, dados):
    penalizacao = 0
    alunos_por_slot = defaultdict(set)
    for agenda in individuo:
        for i, (aluno, _) in enumerate(agenda):
            if aluno in alunos_por_slot[i]:
                penalizacao += 100
            alunos_por_slot[i].add(aluno)
    contagem_alunos = defaultdict(int)
    for agenda in individuo:
        for aluno, _ in agenda:
            contagem_alunos[aluno] += 1
    for equipamento, alunos in dados.items():
        for aluno, qtde in alunos.items():
            penalizacao += abs(contagem_alunos[aluno] - qtde)
    return 1 / (1 + penalizacao)

def mutar_gene(individuo):
    for agenda in individuo:
        if random.random() < PROBABILIDADE_MUTACAO:
            i, j = random.sample(range(len(agenda)), 2)
            agenda[i], agenda[j] = agenda[j], agenda[i]

def gerar_populacao_inicial(equipamentos, alunos):
    return [gerar_individuo(equipamentos, alunos) for _ in range(TAMANHO_POPULACAO)]

def selecionar_sobreviventes(populacao, dados, elite_size=2):
    elite = sorted(populacao, key=lambda x: calcular_aptidao(x, dados), reverse=True)[:elite_size]
    return elite + sorted(random.sample(populacao, len(populacao) - elite_size), key=lambda x: calcular_aptidao(x, dados), reverse=True)[:TAMANHO_POPULACAO - elite_size]

def evoluir(populacao, dados):
    nova_populacao = selecionar_sobreviventes(populacao, dados)
    while len(nova_populacao) < TAMANHO_POPULACAO:
        pai1, pai2 = random.sample(nova_populacao[:20], 2)  
        filho = crossover(pai1, pai2)
        mutar_gene(filho)
        nova_populacao.append(filho)
    return nova_populacao

def crossover(pai1, pai2):
    filho = []
    for i in range(len(pai1)):
        if random.random() > 0.5:
            filho.append(pai1[i])
        else:
            filho.append(pai2[i])
    return filho

def gerar_saida(horarios):
    saida = []
    for agenda in horarios:
        equipamento = agenda[0][1]
        linha = f"{equipamento}: " + "-".join(aluno for aluno, _ in agenda)
        saida.append(linha)
    return "\n".join(saida)

def salvar_saida(saida, nome_arquivo_saida):
    with open(nome_arquivo_saida, 'w', encoding='UTF-8') as f:
        f.write(saida)

def main():
    input_directory = '../entrada_50'
    output_directory = '../saida_ag'
    os.makedirs(output_directory, exist_ok=True)
    
    for nome_arquivo_entrada in os.listdir(input_directory):
        if nome_arquivo_entrada.endswith('.txt'):
            caminho_completo_entrada = os.path.join(input_directory, nome_arquivo_entrada)
            nome_arquivo_saida = f"{output_directory}/saida_{nome_arquivo_entrada.split('_')[-1]}"

            with open(caminho_completo_entrada, 'r', encoding='ISO-8859-1') as f:
                entrada = f.read()

            dados = processar_entrada(entrada)
            equipamentos = list(dados.keys())
            todos_alunos = set(sum([list(alunos.keys()) for alunos in dados.values()], []))
            alunos = {aluno: sum(dados[equipamento].get(aluno, 0) for equipamento in equipamentos) for aluno in todos_alunos}
            
            populacao = gerar_populacao_inicial(equipamentos, alunos)
            for _ in range(NUMERO_GERACOES):
                populacao = evoluir(populacao, dados)
            melhor_solucao = populacao[0]
            
            saida = gerar_saida(melhor_solucao)
            salvar_saida(saida, nome_arquivo_saida)

            print(f"O arquivo de saída '{nome_arquivo_saida}' foi gerado com sucesso.")

if __name__ == "__main__":
    main()
