import os
import psutil
import multiprocessing as mp


def child_process(func, *args, **kwargs):
    p = mp.Process(target=func, args=args, kwargs=kwargs)
    p.start()
    print(p.pid)
    return func


def orphan_process(func, *args, **kwargs):

    @child_process
    def unfortunate_parent():
        child_process(func, *args, **kwargs)  # make a child process
        os._exit(0)  # abruptly die, thus orphaning the child

    return func


def atcrash(func, *args, **kwargs):
    parent_pid = os.getpid()

    @orphan_process
    def func_at_crash():
        psutil.Process(parent_pid).wait()
        func(*args, **kwargs)

    return func
