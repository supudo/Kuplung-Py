# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""

__author__ = 'supudo'
__version__ = "1.0.0"

from gl_utils.objects.MeshModel import MeshModel
from gl_utils.objects.Material import Material
from gl_utils.objects.Material import MaterialTextureImage
from maths.types.Vector2 import Vector2
from maths.types.Vector3 import Vector3


class ParserObj1:

    def __init__(self):
        pass


    def parse_file(self, obj_folder, obj_filename):
        self.folder = obj_folder
        file_obj = open(obj_folder + obj_filename, 'r')

        self.vertices = []
        self.normals = []
        self.textureCoordinates = []
        self.indices = []

        self.faces = []
        self.mesh_models = {}
        self.models = []

        current_mesh_model = None
        meshModelCounter = 0
        indicesCounter = 0

        indexModels = []
        indexVertices = []
        indexTexture = []
        indexNormals = []

        for line in file_obj:
            values = line.split()
            if not values or values[0] == '#':
                continue
            elif values[0] == 'mtllib':
                self.parse_material_file(self.folder, values[1])
            elif values[0] == 'o':
                self.model_title = ' '.join(values[1:])
                current_mesh_model = MeshModel()
                current_mesh_model.ModelTitle = self.model_title
                current_mesh_model.ID = meshModelCounter
                current_mesh_model.file = obj_folder + obj_filename
                current_mesh_model.countVertices = 0
                current_mesh_model.countTextureCoordinates = 0
                current_mesh_model.countNormals = 0
                current_mesh_model.countIndices = 0
                self.mesh_models[str(current_mesh_model.ModelTitle)] = current_mesh_model
                meshModelCounter += 1
                self.models.append(current_mesh_model)
            elif values[0] == 'v':
                self.vertices.append(Vector3([float(i) for i in values[1:4]]))
            elif values[0] == 'vn':
                self.normals.append(Vector3([float(i) for i in values[1:4]]))
            elif values[0] == 'vt':
                self.textureCoordinates.append(Vector2([float(i) for i in values[1:3]]))
            elif values[0] in 'usemtl':
                if not values[1] == 'off' and not values[0] == 's':
                    material = self.materials[values[1]]
                    self.mesh_models[str(current_mesh_model.ModelTitle)].MaterialTitle = material.material_title
                    self.mesh_models[str(current_mesh_model.ModelTitle)].ModelMaterial = material
                    self.models[meshModelCounter - 1].MaterialTitle = material.material_title
                    self.models[meshModelCounter - 1].ModelMaterial = material
            elif values[0] == 's':
                pass
            elif values[0] == 'f':
                for v in values[1:]:
                    w = v.split('/')
                    model_key = str(current_mesh_model.ModelTitle)

                    vert = self.vertices[int(w[0]) - 1]
                    self.mesh_models[model_key].vertices.append(vert)
                    self.mesh_models[model_key].countVertices += 1

                    if len(w) >= 2 and len(w[1]) > 0:
                        tc = self.textureCoordinates[int(w[1]) - 1]
                        self.mesh_models[model_key].texture_coordinates.append(tc)
                        self.mesh_models[
                            model_key].countTextureCoordinates += 1

                    nrm = 0
                    if len(w) >= 3 and len(w[2]) > 0:
                        nrm = self.normals[int(w[2]) - 1]
                    self.mesh_models[model_key].normals.append(nrm)
                    self.mesh_models[model_key].countNormals += 1

                    self.mesh_models[model_key].indices.append(indicesCounter)
                    self.mesh_models[model_key].countIndices += 1
                    indicesCounter += 1

        file_obj.close()

        return self.models


    def get_similar_vertex_index(self, packed, vertexToOutIndex):
        result = -1
        for idx in range(len(vertexToOutIndex)):
            m = vertexToOutIndex[idx]
            if m['vertices'] == packed['vertices'] and m['normals'] == packed['normals']:
                result = idx
        return result


    def parse_material_file(self, folder, filename):
        self.materials = {}
        current_material = Material()
        for line in open(folder + filename, "r"):

            if line.startswith('#'):
                continue

            values = line.split()

            if not values:
                continue
            if values[0] == 'newmtl':
                current_material.material_title = values[1]
                self.materials[current_material.material_title] = current_material
            elif values[0] == 'Ka':
                current_material.color_ambient = [float(i) for i in values[1:]]
            elif values[0] == 'Kd':
                current_material.color_diffuse = [float(i) for i in values[1:]]
            elif values[0] == 'Ks':
                current_material.color_specular = [float(i) for i in values[1:]]
            elif values[0] == 'Ke':
                current_material.color_emission = [float(i) for i in values[1:]]
            elif values[0] == 'Ns':
                current_material.specular_exp = float(values[1])
            elif values[0] == 'Tr' or values[0] == 'd':
                current_material.transparency = float(values[1])
            elif values[0] == 'Ni':
                current_material.optical_density = float(values[1])
            elif values[0] == 'illum':
                current_material.illumination_mode = int(values[1])
            elif values[0] == 'map_Ka':
                current_material.texture_ambient = self.load_texture(values[1:])
            elif values[0] == 'map_Kd':
                current_material.texture_diffuse = self.load_texture(values[1:])
            elif values[0] == 'map_Bump':
                current_material.texture_normal = self.load_texture(values[1:])
            elif values[0] == 'disp':
                current_material.texture_displacement = self.load_texture(values[1:])
            elif values[0] == 'map_Ks':
                current_material.texture_specular = self.load_texture(values[1:])
            elif values[0] == 'map_Ns':
                current_material.texture_specular_exp = self.load_texture(values[1:])
            elif values[0] == 'map_d':
                current_material.texture_dissolve = self.load_texture(values[1:])


    def load_texture(self, values):
        mti = MaterialTextureImage()
        mti.image_url = values[0]
        return mti