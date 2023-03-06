"""
Program represents different sequences of using mutex
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""


__authors__ = "Marián Šebeňa, Matúš Jokay, Šimon Krupa"
__email__ = "xkrupas@stuba.sk"
__license__ = "MIT"


from fei.ppds import Mutex, Thread, Semaphore, print
from time import sleep
from random import randint


class Shared(object):

    def __init__(self):
        self.mutex = Mutex()
        self.mutex2 = Mutex()
        self.mutex3 = Mutex()
        self.counter = 0
        self.multiplex = Semaphore(N)
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)


def get_haircut(i):
    print(f'\nCustomer {i} getting a haircut')


def cut_hair():
    print("\nBarber cuts a haircut")
    sleep(randint(2,4))


def balk(i):
    print(f'Customer {i} entered, but waiting room is full')
    sleep(randint(2, 5))


def growing_hair(i):
    print(f'Customer {i} left and is growing his hair')
    sleep(randint(4, 8))


def customer(i, shared):
    while True:
        shared.mutex.lock()
        if shared.counter == N:
            shared.mutex.unlock()
            balk(i)
            continue
        elif shared.counter < N:
            shared.counter += 1
            shared.mutex.unlock()
        shared.multiplex.wait()
        print(f'Customer {i} enters')

        shared.mutex2.lock()
        shared.barber.signal()
        get_haircut(i)
        shared.customer.wait()

        shared.counter -= 1
        shared.multiplex.signal()
        shared.mutex2.unlock()
        growing_hair(i)


def barber(shared):
    while True:
        shared.barber.wait()
        cut_hair()
        shared.customer.signal()


def main():
    shared = Shared()
    customers = []

    for i in range(C):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)

    for t in customers + [hair_stylist]:
        t.join()


C = 5
N = 3

if __name__ == "__main__":
    main()