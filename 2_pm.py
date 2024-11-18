from flask import Flask, jsonify, request
from http import HTTPStatus
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/book_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)


def initialize_database():
    db.create_all()  
    if not Book.query.filter_by(title="The Great Gatsby").first():
        new_book = Book(id = 1 ,title="The Great Gatsby", author="F. Scott Fitzgerald", year=1925)
        db.session.add(new_book)
        db.session.commit()
        print(f"Book '{new_book.title}' added to the database.")
#Read
@app.route("/api/books", methods=["GET"])
def get_books():
    books = Book.query.all()
    data = [{"id": book.id, 
             "title": book.title, 
             "author": book.author, 
             "year": book.year} 
            for book in books]
    return jsonify({"success": True, 
                    "data": data, 
                    "total": len(books)}), HTTPStatus.OK

@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get(book_id)
 
    if not book:
        return jsonify({ "success": False,
                        "error": "Book not found" }),  HTTPStatus.NOT_FOUND
        

    return jsonify({"success": True, "data": book}), HTTPStatus.OK

#Create

@app.route("/api/books", methods=["POST"])
def create_book():
    if not request.is_json:
        return (
            jsonify({
                "success": False,
                "error": "Content-type must be application/json"
            }),
            HTTPStatus.BAD_REQUEST
        )
    
    data = request.get_json()
    required_fields = ["title", "author", "year"]
    for field in required_fields:
        if field not in data:
            return jsonify({"success": False, "error": f"Missing required field: {field}"}), HTTPStatus.BAD_REQUEST

    new_book = Book(title=data["title"], author=data["author"], year=data["year"])
    db.session.add(new_book)
    db.session.commit()

    return jsonify({"success": True, 
                    "data": {"id": new_book.id, 
                             "title": new_book.title, 
                             "author": new_book.author, 
                             "year": new_book.year}}), HTTPStatus.CREATED



# Update
@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return (
            jsonify({"success": False, 
                     "error": "Book not found"}),
            HTTPStatus.NOT_FOUND,
        )

    if not request.is_json:
        return (
            jsonify(
                {"success": False, 
                 "error": "Content-type must be application/json"}
            ),
            HTTPStatus.BAD_REQUEST,
        )

    data = request.get_json()
    book.title = data.get("title", book.title)
    book.author = data.get("author", book.author)
    book.year = data.get("year", book.year)
    db.session.commit()

    return jsonify({"success": True, 
                    "data": {"id": book.id, 
                             "title": book.title,
                             "author": book.author, 
                             "year": book.year}}), HTTPStatus.OK


#Delete


@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get(book_id)

    if book is None:
        return jsonify({"success": False, 
                        "error": "Book not found"}), HTTPStatus.NOT_FOUND

    db.session.delete(book)
    db.session.commit()
    return jsonify({"success": True,
                     "message": 
                     "Book deleted successfully"}), HTTPStatus.OK


if __name__ == "__main__":
    with app.app_context():
     initialize_database()
     app.run(debug=True)
