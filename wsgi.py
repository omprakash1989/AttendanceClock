from factory import initialize_app
from flask import Flask

application = Flask(__name__, instance_relative_config=True)
initialize_app(application)

if __name__ == '__main__':
    application.run()
