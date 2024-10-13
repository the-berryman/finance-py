# Names: Mia Bruno (PID: 4399000), Gavin Berryman (PID: 5619712), Devin Davis (PID: 3921337)
# Date: 9/22/2024


import math
from typing import List

# Function #1 C-1.15
#  takes a sequence of numbers and determines if all the numbers are different from each other
def distinct(data):
# List Comprehension
    distinct_pair = {x for x in data}
    print(distinct_pair)
    if len(distinct_pair) == len(data):
        return True
    return False

# Driver code function 1
print("Problem #1: ")
list1 = [1, 3, 5, 7, 9, 10, 12, 13] #Distinct
list2 = [1, 1, 2, 3, 3, 4, 5, 6, 6, 7] #Not Distinct
print(distinct(list1))
print(distinct(list2))

# Function #2  C-1.22
#  takes two arrays a and b of length n storing int values, and returns the dot product of a and b
def product(a: List[int], b: List[int]) -> List[int]:
    c = []
    for i in range((len(a)+len(b)-len(a))):
        c.append(a[i] * b[i])
    return c

#Driver code function 2
print("Problem #2: ")
list1 = [2,-4,7,5,4,8]
list2 = [7,-6,-3,0,3,6]
print(product(list1,list2))

# Function #3 C-1.28
# find the Euclidean norm or length of the vector based on p=2 and vector coordinates
def norm(v, p):
    solution = math.sqrt(v[0]**p + v[1]**p)
    return solution

# Driver code function 3
print("Problem #3: ")
vector1 = (3,4)
print(norm(vector1, 2))
vector2 = (5,12)
print(norm(vector2, 2))




