# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""

__author__ = 'supudo'
__version__ = "1.0.0"

import platform
import logging
import time
from enum import Enum


# -------------------------------------------------------------------
# App specific values
# -------------------------------------------------------------------
AppVersion = "1.0 d"

AppMainWindowTitle = "Kuplung"
AppMainWindowWidth = 1300
AppMainWindowHeight = 900

ApplicationRootPath = ''
ApplicationAssetsPath = 'resources/shapes/'

LogDebugWindow = True

class ShapeTypes(Enum):
    ShapeType_None = ''
    ShapeType_BrickWall = 'brick_wall'
    ShapeType_MaterialBall = 'MaterialBall'
    ShapeType_MaterialBallBlender = 'MaterialBallBlender'
    ShapeType_Epcot = 'epcot'
    ShapeType_Cone = 'cone'
    ShapeType_Cube = 'cube'
    ShapeType_Cylinder = 'cylinder'
    ShapeType_Grid = 'grid'
    ShapeType_IcoSphere = 'ico_sphere'
    ShapeType_MonkeyHead = 'monkey_head'
    ShapeType_Plane = 'plane'
    ShapeType_PlaneObjects = 'plane_objects'
    ShapeType_PlaneObjectsLargePlane = 'plane_objects_large'
    ShapeType_Triangle = 'triangle'
    ShapeType_Torus = 'torus'
    ShapeType_Tube = 'tube'
    ShapeType_UVSphere = 'uv_sphere'

class LightSourceType(Enum):
    LightSourceType_Directional = 0
    LightSourceType_Point = 1
    LightSourceType_Spot = 2

class ModelFileParserTypes(Enum):
    ModelFileParser_Own1 = 0
    ModelFileParser_Own2 = 1
    ModelFileParser_Assimp = 2

ModelFileParser = ModelFileParserTypes.ModelFileParser_Assimp

# -------------------------------------------------------------------
# Scene Info
# -------------------------------------------------------------------
SceneCountObjects= 0
SceneCountVertices = 0
SceneCountIndices = 0
SceneCountTriangles = 0
SceneCountFaces = 0

# -------------------------------------------------------------------
# OpenGL specific
# -------------------------------------------------------------------
guiClearColor = [70.0 / 255.0, 70.0 / 255.0, 70.0 / 255.0, 255.0 / 255.0]
Setting_Wireframe = False

class ViewModelSkin(Enum):
    ViewModelSkin_Solid = 0
    ViewModelSkin_Material = 1
    ViewModelSkin_Texture = 2
    ViewModelSkin_Wireframe = 3
    ViewModelSkin_Rendered = 4

Setting_ModelViewSkin = ViewModelSkin.ViewModelSkin_Rendered

Setting_Rendering_Depth = False

# Setting_FOV = 45.0
# Setting_RatioWidth = 4.0
# Setting_RatioHeight = 3.0
# Setting_PlaneClose = 0.1
# Setting_PlaneFar = 100.0

Setting_ZScroll = 999
Setting_GridSize = 30

# -------------------------------------------------------------------
# Logging
# -------------------------------------------------------------------
logger = logging.getLogger('KuplungApp')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def log_info(*args):
    logger.log(logging.INFO, "{0} {1} [Kuplung] {2}".format(time.strftime("%Y/%m/%d"), time.strftime("%H:%M:%S"), ' '.join(args)))

def log_error(*args):
    logger.log(logging.ERROR, "{0} {1} [Kuplung] Error! {2}".format(time.strftime("%Y/%m/%d"), time.strftime("%H:%M:%S"), ' '.join(args)))

FuncDoLog = None
def do_log(*args):
    if not FuncDoLog is None:
        for msg in args:
            FuncDoLog(msg)
    for msg in args:
        log_info(msg)

# -------------------------------------------------------------------
# OS
# -------------------------------------------------------------------
def is_osx():
    return (platform.system().lower().find("darwin") > -1)
