from flask_app import app
from flask_app.controllers import homes, products, abouts, contacts, blogs

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')