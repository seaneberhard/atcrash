import os
import psutil
import multiprocessing as mp


def child_process(func, *args, **kwargs):
    mp.Process(target=func, args=args, kwargs=kwargs).start()
    return func


def orphan_process(func, *args, **kwargs):

    @child_process
    def unfortunate_parent():
        child_process(func, *args, **kwargs)  # make a child process
        os._exit(0)  # abruptly die, thus orphaning the child

    return func


def atcrash(func, *args, **kwargs):
    main_process = psutil.Process(os.getpid())

    @orphan_process
    def func_at_crash():
        main_process.wait()
        func(*args, **kwargs)

    return func
