# StreamoDyno - Stream as many as you want

![Issues](https://img.shields.io/github/issues/DrupalDoesNotExists/StreamoDyno?color=%235865F2&logo=github&style=for-the-badge)

StreamoDyno is an RTSP server software that helps you use ffmpeg to create and draw stream dynamically with Python instead of running heavy and memory consuming programs like OBS, Streamlabs, etc.

## Installation

```bash
git clone https://github.com/DrupalDoesNotExists/StreamoDyno.git
cd StreamoDyno
python -m venv env # Or use your python version like python3.10
. ./env/bin/activate
pip install -r requirements.txt
```

## Usage

After installation you will able to run your streamodyno server
```bash
python -m streamodyno --framerate 30 \ 
--size 1920x1080 \ 
--port 8554 --uri /stream \ 
--pipeline "streamodyno.ext.background" "background=media/background.jpg" \ # Draw background
```

It should be noted that the first element in the pipeline chain must be a "producer", i.e. read/create an image object and pass it on

## Extensions

StreamoDyno uses a pipeline with extensions to it, where each extension draws its own element. If you do not have enough standard set of extensions, you can write your own.

There is example
```python
# nothing.py

import numpy as np
import cv2

class NothingExtension: # Must be first class
    """ Nothing! """

    def __init__(self, dyno, **kwargs):
        """ First, StreamoDyno will call __init__ and pass its instance there and the arguments passed at startup """

        self.dyno = dyno
        self.image = np.zeros((dyno.width, dyno.height, 3), np.uint8)
    
    def produce(self, frame: np.array) -> np.array:
        """ Purge all data and do NOTHING! """

        return self.image

```

And you can add it to pipeline by adding this argument to launch string
```bash
--pipeline "nothing" ""
```

There are some default extensions provided with streamodyno.ext package.
* streamodyno.ext.background - Load external image as background and resize it (background="...") with OpenCV
* streamodyno.ext.new        - Create new blank white image with customizable brightness (brightness=0-255) with NumPy
* streamodyno.ext.text       - Create and customize text over image with PIL and OpenCV

## License

All licensed under MIT.