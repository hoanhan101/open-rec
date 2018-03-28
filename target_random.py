"""
    target_random.py - Test random OpenREC instances
    Author: Hoanh An (hoanhan@bennington.edu)
    Date: 3/22/18
"""

import time

import numpy as np

from worker import Worker
from config import *


if __name__ == "__main__":
    start_time = time.time() 
    print(LOGO)

    threads = []

    # Run n numbers of worker in parallel.
    # For each worker, run for 4 tasks in parallel.
    for i in range(NUMS_WORKERS):
        random_id = np.random.randint(1, MAX_ID)

        worker_TR = Worker(thread_id=i,
                           task='top_favorites',
                           user_id=random_id,
                           limit=NUMS_RECOMMENDATIONS)

        worker_NN = Worker(thread_id=i,
                           task='nearest_neighbours',
                           user_id=random_id,
                           limit=NUMS_RECOMMENDATIONS)

        worker_LT = Worker(thread_id=i, 
                           task='latent_factors',
                           user_id=random_id, 
                           limit=NUMS_RECOMMENDATIONS)

        worker_CC = Worker(thread_id=i,
                           task='collisions',
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
        # print('worker_TR: {}'.format(worker_TR.data))
        # print('worker_NN: {}'.format(worker_NN.data))
        # print('worker_LT: {}'.format(worker_LT.data))
        # print('worker_CC: {}'.format(worker_CC.data))

    print('\nExit code 0. Runtime={}'.format(time.time() - start_time))
