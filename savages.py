"""This module implements feasting savages problem.
Implementation with one cook (chef).
 """

__author__ = "Tomáš Vavro, Marián Šebeňa, Šimon Krupa"
__email__ = "xkrupas@stuba.sk"
__license__ = "MIT"

import random

from fei.ppds import Thread, Mutex, Semaphore, print
from time import sleep

NUMBER_OF_SAVAGES = 4
SIZE_OF_POT = 5


class Shared:
    """Represent shared data for all threads."""
    def __init__(self):
        """Initialize an instance of Shared.
        Two mutexes and two semaphores for reusable barrier.
        Counter and number of servings.
        Two semaphores for signalization.
        """
        self.mutex = Mutex()
        self.mutex_barrier = Mutex()
        self.servings = SIZE_OF_POT
        self.count = 0
        self.fullPot = Semaphore(0)
        self.emptyPot = Semaphore(0)
        self.barrier1 = Semaphore(0)
        self.barrier2 = Semaphore(0)


def get_serving_from_pot(shared, savage_id):
    """Function for simulating savage that is getting his serving from pot.
    Edits number of servings in pot.

    :param shared: instance of object Shared
    :param savage_id: id of savage(thread)
    """
    print(f"Savage {savage_id}: taking a serving.")
    shared.servings = shared.servings - 1
    sleep(1)


def cook(shared):
    """Function that creates functionality of single cook in this implementation.

    :param shared: instance of object Shared
    """
    while True:
        shared.emptyPot.wait()
        print("COOK: cooking")
        sleep(5)
        shared.servings = SIZE_OF_POT
        print("COOK: finished cooking")
        shared.fullPot.signal()


def savage(shared, savage_id):
    """Function that creates functionality for each savage.
    Uses reusable barrier, signalization and mutexes.

    :param shared: instance of object Shared
    :param savage_id: id of savage(thread)
    """
    while True:
        shared.mutex_barrier.lock()
        shared.count += 1
        if shared.count == NUMBER_OF_SAVAGES:
            print(f'Savage {savage_id}: unlocked barrier, all savages ready')
            shared.barrier1.signal(NUMBER_OF_SAVAGES)
        shared.mutex_barrier.unlock()
        shared.barrier1.wait()

        print(f'Savage {savage_id}: in KS')
        shared.mutex.lock()
        print(f"Savage {savage_id}: number of remaining servings in pot {shared.servings}")
        if shared.servings == 0:
            print(f"Savage {savage_id}: pot is empty, waking up cook")
            shared.emptyPot.signal()
            shared.fullPot.wait()
            print(f'Pot is full')
        get_serving_from_pot(shared, savage_id)
        shared.mutex.unlock()

        print(f'Savage {savage_id}: eating')
        sleep(random.randint(2, 4))

        shared.mutex_barrier.lock()
        shared.count -= 1
        if shared.count == 0:
            print(f'Savage {savage_id}: locked barrier')
            shared.barrier2.signal(NUMBER_OF_SAVAGES)
        shared.mutex_barrier.unlock()
        shared.barrier2.wait()
        sleep(3)


if __name__ == '__main__':
    shared = Shared()

    threads = []
    for i in range(NUMBER_OF_SAVAGES):
        threads.append(Thread(savage, shared, i))
    chef = Thread(cook, shared)

    for t in threads + [chef]:
        t.join()
