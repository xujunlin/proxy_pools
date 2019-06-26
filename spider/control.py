#!/usr/bin/env python
# encoding: utf-8
from .scheduling import scheduling, check
from .api import api_run
from multiprocessing import Process


def run_proxy_pool():
    api_process = Process(target=api_run)
    schedul_process = Process(target=scheduling)
    check_process = Process(target=check)

    api_process.start()
    schedul_process.start()
    check_process.start()

    api_process.join()
    schedul_process.join()
    check_process.join()


if __name__ == '__main__':
    run_proxy_pool()