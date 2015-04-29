import multiprocessing

bind = 'localhost:19000'
workers = multiprocessing.cpu_count() * 2 + 1
