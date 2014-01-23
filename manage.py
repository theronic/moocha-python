from flask_script import Manager, Shell
from notify import app, gt, emailer
import nose

manager = Manager(app)

def make_shell_context():
	return dict(
		app=app,
		gt=gt,
		emailer=emailer,
	)

manager.add_command('shell', Shell(make_context=make_shell_context))

@manager.command
def test():
	nose.main(argv=['notify'])

def main():
	manager.run()

if __name__ == '__main__':
	main()
