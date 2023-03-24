"""This module implements feasting savages problem.
Implementation with one cook (chef).
 """

__author__ = "Tomáš Vavro, Marián Šebeňa"
__email__ = "xkrupas@stuba.sk"
__license__ = "MIT"


from fei.ppds import Thread, Mutex, Semaphore, print
from time import sleep

NUMBER_OF_SAVAGES = 3
SIZE_OF_POT = 5


class Shared:
    """Represent shared data for all threads."""
    def __init__(self):
        """Initialize an instance of Shared."""
        self.mutex = Mutex()
        self.mutex_barrier = Mutex()
        self.servings = SIZE_OF_POT
        self.count = 0
        self.fullPot = Semaphore(0)
        self.emptyPot = Semaphore(0)
        self.barrier1 = Semaphore(0)
        self.barrier2 = Semaphore(0)


def get_serving_from_pot(shared, savage_id):
    print(f"Divoch {savage_id}: beriem si porciu.")
    shared.servings = shared.servings - 1
    sleep(1)


def cook(shared):
    while True:
        shared.emptyPot.wait()
        print("Kuchar: varim")
        sleep(5)
        shared.servings = 5
        print("Kuchar: uvarene")
        shared.fullPot.signal()
        print("Kuchar: oddychujem")


def savage(shared, savage_id):
    while True:
        shared.mutex_barrier.lock()
        shared.count += 1
        if shared.count == NUMBER_OF_SAVAGES:
            print(f'Divoch {savage_id}: unlocked barrier')
            shared.barrier1.signal(NUMBER_OF_SAVAGES)
        shared.mutex_barrier.unlock()
        shared.barrier1.wait()

        print(f'Divoch {savage_id}: in KO')
        shared.mutex.lock()
        print(f"Divoch {savage_id}: pocet zostavajucich porcii v hrnci je {shared.servings}")
        if shared.servings == 0:
            print(f"Divoch {savage_id}: budim kuchara")
            shared.emptyPot.signal()
            shared.fullPot.wait()
        get_serving_from_pot(shared, savage_id)
        shared.mutex.unlock()

        shared.mutex_barrier.lock()
        shared.count -= 1
        if shared.count == 0:
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
