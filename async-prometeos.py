from aiohttp import web
import asyncio

from prometheus_client import Summary
from prometheus_async import aio
from prometheus_async.aio import time as metrics
from prometheus_client import Histogram

import random
import time

import json
from datetime import datetime, timezone

import logging
import logging.config
import json

loggingConfigFileName='/app/loggingConfig.json'
loggingConfigFile = open(loggingConfigFileName)
loggingConfig = json.load(loggingConfigFile)


logging.config.dictConfig(loggingConfig)
#logging.basicConfig(level=logging.DEBUG)

# Create a metric to track time spent and requests made.
#FOO_SUMMARY = Summary('request_processing_seconds', 'foo summary')
foo_summary = Summary('foo_summary', 'foo summary')
#FOO_SUMMARY.observe(0.5)
#FOO_SUMMARY = Summary('request_size_bytes', 'foo summary')
#BAR_HISTOGRAM = Histogram('request_latency_seconds', 'bar histogram')

#BAR_HISTOGRAM = Histogram('request_processing_seconds', 'bar histogram')
#BAR_HISTOGRAM.observe(0.1)

routes = web.RouteTableDef()

@routes.get('/foo')
@metrics(foo_summary)
async def foo(request: web.Request) -> web.Response:
    latency = random.random()
    text="foo: {}".format(latency)
    
    print(text)
    await asyncio.sleep(latency)

    return web.Response(text=text)


@routes.get('/bar')
#@metrics(BAR_HISTOGRAM)
async def bar(request: web.Request) -> web.Response:
    latency = random.random()
    text="bar: {}".format(latency)
    
    print(text)
    await asyncio.sleep(latency)
    
    return web.Response(text=text)


app = web.Application()
app.add_routes(routes)
app.router.add_get("/metrics", aio.web.server_stats)

if __name__ == '__main__':
    print("app started")
    web.run_app(app, port=8000)   
    print("app stopped")
