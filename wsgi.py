from factory import initialize_app
from flask import Flask
import os


application = Flask(__name__, instance_relative_config=True)
initialize_app(application)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port)
