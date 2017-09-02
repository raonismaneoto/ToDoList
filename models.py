# -*- coding: utf-8 -*-
"""Models."""
from google.appengine.ext import ndb
import datetime
import time
from google.appengine.api import mail


class Task(ndb.Model):
    """Task model."""

    name = ndb.StringProperty(required=True)
    deadline = ndb.DateProperty(required=True)
    description = ndb.StringProperty(required=True)
    sent = ndb.BooleanProperty(default=False)
    state = ndb.StringProperty(choices=set([
        'in progress',
        'out of date'
    ]), default='in progress')

    def isToWarn(self):
        """isToWarn."""
        if(not self.sent):
            if int(self.deadline.year) - int(datetime.date.today().year) == 0:
                if int(self.deadline.month) - int(datetime.date.today().month) == 0:
                    if abs(int(self.deadline.month) - int(datetime.date.today().month)) < 2:
                        self.sent = True
                        self.put()
                        return True
        return False

    @staticmethod
    def createTask(data):
        """Create Tasks."""
        task = Task()
        task.name = data['name']
        task.description = data['description']
        deadline = data.get('deadline').split('/')
        task.deadline = datetime.date(
            int(deadline[0]), int(deadline[1]), int(deadline[2]))
        Task.setState(task)
        task_key = task.put()
        return task_key

    @staticmethod
    def setState(task):
        """Set the task's state once called."""
        current_date = time.strftime("%x")
        task_date = str(task.deadline)
        if int(task_date[2:4]) > int(current_date[6:8]):
            task.state = 'in progress'
        elif int(task_date[2:4]) < int(current_date[6:8]):
            task.state = 'out of date'
        elif int(task_date[2:4]) == int(current_date[6:8]):
            if int(task_date[5:7]) > int(current_date[0:2]):
                task.state = 'in progress'
            elif int(task_date[5:7]) < int(current_date[0:2]):
                task.state = 'out of date'
            elif int(task_date[5:7]) == int(current_date[0:2]):
                if int(task_date[8:10]) > int(current_date[3:5]):
                    task.state = 'in progress'
                elif int(task_date[8:10]) < int(current_date[3:5]):
                    task.state = 'out of date'
                else:
                    task.state = 'in progress'
        task.put()


class User(ndb.Model):
    """User model."""

    tasks = ndb.KeyProperty(kind='Task', repeated=True)
    email = ndb.StringProperty(required=True)

    def createTask(self, data):
        """Receive a call from main and call Task.createTask."""
        task_key = Task.createTask(data)
        self.tasks.append(task_key)
        self.put()

    def loadTasks(self):
        """Load the user's tasks."""
        user_tasks = []
        for task in self.tasks:
            task_id = task.id()
            task_append = task.get().to_dict()
            task_append['id'] = task_id
            user_tasks.append(task_append)
        return user_tasks

    def deleteTask(self, id):
        """Delete a task with the id."""
        finded = False
        for i in xrange(len(self.tasks)):
            if self.tasks[i].id() == int(id):
                task = self.tasks[i]
                task.delete()
                self.tasks.pop(i)
                self.put()
                finded = True
                break
        return finded

    def loadTask(self, id):
        """Load just one task."""
        for task in self.tasks:
            if task.id() == int(id):
                task_to_return = task.get()
                Task.setState(task_to_return)
                task_to_return = task_to_return.to_dict()
                task_to_return['id'] = int(id)
                return task_to_return
        return None

    def editTask(self, id, data):
        """Edit a task according with the data and id."""
        task_to_edit = None
        for task in self.tasks:
            if task.id() == int(id):
                task_to_edit = task.get()
        if task_to_edit:
            field = data['field']
            value = data['value']
            self.setField(task_to_edit, field, value).put()
            self.put()
            return True
        else:
            return False

    def setField(self, task, field, value):
        """Change a field."""
        if field == 'name':
            task.name = value
        elif field == 'deadline':
            deadline = value.split('/')
            task.deadline = datetime.date(
                int(deadline[0]), int(deadline[1]), int(deadline[2]))
        elif field == 'description':
            task.description = value
        return task

    def sendEmail(self, task):
        """sendEmail."""
        message = 'A sua task de nome %s e descricao %s vence no dia %s' % (
            task.name, task.description, task.deadline)
        subject = '%s esta vencendo.' % task.name
        mail.send_mail(sender="raoni.smaneoto@ccc.ufcg.edu.br",
                       to=self.email,
                       subject=subject,
                       body=message)
