from kac_queue import Queue2, DiskQueue
import multiprocessing
import threading
import time
import sys
import os

"""
Package Description

Working Example - kac_spider.py (thread and proces)
"""

##### Thread Class
class ThreadJob:
    """Przekaz metode \n
    ThreadJob(metoda=Metoda, queue=Queue, qt=3, kwargs) \n
    metoda -  przekaz klase z metoda do wykonania \n
    queue - wprowadz odpowiednia klase obslugujaca zadania \n
    qt - jaka ilosc watkow uruchomic do wykonania zadania (pomnoz x2 bo pozniej nie wiem dlaczego redukuje sie liczba watkow o polowe) \n
    kwargs -> nazwa=wartosc (i tak ile chcemy)
    """

    def __init__(self, metoda=None, queue=None, max_threads=1, **kwargs):
        threads = []
        x = 1

        while threads or x > 0:
            x = 0
            for thread in threads:
                if not thread.is_alive():
                    threads.remove(thread)

            while len(threads) < max_threads and queue.peek():
                thread = threading.Thread(target=metoda, args=(), kwargs=kwargs, daemon=True)
                thread.start()
                threads.append(thread)
                time.sleep(1)
            if not threads:
                break


##### ProcessClass
class ProcessJobs:
    """
    Przekaz metode \n
    ProcessJobs(q_processes=1, metoda=Metoda, queue=Queue, qt=3, kwargs) \n
    q_processes - jaka ilosc procesow uruchomic do wykonania zadania \n
    metoda -  przekaz klase z metoda do wykonania \n
    queue - wprowadz odpowiednia klase obslugujaca zadania \n
    kwargs -> nazwa=wartosc (i tak ile chcemy)
    """
    # os.getpid() - id procesu

    def __init__(self,q_processes=1, **kwargs):
        if q_processes > multiprocessing.cpu_count(): num_cpus = multiprocessing.cpu_count()
        else: num_cpus = q_processes

        processes = []
        for i in range(num_cpus):
            p = multiprocessing.Process(target=ThreadJob, kwargs=kwargs) # bez args=args,
            p.start()
            processes.append(p)
            time.sleep(.01) # spowalnia ale nie wywala VS Code
        for p in processes: # wait for processes to complete
            p.join()

##### main 
# if __name__ == '__main__':

#     sys.exit()
    