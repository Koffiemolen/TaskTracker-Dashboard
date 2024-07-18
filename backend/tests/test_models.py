"""Test the User model."""
import unittest
# from models.user_model import User_model  # pylint: disable=import-error
from app.models.user_model import User  # pylint: disable=import-error


class TestUserModel(unittest.TestCase):
    """ Test the User model. """
    def setUp(self):
        # Setup code if needed
        pass

    def test_user_creation(self):
        """ Test user creation. """
        user = User(username="testuser", email="testuser@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")

    def test_user_creation_with_local_account(self):
        """ Test user creation with local account. """
        user = User(username="testuser", email="testuser@contoso.com", local_account=True)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@contoso.com")
        self.assertTrue(user.local_account)

    def test_user_deletion(self):
        """ Test user deletion. """
        user = User(username="testuser", email="testuser@contoso.com")
        user.deleted = True
        self.assertTrue(user.deleted)

if __name__ == "__main__":
    unittest.main()
