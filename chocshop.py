import os
from app import create_app, db
from app.models import User, Role, Purchase, Product
from flask_migrate import Migrate, upgrade

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db, compare_type=True)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Product=Product, Purchase=Purchase)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()

    # create or update user roles
    Role.insert_roles()




