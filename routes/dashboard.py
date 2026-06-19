from flask import Blueprint, render_template
from datetime import datetime
from .scheduling import ler_agendamentos

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    linhas_csv = ler_agendamentos()
    agendamentos_reais = []
    
    for linha in linhas_csv:
        linha_limpa = linha.strip()
        
        if not linha_limpa:
            continue
            
        dados = [d.strip() for d in linha_limpa.split(',')]
        
        if len(dados) == 6 and all(dados):
            agendamento_dict = {
                "servico": dados[0],
                "data": dados[1],
                "barbeiro": dados[2],
                "horario": dados[3],
                "nome": dados[4],
                "telefone": dados[5]
            }
            
            try:
                data_hora_str = f"{dados[1]} {dados[3]}"
                agendamento_dict["datetime_obj"] = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M")
            except ValueError:
                agendamento_dict["datetime_obj"] = datetime.max
                
            agendamentos_reais.append(agendamento_dict)
            
    agendamentos_reais.sort(key=lambda x: x["datetime_obj"])
            
    return render_template('dashboard.html', agendamentos=agendamentos_reais)