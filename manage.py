from flask_script import Manager, Shell
from moocha import create_app, sender_instance, db
from moocha.gumtree import Gumtree
from moocha import models
import nose

app = create_app()

gumtree_instance = Gumtree

manager = Manager(app)

def make_shell_context():
	return dict(
		app=app,
		gt=gumtree_instance,
		models=models,
		db=db,
	)

manager.add_command('shell', Shell(make_context=make_shell_context))

@manager.command
def create_all():
	db.create_all()

@manager.command
def send_emails():
	sender_instance.process_email_rules()

@manager.command
def test():
	nose.main(argv=['moocha', '--failed'])

#TODO: Implement a dev command which runs create_all and then runs the server.

def main():
	manager.run()

if __name__ == '__main__':
	main()
