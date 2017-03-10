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

    def init_systems(self, mo):
        self.renderingForward = RenderingForward()
        self.renderingForward.init_renderer(mo)

        self.renderingDeferred = RenderingDeferred()
        self.renderingDeferred.init_renderer(mo)

        self.renderingShadowMapping = RenderingShadowMapping()
        self.renderingShadowMapping.init_renderer(mo)

    def render(self, mo, selectedModel):
        self.renderingForward.model_faces = self.model_faces
        self.renderingDeferred.model_faces = self.model_faces
        self.renderingShadowMapping.model_faces = self.model_faces
        if Settings.Setting_RendererType == Settings.InAppRendererType.InAppRendererType_Forward:
            mo = self.renderingForward.render(mo, selectedModel)
        elif Settings.Setting_RendererType == Settings.InAppRendererType.InAppRendererType_Deferred:
            mo = self.renderingDeferred.render(mo, selectedModel)
        elif Settings.Setting_RendererType == Settings.InAppRendererType.InAppRendererType_ForwardShadowMapping:
            mo = self.renderingShadowMapping.render(mo, selectedModel)
        return mo
