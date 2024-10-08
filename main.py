import time
import sys
import os

configuration = 0 

def time_decorator(func):
    def wrapper(*args, **kwargs):
        with open("output.txt", 'a') as f:
            start_time = time.time()  
            result = func(*args, **kwargs) 
            end_time = time.time()  
            elapsed_time = end_time - start_time 
            memory_usage = get_memory_usage()  
            print(f"Function '{func.__name__}' took {elapsed_time:.4f} seconds to execute and used {memory_usage} bytes of memory.")
            f.write(f"python,{len(args[0][0])},{elapsed_time:.4f},{memory_usage}, {configuration}\n")
        return result 
    return wrapper


def get_memory_usage():
    """Function to get current memory usage of the process."""
    return os.getpid() 


def parse_file(size, total_matrices):
    with open("data.txt", 'r') as f:
        content = f.read()
        number_list = [int(i) for i in content.split()]
    matrices = []
    for _ in range(total_matrices):
        matrix = []
        for i in range(0, size**2, size):
            l = [number_list[j] for j in range(i, i + size)]
            matrix.append(l)
        matrices.append(matrix)
    return matrices


def multiply(a, b):
    result = [[0] * len(a) for _ in range(len(a))]

    match configuration:
        case 0:  # ijk
            for i in range(len(a)):
                for j in range(len(a)):
                    sum_val = 0
                    for k in range(len(a)):
                        sum_val += a[i][k] * b[k][j]
                    result[i][j] = sum_val
        
        case 1:  # ikj
            for i in range(len(a)):
                for k in range(len(a)):
                    a_ik = a[i][k]  # cache a[i][k]
                    for j in range(len(a)):
                        result[i][j] += a_ik * b[k][j]
        
        case 2:  # jik
            for j in range(len(a)):
                for i in range(len(a)):
                    sum_val = 0
                    for k in range(len(a)):
                        sum_val += a[i][k] * b[k][j]
                    result[i][j] = sum_val
        
        case 3:  # kij
            for k in range(len(a)):
                for i in range(len(a)):
                    a_ik = a[i][k]  # cache a[i][k]
                    for j in range(len(a)):
                        result[i][j] += a_ik * b[k][j]
        
        case 4:  # jki
            for j in range(len(a)):
                for k in range(len(a)):
                    b_kj = b[k][j]  # cache b[k][j]
                    for i in range(len(a)):
                        result[i][j] += a[i][k] * b_kj
        
        case 5:  # kji
            for k in range(len(a)):
                for j in range(len(a)):
                    b_kj = b[k][j]  # cache b[k][j]
                    for i in range(len(a)):
                        result[i][j] += a[i][k] * b_kj
        
        case _:
            for i in range(len(a)):
                for j in range(len(a)):
                    sum_val = 0
                    for k in range(len(a)):
                        sum_val += a[i][k] * b[k][j]
                    result[i][j] = sum_val


    memory_usage = sys.getsizeof(result)
    for row in result:
        memory_usage += sys.getsizeof(row)
        for item in row:
            memory_usage += sys.getsizeof(item)
    
    return result, memory_usage


@time_decorator
def multiplication(matrices):
    for i in range(len(matrices) // 2):
        multiply(matrices[i], matrices[i + len(matrices) // 2])


def main():
    if len(sys.argv) < 7:  
        print("Usage: python main.py -s <size> -i <total_matrices> -c <configuration>")
        sys.exit(1)

    size = None
    total_matrices = None
    global configuration  
    
    for i in range(1, len(sys.argv), 2):
        if sys.argv[i] == '-s':
            size = int(sys.argv[i + 1])
        elif sys.argv[i] == '-i':
            total_matrices = int(sys.argv[i + 1])
        elif sys.argv[i] == '-c':
            configuration = int(sys.argv[i + 1])  
            
    matrices = parse_file(size, total_matrices)
    multiplication(matrices)


if __name__ == "__main__":
    main()
