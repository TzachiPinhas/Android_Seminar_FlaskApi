from flask import Blueprint, request, jsonify
from mongodb_connection_manager import MongoConnectionHolder
import uuid


# יצירת Blueprint עבור הנתיבים
books_blueprint = Blueprint('books', __name__)


books = []



@books_blueprint.route('/books', methods=['GET'])
def get_books():
    """
    Get all books from the database
    ---
    responses:
      200:
        description: A list of all books in the store
    """
    db = MongoConnectionHolder.get_db()
    books_collection = db['books']  # אוספים את הקולקציה של הספרים
    all_books = list(books_collection.find({}))
    for book in all_books:
        book['_id'] = str(book['_id'])
    return jsonify(all_books)

@books_blueprint.route('/books', methods=['POST'])
def add_book():
    """
    Add a new book
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - title
            - author
            - price
            - stock
            - category
          properties:
            title:
              type: string
              description: Title of the book
              example: "The Great Gatsby"
            author:
              type: string
              description: Author of the book
              example: "F. Scott Fitzgerald"
            price:
              type: number
              format: float
              description: Price of the book
              example: 10.99
            stock:
              type: integer
              description: Number of copies in stock
              example: 5
            category:
              type: string
              description: Book category
              example: "Fiction"
    responses:
      201:
        description: Book created successfully
        schema:
          id: Book
          properties:
            id:
              type: string
              description: Unique identifier for the book
            title:
              type: string
            author:
              type: string
            price:
              type: number
              format: float
            stock:
              type: integer
            category:
              type: string
      400:
        description: Invalid data or missing fields
        schema:
          properties:
            error:
              type: string
              example: "Missing or empty field: title"
    """
    db = MongoConnectionHolder.get_db()  # חיבור למסד הנתונים
    new_book = request.json
    new_book['_id'] = str(uuid.uuid4())  # יצירת ID אוטומטי

    required_fields = ['title', 'author', 'price', 'stock', 'category']
    for field in required_fields:
        if not new_book.get(field):
            return jsonify({"error": f"Missing or empty field: {field}"}), 400

    # הכנסת הספר למסד הנתונים
    db.books.insert_one(new_book)
    return jsonify(new_book), 201



@books_blueprint.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):  # book_id הוא מחרוזת UUIDdef get_book(book_id):
    """
    Get a specific book by ID
    ---
    parameters:
      - name: book_id
        in: path
        type: string
        required: true
        description: The ID of the book to retrieve
    responses:
      200:
        description: Book found successfully
      404:
        description: Book not found
    """
    db = MongoConnectionHolder.get_db()
    books_collection = db['books']
    book = books_collection.find_one({"_id": book_id}, {"_id": 0})

    if book:
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404




@books_blueprint.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
    Delete a book by ID
    ---
    parameters:
      - name: book_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Book deleted successfully
      404:
        description: Book not found
    """
    db = MongoConnectionHolder.get_db()
    books_collection = db['books']

    result = books_collection.delete_one({"_id": book_id})

    if result.deleted_count == 0:
        return jsonify({"error": "Book not found"}), 404

    return jsonify({"message": "Book deleted successfully"}), 200
