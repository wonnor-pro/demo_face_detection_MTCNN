import multiprocessing as mp
from timeit import default_timer as timer
import numpy as np
import time

def get_frame():
    """
   skeleton function which gets one frame from video
    :return:
    """
    frame = np.random.rand(320,240,3)
    return frame

def show_frame(img):
    """
    skeleton function which shows one frame
    :return:
    """

def drawbox(img,bbox):
    """
    skeleton function which draws bbox on an img
    :param img:
    :param bbox:
    :return:
    """
    return img

def detect_face(img):
    """
    skeleton function which stands for detection
    :param img:
    :return:
    """
    bbox = []
    return bbox

def worker(qin,qout):
    # initialize neural network
    pass

    while True:
        img, time_stamp = qin.get()
        if img is None:
            continue
        bbox = detect_face(img)
        qout.put((bbox,time_stamp))
        if img == 'Done': # signal to exit the program
            break

if __name__ == '__main__':
    # camera setup
    pass
    bbox = []
    raw_queue = mp.Queue()
    det_queue = mp.Queue()

    worker1 = mp.Process(target=worker,args=(raw_queue,det_queue))
    worker2 = mp.Process(target=worker,args=(raw_queue,det_queue))
    worker3 = mp.Process(target=worker,args=(raw_queue,det_queue))

    worker1.start()
    worker2.start()
    worker3.start()

    terminate = False
    latest_det_time = timer()

    while True:
        image = get_frame()
        time_stamp = timer()
        raw_queue.put((image,time_stamp))
        if not det_queue.empty():
            _bbox, _time = det_queue.get()
            if latest_det_time < _time:
                bbox = _bbox

        image = drawbox(image,bbox)
        show_frame(image)

        if terminate is True:
            for i in range(3):
                raw_queue.put(('Done',None))
            worker1.join()
            worker2.join()
            worker3.join()
            break




