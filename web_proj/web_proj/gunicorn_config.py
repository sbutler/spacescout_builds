import multiprocessing

preload_app = False
bind = 'localhost:18001'
workers = multiprocessing.cpu_count() * 2 + 1
