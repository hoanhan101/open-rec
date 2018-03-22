"""
    worker.py - OpenREC Worker
    Author: Hoanh An (hoanhan@bennington.edu)
    Date: 03/22/18
"""

import threading
import time

import numpy as np

from open_rec import OpenREC
from config import *


class Worker(threading.Thread):
    def __init__(self, thread_id, task, user_id, limit):
        """
        Initialize a OpenREC's worker thread.

        Details:
            OpenREC's thread has a thread ID, an user ID, a task, and a
            maximum numbers of returning items, which then stores in memory.
        
        Params:
            thread_id (int): Thread UID
            task (string): Task be to be executed
            user_id (int): User UID
            limit (int): Number of items

        Return:
            None
        """
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.worker = OpenREC()
        self.task = task
        self.user_id = user_id
        self.limit= limit
        self.daemon = True
        self.data = []
    def run(self):
        """
        Execute a worker thread given a specific task.

        Params:
            None

        Return:
            None
        """
        # thread_lock.acquire()

        if self.task == 'nearest_neighbours':
            self.data = self.worker.execute_nearest_neighbour(uid=self.thread_id, 
                                                              active_user=self.user_id, 
                                                              limit=self.limit)
        elif self.task == 'latent_factors':
            self.data = self.worker.execute_latent_factor(uid=self.thread_id, 
                                                          active_user=self.user_id, 
                                                          limit=self.limit)
        elif self.task == 'top_favorites':
            self.data = self.worker.get_top_favorites(uid=self.thread_id, 
                                                            active_user=self.user_id, 
                                                            limit=self.limit)
        elif self.task == 'collisions':
            self.data = self.worker.check_collisions(uid=self.thread_id, 
                                                    active_user=self.user_id)
        else:
            print('\nUnavaiable command')

        # thread_lock.release()
