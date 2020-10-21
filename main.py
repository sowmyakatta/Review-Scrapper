from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uopen
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    return (render_template("index.html"))

@app.route("/scrap", methods=["POST"])
def scrap():
    if request.method=="POST":
        searchString = request.form['content'].replace(" ","")
        noc = int(request.form['numOfComments'])
        try:
            flipkart_search_url = r"https://www.flipkart.com/search?q="+searchString
            page = uopen(flipkart_search_url)
            page_content = page.read()
            page.close()
            page_html = bs(page_content, "html.parser")
            boxes =page_html.findAll("div", {"class":"bhgxx2 col-12-12"})
            boxes = boxes[2:]
            box = boxes[0]
            product_url = r"https://www.flipkart.com"+ box.div.div.div.a['href']
            product = uopen(product_url)
            product_content = product.read()
            product.close()
            product_html = bs(product_content, "html.parser")
            reviews = product_html.findAll("div", {"class": "_3nrCtb"})
            reviews_df = []
            for i in range(noc):
                Heading= reviews[i].div.div.div.p.text
                comm = reviews[i].findAll("div", {"class": ""})
                Content = comm[0].div.text
                reviews_df.append([Heading, Content])

            reviews_df = pd.DataFrame(reviews_df, columns=["Heading", "Content"])
            reviews_df = reviews_df.to_dict("records")
            print(reviews_df)

            return (render_template("result.html", reviews_df= reviews_df))
        except Exception as e:
            return (str(e))
    else :
        return "not post"

if (__name__=="__main__") :
    app.run(port = 8000, debug =True)