import dataclasses as dc
import os
from dotenv import load_dotenv


load_dotenv()


@dc.dataclass
class ServerConfig:
    host: str
    port: int
    debug: bool


def create_server_config() -> ServerConfig:
    return ServerConfig(
        host=os.environ["HOST"],
        port=int(os.environ["PORT"]),
        debug=bool(os.environ["DEBUG"]))
