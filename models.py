from extensions import app, db
from flask_login import LoginManager, UserMixin
from extensions import login_manager

class Product(db.Model):
    name = db.Column(db.String)
    file = db.Column(db.String)
    price = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)

    def __str__(self):
        return f"{self.name}"


class User(db.Model, UserMixin):
    username = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.String)
    password = db.Column(db.String, nullable=False)
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, username, password, role="guest"):
        self.username = username 
        self.password = password
        self.role = role

    def __str__(self):
        return f"{self.username}"

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # users
        admin = User(username="salomenarimanidze", password="$salome7256", role="admin")
        user = User(username="salome123", password="salome123")

        db.session.add_all([user, admin])
        db.session.commit()

        # products
        products = [
            Product(name='ოპტიკური ჩარჩო – George Piralli 2125', file='/static/images/1.jpg', price=149),
            Product(name='ოპტიკური ჩარჩო – George Piralli 2204', file='/static/images/2.jpg', price=99),
            Product(name='SEVEN 8243 C3, კომპიუტერის მზა სათვალე ბუდით', file='/static/images/3.png', price=49),
            Product(name='SEVEN 8243 C2, კომპიუტერის მზა სათვალე ბუდით', file='/static/images/4.png', price=97),
            Product(name='ოპტიკური ჩარჩო – Emporio Armani EA1041', file='/static/images/5.jpg', price=89),
            Product(name='ოპტიკური ჩარჩო – George Piralli 2404', file='/static/images/6.jpg', price=100),
            Product(name='ოპტიკური ჩარჩო – Fendi F893 317 Green Rectangular Glitter Logos 51-14-130', file='/static/images/7.PNG', price=77),
            Product(name='ოპტიკური ჩარჩო – MP 20213 Bk', file='/static/images/8.PNG', price=119)
        ]

        db.session.add_all(products)
        db.session.commit()