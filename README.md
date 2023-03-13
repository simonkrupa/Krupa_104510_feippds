# PPDS 2023 Krupa

This branch is dedicated to the third assignment - Dining philosophers problem.
In dining philosophers problem we have N philosophers (in our case it will be 5) and same number N of forks. 
Philosophers are sitting around one table, next to each philosopher there is fork, that means that between each philosopher there is one fork.
Each philosopher is thinking and after some time he has to eat.
To be able to eat philosopher has to pick up fork on his right side and also fork on his left side.
At the same time only two philosophers can eat, because any other philosopher will not have both forks available.

### Problem
We are having 5 philosophers. In case that each philosopher will pick fork on his right side,
we will get to situation where there is no fork left and none of philosophers can eat - deadlock.

### Waiter solution
In waiter solution (_waiter.py_) we use Semaphore that only allow NUM_PHILOSOPHERS - 1 to enter part where philosophers are picking forks.
That means there is no possibility of deadlock because if all, in our case, 4 philosophers that got through Semaphore 
try to pick fork on their right side there will still be one fork left. So one philosopher is able to pick it up and eat.
After eating the philosopher put both forks down on the table and signal Semaphore that he left, next philosopher can enter. 

### Left-handed philosopher solution
In Left-handed philosopher solution we have one left-handed philosopher. Meaning that left-handed philosopher will pick fork
on his left side first and other 4 right-handed philosophers will pick fork on their right side first. In situation where 
all right-handed philosophers picked one fork, the left-handed one will not be able to pick his fork on left side because it is
already taken by other philosopher, so he can not pick fork on his right side because he has to pick the left one first. That means he will have to wait.
Result is that there is one fork still free. It is picked up by philosopher that already ahs one fork and he can eat.

### Implementation
We have class that is shared with each thread _Shared_ with array of mutexes for each philosopher.
Functions _think_ and _eat_ are simulations for events of thinking philosopher and eating philosopher.
We have thread for each philosopher. In function _philosopher_ we have forloop (loops NUM_RUNS times). To differ left-handed philosopher from
right-handed philosophers we have if condition where we declare that philosopher with index 0 is going to be left-handed.
So he will pick _(i+1) % NUM_PHILOSOPHERS_ fork first and then _i_ fork. Other philosophers will do it the other way.




