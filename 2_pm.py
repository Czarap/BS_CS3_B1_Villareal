from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:your_password@localhost/book_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


def find_book(book_id):
    for book in books:
        if book["id"] == book_id:
            return book
    return None


#Read
@app.route("/api/books", methods=["GET"])
def get_books():
    return jsonify({"success": True, 
                    "data": books, 
                    "total": len(books)}), HTTPStatus.OK

@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):

    book = find_book(book_id)

 
    if book is None:
        return (
            jsonify({
                "success": False,
                "error": "Book not found"
            }),
            HTTPStatus.NOT_FOUND
        )

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
            return jsonify({
                "success": False,
                "error": f"Missing required field: {field}"
            }), HTTPStatus.BAD_REQUEST

    new_book = {
        "id": max(book["id"] for book in books) + 1, 
        "title": data["title"],
        "author": data["author"],
        "year": data["year"]
    }

    books.append(new_book)

    return jsonify({
        "success": True,
        "data": new_book
    }), HTTPStatus.CREATED


# Update
@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = find_book(book_id)
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

    book["title"] = data.get("title", book["title"])
    book["author"] = data.get("author", book["author"])
    book["year"] = data.get("year", book["year"])

    return jsonify({"success": True,
                     "data": book}),HTTPStatus.OK

#Delete


@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = find_book(book_id)

    if book is None:
        return jsonify({"success": False, 
                        "error": "Book not found"}), HTTPStatus.NOT_FOUND

    books.remove(book)
    return jsonify({"success": True, 
                    "message": "Book deleted successfully"}), HTTPStatus.OK

if __name__ == "__main__":
    app.run(debug=True)
