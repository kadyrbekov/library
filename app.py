from flask import Flask, render_template, request
from openpyxl import load_workbook

app = Flask(__name__)


@app.route("/")
def homepage():
   
    
    return render_template("index.html")


@app.route("/books/")
def books():
    excel = load_workbook("tales.xlsx")
    page = excel["Sheet1"]

    #tales = [tale.value for tale in page["A"]][1:]
    tales = []

    for tale in page["A"][1:]:
        tales.append(tale.value)


    authors = [author.value for author in page["B"]][1:]

    html = """
    
        <a href="/authors">Authors</a>
        <a href="/books">Books</a>
        <a href="/">Homepage</a>
        <h1>Тут будет список книг:</h1>
    
    """

    for i in range(len(tales)):
        html += f"<h2>{tales[i]} - {authors[i]}</h2>"

    # return f"""
    #     <h1>Тут будет список книг:</h1>
    #     <h2>{tales[0]} - {authors[0]}</h2>
    #     <h2>{tales[1]} - {authors[1]}</h2>
    #     <h2>{tales[2]} - {authors[2]}</h2>
    #     <h2>{tales[3]} - {authors[3]}</h2>
    #     <h2>{tales[4]} - {authors[4]}</h2
        
    # """

    return html


@app.route("/authors")
def authors():
    excel = load_workbook("tales.xlsx")
    page = excel["Sheet1"]
    authors = {author.value for author in page["B"][1:]}
    return render_template("authors.html")


@app.route("/add/", methods=["POST"])
def add():
    f = request.form
    print(f["author"], f["book"])
    return "Success!"