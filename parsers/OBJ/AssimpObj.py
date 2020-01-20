# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import os
import pyassimp
import pyassimp.postprocess
from gl_utils.objects.MeshModel import MeshModel
from gl_utils.objects.Material import Material
from gl_utils.objects.Material import MaterialTextureImage
from maths.types.Vector2 import Vector2
from maths.types.Vector3 import Vector3
from settings import Settings


class AssimpObj:

    def __init__(self):
        pass

    def parse_file(self, obj_folder, obj_filename):
        self.folder = obj_folder
        self.file_obj = obj_folder + obj_filename
        self.mesh_models = []
        self.index_model = 0
        scene = pyassimp.load(
            self.file_obj,
            None,
            pyassimp.postprocess.aiProcess_Triangulate
        )
        self.process_node(scene)
        pyassimp.release(scene)
        return self.mesh_models

    def process_node(self, scene):
        for index, mesh in enumerate(scene.meshes):
            self.mesh_models.append(self.process_mesh(mesh, scene, mesh.name))
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

            # TODO: fix assimp parser crash
            entityMaterial.specular_exp = float(material.properties['shininess'] / 4.0)
            entityMaterial.optical_density = float(material.properties['refracti'])
            entityMaterial.transparency = float(material.properties['opacity'])
            entityMaterial.illumination_mode = int(material.properties['shadingm'])

            entityMaterial.color_ambient = Vector3(material.properties['ambient'])
            entityMaterial.color_diffuse = Vector3(material.properties['diffuse'])
            entityMaterial.color_specular = Vector3(material.properties['specular'])
            entityMaterial.color_emission = Vector3(material.properties['emissive'])

            textures = self.parse_textures(entityModel.MaterialTitle)

            entityMaterial.texture_ambient = textures['ambient']
            entityMaterial.texture_diffuse = textures['diffuse']
            entityMaterial.texture_normal = textures['normal']
            entityMaterial.texture_displacement = textures['displacement']
            entityMaterial.texture_specular = textures['specular']
            entityMaterial.texture_specular_exp = textures['specular_exp']
            entityMaterial.texture_dissolve = textures['dissolve']

            entityModel.ModelMaterial = entityMaterial

        return entityModel

    def parse_textures(self, materialTitle):
        # PyAssimp does not yet support textures, so we roll our own ...
        mtl_file = self.get_mtl_file()
        textures = {
            'ambient': MaterialTextureImage(),
            'diffuse': MaterialTextureImage(),
            'normal': MaterialTextureImage(),
            'displacement': MaterialTextureImage(),
            'specular': MaterialTextureImage(),
            'specular_exp': MaterialTextureImage(),
            'dissolve': MaterialTextureImage()
        }
        if mtl_file != '':
            for line in open(self.folder + mtl_file, "r"):
                if line.startswith('#'):
                    continue
                values = line.split()
                if not values:
                    continue
                elif values[0] == 'map_Ka':
                    textures['ambient'] = self.load_texture(''.join(values[1:]))
                elif values[0] == 'map_Kd':
                    textures['diffuse'] = self.load_texture(''.join(values[1:]))
                elif values[0] == 'map_Bump':
                    textures['normal'] = self.load_texture(''.join(values[1:]))
                elif values[0] == 'disp':
                    textures['displacement'] = self.load_texture(''.join(values[1:]))
                elif values[0] == 'map_Ks':
                    textures['specular'] = self.load_texture(''.join(values[1:]))
                elif values[0] == 'map_Ns':
                    textures['specular_exp'] = self.load_texture(''.join(values[1:]))
                elif values[0] == 'map_d':
                    textures['dissolve'] = self.load_texture(''.join(values[1:]))
        return textures

    def load_texture(self, line):
        mti = MaterialTextureImage()
        mti.Image = ''
        mti.UseTexture = True
        mti.Height = 0
        mti.Width = 0
        if line.count('-') > 0:
            # TODO: commands
            pass
        else:
            mti.Image = line
        if not os.path.exists(mti.Image):
            mti.Image = self.folder + '/' + mti.Image
        k = mti.Image.rfind('/')
        mti.Filename = mti.Image[k + 1:]
        return mti

    def get_mtl_file(self):
        # quick and dirty parser, presumable mtl definition is not too far
        # down the file, so it should be quick
        file_obj = open(self.file_obj, 'r')
        for line in file_obj:
            values = line.split()
            if not values or values[0] == '#':
                continue
            elif values[0] == 'mtllib':
                return values[1]

