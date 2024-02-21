import os
from collections import defaultdict

def processar_entrada(entrada):
    # divide a entrada por linhas e itera sobre cada linha para extrair os dados de cada equipamento e os alunos com suas respectivas frequências
    linhas = entrada.strip().split('\n')
    dados = {}
    for linha in linhas:
        equipamento, alunos_str = linha.split(':')
        alunos = alunos_str.split(';')[:-1]  # ignora o último elemento vazio
        # cria um dicionário para cada equipamento com alunos e suas frequências
        dados[equipamento.strip()] = {aluno.split('=')[0]: int(aluno.split('=')[1]) for aluno in alunos}
        print(f"Dados processados de {equipamento}: {dados[equipamento.strip()]}")
    return dados

def alocar_tempo(dados):
    # prepara um dicionário para manter os horários alocados e outro para contar as alocações
    horarios_alocados = {equipamento: ["-" for _ in range(12)] for equipamento in dados}
    alocacoes = defaultdict(lambda: defaultdict(int))
    todos_alunos = {aluno for alunos in dados.values() for aluno in alunos}

    print("Iniciando alocação com backtracking...")

    def backtrack(equipamento, horario):
        # tenta alocar alunos em cada horário de cada equipamento usando backtracking
        if equipamento == len(dados): # se todos os equipamentos foram alocados, retorna  
            return True
        if horario == 12:  # se todos os horários de um equipamento foram alocados, move para o próximo equipamento
            return backtrack(equipamento + 1, 0)
        
        for aluno in todos_alunos:
            if pode_alocar(equipamento, horario, aluno):
                realizar_alocacao(equipamento, horario, aluno)
                if backtrack(equipamento, horario + 1):
                    return True
                desfazer_alocacao(equipamento, horario, aluno)
        
        return False  

    def pode_alocar(equipamento, horario, aluno):
        # verifica se o aluno pode ser alocado no horário especificado de acordo com as restrições
        equipamento_atual = list(dados)[equipamento]
        if aluno not in dados[equipamento_atual] or alocacoes[equipamento_atual][aluno] >= dados[equipamento_atual][aluno]:
            return False
        for eq, horarios_eq in horarios_alocados.items():
            if horarios_eq[horario] == aluno:
                return False
        return True

    def realizar_alocacao(equipamento, horario, aluno):
        # aloca o aluno no horário especificado e atualiza o contador de alocações
        equipamento_atual = list(dados)[equipamento]
        horarios_alocados[equipamento_atual][horario] = aluno
        alocacoes[equipamento_atual][aluno] += 1
        print(f"Alocando {aluno} em {equipamento_atual} no horário {horario}. Alocacoes agora: {alocacoes[equipamento_atual][aluno]}")

    def desfazer_alocacao(equipamento, horario, aluno):
        # desfaz a alocação do aluno no horário especificado e atualiza o contador de alocações
        equipamento_atual = list(dados)[equipamento]
        horarios_alocados[equipamento_atual][horario] = "-"
        alocacoes[equipamento_atual][aluno] -= 1
        print(f"Desfazendo alocação de {aluno} em {equipamento_atual} no horário {horario}. Alocacoes agora: {alocacoes[equipamento_atual][aluno]}")

    if backtrack(0, 0):
        print("Alocação completada com sucesso.")
        return horarios_alocados
    else:
        print("Não foi possível alocar todos os alunos seguindo as restrições.")
        return None  

def gerar_saida(horarios):
    # gera a saída formatada com base nos horários alocados
    if horarios is None:
        return ["Não foi possível alocar todos os alunos seguindo as restrições."]
    saida = []
    for equipamento, alunos in horarios.items():
        saida_linha = f"{equipamento}:"
        for aluno in alunos:
            saida_linha += f"-{aluno}" if aluno != "-" else "- "
        saida.append(saida_linha)
    return saida

def salvar_saida(saida, nome_arquivo_saida):
    # salva a saida arquivo
    with open(nome_arquivo_saida, 'w', encoding='ISO-8859-1') as f:
        for linha in saida:
            f.write(f"{linha}\n")

def main():
    # lê o dir dos arquivos de entrada, processa os dados(cada .txt), aloca os horários com backtracking, gera e salva as saidas
    input_directory = '../entrada_1'
    output_directory = 'saida_1'
    os.makedirs(output_directory, exist_ok=True)

    for nome_arquivo_entrada in os.listdir(input_directory):
        if nome_arquivo_entrada.endswith('.txt'):
            caminho_completo_entrada = os.path.join(input_directory, nome_arquivo_entrada)
            nome_arquivo_saida = f"{output_directory}/saida_{nome_arquivo_entrada.split('_')[-1]}"

            with open(caminho_completo_entrada, 'r', encoding='ISO-8859-1') as f:
                entrada = f.read()

            dados = processar_entrada(entrada)
            horarios = alocar_tempo(dados)
            saida = gerar_saida(horarios)
            salvar_saida(saida, nome_arquivo_saida)

            print(f"O arquivo de saída '{nome_arquivo_saida}' foi gerado com sucesso.")

if __name__ == "__main__":
    main()
