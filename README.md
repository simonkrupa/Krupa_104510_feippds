# PPDS 01

This branch is dedicated to the first assignment - implementation of Bakery Algorithm.
### Bakery Algorithm
Aim of this algorithm is to solve critical section problem in parallel systems. Each process receives number that determinate when is process allowed to execute critical section.
### Implementation
We initialize two arrays as global variables with length N (N - number of threads) and fill them with zeros. The first array '*num*' will hold numbers for each process that determinate their order. The second array '*in_*' will check if thread is in process of generating its order number.
We create function _process_ that each thread will call. The function has two arguments:

_tid_ - thread id

_num_runs_ - number of runs each thread will do, if number of runs is not declared its default value is 1

The function is wrapped in forloop (number of runs). 

Each thread will receive its order. Variable _i_ is thread id. We assign value 1 (True) to _in__[i]. We find maximal value from array _num_, at start it will be 0 because the array is filled with zeros and add 1 to it. That will be order of the first thread with id _i_. 
After thread receive order number we assign value 0 (False) back to _in__[i].

```
i = tid
in_[i] = 1
num[i] = 1 + max(num)
in_[i] = 0
```

Next there is forloop (number of threads) where we loop through each thread and check if it is current thread's turn to continue to critical section.



```
for j in range(NUM_THREADS):
    while in_[j] == 1:
        continue

    # wait for other processes to finish their execution of critical section
    while num[j] != 0 and (num[j] < num[i] or (num[j] == num[i] and j < i)):
        continue
```
The first condition is checking if looped thread is not choosing it's order number at the moment. If it is the current thread has to wait.

If the order of thread with id _j_ is not zero and is lower than the current thread or if they are equal but j < i, the current thread has to wait till thread/threads with lower order number finish their critical section.

After thread complete all checks it continues to critical section and after exiting critical section we set order for the thread back to zero, so other threads with higher order number can continue.

```num[i] = 0```

### Conclusion
The Bakery Algorithm is working because only one thread can enter critical section at the time. We have order number for each thread that wants to enter critical section and conditions that take care of allowing only one thread to enter critical section in corresponding order.
No thread is preventing other threads to enter critical section only if the thread itself is in critical section at the time.
There is no possibility of deadlock, each process will end. After process request to enter critical section, there is no possibility for other process to request entering critical section and getting into critical section before the first process. The order is given.

