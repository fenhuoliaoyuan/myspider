from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from threading import Thread
from multiprocessing import Process
class myThread(Thread):
    # def __init__(self, name):
        # super(Son, self).__init__(name)
    # def __init__(self,m):
    #     super(myThread,self).__init__(m)
    #     self.m = m
    #     Thread.__init__(self,m)
    #     self.m = m
    def run(self):
        for i in range(1000):
            print("子线程",i)
class myProcess(Process):
    def run(self):
        for i in range(1000):
            print("子进程",i)
def fn(name):
    for i in range(1000):
        print(name,i)
if __name__ == '__main__':
    # mt1 = myThread()
    # mt1.start()
    # mt2 = myThread()
    # mt2.start()
    #
    # ps1 = myProcess()
    # ps1.start()
    # ps2 = myProcess()
    # ps2.start()
    # for i in range(1000):
    #     print('主进程',i)
    # # 多线程
    # t1 = Thread(target=fn,args=('第1个子线程',))
    # t1.start()
    # t2 = Thread(target=fn, args=('第2个子线程',))
    # t2.start()
    #
    # # 多进程
    # t3 = Process(target=fn, args=('第1个子进程',))
    # t3.start()
    # t4 = Process(target=fn, args=('第2个子进程',))
    # t4.start()

    # 线程池
    with ThreadPoolExecutor(50) as th:
        for i in range(100):
            th.submit(fn('第{}个线程'.format(i)))

    # 进程池
    # with ProcessPoolExecutor(50) as th:
    #     for i in range(100):
    #         th.submit(fn('第{}个进程'.format(i)))
