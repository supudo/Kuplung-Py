"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""

__author__ = 'supudo'
__version__ = "1.0.0"

import platform
import logging


guiClearColor = [70 / 255.0, 70 / 255.0, 70 / 255.0, 255 / 255.0]

AppVersion = "1.0 d"

AppMainWindowWidth = 1200
AppMainWindowHeight = 900

ApplicationRootPath = ''

LogDebugWindow = True

SceneCountObjects= 0
SceneCountVertices = 0
SceneCountIndices = 0
SceneCountTriangles = 0
SceneCountFaces = 0

# -------------------------------------------------------------------
# Logging
# -------------------------------------------------------------------
logger = logging.getLogger('KuplungApp')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def log_info(*args):
    logger.log(logging.INFO, "[Kuplung] {0}".format(' '.join(args)))

def log_error(*args):
    logger.log(logging.ERROR, "[Kuplung] Error! {0}".format(' '.join(args)))


# -------------------------------------------------------------------
# OS
# -------------------------------------------------------------------
def is_osx():
    return (platform.system().lower().find("darwin") > -1)