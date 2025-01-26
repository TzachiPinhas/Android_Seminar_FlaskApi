import uuid

from flask import Blueprint, request, jsonify
from mongodb_connection_manager import MongoConnectionHolder
import datetime

borrow_blueprint = Blueprint('borrow', __name__)
db = MongoConnectionHolder.get_db()

@borrow_blueprint.route('/request-borrow', methods=['POST'])
def request_borrow():
    """
    Request to borrow a book
    ---
    tags:
      - Borrow
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            user_id:
              type: string
              description: ID of the user requesting the book
            book_id:
              type: string
              description: ID of the book to borrow
    responses:
      201:
        description: Borrow request submitted
      400:
        description: Missing user ID or book ID, or book out of stock
      404:
        description: Book or user not found
    """
    data = request.get_json()
    user_id = data.get('user_id')
    book_id = data.get('book_id')

    if not user_id or not book_id:
        return jsonify({"error": "User ID and Book ID are required"}), 400

    user = db['users'].find_one({"_id": user_id})
    if not user:
        return jsonify({"error": "User not found"}), 404

    book = db['books'].find_one({"_id": book_id})
    if not book:
        return jsonify({"error": "Book not found"}), 404

    if book['stock'] <= 0:
        return jsonify({"error": "Book is out of stock"}), 400

    db['books'].update_one(
        {"_id": book_id},
        {"$inc": {"stock": -1}}
    )

    borrow = {
        "_id": str(uuid.uuid4()),
        "user_id": user_id,
        "username": user['username'],
        "book_id": book_id,
        "book_title": book['title'] if 'title' in book else "Unknown",
        "borrowed_at": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "pending"
    }

    db['borrows'].insert_one(borrow)
    return jsonify({"message": "Borrow request submitted"}), 201



@borrow_blueprint.route('/my-borrows/<user_id>', methods=['GET'])
def get_my_borrows(user_id):
    """
    Get my borrow records
    ---
    tags:
      - Borrow
    parameters:
      - in: path
        name: user_id
        required: true
        type: string
        description: ID of the user to get borrow records for
    responses:
      200:
        description: List of user's borrows
      404:
        description: User not found
    """
    user = db['users'].find_one({"_id": user_id})
    if not user:
        return jsonify({"error": "User not found"}), 404

    borrows = list(db['borrows'].find({"user_id": user_id}))

    for borrow in borrows:
        book = db['books'].find_one({"_id": borrow['book_id']})
        borrow['book_title'] = book['title'] if book else "Unknown"
        borrow['_id'] = str(borrow['_id'])
        borrow['book_id'] = str(borrow['book_id'])
        if isinstance(borrow['borrowed_at'], datetime.datetime):
            borrow['borrowed_at'] = borrow['borrowed_at'].strftime("%Y-%m-%d %H:%M:%S")
        else:
            borrow['borrowed_at'] = str(borrow['borrowed_at'])  #         borrow['status'] = borrow['status']

    return jsonify(borrows), 200



@borrow_blueprint.route('/admin/approve-borrow/<borrow_id>', methods=['PUT'])
def approve_borrow(borrow_id):
    """
    Approve a borrow request
    ---
    tags:
      - Admin
    parameters:
      - in: path
        name: borrow_id
        required: true
        description: ID of the borrow request
    responses:
      200:
        description: Borrow request approved
      404:
        description: Borrow request not found
    """
    borrow = db['borrows'].find_one({"_id": borrow_id})

    if not borrow:
        return jsonify({"error": "Borrow request not found"}), 404

    if borrow["status"] != "pending":
        return jsonify({"error": "Only pending requests can be approved"}), 400

    db['borrows'].update_one({"_id": borrow_id}, {"$set": {"status": "approved"}})

    return jsonify({"message": "Borrow request approved"}), 200



@borrow_blueprint.route('/admin/return/<borrow_id>', methods=['PUT'])
def return_book(borrow_id):
    """
    Mark a book as returned
    ---
    tags:
      - Admin
    parameters:
      - in: path
        name: borrow_id
        required: true
        description: ID of the borrow record
    responses:
      200:
        description: Book returned successfully
      404:
        description: Borrow record not found
   """
    borrow = db['borrows'].find_one({"_id": borrow_id})

    if not borrow:
        return jsonify({"error": "Borrow record not found"}), 404

    if borrow["status"] == "returned":
        return jsonify({"error": "This book has already been returned"}), 400

    if borrow["status"] != "approved":
        return jsonify({"error": "Only approved borrow requests can be returned"}), 400

    db['borrows'].update_one({"_id": borrow_id}, {"$set": {"status": "returned"}})


    db['books'].update_one({"_id": borrow["book_id"]}, {"$inc": {"stock": 1}})

    return jsonify({"message": "Book returned successfully"}), 200


@borrow_blueprint.route('/admin/borrows', methods=['GET'])
def get_all_borrows():
    """
    Get all borrow records (Admin)
    ---
    tags:
      - Admin
    responses:
      200:
        description: List of all borrows
    """
    borrows = list(db['borrows'].find())

    for borrow in borrows:
        book = db['books'].find_one({"_id": borrow['book_id']})
        user = db['users'].find_one({"_id": borrow['user_id']})

        borrow['book_title'] = book['title'] if book else "Unknown"
        borrow['username'] = user['username'] if user else "Unknown"

        borrow['_id'] = str(borrow['_id'])
        borrow['book_id'] = str(borrow['book_id'])
        borrow['user_id'] = str(borrow['user_id'])

        if isinstance(borrow['borrowed_at'], datetime.datetime):
            borrow['borrowed_at'] = borrow['borrowed_at'].strftime("%Y-%m-%d %H:%M:%S")
        else:
            borrow['borrowed_at'] = str(borrow['borrowed_at'])

        borrow['status'] = borrow['status']

    return jsonify(borrows), 200