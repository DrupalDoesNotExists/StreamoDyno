""" Add text to image """

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2

class TextExtension:
    """ Add text to image with PIL and OpenCV """
    
    def __init__(self, dyno, **kwargs):
        self.dyno = dyno
        self.font = ImageFont.truetype(kwargs["font"], int(kwargs["size"]))
        self.x, self.y = kwargs.get("x"), kwargs.get("y")
        self.text = kwargs['text']
    
    def produce(self, frame):
        frame = Image.fromarray(frame)
        draw = ImageDraw.Draw(frame)

        if (self.x and self.y) is None:
            width, height = draw.textsize(self.text, font=self.font)
            x = self.x if self.x is not None else (self.dyno.width - width) / 2
            y = self.y if self.y is not None else (self.dyno.height - height) / 2
        else:
            x, y = self.x, self.y
        
        draw.text((x, y), self.text, font=self.font)

        return np.asarray(frame)

extension = TextExtension