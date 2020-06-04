from random import randint, randrange
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, Product
from .main.views import buy

def users(count=100):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='password',
                 confirmed=True,
                 name=fake.name(),
                 member_since=fake.past_date(),
                 balance=randrange(0,50,5)
        )
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()
            
def products(count=10):
    fake = Faker()
    i = 0
    # class Product(db.Model):
    # #ie a particular chocolate or drink
    # __tablename__ = 'products'
    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(64), unique=True)
    # description = db.Column(db.String(128))
    # barcode = db.Column(db.String(64), unique=True)
    # current_price = db.Column(db.Numeric(precision=5, scale=2, asdecimal=True))
    # purchases = db.relationship('Purchase', backref='product', lazy='dynamic')
    # url = db.Column(db.String(128))
    while i < count:
        u = Product(name=fake.user_name(),
                 description=fake.text(30),
                 barcode=randint(1000000,9999999),
                 current_price=fake.random_element(elements=(1.2,1.5,0.5,1.0)),
                 url=fake.image_url()
        )
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

def purchases(count=100):
    fake = Faker()
    user_count = User.query.count()
    product_count = Product.query.count()
    for i in range(count):
        p = Product.query.offset(randint(0, product_count - 1)).first()
        u = User.query.offset(randint(0, user_count - 1)).first()
        buy(u,p)
