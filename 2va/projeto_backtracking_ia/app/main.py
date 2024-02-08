import os
import glob

def ler_entradas(diretorio):
    arquivos = glob.glob(os.path.join(diretorio, 'entrada_*.txt'))
    resultados = []
    
    for arquivo in sorted(arquivos):
        with open(arquivo, 'r') as f:
            conteudo = f.read()
            equipamentos = processar_conteudo(conteudo)
            resultado = alocar(equipamentos)
            resultados.append((arquivo, resultado))
    
    return resultados

def processar_conteudo(conteudo):
    #conversão do conteúdo do arquivo 
    pass

def alocar(equipamentos):
    # backtracking
    pass

def salvar_saida(arquivo_saida, resultado):
    with open(arquivo_saida, 'w') as f:
        for equipamento, alunos in resultado.items():
            f.write(f"{equipamento}:")
            for aluno in alunos:
                f.write(f"-{aluno} ")
            f.write("\n")

diretorio_entradas = '../entrada_50'

diretorio_saidas = 'saida/'

os.makedirs(diretorio_saidas, exist_ok=True)

resultados = ler_entradas(diretorio_entradas)
for arquivo, resultado in resultados:
    nome_arquivo_saida = os.path.basename(arquivo).replace('entrada', 'saida')
    arquivo_saida = os.path.join(diretorio_saidas, nome_arquivo_saida)
    if resultado:
        salvar_saida(arquivo_saida, resultado)
    else:
        print(f'Não foi possível realizar a alocação para {arquivo}')
