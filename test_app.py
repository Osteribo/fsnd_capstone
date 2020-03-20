
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from config import bearer_tokens
from app import create_app
from models import setup_db, Donor, Program

# Create dict with Authorization key and Bearer token as values. 
# Later used by test classes as Header

inventory_peon_auth = {
    'Authorization': bearer_tokens['inventory_peon']
}

inventory_manager_auth = {
    'Authorization': bearer_tokens['inventory_manager']
}



class fsnd_capstone(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "fsnd_capstone"
        self.database_path = "postgres://{}/{}".format('localhost:5432',
                                                       self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_get_donors_true(self):
        res = self.client().get('/donors', headers=inventory_manager_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['donors']) > -1 )

    def test_get_donor_fail(self):
        res = self.client().get('/donors/1000' , headers=inventory_manager_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_get_programs_true(self):
        res = self.client().get('/programs', headers=inventory_manager_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['programs']) > -1 )

    def test_get_programs_fail(self):
        res = self.client().get('/programs/1000' , headers=inventory_manager_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_post_programs_true(self):
        json_post = {
                "division" : "gbc",
                "director": "human"
            }
        res = self.client().post('/programs', json=json_post, headers=inventory_manager_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['programs']) > -1 )

    def test_post_programs_fail(self):
        json_post = {
                "division" : "gbc",
                "director": "human"
            }
        res = self.client().post('/programs', json=json_post)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
    
    def test_post_donors_true(self):
        json_post = {
                "name" : "rrrr",
                "donation": 40
            }
        res = self.client().post('/programs', json=json_post, headers=inventory_manager_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['programs']) > -1 )

    def test_post_donors_fail(self):
        json_post = {
                "name" : "rrrr",
                "donation": 40
            }
        res = self.client().post('/programs', json=json_post)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    
    
    
        


# From app directory, run 'python test_app.py' to start tests
if __name__ == "__main__":
    unittest.main()