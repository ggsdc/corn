from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from cornflow.commands import *

from cornflow.app import create_app, db

env_name = 'development'
app = create_app(env_name)

migrate = Migrate(app=app, db=db)
manager=Manager(app=app)

manager.add_command('db', MigrateCommand)
manager.add_command('create_super_user', CreateSuperAdmin)
manager.add_command('clean_historic_data', CleanHistoricData)

if __name__ == '__main__':
    manager.run()