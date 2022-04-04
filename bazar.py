
from crypt import methods
import imghdr
from pydoc import render_doc
from turtle import turtlesize
from unicodedata import category
from warnings import catch_warnings
from flask import Flask, render_template, request, redirect, session, flash, url_for
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import urllib.request
import uuid
from datetime import date

### app settings ###

app = Flask(__name__)
app.secret_key = "jsiodjfiewnown7881U2HD912HND912"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.sqlite3"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)



### images setting ###

UPLOAD_FOLDER = "//Users/jiridofek/desktop/Coding project portfolio/lezeckybazar.cz/static/post_img"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024 

ALLOWED_EXTENSIONS = set (["png", "jpg", "jpeg"])

def allowed_file (filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS



### database model ###

class Posts(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    date = db.Column("date", db.String(100))
    sport = db.Column("sport", db.String(100))
    category = db.Column("category", db.String(100))
    post_name = db.Column("post_name", db.String(100))
    description = db.Column("description", db.String(100))
    image = db.Column("image", db.String(200))
    price = db.Column("price", db.String(100))
    location = db.Column("location", db.String(100))
    person_name = db.Column("person_name", db.String(100))
    contact = db.Column("contact", db.String(100))
    password = db.Column("password", db.String(100))

    def __init__(self, date, sport, category, post_name, description, image, price, location, person_name, contact, password):
        self.date = date
        self.sport = sport
        self.category = category
        self.post_name = post_name
        self.description = description
        self.image = image
        self.price = price
        self.location = location
        self.person_name = person_name
        self.contact = contact
        self.password = password

##############################################################################################################

###################
##### Routes #################################################################################################
###################

##############################################################################################################










@app.route("/", methods=["POST", "GET"])
def home():


    return render_template("home.html")





########################################################################################################################################################
######## routes - 3 sports ##############
########################################################################################################################################################


@app.route("/lezeni/vse/<int:page_num>", methods=["POST", "GET"]) ### all categories ###
def all(page_num):

    location_filter = ""

    if "location_filter" in session:

        location_filter = session["location_filter"]
        location_tag = location_filter
        posts = Posts.query.filter_by(sport = "1",location = location_filter).order_by(Posts._id.desc()).paginate(per_page=2, page=page_num, error_out=True )

    else:

        posts = Posts.query.filter_by(sport = "1").order_by(Posts._id.desc()).paginate(per_page=2, page=page_num, error_out=True )
  
        
    
  
    

    if request.method == "POST":

        location_filter = request.form["location_filter"]


        if location_filter != "all":

            posts = Posts.query.filter_by(sport = "1", location = location_filter).order_by(Posts._id.desc()).paginate(per_page=2, page=page_num, error_out=True )
            
            session["location_filter"] = location_filter
            
        
        else:
            posts = Posts.query.filter_by(sport = "1").order_by(Posts._id.desc()).paginate(per_page=2, page=page_num, error_out=True )
            session.pop("location_filter", None)
    
    


        
    
    return render_template ("all_categories.html", posts = posts, location_tag = location_filter)



@app.route("/lezecky/<int:page_num>", methods=["POST", "GET"]) ### lezecky category ###
def lezecky(page_num):

    posts = Posts.query.filter_by(category = "Lezecky").order_by(Posts._id.desc()).paginate(per_page=2, page=page_num, error_out=True )
    location_tag = ""

    if request.method == "POST":

        location_filter = request.form["location_filter"]

        if location_filter != "all":

            posts = Posts.query.filter_by(category = "Lezecky", location = location_filter).order_by(Posts._id.desc()).paginate(per_page=2, page=page_num, error_out=True )
            location_tag = location_filter

    return render_template ("lezecky.html", posts = posts, location_tag = location_filter)












##################################
## adding new post - 3 variants ##
####### + choose sport  ##########
##################################

@app.route("/pridat-inzerat", methods=["POST", "GET"]) ### choose sport, where you want to insert
def choose_sport ():

    return render_template("choose_sport.html")



@app.route("/pridat-inzerat/drytool", methods=["POST", "GET"]) ### adding new post ###
def add_post_ice ():



    
    if request.method == "POST":




        category = request.form["category"]
        post_name = request.form["post_name"]
        description = request.form["description"]
        price = request.form["price"]
        location = request.form["location"]
        person_name = request.form["person_name"]
        contact = request.form["contact"]
        password = request.form["password"]
               
        
        if request.files:






            image = request.files["image"]
            filename = str(uuid.uuid4().hex + ".jpg")
            
            

            if image and allowed_file(image.filename):
                
                image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                new_post = Posts(date = date.today().strftime("%d/%m/%Y"), sport = "3", category = category, post_name = post_name, description = description, image = filename, price = price, location = location, person_name = person_name, contact = contact, password = password )
                db.session.add(new_post)
                db.session.commit()
                
                
            else:
                image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                new_post = Posts(date = date.today().strftime("%d/%m/%Y"), sport = "3", category = category, post_name = post_name, description = description, image= filename, price = price, location = location, person_name = person_name, contact = contact, password = password )
                db.session.add(new_post)
                db.session.commit()
                


        

    return render_template("add_ice.html")

@app.route("/pridat-inzerat/vhs", methods=["POST", "GET"]) ### adding new post in VHS ###
def add_post_vhs ():



    
    if request.method == "POST":




        category = request.form["category"]
        post_name = request.form["post_name"]
        description = request.form["description"]
        price = request.form["price"]
        location = request.form["location"]
        person_name = request.form["person_name"]
        contact = request.form["contact"]
        password = request.form["password"]
               
        
        if request.files:






            image = request.files["image"]
            filename = str(uuid.uuid4().hex + ".jpg")
            
            

            if image and allowed_file(image.filename):
                
                image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                new_post = Posts(date = date.today().strftime("%d/%m/%Y"), sport = "2", category = category, post_name = post_name, description = description, image = filename, price = price, location = location, person_name = person_name, contact = contact, password = password )
                db.session.add(new_post)
                db.session.commit()
                
                
            else:
                image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                new_post = Posts(date = date.today().strftime("%d/%m/%Y"), sport = "2", category = category, post_name = post_name, description = description, image= filename, price = price, location = location, person_name = person_name, contact = contact, password = password )
                db.session.add(new_post)
                db.session.commit()
                


        

    return render_template("add_vhs.html")





@app.route("/pridat-inzerat/lezeni", methods=["POST", "GET"]) ### adding new post ###
def add_post_climbing ():



    
    if request.method == "POST":



        category = request.form["category"]
        post_name = request.form["post_name"]
        description = request.form["description"]
        price = request.form["price"]
        location = request.form["location"]
        person_name = request.form["person_name"]
        contact = request.form["contact"]
        password = request.form["password"]
               
        
        if request.files:






            image = request.files["image"]
            filename = str(uuid.uuid4().hex + ".jpg")
            
            

            if image and allowed_file(image.filename):
                
                image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                new_post = Posts(date = date.today().strftime("%d/%m/%Y"), sport = "1", category = category, post_name = post_name, description = description, image = filename, price = price, location = location, person_name = person_name, contact = contact, password = password )
                db.session.add(new_post)
                db.session.commit()
                
                
            else:
                image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                new_post = Posts(date = date.today().strftime("%d/%m/%Y"), sport = "1", category = category, post_name = post_name, description = description, image= filename, price = price, location = location, person_name = person_name, contact = contact, password = password )
                db.session.add(new_post)
                db.session.commit()
                


        

    return render_template("add_climbing.html")



@app.route("/smazat-inzerat", methods=["POST", "GET"])
def smazat():

    posts = ""

    if request.method == "POST":

        contact = request.form.get("contact") ### which form was send ###

        

        if contact is not None : ### searching for posts to delete ###
            contact = request.form["contact"]
            password = request.form["password"]
            posts = Posts.query.filter_by(contact = contact, password = password).order_by(Posts._id.desc()).all()
        
        else: ### deleting post and image from folder ###
            id = request.form["_id"]
            post = Posts.query.filter_by(_id = id).first()
            post_img = post.image
            os.remove("//Users/jiridofek/desktop/Coding project portfolio/lezeckybazar.cz/static/post_img/" + post_img)
            Posts.query.filter_by(_id = id).delete()
            db.session.commit()
            flash("Inzerat byl uspesne smazan.")
            
            print(id)

        





    return render_template("delete_post.html", posts = posts)







if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)
