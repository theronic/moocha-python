from flask_script import Manager, Shell
from notify import create_app, sender_instance, db
from notify.gumtree import Gumtree
from notify import models
import nose

app = create_app('sqlite:///hello.db')

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
	sender_instance.send_emails()

@manager.command
def test():
	nose.main(argv=['notify'])

def main():
	manager.run()

if __name__ == '__main__':
	main()
