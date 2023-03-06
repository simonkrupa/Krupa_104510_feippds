# PPDS 02

This branch is dedicated to the second assignment - implementation of Barbershop.
Main task of the barbershop is to create multiple customers that each customer represents different thread and barber that is represented by his own thread.
We have waiting room where customers are waiting to get haircut. Waiting room has limited space, so not every customer can wait inside.
Barber is waiting for customers, after they arrive he cuts customers gradually one by one.
After customer gets haircut he leaves barbershop and waits to grow his hair, after that process repeats.

### Implementation
We have object _Shared_ that consists of 2 mutexes and 3 semaphores. These will us to ensure integrity and correct functionality of each thread.
_Shared_ also contains counter that represents number of customers in waiting room.

There are 4 functions _cut_hair()_, _balk()_, _get_haircut()_, _growing_hair()_.
Each function prints information about situations that customers and barber are in. They also invoke _sleep()_ to stimulate waiting process.

Two global variables:

_C_ : number of customers

_N_ : number of seats in waiting room

In _main()_ we create threads for customers, call function _customer()_ and thread for barber, call function _barber()_.

In function _customer()_ we have two parameters, id of customer and instance of object Shared.
While loop ensure that whole process of barbershop repeats itself.
First we need to check if there is space in waiting room by checking counter
_shared.counter_. We have to lock process to ensure that only one thread can check and possibly
increment counter at the same time. If waiting room is full we unlock mutex and call function _balk()_, thread will wait few seconds and after it will try again.
If there is space in waiting room we increment counter, unlock mutex. Multiplex on line 93 is set to N. It will let only N threads to pass at the same time. 

After we have at least one thread in waiting room we use mutex to ensure only one thread can get haircut. The thread
will signal barber that customer is ready and will wait. In function _barber()_, barber is waiting for signal. After he gets signal from customer it will cut his hair.
After process of cutting barber signal customer that cut is finished. Customer thread stops waiting and decrement counter, signal multiplex that there is new space in waiting room, we unlock a mutex and customer leaves barbershop.


