"""
This module is implementation of Lamport's Bakery Algorithm.
Module works for multiple threads.
Threads can run multiple times.
"""

__author__ = "Šimon Krupa, Tomáš Vavro"
__email__ = "xkrupas@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread

NUM_RUNS = 1
NUM_THREADS = 8
num = [0] * NUM_THREADS
in_ = [0] * NUM_THREADS


def process(tid, num_runs=1):
    """Simulates a process.

    Arguments:
        tid      -- thread id
        num_runs -- number of executions of the critical section, if not declared set to 1
    """
    global num
    global in_

    for n in range(num_runs):
        i = tid
        # assign order number
        in_[i] = 1
        num[i] = 1 + max(num)
        in_[i] = 0

        for j in range(NUM_THREADS):
            # wait if process is assign its order number at the moment
            while in_[j] == 1:
                continue

            # wait for other processes to finish their execution of critical section
            while num[j] != 0 and (num[j] < num[i] or (num[j] == num[i] and j < i)):
                continue

        # execute critical section
        print(f"Process {tid} runs a complicated computation!")

        # exit critical section
        num[i] = 0


if __name__ == '__main__':
    threads = [Thread(process, i, NUM_RUNS) for i in range(NUM_THREADS)]
    [t.join() for t in threads]
