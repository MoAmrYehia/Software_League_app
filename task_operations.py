# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 20:47:41 2020

@author: dinaa
"""
import datetime
import threading 
import continuous_threading
import time
from tinydb import TinyDB, Query 
from operator import itemgetter

db_tasks=TinyDB('taskdb.json')
tasks=Query()


class Manage():
    """Class that manages operations on the user's tasks"""
    def __init__(self,username):
        self.username = username
        self.unsorted_tasks = db_tasks.search(tasks.username == self.username)
        self.x = len(self.unsorted_tasks)

          
    def sort_by_name(self):
        """Sorts the user's tasks alphabetically."""
        self.unsorted_tasks.sort(key=lambda x: x['task'])
        self.result = sorted(self.unsorted_tasks, key=itemgetter('task'))
        for i in self.result:
            print(i['task'])
 

    def sort_by_end_date(self):
        """Sorts the user's tasks based on end-date"""
        self.unsorted_tasks.sort(key=lambda x: datetime.datetime.strptime(x['end_date'], '%d/%m/%Y %H:%M:%S'))
  
        for i in range(self.x):
            self.unsorted_tasks[i]['end_date'] = datetime.datetime.strptime(self.unsorted_tasks[i]['end_date'], '%d/%m/%Y %H:%M:%S')
            print(self.unsorted_tasks[i]['task'])


        
    def show_progress(self):
        """Shows finished and on-going tasks."""
        self.on_going_tasks = db_tasks.search((tasks['status'] == "On-going") & (tasks.username == self.username))
        for i in self.on_going_tasks:
            print("On-going task, " , i['task'])
        self.finished_tasks = db_tasks.search((tasks.status == "Finished") & (tasks.username == self.username))
        if self.finished_tasks:
            for i in self.finished_tasks:
                print("Finished task, ", i["task"])

    
          
    def show_weekly_report(self):
        """Produces a weekly report every Friday that shows (un)/finished tasks."""
        if datetime.date.today().weekday() == 5: #5 means Friday
            self.total_score = 0
            self.finished_tasks = db_tasks.search((tasks.status == "Finished") & (tasks.username == self.username))
            for i in range (0,len(self.finished_tasks)):
                self.total_score = self.finished_tasks[i]["score"] + self.total_score
            if self.finished_tasks:
                print("Congratulations! Your overall score is" , self.total_score)
                print("You have finished the following tasks: ")
                for i in self.finished_tasks:
                    print("Finished task:", i["task"])
            self.on_going_tasks = db_tasks.search((tasks['status'] == "On-going") & (tasks.username == self.username))
            if self.on_going_tasks:
                print("\nYou still have to finish the following tasks:")
                for i in self.on_going_tasks:
                    print(i['task'], ">>>", i["end_date"])


    def push_notifications(self):
        """Pushes a notification at the task's end date."""
        self.count = self.x #The number of tasks for each user which will determine the end conidition of the while loop
        #Making sure that all end_dates are in datetime format not str
        for i in range (0,self.x):
            try:
                self.unsorted_tasks[i]['end_date'] = datetime.datetime.strptime(self.unsorted_tasks[i]['end_date'], '%d/%m/%Y %H:%M:%S')  
            except: 
                pass
        # Measuring the time now and calculating the difference between it and the end_date of the task
        while self.count:
            for i in range (0,self.x): #Iterating over the tasks where x is the number of tasks
                 self.now = datetime.datetime.now().replace(microsecond=0)
           #     print(type(self.now))
           #     print(type(self.unsorted_tasks[i]["end_date"]))
                 self.diff = (self.unsorted_tasks[i]["end_date"] - self.now).total_seconds() #Time difference
                 
                 if int(self.diff) == 0 and self.unsorted_tasks[i]["status"] == "On-going":
                    print("Task deadline reminder for >> ", self.unsorted_tasks[i]["task"])
                    self.count = self.count - 1
                 else:
                     print(self.diff)
            time.sleep(10) # We check for new tasks every 10 seconds

 



manage_dina = Manage("dinaashraf")

#manage_dina.sort_by_end_date()
#manage_dina.show_weekly_report()
#manage_dina.sort_by_name()
#manage_dina.show_progress()
#manage_dina.push_notifications()

#Running a thread
th = threading.Thread(target = manage_dina.push_notifications(), ).start()


