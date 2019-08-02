import numpy as np
import cv2

class Tracker:
    """
    INITIALIZATION:

    USAGE:
        1. call update_result
            self.result_box is updated
            self.window is updated
        2. call update_image
            self.img is updated
        3. get_window_img()
        4. get_result_bbox()
    """
    def __init__(self,spawn_box,total_width,total_height,_id,w_ratio=0.4,h_ratio=0.4):
        self._id = _id
        self.result_bbox = spawn_box # result_box [x1,y1,x2,y2,score]
        self.total_width = total_width
        self.total_height = total_height
        self.w_ratio = w_ratio
        self.h_ratio = h_ratio

        self.window = np.zeros(4)
        self._update_window()

        self.img = None

    def _update_window(self):
        """
        update the new window to crop image
        """
        w = self.result_bbox[2]-self.result_bbox[0]
        h = self.result_bbox[3]-self.result_bbox[1]
        dw = w * self.w_ratio/2
        dh = h * self.h_ratio/2
        self.window[0] = max(0,int(self.result_bbox[0]-dw))
        self.window[1] = max(0,int(self.result_bbox[1]-dh))
        self.window[2] = min(self.total_width,int(self.result_bbox[2]+dw))
        self.window[3] = min(self.total_height,int(self.result_bbox[3]+dh))

    def _offset_bbox(self,boundingbox):
        """
        offset the detection result according to the window. self.result_bbox is updated
        :param boundingbox:
        :return:
        """

        w = self.window[2] - self.window[0]
        h = self.window[3] - self.window[1]
        resize_ratio = min(w/20, h/20)

        print('resize_ratio', resize_ratio)

        result_bbox = np.zeros(5)
        result_bbox[0] = int(boundingbox[0]*resize_ratio+self.window[0])
        result_bbox[1] = int(boundingbox[1]*resize_ratio+self.window[1])
        result_bbox[2] = int(boundingbox[2]*resize_ratio+self.window[0])
        result_bbox[3] = int(boundingbox[3]*resize_ratio+self.window[1])
        return result_bbox

    def __repr__(self):
        return "Tracker id {0}\nTracker window:{1}".format(self._id,self.window)

    def update_img(self,img):
        """
        update self.img according to self.window
        :param img: new frame
        :return:
        """
        if self.img is None:
            self.img = img[int(self.window[1]):int(self.window[3]), int(self.window[0]):int(self.window[2])]

        else:
            self.img = img[int(self.window[1]):int(self.window[3]), int(self.window[0]):int(self.window[2])]
            img_ratio = self.img.shape[0] / self.img.shape[1]
            if img_ratio <= 1:
                self.img = cv2.resize(self.img, (int(20 / img_ratio), 20))
            if img_ratio > 1:
                self.img = cv2.resize(self.img, (20, int(20 * img_ratio)))


    def update_result(self,boundingbox):
        """
        self.result_bbox is updated such that it can be shown correctly on the original image
        :param boundingbox:  The detection result of the cropped image.[x1,y1,x2,y2,score]
        :return:
        """

        self.result_bbox = self._offset_bbox(boundingbox)
        self._update_window()
        return self.result_bbox

    def get_id(self):
        return self._id

    def get_window_img(self):
        return self.img

    def get_result_bbox(self):
        return self.result_bbox

if __name__ == '__main__':
    img = np.random.rand(320,240,3)
    spawn_box = np.array([32,20,100,140,0.9])
    tracker = Tracker(spawn_box=spawn_box,total_width=320,total_height=240,_id=1)
    print(tracker)
    window1 = tracker.window

    offset = [10, 30, 30, 20]
    det_bbox = np.array([int(offset[0]/4.75),int(offset[1]/4.75),int(offset[2]/4.75),int(offset[3]/4.75),0.99])
    tracker.update_result(det_bbox)
    tracker.update_img(img)
    print(tracker)
    print('result box',tracker.get_result_bbox())
    print('ground true box', window1 + offset)
    print(tracker.get_window_img().shape)


