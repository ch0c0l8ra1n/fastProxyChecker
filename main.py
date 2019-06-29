from multiprocessing import Pool, Queue, Lock ,cpu_count
from multiprocessing.pool import ThreadPool
import sys
import queue
from checker import *



def main():
    fName = sys.argv[1]
    proxiesQueue = Queue()
    processCount =  cpu_count()
    threadCount = 500
    lock=Lock()

    with open(fName) as lines:
        for line in lines:
            line = line.strip("\n")
            proxiesQueue.put(line)
    
    pool = Pool( processCount , initProcess, [proxiesQueue,threadCount,lock] )
    pool.map( process, range(processCount) )
    pool.close()
    pool.join()

if __name__ == "__main__":
    main()
