# Gavin Berryman
# PID: 5619712
# 9/22/2024
# the function takes a sequence of numbers as an input.
# in the function we create an empty set called 'odds'. sets allow for fast testing and doesnt allow duplicates
# we iterate through each number in the sequence
# for each number we check if its odd by using operator % not equal 0 means it has a remainder, meaning its odd, and add to set
#  return true if two numbers in the set are odd


import math

def has_odd_product_pair(sequence):
    odds = set()
    for num in sequence:
        if num % 2 != 0:
            if odds:
                return True
            odds.add(num)

    return False


# driver
test_array = [9, 2, 3, 4, 5]
result = has_odd_product_pair(test_array)

# result
print(f"Array: {test_array}")
print(f"Has odd product pair: {result}")