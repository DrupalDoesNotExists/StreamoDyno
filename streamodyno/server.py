from loguru import logger
from importlib import import_module
import gi

gi.require_version("Gst", "1.0")
gi.require_version("GstRtspServer", "1.0")
from gi.repository import Gst, GstRtspServer, GLib


class DynoFactory(GstRtspServer.RTSPMediaFactory):
    """ Dyno server factory """
    
    def __init__(self, options, **properties) -> None:
        super(DynoFactory, self).__init__(**properties)
        
        self.fps = options.framerate
        self.width, self.height = options.size
        self.extensions = self.initialize_extensions(options.pipeline)

        self.frames = 0
        self.duration = 1 / self.fps * Gst.SECOND
        self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                             'caps=video/x-raw,format=BGR,width={},height={},framerate={}/1 ' \
                             '! videoconvert ! video/x-raw,format=I420 ' \
                             '! x264enc speed-preset=ultrafast tune=zerolatency ' \
                             '! rtph264pay config-interval=1 name=pay0 pt=96' \
                             .format(self.width, self.height, self.fps)
    
    def initialize_extensions(self, pipeline: list) -> list:
        """ Initialize all extensions """

        logger.info("Pipeline: {}", pipeline)

        extensions = []
        for extension in pipeline:
            path, *args = extension
            module = import_module(path)

            args = dict([arg.split("=") for arg in args])
            logger.info("Initializing pipeline step {name} with {args}", name=path, args=args)
            extensions.append(module.extension(self, **args))
        
        return extensions
    
    def produce(self, src, length):
        """ Produce data """

        frame = None
        for extension in self.extensions:
            frame = extension.produce(frame)
            if frame is None: return
        
        data = frame.tobytes()
        buf = Gst.Buffer.new_allocate(None, len(data), None)
        buf.fill(0, data)
        buf.duration = self.duration
        timestamp = self.frames * self.duration
        buf.pts = buf.dts = int(timestamp)
        buf.offset = timestamp
        self.frames += 1
        src.emit('push-buffer', buf)
    
    def do_create_element(self, url):
        return Gst.parse_launch(self.launch_string)
    
    def do_configure(self, rtsp):
        self.frames = 0
        appsrc = rtsp.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.produce)

class DynoServer(GstRtspServer.RTSPServer):
    """ Dyno RTSP server """
    
    def __init__(self, options, **properties):
        super(DynoServer, self).__init__(**properties)

        self.factory = DynoFactory(options)
        self.factory.set_shared(True)
        self.set_service(str(options.port))
        self.get_mount_points().add_factory(options.uri, self.factory)
        self.attach(None)
    

def create_server(options) -> None:
    """ Create server """

    logger.info("Initializing GST")
    Gst.init(None)

    logger.info("Instantiating DynoServer and running main loop")
    server = DynoServer(options)
    loop = GLib.MainLoop()
    loop.run()