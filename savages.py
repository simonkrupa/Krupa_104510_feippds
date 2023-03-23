"""This module implements dinning philosophers problem.
 Solution using a waiter is implemented.
 Waiter is represented by a Semaphore(4).
 """

__author__ = "Tomáš Vavro"
__email__ = "xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, Semaphore, print
from time import sleep


class Shared:
    """Represent shared data for all threads."""
    def __init__(self):
        """Initialize an instance of Shared."""
        self.mutex = Mutex()
        self.mutex_barrier = Mutex()
        self.servings = 5
        self.count = 0
        self.fullPot = Semaphore(0)
        self.emptyPot = Semaphore(0)
        self.barrier1 = Semaphore(0)
        self.barrier2 = Semaphore(0)


def getServingFromPot(shared, savage_id):
    print(f"divoch {savage_id}: beriem si porciu")
    shared.servings = shared.servings - 1


# konkurentne vykonavany kod print("divoch %2d: hodujem" % savage_id)
def cook(shared):
    while True:
        shared.emptyPot.wait()
        print("kuchar: varim")
        shared.servings = 5
        print("kuchar: uvarene")
        shared.fullPot.signal()
        print("kuchar: oddychujem")


def savage(shared, savage_id):
    #     barrier1.wait("divoch %2d: prisiel som na veceru, uz nas je %2d", savage_id, print_each_thread = True)
    #     barrier2.wait("divoch %2d: uz sme vsetci, zaciname vecerat", savage_id, print_last_thread = True)
    while True:
        shared.mutex_barrier.lock()
        shared.count += 1
        if shared.count == M:
            print(f'thread {savage_id} unlocked barrier')
            shared.barrier1.signal(M)
        shared.mutex_barrier.unlock()
        print(f'thread {savage_id} waiting barrier')
        shared.barrier1.wait()

        print(f'Thread {savage_id} in KO')
        shared.mutex.lock()
        print(f"divoch {savage_id}: pocet zostavajucich porcii v hrnci je {shared.servings}")
        if shared.servings == 0:
            print(f"divoch {savage_id}: budim kuchara")
            shared.emptyPot.signal()
            shared.fullPot.wait()
        getServingFromPot(shared, savage_id)
        shared.mutex.unlock()

        shared.mutex_barrier.lock()
        shared.count -= 1
        if shared.count == 0:
            shared.barrier2.signal(M)
        shared.mutex_barrier.unlock()
        shared.barrier2.wait()



N = 4
M = 3

if __name__ == '__main__':
    shared = Shared()

    threads = []
    for i in range(M):
        threads.append(Thread(savage, shared, i))
    chef = Thread(cook, shared)

    for t in threads + [chef]:
        t.join()