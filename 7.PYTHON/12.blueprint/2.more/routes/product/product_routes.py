from flask import Blueprint, render_template

product_blreprint = Blueprint('product', __name__, template_folder="../../templates/product")

@product_blreprint.route('/')
def product_page():
    return render_template('product.html')

@product_blreprint.route('/detail')
def product_detail_page():
    return render_template('product_detail.html')