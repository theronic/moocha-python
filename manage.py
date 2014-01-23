from flask_script import Manager
from notify import app
import nose

manager = Manager(app)

@manager.command
def test():
	nose.main(argv=['notify'])

def main():
	manager.run()

if __name__ == '__main__':
	main()
