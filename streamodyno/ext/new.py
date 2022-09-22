""" New image producer """

import numpy as np

class NewImageExtension:
    """ Produce new image """
    
    def __init__(self, dyno, **kwargs) -> None:
        self.dyno = dyno
        self.brightness = int(kwargs['brightness'])
        self.image = np.full((dyno.width, dyno.height, 3), self.brightness)
    
    def produce(self, frame) -> np.array:
        """ Produce new image """

        return self.image
    