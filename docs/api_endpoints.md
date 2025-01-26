# API Endpoints Documentation

This document provides an overview of the API endpoints available in the Book Management System.

---

## 1. Authentication Endpoints

### Register a new user
- **Endpoint:** `POST /register`
- **Description:** Allows users to register by providing a username and password.
- **Request:** JSON containing username and password.
- **Response:** Confirmation of successful registration or an error message.

### User login
- **Endpoint:** `POST /login`
- **Description:** Authenticates a user and returns their user ID.
- **Request:** JSON containing username and password.
- **Response:** User ID if authentication is successful or an error message.

---

## 2. Book Management Endpoints

### Get all books
- **Endpoint:** `GET /books`
- **Description:** Retrieves a list of all available books.
- **Request:** None.
- **Response:** A list of books with their details.

### Add a new book
- **Endpoint:** `POST /books`
- **Description:** Adds a new book to the inventory.
- **Request:** JSON containing book details (title, author, stock, category).
- **Response:** Confirmation of successful addition or an error message.

### Update a book
- **Endpoint:** `PUT /books/{book_id}`
- **Description:** Updates the details of an existing book.
- **Request:** JSON with updated book details.
- **Response:** Confirmation of successful update or an error message.

### Delete a book
- **Endpoint:** `DELETE /books/{book_id}`
- **Description:** Deletes a book if it's not currently borrowed.
- **Request:** Book ID in the URL.
- **Response:** Confirmation of successful deletion or an error message.

### Get available books
- **Endpoint:** `GET /books/available`
- **Description:** Retrieves a list of books that are in stock.
- **Request:** None.
- **Response:** A list of available books.

---

## 3. Borrow Management Endpoints

### Request to borrow a book
- **Endpoint:** `POST /request-borrow`
- **Description:** Allows a user to request borrowing a book.
- **Request:** JSON containing user ID and book ID.
- **Response:** Confirmation of the borrow request or an error message.

### Get user's borrow records
- **Endpoint:** `GET /my-borrows/{user_id}`
- **Description:** Retrieves a list of books borrowed by a specific user.
- **Request:** User ID in the URL.
- **Response:** A list of borrow records.

### Approve a borrow request (Admin)
- **Endpoint:** `PUT /admin/approve-borrow/{borrow_id}`
- **Description:** Approves a pending borrow request.
- **Request:** Borrow ID in the URL.
- **Response:** Confirmation of approval or an error message.

### Return a borrowed book (Admin)
- **Endpoint:** `PUT /admin/return/{borrow_id}`
- **Description:** Marks a book as returned and updates stock.
- **Request:** Borrow ID in the URL.
- **Response:** Confirmation of return or an error message.

### Get all borrow records (Admin)
- **Endpoint:** `GET /admin/borrows`
- **Description:** Retrieves a list of all borrow records.
- **Request:** None.
- **Response:** A list of all borrow records.

---

