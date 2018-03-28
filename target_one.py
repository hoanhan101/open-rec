"""
    target_one.py - Use OpenREC for a specific user
    Author: Hoanh An (hoanhan@bennington.edu)
    Date: 3/27/18
"""

import time

import numpy as np
from pprint import pprint

from worker import Worker
from config import *


if __name__ == "__main__":
    start_time = time.time() 
    print(LOGO)

    configs = {
        'MF_STEPS': MF_STEPS,
        'MF_GRAMMA': MF_GAMMA,
        'MF_LAMDA': MF_LAMDA,
        'NUMS_RECOMMENDATIONS': NUMS_RECOMMENDATIONS,
        'TARGET_ID': TARGET_ID
    }
    print('CONFIGS={}'.format(configs))

    threads = []


    worker_TR = Worker(thread_id=0,
                       task='top_favorites',
                       user_id=TARGET_ID,
                       limit=NUMS_RECOMMENDATIONS)

    worker_NN = Worker(thread_id=1,
                       task='nearest_neighbours',
                       user_id=TARGET_ID,
                       limit=NUMS_RECOMMENDATIONS)

    worker_LT = Worker(thread_id=2, 
                       task='latent_factors',
                       user_id=TARGET_ID, 
                       limit=NUMS_RECOMMENDATIONS)

    worker_CC = Worker(thread_id=3,
                       task='collisions',
                       user_id=TARGET_ID,
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

    print('\nExit code 0. Runtime={}'.format(time.time() - start_time))
