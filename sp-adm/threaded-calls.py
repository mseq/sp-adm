#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" An exercise to understand threads. """

import logging
import threading
import time
import concurrent.futures

def thread_function(name, bs):
    logging.info("Thread %s: starting " + bs, name)
    time.sleep(2)
    logging.info("Thread %s: finishing " + bs, name)

# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")

#     threads = list()
#     for index in range(3):
#         logging.info("Main    : create and start thread %d.", index)
#         x = threading.Thread(target=thread_function, args=(index,))
#         threads.append(x)
#         x.start()

#     for index, thread in enumerate(threads):
#         logging.info("Main    : before joining thread %d.", index)
#         thread.join()
#         logging.info("Main    : thread %d done", index)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for i in range(1,10):
            executor.submit(thread_function, i, 'Bullshit')
            # executor.map(thread_function, args(range(10), 'Bullshit'))

    print("Ended")