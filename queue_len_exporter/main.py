import logging
import uvicorn
from fastapi import FastAPI
import prometheus_client
from prometheus_client import REGISTRY
from . import route
from .config import *

# a banner of 'nbl-exporter'
from art import text2art

Art = text2art("queue-len-exporter")
print(Art)
del Art, text2art

# remove default metric
REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)

# config log
if log_file is None:
    logging.basicConfig(
        level=log_level, format="%(asctime)s %(levelname)-8s %(name)s %(message)s"
    )
else:
    logging.basicConfig(
        filename=log_file,
        level=log_level,
        format="%(asctime)s %(levelname)-8s %(name)s %(message)s",
    )

app = FastAPI()

route.register_routes(app)

if __name__ == "__main__":
    uvicorn.run(app)
