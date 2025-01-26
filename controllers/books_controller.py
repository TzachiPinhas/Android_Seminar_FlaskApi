from flask import Blueprint, request, jsonify
from mongodb_connection_manager import MongoConnectionHolder
import uuid


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
    books_collection = db['books']
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
    db = MongoConnectionHolder.get_db()
    new_book = request.json
    new_book['_id'] = str(uuid.uuid4())

    required_fields = ['title', 'author', 'stock', 'category']
    for field in required_fields:
        if not new_book.get(field):
            return jsonify({"error": f"Missing or empty field: {field}"}), 400

    db.books.insert_one(new_book)
    return jsonify(new_book), 201


@books_blueprint.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
    Delete a book by ID if it's not currently borrowed
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
        description: Book not found or is currently borrowed
    """
    db = MongoConnectionHolder.get_db()

    borrowed = db['borrows'].find_one({"book_id": book_id, "status": {"$in": ["pending", "approved"]}})
    if borrowed:
        return jsonify({"error": "Cannot delete book that is currently borrowed or pending approval"}), 400

    result = db['books'].delete_one({"_id": book_id})

    if result.deleted_count == 0:
        return jsonify({"error": "Book not found"}), 404

    return jsonify({"message": "Book deleted successfully"}), 200



@books_blueprint.route('/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    """
    Update a book's information
    ---
    parameters:
      - name: book_id
        in: path
        type: string
        required: true
        description: The ID of the book to update
      - name: body
        in: body
        required: true
        schema:
          properties:
            title:
              type: string
            author:
              type: string
            stock:
              type: integer
            category:
              type: string
    responses:
      200:
        description: Book updated successfully
      404:
        description: Book not found
    """
    db = MongoConnectionHolder.get_db()
    updated_data = request.json

    update_fields = {k: v for k, v in updated_data.items() if k in ['title', 'author', 'stock', 'category']}

    result = db['books'].update_one({"_id": book_id}, {"$set": update_fields})

    if result.matched_count == 0:
        return jsonify({"error": "Book not found"}), 404

    return jsonify({"message": "Book updated successfully"}), 200


@books_blueprint.route('/books/available', methods=['GET'])
def get_available_books():
    """
    Get all available books (in stock)
    ---
    responses:
      200:
        description: List of books with stock > 0
    """
    db = MongoConnectionHolder.get_db()
    books_collection = db['books']

    available_books = list(books_collection.find({"stock": {"$gt": 0}}))

    for book in available_books:
        book['_id'] = str(book['_id'])

    return jsonify(available_books), 200
