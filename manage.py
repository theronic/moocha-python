from flask_script import Manager, Shell
from notify import create_app
from notify.gumtree import Gumtree
import nose

app = create_app()

gumtree_instance = Gumtree

manager = Manager(app)

def make_shell_context():
	return dict(
		app=app,
		gt=gumtree_instance,
	)

manager.add_command('shell', Shell(make_context=make_shell_context))

@manager.command
def test():
	nose.main(argv=['notify'])

def main():
	manager.run()

if __name__ == '__main__':
	main()
