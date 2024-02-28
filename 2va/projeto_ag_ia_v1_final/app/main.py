import os
from collections import defaultdict
import random

def processar_entrada(entrada):
    linhas = entrada.strip().split('\n')
    dados = {}
    for linha in linhas:
        equipamento, alunos_str = linha.split(':')
        alunos = alunos_str.split(';')[:-1]
        dados[equipamento.strip()] = {aluno.split('=')[0]: int(aluno.split('=')[1]) for aluno in alunos}
    return dados

def inicializar_populacao(dados, tamanho_populacao):
    populacao = []
    for _ in range(tamanho_populacao):
        cromossomo = {}
        for equipamento, alunos in dados.items():
            horarios = [[] for _ in range(max(alunos.values()))]
            for aluno, repeticoes in alunos.items():
                indices_horarios = random.sample(range(len(horarios)), repeticoes)
                for indice in indices_horarios:
                    horarios[indice].append(aluno)
            cromossomo[equipamento] = horarios
        populacao.append(cromossomo)
    return populacao

def calcular_aptidao(cromossomo, dados):
    penalizacao = 0
    recompensa = 0
    alunos_por_horario = defaultdict(set)
    alunos_em_duas_maquinas = set()

    for equipamento, horarios in cromossomo.items():
        for i, horario in enumerate(horarios):
            alunos_por_horario[i].update(horario)
            penalizacao += (len(horario) - len(set(horario))) * 50
            alunos_duas_maquinas = set(horario)
            intersecao = alunos_em_duas_maquinas.intersection(alunos_duas_maquinas)
            if intersecao:
                penalizacao += len(intersecao) * 10000
                alunos_em_duas_maquinas.update(intersecao)

    for i, horario in alunos_por_horario.items():
        if len(horario) != len(set(horario)):
            penalizacao += (len(horario) - len(set(horario))) * 200

    for equipamento, alunos in dados.items():
        for aluno, quantidade_esperada in alunos.items():
            quantidade_real = sum(aluno in horario for horario in cromossomo[equipamento])
            if quantidade_real == quantidade_esperada:
                recompensa += 1500
            elif quantidade_real < quantidade_esperada:
                penalizacao += 100
            elif quantidade_real > quantidade_esperada:
                penalizacao += 100

    return penalizacao - recompensa

def selecao(populacao, dados, percentual_elitismo):
    populacao_ordenada = sorted(populacao, key=lambda x: calcular_aptidao(x, dados))
    elitismo = int(len(populacao) * percentual_elitismo)
    return populacao_ordenada[:elitismo] + random.sample(populacao_ordenada[elitismo:], len(populacao) - elitismo)

def crossover(individuo1, individuo2):
    filho = {}
    for equipamento in individuo1:
        if random.random() < 0.5:
            ponto_corte = random.randint(1, len(individuo1[equipamento]) - 1)
            filho[equipamento] = individuo1[equipamento][:ponto_corte] + individuo2[equipamento][ponto_corte:]
        else:
            filho[equipamento] = individuo2[equipamento]
    return filho

def mutacao(individuo, taxa_mutacao):
    for equipamento, horarios in individuo.items():
        for horario in horarios:
            if random.random() < taxa_mutacao:
                indice1, indice2 = random.sample(range(len(horario)), 2)
                horario[indice1], horario[indice2] = horario[indice2], horario[indice1]
    return individuo

def evoluir(populacao, dados, percentual_elitismo, taxa_crossover, taxa_mutacao):
    nova_populacao = selecao(populacao, dados, percentual_elitismo)

    while len(nova_populacao) < len(populacao):
        pai1, pai2 = random.sample(nova_populacao, 2)
        if random.random() < taxa_crossover:
            filho = crossover(pai1, pai2)
        else:
            filho = random.choice([pai1, pai2])
        filho = mutacao(filho, taxa_mutacao)
        nova_populacao.append(filho)

    return nova_populacao

def alocar_tempo_ag(dados, tamanho_populacao, percentual_elitismo, taxa_crossover, taxa_mutacao, numero_geracoes):
    populacao = inicializar_populacao(dados, tamanho_populacao)
    for geracao in range(numero_geracoes):
        populacao = evoluir(populacao, dados, percentual_elitismo, taxa_crossover, taxa_mutacao)
    return encontrar_melhor_solucao(populacao, dados)

def encontrar_melhor_solucao(populacao, dados):
    return min(populacao, key=lambda x: calcular_aptidao(x, dados))

def gerar_saida_ag(melhor_solucao):
    if melhor_solucao is None:
        return ["Não foi possível alocar todos os alunos seguindo as restrições."]
    saida = []
    for equipamento, horarios in melhor_solucao.items():
        saida_linha = f"{equipamento}:"
        for horario in horarios:
            alunos_no_horario = '-'.join(horario)
            hifens_necessarios = max(0, 11 - (len(horario) - 1))
            alunos_no_horario += '-' * hifens_necessarios
            saida_linha += f" {alunos_no_horario}"
        saida.append(saida_linha.strip())
    return saida

def salvar_saida_ag(saida, nome_arquivo_saida):
    with open(nome_arquivo_saida, 'w', encoding='ISO-8859-1') as f:
        for linha in saida:
            f.write(f"{linha}\n")

def contar_alunos_por_maquina(saida):
    contagem_alunos = defaultdict(lambda: defaultdict(int))
    for linha in saida:
        equipamento, alunos = linha.split(":")
        alunos = alunos.strip().split("-")
        for aluno in alunos:
            if aluno != "":
                contagem_alunos[equipamento][aluno] += 1
    return contagem_alunos

def contar_alunos_por_entrada(entrada):
    contagem_alunos = defaultdict(lambda: defaultdict(int))
    linhas = entrada.strip().split("\n")
    for linha in linhas:
        equipamento, alunos_str = linha.split(":")
        alunos = alunos_str.strip().split(";")[:-1]
        for aluno in alunos:
            nome_aluno, quantidade = aluno.split("=")
            contagem_alunos[equipamento][nome_aluno] += int(quantidade)
    return contagem_alunos

def alunos_em_duas_maquinas(saida):
    alunos_presentes = set()
    for linha in saida:
        equipamento, alunos = linha.split(":")
        alunos = alunos.strip().split("-")
        for aluno in alunos:
            if aluno != "":
                if aluno in alunos_presentes:
                    return True
                alunos_presentes.add(aluno)
    return False

def verificar_saidas_corretas(entrada, saida):
    contagem_alunos_entrada = contar_alunos_por_entrada(entrada)
    contagem_alunos_saida = contar_alunos_por_maquina(saida)

    for equipamento, alunos_saida in contagem_alunos_saida.items():
        alunos_entrada = contagem_alunos_entrada[equipamento]
        for aluno, quantidade_saida in alunos_saida.items():
            if aluno not in alunos_entrada:
                print(f"Aluno não deveria estar nessa máquina")
                return False
            quantidade_entrada = alunos_entrada[aluno]
            if quantidade_saida != quantidade_entrada:
                print(f"Quantidade incorreta de alocações para o aluno")
                return False

    if alunos_em_duas_maquinas(saida):
        print(f"Um aluno está alocado em duas máquinas ao mesmo tempo")
        return False

    return True

def ler_arquivos_de_diretorio(diretorio):
    conteudos = {}
    for nome_arquivo in os.listdir(diretorio):
        caminho_completo = os.path.join(diretorio, nome_arquivo)
        with open(caminho_completo, 'r', encoding='ISO-8859-1') as arquivo:
            conteudos[nome_arquivo] = arquivo.read()
    return conteudos

def verificar_saida(dados_entrada, dados_saida):
    requisitos = {}
    total_alocacoes_corretas = 0
    total_alocacoes_esperadas = 0
    alocacoes_por_hora = [set() for _ in range(12)]  
    erros = []
    alocacoes_simultaneas = 0

    # Processar dados de entrada para mapear requisitos esperados
    for linha in dados_entrada.strip().split('\n'):
        if ':' not in linha:
            continue
        equipamento, detalhes = linha.split(':')
        for detalhe in detalhes.split(';'):
            if detalhe:
                aluno, vezes = detalhe.split('=')
                if aluno not in requisitos:
                    requisitos[aluno] = {}
                requisitos[aluno][equipamento] = int(vezes)
                total_alocacoes_esperadas += int(vezes)

    # Processar dados de saída
    for linha in dados_saida.strip().split('\n'):
        if ':' not in linha:
            continue
        equipamento, alunos_alocados_str = linha.split(':')
        alunos_alocados = alunos_alocados_str.strip().split('-')
        contagem_alocacoes = defaultdict(int)

        for aluno in alunos_alocados:
            if aluno:  # Verificar se o nome do aluno não está vazio
                contagem_alocacoes[aluno] += 1
                for hora in range(12):  # Supondo que temos 12 horas para alocação, ajuste conforme necessário
                    if aluno in alocacoes_por_hora[hora]:
                        alocacoes_simultaneas += 1
                        break  # Para evitar contar múltiplas alocações simultâneas para o mesmo aluno
                    alocacoes_por_hora[hora].add(aluno)
                    break  # Assumir que cada aluno só pode ser alocado uma vez por hora

        for aluno, vezes in contagem_alocacoes.items():
            if aluno in requisitos and equipamento in requisitos[aluno]:
                if requisitos[aluno][equipamento] == vezes:
                    total_alocacoes_corretas += vezes
                else:
                    erros.append(f"Inconsistência: {aluno} deveria estar {requisitos[aluno][equipamento]} vezes em {equipamento}, mas está {vezes} vezes.")

    taxa_acerto = (total_alocacoes_corretas / total_alocacoes_esperadas) * 100 if total_alocacoes_esperadas > 0 else 0
    print(f"Taxa de acerto: {taxa_acerto:.2f}%")
    #print(f"Alocações simultâneas indevidas: {alocacoes_simultaneas}")
    if erros:
        for erro in erros:
            print(erro)
    else:
        print("Todas as alocações estão corretas e sem alocações simultâneas para o arquivo analisado.")


def printar_porcentagens():
    input_directory = './entrada_50'
    output_directory = './saida_ag'

    dados_entrada = ler_arquivos_de_diretorio(input_directory)
    dados_saida = ler_arquivos_de_diretorio(output_directory)

    for nome_arquivo, entrada in dados_entrada.items():
        nome_arquivo_saida = 'saida' + nome_arquivo.split('entrada')[-1]
        saida_correspondente = dados_saida.get(nome_arquivo_saida)
        if saida_correspondente:
            print(f"Verificando {nome_arquivo} e sua saída correspondente...")
            verificar_saida(entrada, saida_correspondente)
        else:
            print(f"Não foi encontrada uma saída correspondente para {nome_arquivo}.")

def main():
    input_directory = './entrada_50'
    output_directory = './saida_ag'
    os.makedirs(output_directory, exist_ok=True)

    for nome_arquivo_entrada in os.listdir(input_directory):
        if nome_arquivo_entrada.endswith('.txt'):
            caminho_completo_entrada = os.path.join(input_directory, nome_arquivo_entrada)
            nome_arquivo_saida = f"{output_directory}/saida_{nome_arquivo_entrada.split('_')[-1]}"

            with open(caminho_completo_entrada, 'r', encoding='ISO-8859-1') as f:
                entrada = f.read()

            dados = processar_entrada(entrada)
            melhor_solucao = alocar_tempo_ag(dados, tamanho_populacao=100, percentual_elitismo=0.01, taxa_crossover=0.999, taxa_mutacao=0.2, numero_geracoes=750)

            saida = gerar_saida_ag(melhor_solucao)
            salvar_saida_ag(saida, nome_arquivo_saida)

            print(f"O arquivo de saída '{nome_arquivo_saida}' foi gerado com sucesso.")

    printar_porcentagens()

if __name__ == "__main__":
    main()
