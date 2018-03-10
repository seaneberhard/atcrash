import os
from main import atcrash


@atcrash
def life_after_death():
    print('Hello from the afterlife!')


os._exit(0)
