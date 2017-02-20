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
AppFramebufferWidth = 1300
AppFramebufferHeight = 900
AppWindowWidth = 1300
AppWindowHeight = 900

ApplicationRootPath = ''
ApplicationAssetsPath = 'resources/shapes/'

ApplicationGLFW3 = False

LogDebugWindow = True

class ShapeTypes(Enum):
    ShapeType_None = ['', '', 0]

    ShapeType_Triangle = ['triangle', 'Triangle', 1]
    ShapeType_Cone = ['cone', 'Cone', 1]
    ShapeType_Cube = ['cube', 'Cube', 1]
    ShapeType_Cylinder = ['cylinder', 'Cylinder', 1]
    ShapeType_Grid = ['grid', 'Grid', 1]
    ShapeType_IcoSphere = ['ico_sphere', 'ICO Sphere', 1]
    ShapeType_Plane = ['plane', 'Plane', 1]
    ShapeType_Torus = ['torus', 'Torus', 1]
    ShapeType_Tube = ['tube', 'Tube', 1]
    ShapeType_UVSphere = ['uv_sphere', 'UV Sphere', 1]
    ShapeType_MonkeyHead = ['monkey_head', 'Monkey Head', 1]

    ShapeType_Separator = ['separator', 'separator', -1]

    ShapeType_Epcot = ['epcot', 'Epcot', 2]
    ShapeType_BrickWall = ['brick_wall', 'Brick Wall', 2]
    ShapeType_PlaneObjects = ['plane_objects', 'Plane Objects', 2]
    ShapeType_PlaneObjectsLargePlane = ['plane_objects_large', 'Plane Objects - Large Plane', 2]
    ShapeType_MaterialBall = ['MaterialBall', 'Material Ball', 2]
    ShapeType_MaterialBallBlender = ['MaterialBallBlender', 'Material Ball - Blender', 2]

class LightSourceTypes(Enum):
    LightSourceType_Directional = ['Directional (Sun)', 'light_directional', 0]
    LightSourceType_Point = ['Point (Light bulb)', 'light_point', 1]
    LightSourceType_Spot = ['Spot (Flashlight)', 'light_spot', 2]

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
