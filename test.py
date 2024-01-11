import cvtest
from multiprocessing import Process, Manager

if __name__ == '__main__':
    manager = Manager()
    center = manager.list([0, 0])
    startBot = manager.list([0])
    direction = manager.list([0])
    bounds = manager.list([0, 0, 0])

    p1 = Process(target=cvtest.capture, args=(center, startBot, direction, bounds))
    p2 = Process(target=cvtest.movement, args=(center, startBot, direction, bounds))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
