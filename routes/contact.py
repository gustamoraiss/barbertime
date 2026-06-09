from flask import Blueprint, render_template

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/contato')
def contato():
    return render_template('contato.html')