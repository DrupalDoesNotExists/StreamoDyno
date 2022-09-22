""" Background-producing extension """

import cv2
import numpy as np

class BackgroundExtension:
    """ Produce background from file """

    def __init__(self, dyno, **kwargs):
        self.dyno = dyno
        self.background = cv2.resize(cv2.imread(kwargs["background"]),
                                     (dyno.width, dyno.height),
                                     interpolation=cv2.INTER_LINEAR)
    
    def produce(self, frame) -> np.array:
        """ Produce background """

        return self.background

extension = BackgroundExtension