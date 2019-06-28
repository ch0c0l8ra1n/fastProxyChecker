from multiprocessing import Pool, Queue, Lock ,cpu_count
from multiprocessing.pool import ThreadPool
import sys
import queue
import requests
import socket
import threading

class ProxyType:
    socks5 = 0
    socks4  = 1
    https = 2
    invalid = 3

def getProxyType(proxy,timeout=10):
    URL = "http://ip-api.com/json"
    addrs = [
            ("socks5://{}".format(proxy), ProxyType.socks5 ),
            ("socks4://{}".format(proxy), ProxyType.socks4),
            ("https://{}".format(proxy), ProxyType.https)
            ]
    for addr,pType in addrs:
        #print("\033[F{}/{}/{}".format(working,counter,totalProxies))
        temp = {
                "http" : addr,
                "https": addr
                }
        try:
            resp = requests.head(URL,proxies=temp,timeout=timeout)
            print(addr)
        except requests.exceptions.RequestException:
            pass
        except socket.error:
            pass
    return addr,ProxyType.invalid



def initProcess(proxiesQueue_,threadCount_,lock_):
    global proxiesQueue,threadCount,lock,tLock
    proxiesQueue = proxiesQueue_
    threadCount = threadCount_
    lock = lock_
    tLock = threading.Lock()
    return 

def worker(_):
    global proxiesQueue
    while True:
        with lock:
            if proxiesQueue.empty():
                return
            proxy = proxiesQueue.get()
        getProxyType(proxy)


def process(i):
    global proxiesQueue
    
    pool = ThreadPool(threadCount)
    pool.map(worker,range(threadCount))
    pool.close()
    pool.join()

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
