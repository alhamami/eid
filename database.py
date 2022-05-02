from datetime import datetime
from email.mime import message
from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pytz import country_names
from sqlalchemy import func


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


db = SQLAlchemy()
''''''

database_path = 'postgresql://postgres:SqzswPqlyMHAzfy0bQFZ@containers-us-west-48.railway.app:5975/railway'

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app,database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()





#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class User(db.Model):
    __tablename__ = 'User'

    userId = db.Column(db.Integer, primary_key=True , autoincrement=True)
    name = db.Column(db.String, nullable=True)
    message = db.Column(db.String, nullable=True)
    country = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=True)



#----------------------------------------------------------------------------#
#                               Query section.                               #
#----------------------------------------------------------------------------#


def registerUser(username , message , country, image):

    try:
        
        prim_qry = db.session.query(func.max(User.userId)).all()[0][0]
        if(prim_qry is None):
            prim_qry = 0
        
        
        newUser = User(userId = prim_qry+1 , name = username ,  message = message , country = country, image=image)

        db.session.add(newUser)
        db.session.commit()
        print("User added successfully")
        db.session.close()
        return True

    except:
        db.session.rollback()
        print("There is an error in adding the user")
        db.session.close()
        return False


def displayLastFive():

    names = []
    messages = []
    countries = []
    images = []

    qry = db.session.query(User.name ,User.message , User.country, User.image).order_by(User.userId.desc()).limit(5).all()

    if len(qry) == 0:
        print("Empty table!")
        return names ,messages , countries, images
    
    for i in range(len(qry)):
        names.append(qry[i][0])
        messages.append(qry[i][1])
        countries.append(qry[i][2])
        images.append(qry[i][3])

    print(names)
    print(messages)
    print(countries)


    return names , messages , countries, images


def displayFiveMostcountries():
    qry = db.session.query(User.country, func.count(User.country)).group_by(User.country).all()
    print(qry)


#if __name__ == '__main__':
    #check = registerUser("oooor" , "eeeee" , "qqqqqqq","")
    #print(check)
    #displayLastFive()

    #displayFiveMostcountries()




