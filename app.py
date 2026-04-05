from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
api = Api(app)

class BookModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

book_args = reqparse.RequestParser()
book_args.add_argument("book_name", type=str, required=True)
book_args.add_argument("author", type=str, required=True)
book_args.add_argument("publisher", type=str, required=True)

resource_fields = {
    "id": fields.Integer,
    "book_name": fields.String,
    "author": fields.String,
    "publisher": fields.String
}

class Book(Resource):
    @marshal_with(resource_fields)
    def get(self, book_id):
        book = BookModel.query.get(book_id)
        if not book:
            abort(404, message="Book not found")
        return book

    @marshal_with(resource_fields)
    def put(self, book_id):
        args = book_args.parse_args()
        book = BookModel(
            id=book_id,
            book_name=args["book_name"],
            author=args["author"],
            publisher=args["publisher"]
        )
        db.session.add(book)
        db.session.commit()
        return book, 201

    def delete(self, book_id):
        book = BookModel.query.get(book_id)
        if not book:
            abort(404, message="Book not found")
        db.session.delete(book)
        db.session.commit()
        return {"message": "Deleted"}

api.add_resource(Book, "/book/<int:book_id>")

if __name__ == "__main__":
    app.run(debug=True)