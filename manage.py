from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from app.models import User
import unittest
import coverage
import os

# Initializing the manager
manager = Manager(app)

# Initialize flask migrate
migrate = Migrate(app, db)

# Adding Migration commands to the manager
manager.add_command('db', MigrateCommand)

# Test coverage configuration
COV = coverage.coverage(
    branch=True,
    include='app/*',
    omit=[
        'app/auth/__init__.py',
        'app/bucket/__init__.py',
        'app/bucketitems/__init__.py'
    ]
)
COV.start()


# Add test command
@manager.command
def test():
    """
    Run tests without coverage
    :return:
    """
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """
    Run tests with coverage
    :return:
    """
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Report')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1

# Run the manager
if __name__ == '__main__':
    manager.run()
