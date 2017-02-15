# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""

__author__ = 'supudo'
__version__ = "1.0.0"

import scanf
from gl_utils.MeshModel import MeshModel
from gl_utils.Material import Material
from maths.types.Vector3 import Vector3
from maths.types.Vector2 import Vector2


class ParserObj:

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
                if len(values) == 4:
                    tri_uvIndex = []
                    line = ' '.join(values[1:])
                    face_values = scanf.scanf('%d/%d/%d %d/%d/%d %d/%d/%d', line)
                    if face_values is None:
                        face_values = scanf.scanf('%d//%d %d//%d %d//%d', line)
                        tri_vertexIndex = [
                            face_values[0],
                            face_values[2],
                            face_values[4]
                        ]
                        tri_normalIndex = [
                            face_values[1],
                            face_values[3],
                            face_values[5]
                        ]
                    else:
                        tri_vertexIndex = [
                            face_values[0],
                            face_values[3],
                            face_values[6]
                        ]
                        tri_uvIndex = [
                            face_values[1],
                            face_values[4],
                            face_values[7]
                        ]
                        tri_normalIndex = [
                            face_values[2],
                            face_values[5],
                            face_values[8]
                        ]

                    indexModels.append(meshModelCounter)
                    indexModels.append(meshModelCounter)
                    indexModels.append(meshModelCounter)
                    indexVertices.append(tri_vertexIndex[0])
                    indexVertices.append(tri_vertexIndex[1])
                    indexVertices.append(tri_vertexIndex[2])
                    if len(tri_uvIndex) > 0:
                        indexTexture.append(tri_uvIndex[0])
                        indexTexture.append(tri_uvIndex[1])
                        indexTexture.append(tri_uvIndex[2])
                    indexNormals.append(tri_normalIndex[0])
                    indexNormals.append(tri_normalIndex[1])
                    indexNormals.append(tri_normalIndex[2])
                elif len(values) == 5:
                    tri_uvIndex = []
                    line = ' '.join(values[1:])
                    face_values = scanf.scanf('%d/%d/%d %d/%d/%d %d/%d/%d %d/%d/%d', line)
                    if face_values is None:
                        face_values = scanf.scanf('%d//%d %d//%d %d//%d %d//%d', line)
                        tri_vertexIndex = [
                            face_values[0],
                            face_values[2],
                            face_values[4],
                            face_values[6]
                        ]
                        tri_normalIndex = [
                            face_values[1],
                            face_values[3],
                            face_values[5],
                            face_values[7]
                        ]
                    else:
                        tri_vertexIndex = [
                            face_values[0],
                            face_values[3],
                            face_values[6],
                            face_values[9]
                        ]
                        tri_uvIndex = [
                            face_values[1],
                            face_values[4],
                            face_values[7],
                            face_values[10]
                        ]
                        tri_normalIndex = [
                            face_values[2],
                            face_values[5],
                            face_values[8],
                            face_values[11]
                        ]

                    indexModels.append(meshModelCounter)
                    indexModels.append(meshModelCounter)
                    indexModels.append(meshModelCounter)
                    indexVertices.append(tri_vertexIndex[0])
                    indexVertices.append(tri_vertexIndex[1])
                    indexVertices.append(tri_vertexIndex[2])
                    if len(tri_uvIndex) > 0:
                        indexTexture.append(tri_uvIndex[0])
                        indexTexture.append(tri_uvIndex[1])
                        indexTexture.append(tri_uvIndex[2])
                    indexNormals.append(tri_normalIndex[0])
                    indexNormals.append(tri_normalIndex[1])
                    indexNormals.append(tri_normalIndex[2])

                    indexModels.append(meshModelCounter)
                    indexModels.append(meshModelCounter)
                    indexModels.append(meshModelCounter)
                    indexVertices.append(tri_vertexIndex[2])
                    indexVertices.append(tri_vertexIndex[3])
                    indexVertices.append(tri_vertexIndex[0])
                    if len(tri_uvIndex) > 0:
                        indexTexture.append(tri_uvIndex[2])
                        indexTexture.append(tri_uvIndex[3])
                        indexTexture.append(tri_uvIndex[0])
                    indexNormals.append(tri_normalIndex[2])
                    indexNormals.append(tri_normalIndex[3])
                    indexNormals.append(tri_normalIndex[0])

        for i in range(len(indexVertices)):
            modelIndex = indexModels[i]
            vertexIndex = indexVertices[i]
            normalIndex = indexNormals[i]

            v = self.vertices[vertexIndex - 1]
            n = self.normals[normalIndex - 1]
            self.models[modelIndex - 1].vertices.append(v)
            self.models[modelIndex - 1].countVertices += 1
            self.models[modelIndex - 1].normals.append(n)
            self.models[modelIndex - 1].countNormals += 1

            if len(self.textureCoordinates) > 0:
                uvIndex = indexTexture[i]
                uv = self.textureCoordinates[uvIndex - 1]
                self.models[modelIndex - 1].texture_coordinates.append(uv)
                self.models[modelIndex - 1].countTextureCoordinates += 1
            else:
                self.models[modelIndex - 1].countTextureCoordinates = 0

        vertexToOutIndex = {}
        for i in range(len(self.models)):
            m = self.models[i]
            outVertices = []
            outNormals = []
            outTextureCoordinates = []
            for j in range(len(m.vertices)):
                packed = {
                    'vertices': m.vertices[j],
                    'uvs': m.texture_coordinates[j] if len(m.texture_coordinates) else [0, 0],
                    'normals': m.normals[j]
                }

                index = self.get_similar_vertex_index(packed, vertexToOutIndex)
                if index >= 0:
                    m.indices.append(index)
                else:
                    outVertices.append(m.vertices[j])
                    if len(m.texture_coordinates) > 0:
                        outTextureCoordinates.append(m.m.texture_coordinates[j])
                    outNormals.append(m.normals[j])
                    newIndex = len(outVertices) - 1
                    m.indices.append(newIndex)
                    vertexToOutIndex[newIndex] = packed

            self.models[i].vertices = outVertices
            self.models[i].texture_coordinates = outTextureCoordinates
            self.models[i].normals = outNormals
            self.models[i].indices = m.indices
            self.models[i].countIndices = len(m.indices)

        file_obj.close()


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
            elif values[0] == 'Tr':
                current_material.transparency1 = float(values[1])
            elif values[0] == 'd':
                current_material.transparency2 = float(values[1])
            elif values[0] == 'Ni':
                current_material.optical_density = float(values[1])
            elif values[0] == 'illum':
                current_material.illumination_mode = int(values[1])
            elif values[0] == 'map_Ka':
                current_material.texture_ambient = self.parse_texture(values[1:])
            elif values[0] == 'map_Kd':
                current_material.texture_diffuse = self.parse_texture(values[1:])
            elif values[0] == 'map_Bump':
                current_material.texture_normal = self.parse_texture(values[1:])
            elif values[0] == 'disp':
                current_material.texture_displacement = self.parse_texture(values[1:])
            elif values[0] == 'map_Ks':
                current_material.texture_specular = self.parse_texture(values[1:])
            elif values[0] == 'map_Ns':
                current_material.texture_specular_exp = self.parse_texture(values[1:])
            elif values[0] == 'map_d':
                current_material.texture_dissolve = self.parse_texture(values[1:])


    def parse_texture(self, values):
        return values[0]

