import numpy as np

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
        result_bbox = np.zeros(5)
        result_bbox[0] = int(boundingbox[0]+self.window[0])
        result_bbox[1] = int(boundingbox[1]+self.window[1])
        result_bbox[2] = int(boundingbox[2]+self.window[0])
        result_bbox[3] = int(boundingbox[3]+self.window[1])
        return result_bbox

    def __repr__(self):
        return "Tracker id {0}\nTracker window:{1}".format(self._id,self.window)

    def update_img(self,img):
        """
        update self.img according to self.window
        :param img: new frame
        :return:
        """
        self.img = img[int(self.window[1]):int(self.window[3]+1),int(self.window[0]):int(self.window[2]+1)]

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
    spawn_box = np.array([0,0,200,200,0.9])
    tracker = Tracker(spawn_box=spawn_box,total_width=320,total_height=240,_id=1)
    print(tracker)

    det_bbox = np.array([30,30,50,50,0.99])
    tracker.update_result(det_bbox)
    tracker.update_img(img)
    print(tracker)
    print(tracker.get_result_bbox())
    print(tracker.get_window_img().shape)


