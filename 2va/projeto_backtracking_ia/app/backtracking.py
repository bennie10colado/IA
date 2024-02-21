import os
from collections import defaultdict

def processar_entrada(entrada):
    linhas = entrada.strip().split('\n')
    dados = {}
    for linha in linhas:
        equipamento, alunos_str = linha.split(':')
        alunos = alunos_str.split(';')[:-1]
        dados[equipamento.strip()] = {aluno.split('=')[0]: int(aluno.split('=')[1]) for aluno in alunos}
    return dados

def alocar_tempo(dados):
    horarios_alocados = {equipamento: ["-" for _ in range(12)] for equipamento in dados}
    alocacoes = defaultdict(lambda: defaultdict(int))  
    todos_alunos = {aluno for alunos in dados.values() for aluno in alunos}

    def backtrack(equipamento, horario):
        if equipamento == len(dados):  
            return True
        if horario == 12:  
            return backtrack(equipamento + 1, 0)
        
        for aluno in todos_alunos:
            if pode_alocar(equipamento, horario, aluno):
                realizar_alocacao(equipamento, horario, aluno)
                if backtrack(equipamento, horario + 1):
                    return True
                desfazer_alocacao(equipamento, horario, aluno)
        
        return False  

    def pode_alocar(equipamento, horario, aluno):
        equipamento_atual = list(dados)[equipamento]
        if aluno not in dados[equipamento_atual] or alocacoes[equipamento_atual][aluno] >= dados[equipamento_atual][aluno]:
            return False
        for eq, horarios_eq in horarios_alocados.items():
            if horarios_eq[horario] == aluno:
                return False
        return True

    def realizar_alocacao(equipamento, horario, aluno):
        equipamento_atual = list(dados)[equipamento]
        horarios_alocados[equipamento_atual][horario] = aluno
        alocacoes[equipamento_atual][aluno] += 1

    def desfazer_alocacao(equipamento, horario, aluno):
        equipamento_atual = list(dados)[equipamento]
        horarios_alocados[equipamento_atual][horario] = "-"
        alocacoes[equipamento_atual][aluno] -= 1

    if backtrack(0, 0):
        return horarios_alocados
    else:
        return None  

def gerar_saida(horarios):
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
    with open(nome_arquivo_saida, 'w', encoding='ISO-8859-1') as f:
        for linha in saida:
            f.write(f"{linha}\n")

def main():
    input_directory = '../entrada_50'
    output_directory = 'saida'
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
