import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Donor, Program
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)
    cors = CORS(app, resources={'/': {"origins": "*"}})

    def get_error_message(error, default_text):
        try:
            # Return message contained in error, if possible
            return error.description['message']
        except:
            # otherwise, return given default text
            return default_text

        # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # Endpoint /  check that app is functioning

    @app.route('/')
    def get_greeting():
        greeting = "Hello"

        return greeting

    # Endpoint /donors and /programs GET/POST/DELETE/PATCH

    @app.route('/donors')
    @requires_auth('get:donors')
    def get_donors(token):
        try:
            available_donor = Donor.query.all()
            available_donors = [donor.long() for donor in available_donor]

            return jsonify({
                'success': True,
                'donors': available_donors
            })
        except:
            abort(405)

    @app.route('/programs')
    @requires_auth('get:programs')
    def get_programs(token):
        try:
            available_program = Program.query.all()
            available_programs = [program.long() for program
                                  in available_program]

            return jsonify({
                'success': True,
                'programs': available_programs
            })
        except:
            abort(404)

    @app.route('/donors', methods=['POST'])
    @requires_auth('post:donors')
    def new_donor(token):
        try:
            body = request.get_json()
            if body is None:
                abort(404)
            new_name = body.get('name')
            new_donation = body.get('donation')
            new_donor = Donor(name=new_name, donation=new_donation)
            new_donor.insert()
            new_donor = Donor.query.filter_by(id=new_donor.id).first()
            return jsonify({
                    'success': True,
                    'donors': [new_donor.long()]
                })
        except AuthError:
            abort(422)

    @app.route('/programs', methods=['POST'])
    @requires_auth('post:programs')
    def new_program(token):
        try:
            body = request.get_json()
            if body is None:
                abort(404)
            new_division = body.get('division')
            new_director = body.get('director')
            new_program = Program(division=new_division, director=new_director)
            new_program.insert()
            new_program = Program.query.filter_by(id=new_program.id).first()
            return jsonify({
                    'success': True,
                    'programs': [new_program.long()]
                })
        except:
            abort(401)

    @app.route('/donors/<int:donor_id>', methods=['PATCH'])
    @requires_auth('patch:donors')
    def update_donor(payload, donor_id):
        try:
            body = request.get_json()
            update_name = body.get('name')
            update_donation = body.get('donation')
            donor_to_update = Donor.query.filter(Donor.id == donor_id
                                                 ).one_or_none()
            if donor_to_update is None:
                abort(404)
            if update_name:
                donor_to_update.name = update_name
            if update_donation:
                donor_to_update.donation = update_donation
            donor_to_update.update()

            return jsonify({
                'success': True,
                'donors': [donor_to_update.long()]
            })
        except:
            abort(401)

    @app.route('/donors/<int:donor_id>', methods=['DELETE'])
    @requires_auth('delete:donors')
    def delete_donor(payload, donor_id):
        try:
            donor_to_delete = Donor.query.filter(Donor.id ==
                                                 donor_id).one_or_none()
            donor_to_delete.delete()

            return jsonify({
                'success': True,
                'delete': donor_id
                })

        except:
            abort(404)

    # Error Handlers

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
                        "success": False,
                        "error": 404,
                        "message": "Page not found"
                        }), 404

    @app.errorhandler(405)
    def no_method(error):
        return jsonify({
                        "success": False,
                        "error": 405,
                        "message": "Method not allowed"
                        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False,
                        "error": 422,
                        "message": "unprocessable"
                        }), 422

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
                        "success": False,
                        "error": AuthError,
                        "message": "Error with authorization"
                        }), AuthError

    @app.errorhandler(401)
    def Unauthorized(error):
        return jsonify({
                        "success": False,
                        "error": 401,
                        "message": "Unauthorized"
                        }), 401

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
            }), 400

    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
