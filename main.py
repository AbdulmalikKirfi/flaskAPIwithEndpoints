from flask import Flask, request, Response
import sqlite3

app = Flask(__name__)

def create_table():
    connection = sqlite3.connect("products_table.db")
    c = connection.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS products(
            product TEXT,
            id INTEGER
            )""")
    connection.commit()
    connection.close()

create_table()

#Endpoint to post a new product
@app.route("/product", methods = ["POST"])
def add_product():
    connection = sqlite3.connect("products_table.db")
    c = connection.cursor()
    product = request.form["product"]
    id = request.form["id"]
    c.execute("INSERT INTO products (product, id) VALUES(?,?)",(product, id))
    connection.commit()
    connection.close()
    return Response("product added")

#Endpoint to get a single product by its ID
@app.route("/product/<int:id>", methods = ["GET"])
def get_product(id):
    connection = sqlite3.connect("products_table.db")
    c = connection.cursor()
    c.execute("SELECT * FROM products WHERE id=?",(id, ))
    searched_product = c.fetchone()
    connection.close()
    return Response(searched_product)


#Endpoint that deletes a product by its ID
@app.route("/product/delete/<int:id>", methods = ["DELETE"])
def delete_product(id):
    connection = sqlite3.connect("products_table.db")
    c = connection.cursor()
    c.execute("DELETE FROM products WHERE id=?",(id, ))
    connection.commit()
    connection.close()
    return Response("product deleted")

#Endpoint that gets all products
@app.route("/products", methods = ["GET"])
def get_productS():
    connection = sqlite3.connect("products_table.db")
    c = connection.cursor()
    c.execute("SELECT * FROM products")
    all_products = c.fetchall()
    connection.close()
    print(all_products)
    return Response(all_products)


if __name__ == "__main__":
    app.run(debug=True)


