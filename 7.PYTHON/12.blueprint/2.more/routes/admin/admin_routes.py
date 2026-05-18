from flask import Blueprint, render_template

admin_blueprint = Blueprint('admin', __name__, template_folder="../../templates/admin")

@admin_blueprint.route('/')
def admin_age():
    return render_template('admin.html')