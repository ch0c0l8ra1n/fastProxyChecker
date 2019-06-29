from multiprocessing import Pool, Queue, Lock ,cpu_count
from multiprocessing.pool import ThreadPool
import sys
import queue
from checker import *
import time
import threading


class ProxyChecker:
    def __init__(self,proxiesQueue):
        self.proxiesQueue = proxiesQueue
        self.processesRunning = False
        self.workingProxies=Queue()
        self.outFileName = "output.txt"
        open(self.outFileName,"w+").close()

    def check(self,processCount,threadCount):
        lock=Lock()
        
        self.processesRunning = True
        thread = threading.Thread(target=self.writeToFile,args=[10] )
        thread.start()
        pool = Pool(processCount,initProcess,
                [self.proxiesQueue,threadCount,lock,self.workingProxies])
        pool.map(process, range(processCount))
        pool.close()
        pool.join()
        self.processesRunning = False

    def writeToFile(self,interval):
        while self.processesRunning:
            t1 = time.time()

            time.sleep(interval)
            writeBuffer = ""
            counter = 0
            while True:
                try:
                    with lock:
                        proxy = self.workingProxies.get_nowait()
                    writeBuffer += proxy + "\n"
                    counter += 1
                except queue.Empty:
                    break
            if writeBuffer == "":
                continue
            f = open(self.outFileName,"a+")
            f.write(writeBuffer)
            f.close()
            
            t2 = time.time()
            print("Got {} proxies in {} seconds".format(counter,t2-t1))



            
        

def main():
    fName = sys.argv[1]
    proxiesQueue = Queue()
    processCount =  cpu_count()
    threadCount = 500
    workingProxies = Queue()
    lock=Lock()

    with open(fName) as lines:
        for line in lines:
            line = line.strip("\n")
            proxiesQueue.put(line)
    
    checker = ProxyChecker(proxiesQueue)
    checker.check(processCount,threadCount)



if __name__ == "__main__":
    main()
