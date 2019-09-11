"""
Handles mangement commands.
"""

from flask_script import Manager
from flask import Flask
from factory import initialize_app

app = Flask(__name__)
app = initialize_app(app)
manager = Manager(app)

# register management command.

if __name__ == "__main__":
    manager.run()
