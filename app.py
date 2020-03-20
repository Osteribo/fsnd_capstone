import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Donor, Program, db_drop_and_create_all
from auth import AuthError, requires_auth


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  
  setup_db(app)
  
  @app.route('/')
  def get_greeting():
      
      greeting = "Hello" 

      return greeting

  @app.route('/coolkids')
  def be_cool():
      return "Be cool, man, be coooool! You're almost a FSND grad!"

  #----------------------------------------------------------------------------#
  # Endpoint /donors and /programs GET/POST/DELETE/PATCH
  #----------------------------------------------------------------------------#

  @app.route('/donors')
  @requires_auth('get:donors')
  def get_donors(token):
      available_donors = Donor.query.all()

      print(available_donors)
      
      return jsonify({
        'success': True,
        'donors': available_donors
      })
  
  @app.route('/programs')
  @requires_auth('get:programs')
  def get_programs(token):
      available_program = Program.query.all()

      print(available_program)
      
      return jsonify({
        'success': True,
        'programs': available_program
      })

  @app.route('/donors', methods=['POST'])
  @requires_auth('post:donors')
  def new_donor(token):
      try:
          body = request.get_json()
          if body is None:
                abort(404)
          new_name= body.get('name')
          new_donation = body.get('donation')
          new_donor = Donor(name=new_name, donation=new_donation)
          new_donor.insert()
          new_donor = Donor.query.filter_by(id=new_donor.id).first()
          return jsonify({
                'success': True,
                'drinks': [new_donor.long()]
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
          new_division= body.get('division')
          new_director = body.get('director')
          new_program = Program(division=new_division, director=new_director)
          new_program.insert()
          new_program = Program.query.filter_by(id=new_donor.id).first()
          return jsonify({
                'success': True,
                'drinks': [new_program.long()]
            })
      except AuthError:
          abort(422)

  @app.route('/donors/<int:donor_id>', methods=['PATCH'])
  @requires_auth('patch:donors')
  def update_donor(payload, donor_id):
      body = request.get_json()
      update_name= body.get('name')
      update_donation = body.get('donation')
      donor_to_update = Donor.query.filter(Donor.id == donor_id).one_or_none()
      if donor_to_update is None:
        abort(404)
      if update_name:
          donor_to_update.name = update_name
      if update_donation:
          donor_to_update.donation = update_donation
      donor_to_update.update()


      return jsonify({
        'success': True,
        'drinks': donor_to_update.long()
      })

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




  #----------------------------------------------------------------------------#
  # Error Handlers
  #----------------------------------------------------------------------------#



  @app.errorhandler(404)
  def page_not_found(error):
      return jsonify({
                      "success": False,
                      "error": 404,
                      "message": "Page not found"
                      }), 404


  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
                      "success": False,
                      "error": 422,
                      "message": "unprocessable"
                      }), 422
  @app.errorhandler(AuthError)
  def unprocessable(error):
      return jsonify({
                      "success": False,
                      "error": AuthError,
                      "message": "Error with authorization"
                      }), AuthError


  @app.errorhandler(401)
  def page_not_found(error):
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