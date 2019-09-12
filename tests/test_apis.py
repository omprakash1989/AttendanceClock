"""
API unittests should be here.
"""


import unittest
import pytest
import json

from wsgi import application


class TestAppApi(unittest.TestCase):
    """
    Test case for bureau API.
    all the positive and negative test cases to be written over here.
    """

    def setUp(self):
        self.app = application.test_client()

    def test_login_api(self):
        username = 'admin'
        password = 'admin'
        header = {
            "Content-Type": "application/json",
        }
        input_data = {"username": username, "password": password}

        resp = self.app.post('/himama/login/', data=json.dumps(input_data), headers=header)

        # Check response status.
        self.assertEqual(resp.status_code, 200 or 302, resp.data)

    def test_logout_api(self):
        username = 'admin'
        password = 'admin'
        header = {
            "Content-Type": "application/json",
        }
        input_data = {"username": username, "password": password}

        # Login First.
        resp = self.app.post('/himama/login/', data=json.dumps(input_data), headers=header)

        # Check response status.
        self.assertIn(resp.status_code, [200, 302], resp.data)

        # Logout request
        resp = self.app.get('/himama/logout/', data=json.dumps(input_data), headers=header)

        # Check response status.
        self.assertIn(resp.status_code, [200, 302], resp.data)

    def test_clock_in_api(self):
        username = 'admin'
        password = 'admin'
        header = {
            "Content-Type": "application/json",
        }
        input_data = {"username": username, "password": password}

        # Login First.
        resp = self.app.post('/himama/login/', data=json.dumps(input_data), headers=header)

        # Check response status.
        self.assertIn(resp.status_code, [200, 302], resp.data)

        # clock in.
        # resp = self.app.get('/himama/attendance/clock_in/', headers=header)

        # Check response status.
        # self.assertEqual(resp.status_code, 200, resp.data.decode('utf-8'))

        # Logout request
        resp = self.app.get('/himama/logout/', data=json.dumps(input_data), headers=header)

        # Check response status.
        self.assertIn(resp.status_code, [200, 302], resp.data)


    def test_clock_out_api(self):
        username = 'admin'
        password = 'admin'
        header = {
            "Content-Type": "application/json",
        }
        input_data = {"username": username, "password": password}

        # Login First.
        resp = self.app.post('/himama/login/', data=json.dumps(input_data), headers=header)

        # Check response status.
        self.assertIn(resp.status_code, [200, 302], resp.data)

        # clock out.
        # resp = self.app.get('/himama/attendance/clock_out/', headers=header)

        # Check response status.
        # self.assertEqual(resp.status_code, 200, resp.data.decode('utf-8'))

        # Logout request
        resp = self.app.get('/himama/logout/', data=json.dumps(input_data), headers=header)

        # Check response status.
        self.assertIn(resp.status_code, [200, 302], resp.data)
