# imports
# from crypt import methods
from unicodedata import category
from unittest import result
from warnings import catch_warnings
from flask import Flask, jsonify, render_template, request, redirect, session, flash, url_for

from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import urllib.request
import uuid
from datetime import date

# app settings 

app = Flask(__name__)

app.secret_key = "jsiodjfiewnown7881U2HD912HND912"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.sqlite3"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)



# images setting - folder + allowed files 

UPLOAD_FOLDER = "//Users/jiridofek/desktop/Coding project portfolio/lezeckybazar.cz/static/post_img/" 
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024 

ALLOWED_EXTENSIONS = set (["png", "jpg", "jpeg"])

def allowed_file (filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS



# database model 

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







# home page #


@app.route("/", methods=["POST", "GET"])
def home():


    return render_template("home.html")


# posts page #


@app.route("/lezeni/<int:page_num>", methods=["POST", "GET"])
def all(page_num):

    session.permanent = False

    location_filter = ""
    category = ""


    # user already have some filter active

    if "location_filter" in session or "category" in session:

        # location and category filter active
        if "location_filter" in session and "category" in session:

            location_filter = session["location_filter"]
            category = session["category"]
            posts = Posts.query.filter(Posts.location.in_(location_filter), Posts.sport == "1",Posts.category.in_(category)).order_by(Posts._id.desc()).paginate(per_page=6, page=page_num, error_out=False )

        else:
            # only location filter is used
            if "location_filter" in session:

                location_filter = session["location_filter"]
                posts = Posts.query.filter(Posts.location.in_(location_filter), Posts.sport == "1").order_by(Posts._id.desc()).paginate(per_page=6, page=page_num, error_out=False )

            # only category filter used    
            else:

                category = session["category"]
                posts = Posts.query.filter(Posts.sport == "1",Posts.category.in_(category)).order_by(Posts._id.desc()).paginate(per_page=6, page=page_num, error_out=False )



    # user doesnt use any filter

    else:

        posts = Posts.query.filter_by(sport = "1").order_by(Posts._id.desc()).paginate(per_page=6, page=page_num, error_out=False )
  
        
    
  
    # user just clicked on filter button and we have to store them in sessions

    if request.method == "POST":
        
        

        location_filter = "all"


        # request, which selects were selected
        category = list(request.form.keys())
        
       
        # we need to seperate cities filter and category filter 

        cities = ["Brno", "Ostrava", "Praha", "Plzeň", "Olomouc", "Zlín", "Písek", "České Budějovice", "Ústí nad Labem", "Liberec", "Hradec Králové", "Písek", "Jihlava"]
        location_filter = []
        
        for i in cities:


            try:

               category.remove(str(i))
               location_filter.append(str(i))
               


            
            except ValueError:

               pass

        
       # something is selected, form is not empty 

        if location_filter or category:

            # selected location and category
            if location_filter and category:

                posts = Posts.query.filter(Posts.location.in_(location_filter), Posts.sport == "1",Posts.category.in_(category)).order_by(Posts._id.desc()).paginate(per_page=6, page=page_num, error_out=False )
                
                session["location_filter"] = location_filter
                session["category"] = category
            
            else:
                # selected location only
                if location_filter:

                    posts = Posts.query.filter(Posts.location.in_(location_filter), Posts.sport == "1").order_by(Posts._id.desc()).paginate(per_page=6, page=page_num, error_out=False )
                
                    session["location_filter"] = location_filter
                    session.pop("category", None)
                
                # selected category only
                else:
                    
                    posts = Posts.query.filter(Posts.sport == "1",Posts.category.in_(category)).order_by(Posts._id.desc()).paginate(per_page=6, page=page_num, error_out=False )
                
                    
                    session["category"] = category
                    session.pop("location_filter", None)
                    
                
        # form was sent with no select (empty form)

        else:

            posts = Posts.query.filter_by(sport = "1").order_by(Posts._id.desc()).paginate(per_page=6, page=page_num, error_out=False )
            session.pop("location_filter", None)
            session.pop("category", None)
    
        return redirect("/lezeni/1")
    
    


        
    
    return render_template ("all_categories.html", posts = posts, location_tag = location_filter, category = category)

    
# single post view - user selected from list of post     

@app.route("/inzerat/<int:_id>")
def individual_post(_id):

    post = Posts.query.get_or_404(_id)

    return render_template("post.html", posts = post)


# location filter delete 

@app.route("/vymazat-lokaci")
def delete_location():
    previous_page = request.referrer
    session.pop("location_filter", None)
    return redirect(previous_page)

 # category filter delete    

@app.route("/vymazat-kategorii")
def delete_category():
    previous_page = request.referrer
    session.pop("category", None)
    return redirect(previous_page)


##################################
## adding new post - 3 variants ##
# only one is active #
##################################


# user will choose sport, where post will be added

@app.route("/pridat-inzerat", methods=["POST", "GET"]) ### choose sport, where you want to insert
def choose_sport ():

    return render_template("choose_sport.html")


# add to drytool
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


# add to vhs
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


# add to sport climbing - bouldering

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
                


        return redirect(url_for(("all"), page_num = 1))

    return render_template("add_climbing.html")


# webpage api in JSON - ready for use - all posts

@app.route("/api")
def api():

    posts = Posts.query.all()
    output = []

    for post in posts:
        currentpost = {}
        currentpost ["post._id"] = post._id
        currentpost ["post_name"] = post.post_name
        currentpost ["date"] = post.date
        currentpost ["sport"] = post.sport
        currentpost ["category"] = post.category
        currentpost ["description"] = post.description
        currentpost ["price"] = post.price
        currentpost ["person_name"] = post.person_name
        currentpost ["location"] = post.location
        currentpost ["contact"] = post.contact
        

        output.append(currentpost)

    return jsonify(output)


# user wants to delete post

@app.route("/smazat-inzerat", methods=["POST", "GET"])
def smazat():

    posts = ""
    progress = "50"

    if request.method == "POST":

        contact = request.form.get("contact") ### which form was send ###

        

        if contact is not None : ### searching for posts to delete ###
            contact = request.form["contact"]
            password = request.form["password"]
            posts = Posts.query.filter_by(contact = contact, password = password).order_by(Posts._id.desc()).all()

            if posts:
                progress = "100"

            else:
                flash("Nebyl nalezen žádný inzerát. Možná si zadal špatný kontakt, heslo, nebo nemáš aktivní žádné inzeráty.")
        
        else: ### deleting post and image from folder ###
            id = request.form["_id"]
            post = Posts.query.filter_by(_id = id).first()
            post_img = post.image
            os.remove(UPLOAD_FOLDER + post_img)
            Posts.query.filter_by(_id = id).delete()
            db.session.commit()
            flash("Inzerat byl uspesne smazan.")
            
            

        





    return render_template("delete_post.html", posts = posts, progress = progress)





# running the app

if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)
