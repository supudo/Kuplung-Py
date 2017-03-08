# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""

from rendering.methods.RenderingForward import RenderingForward
from rendering.methods.RenderingDeferred import RenderingDeferred
from rendering.methods.RenderingShadowMapping import RenderingShadowMapping
from settings import Settings

__author__ = 'supudo'
__version__ = "1.0.0"


class RenderingManager:
    def __init__(self):
        self.model_faces = []

    def init_systems(self):
        self.renderingForward = RenderingForward()
        self.renderingForward.initShaderProgram()

        self.renderingDeferred = RenderingDeferred()
        self.renderingDeferred.initShaderProgram()

        self.renderingShadowMapping = RenderingShadowMapping()
        self.renderingShadowMapping.initShaderProgram()

    def render(self, mo, selectedModel):
        self.renderingForward.model_faces = self.model_faces
        self.renderingDeferred.model_faces = self.model_faces
        self.renderingShadowMapping.model_faces = self.model_faces
        if Settings.Setting_RendererType == Settings.InAppRendererType.InAppRendererType_Forward:
            self.renderingForward.render(mo, selectedModel)
        elif Settings.Setting_RendererType == Settings.InAppRendererType.InAppRendererType_Deferred:
            self.renderingDeferred.render(mo, selectedModel)
        elif Settings.Setting_RendererType == Settings.InAppRendererType.InAppRendererType_ForwardShadowMapping:
            self.renderingShadowMapping.render(mo, selectedModel)
