import multiprocessing
import queue
import time
from datetime import datetime


def collatz(n):
    """Обчислює послідовність Коллатца для числа n."""
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
    return True


def worker(start, end, results, progress_queue):
    """Обробляє діапазон чисел та перевіряє гіпотезу Коллатца."""
    count = 0
    report_frequency = 1000000  # Report progress every million numbers

    for n in range(start, end + 1):
        if collatz(n):
            results.put(True)
            count += 1
            if count % report_frequency == 0:
                progress_queue.put(report_frequency)


if __name__ == '__main__':
    results = multiprocessing.Queue()
    progress_queue = multiprocessing.Queue()
    num_processes = multiprocessing.cpu_count()

    total_numbers = 1000000000
    chunk_size = total_numbers // num_processes

    print(f"Starting calculation using {num_processes} CPU cores")
    print(f"Testing numbers from 1 to {total_numbers:,}")
    start_time = time.time()

    processes = []
    for i in range(num_processes):
        start = i * chunk_size + 1
        end = start + chunk_size - 1 if i < num_processes - 1 else total_numbers

        p = multiprocessing.Process(target=worker, args=(start, end, results, progress_queue))
        processes.append(p)
        p.start()

    # Monitor progress
    processed = 0
    while any(p.is_alive() for p in processes):
        try:
            while True:  # Process all available progress updates
                processed += progress_queue.get_nowait()
                elapsed_time = time.time() - start_time
                progress = (processed / total_numbers) * 100
                speed = processed / elapsed_time if elapsed_time > 0 else 0

                print(f"\rProgress: {progress:.2f}% ({processed:,} numbers) "
                      f"Speed: {speed:,.0f} numbers/second "
                      f"Elapsed: {elapsed_time:.0f} seconds", end="")
        except queue.Empty:
            time.sleep(1)
            continue

    # Wait for all processes to complete
    for p in processes:
        p.join()

    total_time = time.time() - start_time

    print("\n\nCalculation completed!")
    print(f"Total time: {total_time:.2f} seconds")

    result_count = results.qsize()
    if result_count == total_numbers:
        print("Гіпотеза Коллатца підтверджується для всіх чисел від 1 до 1 000 000 000")
    else:
        print(f"Гіпотеза Коллатца не підтверджується для деяких чисел. "
              f"Перевірено {result_count:,} з {total_numbers:,}")