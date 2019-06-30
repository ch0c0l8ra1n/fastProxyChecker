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

    def check(self,processCount,threadCount,timeout):
        lock=Lock()
        
        self.processesRunning = True
        thread = threading.Thread(target=self.writeToFile,args=[lock,10] )
        thread.start()
        pool = Pool(processCount,initProcess,
                [self.proxiesQueue,threadCount,
                    lock,self.workingProxies,timeout])
        pool.map(process, range(processCount))
        pool.close()
        pool.join()
        self.processesRunning = False

    def writeToFile(self,lock,interval):
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
            f = open(self.outFileName,"a+")
            f.write(writeBuffer)
            f.close()
            
            t2 = time.time()
            print("Got {} proxies in {} seconds".format(counter,t2-t1))



            
        

def main():
    try:
        fName = sys.argv[1]
        threadCount = int(sys.argv[2])
        timeout = int(sys.argv[3])
    except:
        print("Usage: python3 main.py filename threadCount timeout")
        return
    proxiesQueue = Queue()
    processCount =  cpu_count()
    workingProxies = Queue()
    lock=Lock()

    with open(fName) as lines:
        for line in lines:
            line = line.strip("\n")
            proxiesQueue.put(line)
    
    checker = ProxyChecker(proxiesQueue)
    checker.check(processCount,threadCount,timeout)



if __name__ == "__main__":
    main()
