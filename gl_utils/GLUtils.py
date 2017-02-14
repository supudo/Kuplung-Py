# -*- coding: utf-8 -*-
"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

from OpenGL.GL import *
from settings import Settings


def compileAndAttachShader(shader_program, shaderType, shader_source):
    shader = glCreateShader(shaderType)
    glShaderSource(shader, shader_source)
    glCompileShader(shader)
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        Settings.do_log("[GLUtils] Shader compilation failed! " + str(glGetShaderInfoLog(shader)))
        glDeleteShader(shader)
        return False
    glAttachShader(shader_program, shader)
    glDeleteShader(shader)
    return True


def glGetUniform(shader_program, var_name):
    var = glGetUniformLocation(shader_program, var_name)
    if var == -1:
        Settings.do_log("[GLUtils] Cannot fetch shader uniform - " + str(var_name))
    return var


def glGetAttribute(shader_program, var_name):
    var = glGetAttribLocation(shader_program, var_name)
    if var == -1:
        Settings.do_log("[GLUtils] Cannot fetch shader attribute - " + str(var_name))
    return var
