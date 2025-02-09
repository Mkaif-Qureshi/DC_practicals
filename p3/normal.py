import time

def decimal_to_binary(n):
    """Convert a decimal number to binary without using bin()"""
    binary_str = ""
    while n > 0:
        binary_str = str(n % 2) + binary_str  # Append remainder to binary string
        n //= 2  # Integer division by 2
    return binary_str

if __name__ == "__main__":
    numbers = [10**x for x in range(1020, 1025)]  # Large numbers like 10^20, 10^21, ..., 10^24
    start_time = time.time()

    results = [decimal_to_binary(num) for num in numbers]

    end_time = time.time()
    print(f"Time taken (CPU, no MPI): {end_time - start_time:.6f} seconds")
