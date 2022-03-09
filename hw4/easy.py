from threading import Thread
from multiprocessing import Process
from time import perf_counter


def fib(n):
    output = [0] if n == 1 else [0, 1]
    for i in range(2, n):
        output.append(output[i - 1] + output[i - 2])
    return output


if __name__ == "__main__":
    N = 50000

    start = perf_counter()
    for _ in range(10):
        fib(N)
    time1 = perf_counter() - start

    start = perf_counter()
    jobs = []
    for _ in range(10):
        jobs.append(Thread(target=fib, args=(N,)))
        jobs[-1].start()
    for job in jobs:
        job.join()
    time2 = perf_counter() - start

    start = perf_counter()
    jobs = []
    for _ in range(10):
        jobs.append(Process(target=fib, args=(N,)))
        jobs[-1].start()
    for job in jobs:
        job.join()
    time3 = perf_counter() - start

    
    with open('artifacts/easy.txt', 'w+') as f:
        f.write(f'Sync - {time1}\nThreading - {time2}\nMultiprocessing - {time3}')
