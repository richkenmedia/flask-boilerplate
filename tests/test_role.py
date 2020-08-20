import unittest
from skill_tracker import create_app
from skill_tracker.role import role_blueprint


class TestRole(unittest.TestCase):

    # check for response 200
    def test_create(self):
        tester = skill_tracker.app.test_client(self)
        response = tester.get('api/role/create')
        statuscode = reponse.status_code
        self.assertEqual(statuscode, 200)


if __name__ == "__main__":
    unittest.main()
