from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User

# Let's configure our app to use a different database for tests
app.config['DATABASE_URL'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        self.client = app.test_client()

        test_user = User(first_name="test_first",
                                    last_name="test_last",
                                    img_url=None)

        second_user = User(first_name="test_first_two", last_name="test_last_two",
                           img_url=None)

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Tests show_user_list()"""
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_delete_user(self):
        """tests show_delete_user()"""
        # test for delete something that doesnt exist
        with self.client as c:
            resp = c.post(f"/users/{self.user_id}/delete",
                          follow_redirects=True)
            self.assertEqual(resp.status_code, 302)
            html = resp.get_data(as_text=True)
            self.assertNotIn("test_first", html)
            self.assertNotIn("test_last", html)

    def test_show_user(self):
        """tests show_user_detail()"""
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_add_user(self):
        """tests add_new_user() post"""
        with self.client as c:
            resp = c.post(f"/users/new",
                          data=dict(
                              first_name="add_first_test",
                              last_name="add_last_test",
                              img_url=""),
                          follow_redirects=True
                          )

            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("add_first_test", html)
            self.assertIn("add_last_test", html)

    def test_edit_user(self):
        """tests edit_user() post"""
        # consider the sad path!
        with self.client as c:
            resp = c.post(f"/users/new",
                          data=dict(
                              first_name="edit_first_test",
                              last_name="edit_last_test",
                              img_url=""),
                          follow_redirects=True
                          )

            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("edit_first_test", html)
            self.assertIn("edit_last_test", html)
