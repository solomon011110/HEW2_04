from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import Project
from app import db

bp = Blueprint('project', __name__)

@bp.route('/projects', methods=['GET'])
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

@bp.route('/project/<int:id>', methods=['GET'])
def project_detail(id):
    project = Project.query.get_or_404(id)
    return render_template('project_detail.html', project=project)

@bp.route('/project/create', methods=['GET', 'POST'])
@login_required
def create_project():
    if request.method == 'POST':
        # プロジェクト作成処理
        pass
    return render_template('create_project.html')