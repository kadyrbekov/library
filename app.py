from flask import Flask, render_template, request
from openpyxl import load_workbook
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import scoped_session
from database import engine, book


app = Flask(__name__)

db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def homepage():
   return render_template("index.html")


@app.route("/books/")
def books():
    #v1
    # excel = load_workbook("tales.xlsx")
    # page = excel["Sheet1"]


    # object_list= [[tale.value, tale.offset(column=1).value] for tale in page["A"][1:]]
    # print("Books page!")
    # return render_template('books.html', object_list=object_list)

    #v2

    # session = sessionmaker(engine)()
    # books = session.query("Book")
    
    # session.commit()
    # print(books)

    with engine.connect() as con:
        books = con.execute("""SELECT * FROM "Book"; """)
    return render_template("books.html", object_list=books)


@app.route("/authors")
def authors():
    # excel = load_workbook("tales.xlsx")
    # page = excel["Sheet1"]
    # authors = {author.value for author in page["B"][1:]}
    # authors_all = [author.value for author in page["B"][1:]]
    # counts = []
    # for author in authors_all:
    #     i = authors_all.count(author)
    #     counts.append(i)
    
    # return render_template("authors.html", authors=authors, authors_all=authors_all, counts=counts)

    with engine.connect() as con:
        authors = con.execute("""SELECT author FROM "Book";""")
    return render_template("authors_table.html", authors = authors)


@app.route("/book_edit", methods=["POST", "GET"])
def book_edit():
    #getting requests from fomr located at index.html
    id_num = request.form.get("id_num")
    name=request.form.get("name")
    author=request.form.get("author")
    image=request.form.get("image")
    

    # with engine.connect() as con:
    #     con.execute("INSERT INTO Book (id, name, author, image) f(:id, :name, :author, :image)",
    #             {"id": id, "name": name, "author":author,"image":image}) 
    #     con.commit() 
    #using scoped session we do the sql query
    db.execute(""" INSERT INTO "Book" (id_num, name, author, image) VALUES (:id_num, :name, :author, :image)""",
            {"id_num":id_num, "name": name, "author": author,"image": image}) 
    db.commit()

    return render_template("book_edit.html")


@app.route("/book/<id>/")
def book(id):
    obj = db.execute(f"""SELECT * FROM "Book" WHERE id_num = {id}; """).first()
    db.commit()
    return render_template("book.html", obj=obj) # **kwargs


# @app.route("/book/<num>/edit")
# def book_edit(num):
#     num = int(num) + 2
#     excel_file = load_workbook("tales.xlsx")
#     page = excel_file["Sheet1"]
#     tale = page[f"A{num}"]
#     author = page[f"B{num}"]
#     image = page[f"C{num}"]
#     obj = [tale.value, author.value, image.value, num]
#     return render_template("book_edit.html", obj=obj)


# @app.route("/book/<num>/save/", methods=["POST"])
# def book_save(num):
#     num = int(num)
#     excel_file = load_workbook("tales.xlsx")
#     page = excel_file["Sheet1"]
#     form = request.form
#     page[f"A{num}"] = form["tale"]
#     page[f"B{num}"] = form["author"]
#     page[f"C{num}"] = form["image"]
#     excel_file.save("tales.xlsx")
#     return "Сохранено!"

