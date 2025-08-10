from flask import Flask, jsonify


class UnauthorizedError(Exception):
    pass


class ForbiddenError(Exception):
    pass


class BadRequestError(Exception):
    pass


class ResourceNotFoundError(Exception):
    pass


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(BadRequestError)
    def handle_bad_request(err):
        return jsonify({"error": str(err)}), 400

    @app.errorhandler(ResourceNotFoundError)
    def handle_not_found(err):
        return jsonify({"error": str(err)}), 404

    @app.errorhandler(UnauthorizedError)
    def handle_unauthorized(err):
        return jsonify({"error": str(err)}), 401

    @app.errorhandler(ForbiddenError)
    def handle_forbidden(err):
        return jsonify({"error": str(err)}), 403

    @app.errorhandler(Exception)
    def handle_generic(err):
        return jsonify({"error": str(err)}), 500
