# PPDS 2023 Krupa

This branch is dedicated to the third assignment - feasting savages. In this implementation 
we will simulate feasting of savages. Savages are taking their servings from big pot which 
is prepared by cook, another thread. All savages are feasting at the same time. When they are all 
ready they can start getting their servings from pot. If pot is empty, the cook is alerted and 
starts to cook new food. After he refills the pot, savages can continue taking their meal.
This repeats in infinite loop, after all savages have eaten they will eventually get hungry again.
Hungry savage has to wait for others again to start the feast. This is description of feasting savages with only one cook.

### Implementation

In this implementation, feasting savages with one cook, we will create class _Shared_, that will 
be shared between all threads. We have threads for each savage and one additional thread for the cook.
```
self.mutex = Mutex()
self.mutex_barrier = Mutex()
self.servings = SIZE_OF_POT
self.count = 0
self.fullPot = Semaphore(0)
self.emptyPot = Semaphore(0)
self.barrier1 = Semaphore(0)
self.barrier2 = Semaphore(0)
```
The core function _savage_ contains infinite loop. We have reusable barrier. This part of code 
shows the first part of this barrier. We use mutex, counter set to 0, semaphore(0) that are initialized 
in shared class. Mutex ensures integrity of counter. Counter is being incremented by every thread(savage)
that starts waiting on barrier. If last savage increment counter it will meet condition of if statement
and signal semaphore. All threads can enter.
```
shared.mutex_barrier.lock()
shared.count += 1
if shared.count == NUMBER_OF_SAVAGES:
    print(f'Savage {savage_id}: unlocked barrier, all savages ready')
    shared.barrier1.signal(NUMBER_OF_SAVAGES)
shared.mutex_barrier.unlock()
shared.barrier1.wait()
```

In next section savages one by one (mutex) get serving from pot. There is function _get_serving_from_pot_
that decrement number of servings in pot. Before this function we have to check if there is serving in the pot.
If there is not we signal to cook to start cooking and meanwhile savage wait. There is function _cook_ that is also infinite loop.
It is waiting for this signal. After some time it sets servings to full and signal back to savage that pot is full again.
After the signal savage can continue.
```
if shared.servings == 0:
print(f"Savage {savage_id}: pot is empty, waking up cook")
shared.emptyPot.signal()
shared.fullPot.wait()
print(f'Pot is full')
```

```
def cook(shared):
    while True:
        shared.emptyPot.wait()
        print("COOK: cooking")
        sleep(5)
        shared.servings = SIZE_OF_POT
        print("COOK: finished cooking")
        shared.fullPot.signal()
```

Next there is process of eating not encapsulated in mutex so savages may eat in parallel. 

Last part is to make our barrier reusable. Savages after eating wait on barrier, each savage decrements counter. 
Last savage that shows up signal the barrier and release all savages to again repeat the loop.



