from .urls import url
from .configs import *
import tornado.web

def createAPP():

    return tornado.web.Application(
        handlers=url,
        **settings
    )


application = createAPP()
