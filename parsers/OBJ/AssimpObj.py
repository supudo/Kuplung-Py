# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import pyassimp
import pyassimp.postprocess
from gl_utils.MeshModel import MeshModel
from gl_utils.Material import Material
from gl_utils.Material import MaterialTextureImage
from maths.types.Vector3 import Vector3
from maths.types.Vector2 import Vector2


class AssimpObj:

    def __init__(self):
        pass


    def parse_file(self, obj_folder, obj_filename):
        self.folder = obj_folder
        self.file_obj = obj_folder + obj_filename
        self.models = []
        self.index_model = 0
        scene = pyassimp.load(
            self.file_obj,
            pyassimp.postprocess.aiProcess_Triangulate
        )
        self.process_node(scene)
        pyassimp.release(scene)
        return self.models


    def process_node(self, scene):
        for index, mesh in enumerate(scene.meshes):
            self.models.append(self.process_mesh(mesh, scene, mesh.name))
            self.index_model += 1


    def process_mesh(self, mesh, scene, model_title):
        entityModel = MeshModel()
        entityModel.ModelTitle = model_title
        entityModel.ID = self.index_model
        entityModel.file = self.file_obj
        entityModel.countVertices = 0
        entityModel.countTextureCoordinates = 0
        entityModel.countNormals = 0
        entityModel.countIndices = 0

        for i in range(len(mesh.vertices)):
            # vertices
            v = Vector3(mesh.vertices[i][0], mesh.vertices[i][1], mesh.vertices[i][2])
            entityModel.vertices.append(v)
            entityModel.countVertices += 3

            # normals
            n = Vector3(mesh.normals[i][0], mesh.normals[i][1], mesh.normals[i][2])
            entityModel.normals.append(n)
            entityModel.countNormals += 3

            # texture coordinates
            if len(mesh.texturecoords) > 0 and len(mesh.texturecoords[0]) > 0:
                tc = Vector2(mesh.texturecoords[0][i][0], mesh.texturecoords[0][i][1])
                entityModel.texture_coordinates.append(tc)
                entityModel.countTextureCoordinates += 2

        # indices
        for face in mesh.faces:
            for idx in face:
                entityModel.indices.append(idx)
                entityModel.countIndices += 1

        # material
        if mesh.materialindex > 0:
            material = scene.materials[mesh.materialindex]
            entityModel.MaterialTitle = material.properties['name']

            entityMaterial = Material()
            entityMaterial.material_title = material.properties['name']

            entityMaterial.specular_exp = float(material.properties['shininess'] / 4.0)
            entityMaterial.optical_density = float(material.properties['refracti'])
            entityMaterial.transparency1 = float(material.properties['opacity'])
            entityMaterial.illumination_mode = float(material.properties['shadingm'])

            entityMaterial.color_ambient = Vector3(material.properties['ambient'])
            entityMaterial.color_diffuse = Vector3(material.properties['diffuse'])
            entityMaterial.color_specular = Vector3(material.properties['specular'])
            entityMaterial.color_emission = Vector3(material.properties['emissive'])

            entityMaterial.texture_ambient = self.load_texture()
            entityMaterial.texture_diffuse = self.load_texture()
            entityMaterial.texture_normal = self.load_texture()
            entityMaterial.texture_displacement = self.load_texture()
            entityMaterial.texture_specular = self.load_texture()
            entityMaterial.texture_specular_exp = self.load_texture()
            entityMaterial.texture_dissolve = self.load_texture()

            entityModel.ModelMaterial = entityMaterial

        return entityModel


    def load_texture(self):
        # PyAssimp does not yet support textures ...
        mti = MaterialTextureImage()
        mti.image_url = ''
        return mti

