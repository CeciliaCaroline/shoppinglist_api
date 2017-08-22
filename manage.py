from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db

# Initializing the manager
manager = Manager(app)

# Initialize flask migrate
migrate = Migrate(app, db)

# Adding Migration commands to the manager
manager.add_command('db', MigrateCommand)

# Run the manager
if __name__ == '__main__':
    manager.run()
