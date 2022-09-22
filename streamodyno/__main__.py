from loguru import logger
import argparse
from .server import create_server

def main() -> None:
    """ Main function """

    parser = argparse.ArgumentParser()
    parser.add_argument("--framerate", type=int, default=30, help="Framerate")
    parser.add_argument("--size", type=lambda arg: tuple(int(x) for x in arg.split("x")),
                        required=True, help="Size of image. Format: WIDTHxHEIGHT")
    parser.add_argument("--port", type=int, default=8554, help="Port")
    parser.add_argument("--uri", default="/stream", help="Stream URI")
    parser.add_argument("--pipeline", type=str, nargs="+", action="append",
                        required=True, help="Add extension to pipeline")
    options = parser.parse_args()

    logger.info("StreamoDyno launch options: {options}", options=options)
    create_server(options)

main()
