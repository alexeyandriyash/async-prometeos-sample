from aiohttp import web
import asyncio

from prometheus_client import Summary
from prometheus_async import aio
from prometheus_async.aio import time as metrics
from prometheus_client import Histogram
from prometheus_client import Counter



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
logging.basicConfig(level=logging.DEBUG)

# Create a metric to track time spent and requests made.
#FOO_SUMMARY = Summary('request_processing_seconds', 'foo summary')
foo_summary = Summary('foo_summary', 'foo summary')
#FOO_SUMMARY.observe(0.5)
#FOO_SUMMARY = Summary('request_size_bytes', 'foo summary')
#BAR_HISTOGRAM = Histogram('request_latency_seconds', 'bar histogram')

bar_histogram = Histogram(name = 'bar_histogram', documentation = 'bar histogram')
#BAR_HISTOGRAM.observe(0.1)
bazz_counter = Counter('bazz_counter', 'Description of counter')
bazz_counter.inc()
routes = web.RouteTableDef()



@routes.get('/foo')
@metrics(foo_summary)
async def foo(request: web.Request) -> web.Response:
    return web.Response(text=await base_handler('foo'),
                        content_type='text/html')

@routes.get('/bar')
@metrics(bar_histogram)
async def bar(request: web.Request) -> web.Response:
    return web.Response(text=await base_handler('bar'),
                        content_type='text/html')

@routes.get('/bazz')
async def bar(request: web.Request) -> web.Response:

    return web.Response(text=await base_handler('bazz'),
                        content_type='text/html')

@routes.get('/')
async def root_handler(request: web.Request) -> web.Response:
    return web.Response(text=base_content,
                        content_type='text/html')


app = web.Application()
app.add_routes(routes)
app.router.add_get("/metrics", aio.web.server_stats)

def get_routes_list():
    routes = list()
    for resource in app.router.resources():
        routes.append(resource.get_info().get("path"))

    routes.remove('/metrics')

    routes.sort()
    return routes

def get_base_html_content():
    link_pattern = '<a href="{path}">{text}</a><br>'
    routes = get_routes_list()

    content = [ link_pattern.format(path = route, text = route) for route in routes]

    content.append('<br>')
    content.append('<br>')
    content.append(link_pattern.format(path = '/metrics', text = '/metrics'))

    
    content_str = ""
    return content_str.join(content)


def get_extended_html_content():
    extention = "<br><br>last route: <b>{route_name}</b>, last time: <b>{latency}</b>"
    extended_content = get_base_html_content() + extention
    return extended_content


base_content = get_base_html_content()
extended_content = get_extended_html_content()


async def base_handler(route_name):
    
    latency = random.random()
    await asyncio.sleep(latency)
    text="bar: {}".format(latency)
    
    return extended_content.format(route_name = route_name, latency = latency)



if __name__ == '__main__':
    print("app started")
    web.run_app(app, port=8000)   
    print("app stopped")
