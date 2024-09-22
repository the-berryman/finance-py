# Gavin Berryman
# PID: 5619712
# 9/22/2024
#

import math

def has_odd_product_pair(sequence):
    odds = set()
    for num in sequence:
        if num % 2 != 0:
            if 1 in odds:
                return True
            odds.add(num)

    return False


# driver
test_array = [1, 2, 3, 4, 5]
result = has_odd_product_pair(test_array)

# result
print(f"Array: {test_array}")
print(f"Has odd product pair: {result}")