from flask import Flask, render_template, request, redirect, flash, send_from_directory, url_for 
import os
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from extensions import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from forms import AddProduct, LoginForm, RegistrationForm
from models import Product, User

products = [
    {"name": "ოპტიკური ჩარჩო – George Piralli 2125", "price": 149, "file": "/static/images/1.jpg", "id": "1"},
    {"name": "ოპტიკური ჩარჩო – George Piralli 2204", "price": 99, "file": "/static/images/2.jpg", "id": "2"}, 
    {"name": "SEVEN 8243 C3, კომპიუტერის მზა სათვალე ბუდით", "price": 49, "file": "/static/images/3.png", "id": "3"},
    {"name": "SEVEN 8243 C2, კომპიუტერის მზა სათვალე ბუდით", "price": 97, "file": "/static/images/4.png", "id": "4"},
    {"name": "ოპტიკური ჩარჩო – Emporio Armani EA1041", "price": 89, "file": "/static/images/5.jpg", "id": "5"},
    {"name": "ოპტიკური ჩარჩო – George Piralli 2404", "price": 100, "file": "/static/images/6.jpg", "id": "6"},
    {"name": "ოპტიკური ჩარჩო – Fendi F893 317 Green Rectangular Glitter Logos 51-14-130", "price": 77, "file": "/static/images/7.PNG", "id": "7"},
    {"name": "ოპტიკური ჩარჩო – MP 20213 Bk", "price": 119, "file": "/static/images/8.PNG", "id": "8"},
]

@app.route("/populate_data")
def populate_data():
    product = Product.query.get(id)

    for product_data in products:
        product = Product(name=product_data["name"], price=product_data["price"], file=product_data["file"])
        db.session.add(product)

    db.session.commit()
    print(Product.query.all())
    return redirect("/")

@app.route('/')
def index():
    products = Product.query.all()
    for product in products:
        app.logger.info(f"Product Name: {product.name}, File: {product.file}")
    return render_template('index.html', products=products)

@app.route('/details/<int:id>')
def product_details(id):
    product = Product.query.get_or_404(id)
    return render_template('details.html', product=product)

@app.route('/home')
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You successgfully registered", category="success")
        redirect("/")
    return render_template("register.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        exists = User.query.filter(User.username==form.username.data).first()
        print(exists)
        if exists and exists.password == form.password.data:
            login_user(exists)
            flash("წარმატებით შეხვედით პროფილზე!", category="success")
            return redirect("/")

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/addproduct", methods=["GET", "POST"])
@login_required
def add_product():
    if current_user.role == 'admin':
        form = AddProduct()
        if form.validate_on_submit():
            file = request.files.get('file')
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                product = Product(name=form.name.data, 
                                  price=form.price.data, 
                                  file=f"/static/images/{filename}")
                db.session.add(product)
                db.session.commit()
                flash("წარმატებით დაემატა პროდუქტი!", category="success")
                return redirect(url_for("index"))
            flash("Failed to upload file!", category="danger")
        return render_template("addproduct.html", form=form)
    else:
        flash("!!მხოლოდ ადმინებისთვის!!", category="danger")
        return redirect(url_for('index'))

    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    if current_user.role == 'admin':
        product = Product.query.get_or_404(id)
        form = AddProduct(obj=product)
        
        if form.validate_on_submit():
            form.populate_obj(product)
            
            file = request.files.get('file')
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                product.file = f"/static/images/{filename}"
            
            db.session.commit()
            flash("წარმატებით დარედაქტირდა პროდუქტი!", category="success")
            return redirect(url_for('index'))
        
        return render_template('addproduct.html', form=form, product=product)
    else:
        flash("!!მხოლოდ ადმინებისთვის!!", category="danger")
        return redirect(url_for('index'))


@app.route('/delete_product/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    if current_user.role == 'admin':
        product_to_delete = Product.query.get_or_404(id)
        try:
            db.session.delete(product_to_delete)
            db.session.commit()
            flash("წარმატებით წაიშალა პროდუქტი!", category="success")
        except Exception as e:
            flash(f"There was a problem deleting the product: {str(e)}", category="danger")
        return redirect(url_for('index'))
    else:
        flash("!!მხოლოდ ადმინებისთვის!!", category="danger")
        return redirect(url_for('index'))

