
"""Main."""
import webapp2
from models import User
import json
from utils import data2json
from google.appengine.api import users


def login_required(method):
    """A login_required decorator."""
    def check_login(self, *args):
        user_google = users.get_current_user()
        if user_google is None:
            self.response.set_status(401)
            self.response.headers[
                'Content-Type'] = 'application/json; charset=utf-8'
            self.response.write('{"msg": "erro de autenticacao"}')
            return
        else:
            user = User.query(User.email == user_google.email()).fetch(1)
            if not user:
                user = User()
                user.email = user_google.email()
                user.put()
            else:
                user = user[0]
        method(self, user, *args)
    return check_login


class LoginHandler(webapp2.RequestHandler):
    """LoginHandler."""

    def get(self):
        """Redirect the user."""
        self.redirect(users.create_login_url('/'))


class LogoutHandler(webapp2.RequestHandler):
    """LogoutHandler."""

    def get(self):
        """Redirect the user, if there is one."""
        user = users.get_current_user()
        if user:
            self.redirect(users.create_logout_url('/'))


class MultiDoHandler(webapp2.RequestHandler):
    """Handler that handles with multiples results."""

    @login_required
    def get(self, user):
        """Get all tasks."""
        user_tasks = user.loadTasks()
        self.response.headers[
            'Content-Type'] = 'application/json; charset=utf-8'
        self.response.write(data2json(user_tasks).encode('utf-8'))

    @login_required
    def post(self, user):
        """Post a task."""
        data = json.loads(self.request.body)
        user.createTask(data)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.set_status(201)


class SingleDoHandler(webapp2.RequestHandler):
    """Handler that handles with singles results."""

    @login_required
    def delete(self, user, id):
        """Delete a task by the id."""
        if user.deleteTask(id):
            self.response.headers['Content-Type'] = 'application/json'
            self.response.set_status(201)
        else:
            self.response.headers['Content-Type'] = 'application/json'
            self.response.set_status(204)

    @login_required
    def get(self, user, id):
        """Get a task by id."""
        if user.loadTask(id) is None:
            self.response.set_status(404)
        else:
            self.response.headers[
                'Content-Type'] = 'application/json; charset=utf-8'
            self.response.write(
                data2json(user.loadTask(id)).encode('utf-8'))

    @login_required
    def post(self, user, id):
        """Edit a task."""
        data = json.loads(self.request.body)
        if user.editTask(id, data):
            self.response.set_status(201)
        else:
            self.response.set_status(404)


class DeadLineHandler(webapp2.RequestHandler):
    """DeadLineHandler."""

    def get(self):
        """Handle get requests."""
        users = []
        query = User.query()
        users = [user for user in query]
        for user in users:
            for task in user.tasks:
                task = task.get()
                if task.isToWarn():
                    user.sendEmail(task)


app = webapp2.WSGIApplication([
    ('/api/multido', MultiDoHandler),
    ('/api/singledo/(\d+)', SingleDoHandler),
    ('/api/login', LoginHandler),
    ('/api/logout', LogoutHandler),
    ('/api/deadline', DeadLineHandler)
], debug=True)
