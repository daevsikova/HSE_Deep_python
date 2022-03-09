from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import math
import os
import logging
from time import perf_counter


def func(args):
    f, a, i, step, logger = args
    x = a + i * step
    logger.info(f"parallel version: x = {x}")
    return f(x)


def integrate(f, a, b, *, n_iter=1000, logger=None):
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        logger.info(f"sync version: x = {i}")
        acc += f(a + i * step) * step
    return acc


def multiproc_integrate(f, a, b, *, n_jobs=1, n_iter=1000, logger=None):
    step = (b - a) / n_iter
    args = [(f, a, i, step, logger) for i in range(n_iter)]
    with ProcessPoolExecutor(max_workers=n_jobs) as t:
        parts = list(t.map(func, args))
    return sum(parts) * step


def thread_integrate(f, a, b, *, n_jobs=1, n_iter=1000, logger=None):
    step = (b - a) / n_iter
    args = [(f, a, i, step, logger) for i in range(n_iter)]
    with ThreadPoolExecutor(max_workers=n_jobs) as t:
        parts = list(t.map(func, args))
    return sum(parts) * step


def get_logger(filename):
    logging.basicConfig(filename=filename, level=logging.INFO, format="%(asctime)s;%(levelname)s;%(message)s")
    
    return logging.getLogger(os.path.basename(__file__))


if __name__ == "__main__":
    logger = get_logger("artifacts/medium.txt")
    
    n_iter = 10**3
    n_jobs_range = list(range(1, 2 * os.cpu_count() + 1))

    start = perf_counter()
    res = integrate(math.cos, 0, math.pi / 2, n_iter=n_iter, logger=logger)
    time1 = perf_counter() - start

    threading_time = []
    for n_jobs in n_jobs_range:
        start = perf_counter()
        res = thread_integrate(
            math.cos,
            0,
            math.pi / 2,
            n_jobs=n_jobs,
            n_iter=n_iter,
            logger=logger
        )
        time2 = perf_counter() - start                      
        threading_time.append(time2)

    multiprocess_time = []
    for n_jobs in n_jobs_range:
        start = perf_counter()
        time = multiproc_integrate(
            math.cos,
            0,
            math.pi / 2,
            n_jobs=n_jobs,
            n_iter=n_iter,
            logger=logger
        )
        time3 = perf_counter() - start 
        multiprocess_time.append(time3)

    with open("artifacts/medium_comparing.txt", "w") as f:
        f.write('n_jobs \t sync \t thread \t multiprocess\n')
        for n_jobs, time2, time3 in zip(n_jobs_range, threading_time, multiprocess_time):
            f.write(f'{n_jobs} \t {time1} \t {time2} \t {time3}\n')
