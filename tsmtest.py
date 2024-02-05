import cvtest
from multiprocessing import Process, Manager

if __name__ == '__main__':
    manager = Manager()
    center = manager.list([0, 0])
    trainPath = manager.list([])
    path = manager.list([])
    track = manager.list([0])
    startBot = manager.list([0])

    p1 = Process(target=cvtest.capture, args=(center, trainPath, path, track, startBot))
    p2 = Process(target=cvtest.movement, args=(center, trainPath, path, track, startBot))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
