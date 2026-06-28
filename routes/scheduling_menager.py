from datetime import datetime

def limpar_agendamentos_expirados():
    caminho_csv = 'data/agendamentos.csv'

    arquivo = open(caminho_csv, mode='r')

    linhas = arquivo.readlines()
    
    arquivo.close()

    cabecalho = linhas[0]
    dados_restantes = linhas[1:]
    
    agendamentos_validos = []
    formato_data_hora = "%Y-%m-%d %H:%M"
    agora = datetime.now()

    
    for linha in dados_restantes:
        linha_limpa = linha.strip()
        colunas = linha_limpa.split(',')
        
        data_texto = colunas[1]
        horario_texto = colunas[3]
        
        data_hora_agendamento = datetime.strptime(f"{data_texto} {horario_texto}", formato_data_hora)
            
        if data_hora_agendamento >= agora:
            agendamentos_validos.append(linha)

    arquivo_escrita = open(caminho_csv, mode='w')

    arquivo_escrita.write(cabecalho)
    for linha_valida in agendamentos_validos:
        arquivo_escrita.write(linha_valida)

    arquivo_escrita.close() 