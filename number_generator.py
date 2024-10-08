from random import randint

def generate_numbers():
    f = open("data.txt", 'w')

    total_nums = 10000000
    for _ in range(1, total_nums+1):
        f.write(f'{randint(-2147483648, 2147483647)} ')

    f.close()
    
generate_numbers()