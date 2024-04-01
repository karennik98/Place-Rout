import random

numbers_count = {}
def generate_numbers_until_third_occurrence():
    global numbers_count
    while True:
        num = random.randint(1, 5)
        numbers_count[num] = numbers_count.get(num, 0) + 1
        if numbers_count[num] == 3:
            print(f"Number {num} occurred for the third time. Stopping the generator.")
            continue
        else:
            return num

while True:
    num = generate_numbers_until_third_occurrence()
    print(num)
