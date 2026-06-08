from flask import Blueprint, render_template

scheduling_bp = Blueprint('scheduling', __name__)

@scheduling_bp.route('/agendamento')
def agendamento():
    return render_template('agendamento.html')