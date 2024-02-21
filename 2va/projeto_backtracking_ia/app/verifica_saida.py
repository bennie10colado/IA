import os
from collections import defaultdict

def ler_arquivos_de_diretorio(diretorio):
    """Lê todos os arquivos em um diretório e retorna um dicionário com o conteúdo."""
    conteudos = {}
    for nome_arquivo in os.listdir(diretorio):
        caminho_completo = os.path.join(diretorio, nome_arquivo)
        with open(caminho_completo, 'r', encoding='ISO-8859-1') as arquivo:
            conteudos[nome_arquivo] = arquivo.read()
    return conteudos

def verificar_saida(dados_entrada, dados_saida):
    requisitos = {}
    for linha in dados_entrada.strip().split('\n'):
        equipamento, detalhes = linha.split(':')
        for detalhe in detalhes.split(';'):
            if detalhe:
                aluno, vezes = detalhe.split('=')
                if aluno not in requisitos:
                    requisitos[aluno] = {}
                requisitos[aluno][equipamento] = int(vezes)
                
    alocacoes_por_hora = [set() for _ in range(12)]
    erros = []

    for linha in dados_saida.strip().split('\n'):
        equipamento, alunos_alocados_str = linha.split(':')
        alunos_alocados = alunos_alocados_str.split('-')[1:]
        contagem_alocacoes = {}
        
        for hora, aluno in enumerate(alunos_alocados):
            if aluno not in contagem_alocacoes:
                contagem_alocacoes[aluno] = 0
            contagem_alocacoes[aluno] += 1

            if aluno in alocacoes_por_hora[hora]:
                erros.append(f"Alocação simultânea encontrada para {aluno} no horário {hora}.")
            else:
                alocacoes_por_hora[hora].add(aluno)
        
        for aluno, vezes in contagem_alocacoes.items():
            if aluno in requisitos and equipamento in requisitos[aluno] and requisitos[aluno][equipamento] != vezes:
                erros.append(f"Inconsistência encontrada: {aluno} deveria estar alocado {requisitos[aluno][equipamento]} vezes em {equipamento}, mas está {vezes} vezes.")
    
    if erros:
        for erro in erros:
            print(erro)
    else:
        print("Todas as alocações estão corretas e sem alocações simultâneas para o arquivo analisado.")

def main():
    # Ajuste os caminhos conforme necessário para o seu ambiente
    input_directory = '../entrada_50'
    output_directory = 'saida'

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

if __name__ == "__main__":
    main()
