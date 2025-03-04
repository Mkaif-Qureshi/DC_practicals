from mpi4py import MPI
import time

def decimal_to_binary(n):
    """Convert a decimal number to binary without using bin()"""
    binary_str = ""
    while n > 0:
        binary_str = str(n % 2) + binary_str  # Append remainder to binary string
        n //= 2  # Integer division by 2
    return binary_str

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    numbers = [10**x for x in range(2020, 2025)]  # Large numbers like 10^20, 10^21, ..., 10^24
    chunk_size = len(numbers) // size  # Divide work among processes

    # Scatter work to all processes
    local_numbers = numbers[rank * chunk_size: (rank + 1) * chunk_size] if rank != size - 1 else numbers[rank * chunk_size:]

    start_time = time.time()
    local_results = [decimal_to_binary(num) for num in local_numbers]
    end_time = time.time()

    # Gather results from all processes
    all_results = comm.gather(local_results, root=0)

    if rank == 0:
        all_results = [item for sublist in all_results for item in sublist]  # Flatten list
        print(f"Time taken (MPI, {size} processes): {end_time - start_time:.6f} seconds")
