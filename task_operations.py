# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 20:47:41 2020

@author: dinaa
"""
from push_notification_sc import push_notification
import datetime
import threading
import time
from tinydb import TinyDB, Query, where
import re
import regex
import platform


Notifer=30
db_tasks = TinyDB('taskdb.json')
tasks = Query()
db_scoring = TinyDB('scoringdb.json')
scores = Query()
db = TinyDB('usrdb.json')  # defind database location as json file
users = Query()  # implementing data as user query


class Manage():
    """Class that manages operations on the user's tasks"""

    def __init__(self, username):
        self.username = username

    def show_tasks(self):
        """Shows the user's tasks."""
        unsorted_tasks = db_tasks.search(tasks.username == self.username)
        x = len(unsorted_tasks)  # Total number of tasks
        task_list = []
        for i in range(x):
            task_list.append({'task name' : unsorted_tasks[i]['task'], 'score': unsorted_tasks[i]['score'],
                                   'end_date': unsorted_tasks[i]['end_date'], 
                                   'start_date': unsorted_tasks[i]['start_date'],
                                   'partners': unsorted_tasks[i]['partners'],
                                   'place': unsorted_tasks[i]['place'],
                                   'status':  unsorted_tasks[i]['status'],
                                   'description': unsorted_tasks[i]['description'],
                                   'id': unsorted_tasks[i].doc_id
                                  })
        return task_list

    def sort_by_name(self):
        """Sorts the user's tasks alphabetically."""
        unsorted_tasks = db_tasks.search(tasks.username == self.username)
        x = len(unsorted_tasks)  # Total number of tasks
        unsorted_tasks.sort(key=lambda x: x['task'])  # Sorting by name
        task_list = []
        for i in range(x):
            task_list.append({'task name' : unsorted_tasks[i]['task'], 'score': unsorted_tasks[i]['score'],
                                   'end_date': unsorted_tasks[i]['end_date'], 
                                   'start_date': unsorted_tasks[i]['start_date'],
                                   'partners': unsorted_tasks[i]['partners'],
                                   'place': unsorted_tasks[i]['place'],
                                   'status':  unsorted_tasks[i]['status'],
                                   'description': unsorted_tasks[i]['description'],
                                   'id': unsorted_tasks[i].doc_id
                                  })
        return task_list

    def sort_by_end_date(self):
        """Sorts the user's tasks based on end-date"""
        unsorted_tasks = db_tasks.search(tasks.username == self.username)
        x = len(unsorted_tasks)  # Total number of tasks
        try:
            unsorted_tasks.sort(key=lambda x: datetime.datetime.strptime(x['end_date'], '%d/%m/%Y %H:%M'))
        except:
            pass

        task_list = []
        for i in range(x):
            task_list.append({'task name' : unsorted_tasks[i]['task'], 'score': unsorted_tasks[i]['score'],
                                   'end_date': unsorted_tasks[i]['end_date'], 
                                   'start_date': unsorted_tasks[i]['start_date'],
                                   'partners': unsorted_tasks[i]['partners'],
                                   'place': unsorted_tasks[i]['place'],
                                   'status':  unsorted_tasks[i]['status'],
                                   'description': unsorted_tasks[i]['description'],
                                   'id': unsorted_tasks[i].doc_id
                                  })
        return task_list
    
    
    
  def show_ongoing_tasks(self):
        """Shows on-going tasks."""
        ongoing_list = []  # List of on-going tasks
        on_going_tasks = db_tasks.search((tasks['status'] == "On-going") & (tasks.username == self.username))
        
        for i in range(len(on_going_tasks)):
            ongoing_list.append({'task name' : on_going_tasks[i]['task'], 'score': on_going_tasks[i]['score'],
                                   'end_date': on_going_tasks[i]['end_date'], 
                                   'start_date': on_going_tasks[i]['start_date'],
                                   'partners': on_going_tasks[i]['partners'],
                                   'place': on_going_tasks[i]['place'],
                                   'status':  on_going_tasks[i]['status'],
                                   'description': on_going_tasks[i]['description'],
                                   'id': on_going_tasks[i].doc_id
                                  })
        if ongoing_list:
            return ongoing_list


    def show_finished_tasks(self):
        """Shows finished tasks."""
        finished_list = []  # List of on-going tasks
        finished_tasks = db_tasks.search((tasks['status'] == "Finished") & (tasks.username == self.username))
        
        for i in range(len(finished_tasks)):
            finished_list.append({'task name' : finished_tasks[i]['task'], 'score': finished_tasks[i]['score'],
                                   'end_date': finished_tasks[i]['end_date'], 
                                   'start_date':finished_tasks[i]['start_date'],
                                   'partners': finished_tasks[i]['partners'],
                                   'place': finished_tasks[i]['place'],
                                   'status':  finished_tasks[i]['status'],
                                   'description': finished_tasks[i]['description'],
                                   'id': finished_tasks[i].doc_id
                                  })
        if finished_list:
            return finished_list
        
    def show_weekly_report(self):
        """Produces a weekly report every Friday that shows (un)/finished tasks."""
        unsorted_tasks = db_tasks.search(tasks.username == self.username)
        x = len(unsorted_tasks)
        total_score = 0  # Total score of the week
        today = datetime.datetime.today().replace(second=0, minute=0, hour=0, microsecond=0)  # Return today's date
        finished_before_deadline = []
        not_finished_before_deadline = []
        flag=0

        # Getting all days of the current week to see which tasks have been finished on this week

        day_1 = today - datetime.timedelta(days=1)
        day_2 = today - datetime.timedelta(days=2)
        day_3 = today - datetime.timedelta(days=3)
        day_4 = today - datetime.timedelta(days=4)
        day_5 = today - datetime.timedelta(days=5)
        day_6 = today - datetime.timedelta(days=6)

        if today.weekday() == 4:  # 4 means Friday
            flag=1
            for i in range(0, x):

                # Making sure all end_dates are datetime objects not str
                try:
                    unsorted_tasks[i]['end_date'] = datetime.datetime.strptime(unsorted_tasks[i]['end_date'],
                                                                                    '%d/%m/%Y %H:%M')
                    (unsorted_tasks[i]["end_date"]) = (unsorted_tasks[i]["end_date"]).replace(second=0,
                                                                                                        minute=0,
                                                                                                        hour=0,
                                                                                                        microsecond=0)
                except:
                    pass

                # Finding out which tasks were finished this week and which weren't
                if (unsorted_tasks[i][
                    'end_date']) == today or day_1 or day_2  or day_3 or day_4 or day_5 or day_6:

                    if unsorted_tasks[i]['status'] == "Finished":
                        finished_before_deadline.append(unsorted_tasks[i]["task"])
                        total_score = sunsorted_tasks[i]["score"] + total_score

                    if unsorted_tasks[i]['status'] == "On-going":
                        not_finished_before_deadline.append(unsorted_tasks[i]["task"])

        return flag, finished_before_deadline, not_finished_before_deadline, total_score
        # Returns list of finished tasks, list of not finished tasks & total score of the week

    def push_notifications(self):
        """Pushes a notification at the task's end date."""
        self.task_list = []  # List that will contain the tasks ordered

        # Getting the On-going tasks only and excluding the finished tasks

        self.on_going_tasks = db_tasks.search((tasks['status'] == "On-going") & (tasks.username == self.username))
        self.on_going_tasks.sort(key=lambda x: datetime.datetime.strptime(x['end_date'], '%d/%m/%Y %H:%M'))
        self.number_on_going = len(self.on_going_tasks)


        # Making sure that all end_dates are in datetime format not str

        for i in range(0, self.number_on_going):  # number_on_going is the no. of on-going tasks
            try:
                self.on_going_tasks[i]['end_date'] = datetime.datetime.strptime(self.on_going_tasks[i]['end_date'],
                                                                                '%d/%m/%Y %H:%M')
            except:
                pass
            self.task_list.append(self.on_going_tasks[i]['end_date'])  # Adding the tasks to the list


        # Measuring the time now and calculating the difference between it and the end_date of the task
        while self.task_list:

            self.now = datetime.datetime.now().replace(microsecond=0).replace(second=0)

            self.diff = (self.task_list[0] - self.now).total_seconds()  # Time difference in seconds


            if int(self.diff) <= Notifer:  # Print the notification is the time difference is Notifer seconds or less assuming that will be variable
                #print( self.task_list[0])  # Task notification
                self.task_list.remove(self.task_list[0])  # Removing the task from the list after notification's done
                push_notification(self.on_going_tasks[0]['task'])

            print(self.task_list[0])
            # Sleeping until the next task
            self.now = datetime.datetime.now().replace(microsecond=0).replace(second=0)
            self.diff = (self.task_list[0] - self.now).total_seconds()  # Time difference

            if self.diff-Notifer >= 5:
                time.sleep(self.diff-Notifer)


    def set_level(self):
        """Determines silver/gold/bronze"""
        self.total_score = 0
        self.now = datetime.datetime.now().replace(microsecond=0)
        self.use = db.get(users.username == self.username)
        self.date = self.use['rdate']
        self.creation_date = datetime.datetime.strptime(self.date, '%Y-%m-%d  %H:%M:%S')
        self.creation_date = self.creation_date.replace(microsecond=0)
        self.month_diff = (self.now.year - self.creation_date.year) * 12 + (self.now.month - self.creation_date.month)

        # Score Calculation
        for i in range(self.x):
            if self.unsorted_tasks[i]['status'] == "Finished":
                self.total_score = self.unsorted_tasks[i]["score"] + self.total_score
        db.update({"score": self.total_score}, users.username == self.username)
        try:
            if (self.number_finished / self.x) >= 0.5 and (self.number_finished / self.x) < 0.7 and (
                    self.month_diff >= 1):
                db.update({"level": "Bronze"}, users.username == self.username)

            if (self.number_finished / self.x) >= 0.7 and (self.number_finished / self.x) < 0.8 and (
                    self.month_diff >= 2):  # Silver Level
                db.update({"level": "Silver"}, users.username == self.username)

            if (self.number_finished / self.x) >= 0.8 and (self.month_diff >= 3):  # Gold Level
                db.update({"level": "Gold"}, users.username == self.username)

            if self.number_on_going == 0 and self.number_finished and (self.month_diff >= 3):  # Gold Level
                db.update({"level": "Gold"}, users.username == self.username)


        except ZeroDivisionError:  # Happens if user has zero tasks
            pass

    def search(self, s_key):
        """Function that does both recommendations and search for tasks."""
        # that can both work as search and recommendation with task name Query send for both you can slice it as you wanna
        return db_tasks.search(
            tasks.task.matches(s_key + '.*', flags=re.IGNORECASE) & (tasks.username == self.username))
        #print(db_tasks.search(where('task').matches(s_key + '.*') & (tasks.username == self.username)))  # case sensitve


#print(Manage("mohamezdrazzk").sort_by_end_date())

# Running a thread
# th = threading.Thread(target = manage_razzk.push_notifications()).start()
#manage_razzk.push_notifications()
threading.Thread(target=Manage("mohamezdrazzk").push_notifications()).start()


