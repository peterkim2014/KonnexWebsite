from flask import render_template, redirect, request, flash, session
from flask_app import app


@app.route('/product')
def product_page():
    return render_template("product.html")