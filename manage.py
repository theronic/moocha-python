from flask_script import Manager
from notify import app

manager = Manager(app)

def main():
	manager.run()

if __name__ == '__main__':
	main()
