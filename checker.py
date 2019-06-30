from multiprocessing.pool import ThreadPool
import queue
import requests
import socket
import threading
import urllib3
import requestsSocketsReuse
import time

class ProxyType:
    socks5 = 0
    socks4  = 1
    https = 2
    invalid = 3

def getProxyType(proxy,timeout=10):
    URL = "https://www.cloudflare.com"
    addrs = [
            ("socks5://{}".format(proxy), ProxyType.socks5 ),
            ("socks4://{}".format(proxy), ProxyType.socks4),
            ("https://{}".format(proxy), ProxyType.https)
            ]
    for addr,pType in addrs:
        temp = {
                "http" : addr,
                "https": addr
                }
        try:
            resp = requestsSocketsReuse.head(URL,proxies=temp,timeout=timeout)
            with lock:
                workingProxies.put(addr)
        except requests.exceptions.RequestException:
            pass
        except socket.error:
            pass
        except OverflowError:
            time.sleep(10)
    return addr,ProxyType.invalid



def initProcess(proxiesQueue_,threadCount_,lock_,workingProxies_,timeout_):
    global proxiesQueue,threadCount,lock,tLock,workingProxies,timeout
    proxiesQueue = proxiesQueue_
    threadCount = threadCount_
    lock = lock_
    workingProxies = workingProxies_
    tLock = threading.Lock()
    timeout = timeout_
    return 

def worker(_):
    global proxiesQueue
    while True:
        with lock:
            if proxiesQueue.empty():
                return
            proxy = proxiesQueue.get()
        getProxyType(proxy,timeout=timeout)


def process(i):
    global proxiesQueue
    
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    pool = ThreadPool(threadCount)
    pool.map(worker,range(threadCount))
    pool.close()
    pool.join()
