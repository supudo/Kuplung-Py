"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""

__author__ = 'supudo'
__version__ = "1.0.0"

from gl_utils.MeshModel import MeshModel
from gl_utils.Material import Material


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
        current_mesh_model = None
        meshModelCounter = 0
        indicesCounter = 0

        for line in file_obj:
            values = line.split()
            if not values:
                continue
            elif values[0] == 'mtllib':
                self.parse_material_file(self.folder, values[1])
            elif values[0] == 'o':
                self.model_title = values[1:]
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
            elif values[0] == 'v':
                for v in map(float, values[1:4]):
                    self.vertices.append(v)
            elif values[0] == 'vn':
                for v in map(float, values[1:4]):
                    self.normals.append(v)
            elif values[0] == 'vt':
                for v in map(float, values[1:3]):
                    self.textureCoordinates.append(v)
            elif values[0] in 'usemtl':
                if not values[1] == 'off':
                    material = self.materials[values[1]]
                    self.mesh_models[str(current_mesh_model.ModelTitle)].MaterialTitle = material.material_title
                    self.mesh_models[str(current_mesh_model.ModelTitle)].ModelMaterial = material
            elif values[0] == 's':
                pass
            elif values[0] == 'f':
                 for v in values[1:]:
                    w = v.split('/')
                    model_key = str(current_mesh_model.ModelTitle)

                    vert = float(self.vertices[int(w[0])])
                    self.mesh_models[model_key].vertices.append(vert)
                    self.mesh_models[model_key].countVertices += 1

                    if len(w) >= 2 and len(w[1]) > 0:
                        tc = float(self.textureCoordinates[int(w[1])])
                        self.mesh_models[model_key].texture_coordinates.append(tc)
                        self.mesh_models[model_key].countTextureCoordinates += 1

                    nrm = 0
                    if len(w) >= 3 and len(w[2]) > 0:
                        nrm = float(self.normals[int(w[2])])
                    self.mesh_models[model_key].normals.append(nrm)
                    if nrm > 0:
                        self.mesh_models[model_key].countNormals += 1

                    self.mesh_models[model_key].indices.append(indicesCounter)
                    self.mesh_models[model_key].countIndices += 1
                    indicesCounter += 1

                # verts = []
                # tcoords = []
                # norms = []
                # for v in values[1:]:
                #     w = v.split('/')
                #     verts.append(int(w[0]))
                #     if len(w) >= 2 and len(w[1]) > 0:
                #         tcoords.append(int(w[1]))
                #     else:
                #         tcoords.append(0)
                #     if len(w) >= 3 and len(w[2]) > 0:
                #         norms.append(int(w[2]))
                #     else:
                #         norms.append(0)

                        # face = []
                # texcoords = []
                # norms = []
                # for v in values[1:]:
                #     w = v.split('/')
                #     face.append(int(w[0]))
                #     if len(w) >= 2 and len(w[1]) > 0:
                #         texcoords.append(int(w[1]))
                #     else:
                #         texcoords.append(0)
                #     if len(w) >= 3 and len(w[2]) > 0:
                #         norms.append(int(w[2]))
                #     else:
                #         norms.append(0)
                # self.faces.append((face, norms, texcoords, material))

        file_obj.close()

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
                current_material.color_ambient = values[1]
            elif values[0] == 'Kd':
                current_material.color_diffuse = values[1]
            elif values[0] == 'Ks':
                current_material.color_specular = values[1]
            elif values[0] == 'Ke':
                current_material.color_emission = values[1]
            elif values[0] == 'Ns':
                current_material.specular_exp = values[1]
            elif values[0] == 'Tr':
                current_material.transparency1 = values[1]
            elif values[0] == 'd':
                current_material.transparency2 = values[1]
            elif values[0] == 'Ni':
                current_material.optical_density = values[1]
            elif values[0] == 'illum':
                current_material.illumination_mode = values[1]
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
