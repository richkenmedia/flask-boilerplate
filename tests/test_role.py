import unittest
from flask_dir import create_app
from flask_dir.role import role_blueprint


class TestRole(unittest.TestCase):

    # check for response 200
    def test_create(self):
        tester = flask_dir.app.test_client(self)
        response = tester.get('api/role/create')
        statuscode = reponse.status_code
        self.assertEqual(statuscode, 200)


if __name__ == "__main__":
    unittest.main()
