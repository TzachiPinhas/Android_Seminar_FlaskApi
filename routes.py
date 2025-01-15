from controllers.books_controller import books_blueprint

def initial_routes(app):
    app.register_blueprint(books_blueprint)
