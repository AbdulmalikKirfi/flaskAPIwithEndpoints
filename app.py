from flask import Flask, request, Response, jsonify, redirect, url_for, session
import sqlite3


app = Flask(__name__)
app.secret_key = b"122333444"


def create_tables():
    connection = sqlite3.connect(f"site.db")
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS products(
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            price TEXT
            )''')
    
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password REAL
            )""")

    cursor.execute('''CREATE TABLE IF NOT EXISTS user_products(
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            price TEXT,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
            )''')

    connection.commit()
    connection.close()

create_tables()


#Endpoint to signup
@app.route("/signup", methods = ["POST"])
def signup():
    if "username" in session:
        return jsonify("you are already logged in")
    else:
        username = request.form["username"]
        password = request.form["password"]
        connection = sqlite3.connect(f"site.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users(username, password) VALUES(?,?)",(username, password))
        connection.commit()
        connection.close()
        return jsonify("user created!")


#Endpoint to login
@app.route("/login" ,methods = ["POST"])
def login():
    username =request.form["username"]
    password = request.form["password"]
    connection = sqlite3.connect(f"site.db")
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username=? AND password=?",(username,password))
    user = cursor.fetchone()
    connection.close()
    if user :
        session["user_id"] = user[0]
        return jsonify("logged in!")
    else:
        return jsonify("invalid username or password")


#Endpoint to post a new product
@app.route("/product", methods = ["POST"])
def add_product():
    if "user_id" not in session:
        return jsonify("you have to log in")
    
    connection = sqlite3.connect("site.db")
    cursor = connection.cursor()
    price = request.form["price"]
    user_id = session["user_id"]
    product = request.form["product"]
    cursor.execute(f"INSERT INTO user_products (product, price,user_id) VALUES(?,?)",(product, price, user_id))
    connection.commit()
    connection.close()
    return jsonify("product added")

#Endpoint to get a single product by its ID
@app.route("/product/<int:id>", methods = ["GET"])
def get_product(id):
    connection = sqlite3.connect("site.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products WHERE product_id=?",(id, ))
    searched_product = cursor.fetchone()
    connection.close()
    return Response(searched_product)


#Endpoint that deletes a product by its ID
@app.route("/your_product/delete/<int:id>", methods = ["DELETE"])
def delete_product(id):
    if "user_id" not in session:
        return jsonify("you are not login!")

    user_id = session["user_id"]
    connection = sqlite3.connect(f"products.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM user_products WHERE product_id=?",(id, )) 
    connection.commit()
    connection.close()
    return Response("product deleted")    
    

#Endpoint that gets all products
@app.route("/all_products", methods = ["GET"])
def get_products():
    connection = sqlite3.connect("site.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    all_products = cursor.fetchall()
    connection.close()
    print(all_products)
    # return Response(all_products)
    return jsonify(all_products)

#Endpoint that gets a user's products
@app.route("/your_products", methods = ["GET"])
def get_your_products():
    if "user_id" not in session:
        return jsonify("you are not login!")
    user_id = session["user_id"]
    connection = sqlite3.connect(f"site.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM user_products where user_id = ?",(user_id, ))
    all_products = cursor.fetchall()
    connection.close()
    return jsonify(all_products)



if __name__ == "__main__":
    app.run(debug=True)


