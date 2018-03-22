"""
    worker.py - OpenREC's Worker
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
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.worker = OpenREC()
        self.task = task
        self.user_id = user_id
        self.limit= limit
        self.daemon = True
        self.data = []
    def run(self):
        thread_lock.acquire()
        if self.task == 'nearest_neighbours':
            self.data = self.worker.execute_nearest_neighbour(uid=self.thread_id, 
                                                              active_user=self.user_id, 
                                                              limit=self.limit)
        elif self.task == 'latent_factor':
            self.data = self.worker.execute_latent_factor(uid=self.thread_id, 
                                                          active_user=self.user_id, 
                                                          limit=self.limit, 
                                                          steps=3)
        elif self.task == 'top_recommendations':
            self.data = self.worker.get_top_recommendations(uid=self.thread_id, 
                                                            active_user=self.user_id, 
                                                            limit=self.limit)
        elif self.task == 'check_collision':
            self.data = self.worker.check_collision(uid=self.thread_id, 
                                                    active_user=self.user_id)
        else:
            print('\nUnavaiable command')

        thread_lock.release()


if __name__ == "__main__":
    start_time = time.time() 
    print(LOGO)

    NUMS_WORKERS = 2
    NUMS_RECOMMENDATIONS = 3
    MAX_ID = 10

    thread_lock = threading.Lock()
    threads = []

    for i in range(NUMS_WORKERS):
        random_id = np.random.randint(1, MAX_ID)

        worker_TR = Worker(thread_id=i,
                             task='top_recommendations',
                             user_id=random_id,
                             limit=NUMS_RECOMMENDATIONS)

        worker_NN = Worker(thread_id=i,
                             task='nearest_neighbours',
                             user_id=random_id,
                             limit=NUMS_RECOMMENDATIONS)

        worker_LT = Worker(thread_id=i, 
                           task='latent_factor',
                           user_id=random_id, 
                           limit=NUMS_RECOMMENDATIONS)

        worker_CC = Worker(thread_id=i,
                             task='check_collision',
                             user_id=random_id,
                             limit=NUMS_RECOMMENDATIONS)

        worker_TR.start()
        worker_NN.start()
        worker_LT.start()
        worker_CC.start()

        threads.append(worker_TR)
        threads.append(worker_NN)
        threads.append(worker_LT)
        threads.append(worker_CC)

        for t in threads:
            t.join()

        print('')
        print('worker_TR: {}'.format(worker_TR.data))
        print('worker_NN: {}'.format(worker_NN.data))
        print('worker_LT: {}'.format(worker_LT.data))
        print('worker_CC: {}'.format(worker_CC.data))

    print('\nExit code 0. Runtime={}'.format(time.time() - start_time))
