
import os
from flask import Flask, render_template, request
from regex import P
from database import setup_db
import database as db
from flask_cors import CORS
from werkzeug.utils import secure_filename

MYDIR = os.path.dirname(__file__)
UPLOAD_FOLDER = MYDIR+'/static/img/picture'



def create_app(test_config=None):
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    setup_db(app)
    CORS(app)
    

    @app.route('/',  methods=['GET','POST'])
    def index():

        names , messages , countries, images = [], [], [], []
        if request.method == 'POST':
            name = request.form['name']
            country = request.form['country']
            message = request.form['comment']
            image = request.files['img']
            filename = ""
            if image.filename != "":
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            if name != "" and country != "" and image!= "" and message != "":
                if filename != "":
                    filename = "/static/img/picture/" + filename
                else:
                    filename = "/static/img/picture/profile.png"

                addComment = db.registerUser(name , message , country, filename)
                print("Info == ", name, country, image, message, addComment, filename)

        names , messages , countries, images =  db.displayLastFive()
        

        return render_template("index.html",  info=zip(names,messages,countries, images))




    return app 

app = create_app()	
# main driver function
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")