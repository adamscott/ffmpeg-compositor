from ffmpeg_compositor.graph.node import Node
from ffmpeg_compositor.graph.socket import Socket
from ffmpeg_compositor.graph.stream import VideoStream
from ffmpeg_compositor.graph.parameters import TextParameter


class Movie(Node):
    NAME = "movie"

    def __init__(self):
        super(Movie, self).__init__()
        self.name = Movie.NAME
        self.output_sockets = []
        self.output_sockets.append(Socket(self, VideoStream))
        self.add_parameters(
            TextParameter(name='filename'),
            TextParameter(name='format_name', alias='f'),
            TextParameter(name='seek_point', alias='sp'),
            TextParameter(name='streams', alias='s'),
            TextParameter(name='stream_index', alias='si', default="-1"),
            TextParameter(name='loop', default="1"),
            TextParameter(name='discontinuity'),
        )
