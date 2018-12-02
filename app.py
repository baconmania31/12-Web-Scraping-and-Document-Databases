# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():

    # Find data
    marsData = mongo.db.collection.find()

    # return template and data
    return render_template("index.html", marsData=marsData)

@app.route("/scrape")
def scrape():
    mongo.db.collection.drop()
    mars_data = scrape_mars.scrape()
    marsData = {
        "news_title": mars_data['news_title'], 
        "news_p": mars_data['news_p'], 
        "featured_image_url": mars_data['featured_image_url'],
        "mars_weather": mars_data['mars_weather'],
        "mars_dict": mars_data['mars_dict'],
        "hemisphere_dict": mars_data['hemisphere_dict']
    }
    mongo.db.collection.insert_one(marsData)
    return redirect("/", code=302)
 
if __name__ == "__main__":
    app.run(debug=False)
