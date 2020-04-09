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
                 site=fake.random_element(elements=('FMB','EDN')),
                 building=str(randint(1,99)),
                 room="{}.{}".format(randint(0,5),randint(1,30)),
                 member_since=fake.past_date(),
                 balance=randrange(0,50,5)
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
