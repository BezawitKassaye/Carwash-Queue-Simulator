from collections import deque

class Washer:
    """The washer knows whether it is washing, and if it is, how long it will be until the
    next car can exit the waiting queue.
    """
    def __init__(self, wash_time):
        """Sets up a Washer instance. Make sure you know what the instance attributes should be!"""
        # YOUR CODE HERE
        self.wash_time = wash_time
        self.time_until_done = 0

    def is_busy(self):
        """Return True if the washer is currently washing (so no car can
        exit the queue yet) and False if not (the next car can be dequeued)."""
        # YOUR CODE HERE
        if self.time_until_done!= 0:
            return True 
        else:
            return False
        #raise NotImplementedError()

    def start_washing(self): 
        """Tell the washer to wash the car at the front of the
        queue by updating its attributes appropriately."""
        # YOUR CODE HERE
        self.time_until_done = self.wash_time 

    def one_second(self):
        """Update the washer's attributes to reflect the passage of one second."""
        # YOUR CODE HERE
        if self.is_busy() == True:
            self.time_until_done = self.time_until_done - 1

# Check that the Washer class does what it is supposed to:
from nose.tools import assert_equal
w = Washer(100)
assert_equal(w.wash_time, 100)
assert_equal(w.time_until_done, 0)
for key in vars(w):
    assert(key in ('wash_time', 'time_until_done'))

w.time_until_done = 1
assert(w.is_busy())
w.time_until_done = 0
assert(not w.is_busy())

w.start_washing()
assert_equal(w.time_until_done, w.wash_time)

w.time_until_done = 10
w.one_second()
assert_equal(w.time_until_done, 9)

import random
from random import SystemRandom

class ArrivalGenerator:
    def __init__(self, prob=0.5):
        """The ArrivalGenerator has one job: return True with probability `prob`.
        To do that, it needs to save the value of `prob`.
        """
        # YOUR CODE HERE

        self.probability = prob 

    def query(self):
        """Return True with probability prob. There are many different ways 
        you might use the `random` module's functions
        to do it. If you want a hint, please ask, I don't want you to get hung up on the
        math of probability too much."""
        # YOUR CODE HERE
        self.cars = random.random()
        if self.cars <= self.probability:
            return True
        return False

# Check that ArrivalGenerator does what it is supposed to do:
from nose.tools import assert_equal
a = ArrivalGenerator()
assert_equal(a.probability, 0.5)
a = ArrivalGenerator(0.9)
assert_equal(a.probability, 0.9)

arrivals_list = (a.query() for _ in range(1_000_000))
number_of_arrivals = sum([1 for x in arrivals_list if x])
# You should get something very close to 900000
assert(899000 < number_of_arrivals and number_of_arrivals < 901000)
# If it fails, but you think you are right, just try again. It is probabilistic,
# so could be false negative. But two false negatives is unlikely to happen.

""" Tracking The Average Waiting Time"""

class AverageTracker:
    def __init__(self):
        """The average tracker just needs to know the total of all numbers
        it has received so far and how many numbers it's received."""
        # YOUR CODE HERE

        self.count = 0
        self.sum_ = 0

    def next_value(self, val):
        """This method adds `val` to the total received so far and increments
        the number of values received."""
        # YOUR CODE HERE

        #self.sum_ =sum(self.w_time)
        #return self.count
    
        self.count += 1
        #print(self.count)
        self.sum_ +=val
        #print(self.sum_)
        
    


    def average(self):
        """Return the average of all the values so far."""
        # YOUR CODE HERE

        return self.sum_ /self.count
    def number_of_values(self):
        """Return the number of values received so far."""
        # YOUR CODE HERE
        return self.count
    
a = AverageTracker()
random_value_list = [random.random() for _ in range(6000)]
for val in random_value_list:
    a.next_value(val)
print(a.average())

from nose.tools import assert_equal
import random
at = AverageTracker()
assert_equal(at.count, 0)
assert_equal(at.sum_, 0)
for key in vars(at):
    assert(key in ('count', 'sum_'))

at = AverageTracker()
random_value_list = [random.random() for _ in range(1000)]
for val in random_value_list:
    at.next_value(val)

assert_equal(at.count, len(random_value_list))
assert_equal(at.sum_, sum(random_value_list))
assert(at.average() == sum(random_value_list)/len(random_value_list))

""" Testing Your Simulation"""

from collections import deque

prob = 0.004
simulation_time = 6000
wash_time = 150

# YOUR CODE HERE

def simulation (prob, simulation_time, wash_time):
    queue_wash = deque()
    w = Washer(wash_time)
    avg_time = AverageTracker()
    car_arrival = ArrivalGenerator(prob)
    
    for second in range(simulation_time):
        if car_arrival.query():
            queue_wash.appendleft(second)
            
        if (not w.is_busy()) and len(queue_wash) != 0:
            timestamp = queue_wash.pop()
            avg_time.next_value(second-timestamp)
            
            w.start_washing()
            
        w.one_second()
        
    avg = avg_time.average()
    print(avg)
    wash_count = avg_time.number_of_values()
    
    print(f'The car wash washed {wash_count} cars with an average waiting time of {avg} seconds, in {simulation_time} seconds with a probability of {prob} cars arriving each second.')
    return avg, wash_count


simulation(prob, simulation_time, wash_time)

""" Simulate """

def ten_thousand_runs():
    """
    Get lists of ten thousand counts and averages from the simulator.
    Return the lists like this:
    return counts, averages
    """
    # YOUR CODE HERE
    counts = []
    averages = []
    for _ in range(10000):
        count, avg = simulation(0.004, 6000,150)
        counts.append(counts)
        averages.append(avg)
    return counts, averages


counts, averages = ten_thousand_runs()

""" Graph Simulated Result"""

import matplotlib.pyplot as plt

plt.style.use('seaborn-whitegrid')
plt.plot(counts, averages, '.', color='black')
plt.xlabel("counts")
plt.ylabel("average wait time");