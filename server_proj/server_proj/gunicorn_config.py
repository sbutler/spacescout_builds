import multiprocessing

bind = 'localhost:18000'
workers = multiprocessing.cpu_count() * 2 + 1
