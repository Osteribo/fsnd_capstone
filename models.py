from sqlalchemy import Integer, Column, String, create_engine, Date
from flask_sqlalchemy import SQLAlchemy
import json
import os

# adjust commenting as need for heroku or local use

# Heroku
database_path = os.environ['DATABASE_URL']

# local
# database_name = "fsnd_capstone"
# database_path = "postgres://{}:{}@{}/{}".format('alo', '1234',
#                                                 'localhost:5432',
#                                                 database_name)

db = SQLAlchemy()


def db_drop_and_create_all():
    '''drops the database tables and starts fresh
    can be used to initialize a clean database
    '''
    db.drop_all()
    db.create_all()
    db_init_records()


def db_init_records():
    '''this will initialize the database with some test records.'''

    new_donor = (Donor(
        name='Matthew',
        donation=500
        ))

    new_program = (Program(
        division='Buckn Broncos',
        director='That one human'
        ))

    new_donor.insert()
    new_program.insert()
    db.session.commit()


'''
setup_db(app)
    binds a flask application and SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Donor

'''


class Donor(db.Model):
    __tablename__ = "Donor"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    donation = Column(Integer)

    '''
    long()
        long form representation of the Drink model
    '''
    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'donation': self.donation
        }
    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = 'Black Coffee'
            drink.update()
    '''
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.long())


'''
Product
 later implementation
'''


class Program(db.Model):
    __tablename__ = "Program"

    id = Column(Integer, primary_key=True)
    division = Column(String)
    director = Column(String)

    def long(self):
        return {
            'id': self.id,
            'division': self.division,
            'director': self.director
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = 'Black Coffee'
            drink.update()
    '''
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.long())
