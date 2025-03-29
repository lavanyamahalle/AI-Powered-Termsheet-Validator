from flask import Blueprint, render_template
from .models import Document

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    documents = Document.query.all()
    return render_template('index.html', documents=documents)
