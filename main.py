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
    parent_pid = os.getpid()

    @orphan_process
    def func_at_crash():
        try:
            psutil.Process(parent_pid).wait()
        except psutil._exceptions.NoSuchProcess:
            pass  # original process must already be finished!
        func(*args, **kwargs)

    return func
