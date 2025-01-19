from controllers.books_controller import books_blueprint
from controllers.auth_controller import auth_blueprint
from controllers.borrow_controller import borrow_blueprint


def initial_routes(app):
    app.register_blueprint(books_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(borrow_blueprint)

