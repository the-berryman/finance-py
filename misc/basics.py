# Gavin Berryman
# COT5480
# PID:
# Submission date 09-04-2024
# Python basics, print statements, working with dictonaries and printing key-value pairs, manipulating dictionaries


# a print statement
print('Hello, Fintech!')
print(4%2==0)
portfolio = {'GOOGL': 109, 'META': 157, 'MSFT': 263, 'AAPL': 158, 'AMZN': 128}
del (portfolio['MSFT'])
portfolio['TWTR'] = 16

print(portfolio)


# variables
keys = ['GOOGL', 'META', 'MSFT']
values = [109, 157, 263]

# variables passed into dict to transform to a dictionary
fin_dict = dict(zip(keys, values))

# print the results
print("Here are the contents of the dictionary:", fin_dict)
print("Here is the length of the dictionary:", len(fin_dict))
print("Here are all the keys:", list(fin_dict.keys()))
print("Here is the length of the keys:", len(fin_dict.keys()))

# Loop for deleting keys
while True:
    deleted_key = input("Input the key to delete (or 'done' to finish deleting): ")
    if deleted_key.lower() == 'done':
        break
    if deleted_key in fin_dict:
        del fin_dict[deleted_key]
        print("Key deleted")
    else:
        print("Key not found in the dictionary")
    print("Here are all the keys:", list(fin_dict.keys()))

# Loop for checking keys
while True:
    check_key = input("Input the Key to check if it exists in the dictionary (or 'done' to finish checking): ")
    if check_key.lower() == 'done':
        break
    print(check_key in fin_dict)

# Loop for adding new key-value pairs
while True:
    add_new_key = input("Input a new key name (or 'done' to finish adding): ")
    if add_new_key.lower() == 'done':
        break
    add_new_value = input("Input a new value for the key: ")
    fin_dict[add_new_key] = int(add_new_value)

print("Here are the new contents of the dictionary:", fin_dict)

# Finding minimum value using a loop
min_value = float('inf')
for value in fin_dict.values():
    if value < min_value:
        min_value = value
print("Here is the minimum value in the dictionary:", min_value)

