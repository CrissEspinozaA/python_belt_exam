from flask_app import app # import app from flask_app.py
from flask_app.controllers import routes

if __name__ == '__main__': # if this file is run directly, run the app
    app.run(debug=True)  # run the app in debug mode