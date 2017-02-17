#version 410 core

layout (location = 0) in vec3 vs_vertexPosition;
layout (location = 1) in vec3 vs_vertexNormal;
layout (location = 2) in vec2 vs_textureCoord;
layout (location = 3) in vec3 vs_tangent;
layout (location = 4) in vec3 vs_bitangent;

uniform mat4 vs_MVPMatrix;
uniform mat4 vs_WorldMatrix;
uniform mat4 fs_ModelMatrix;

uniform mat4 shadow_model;
uniform mat4 shadow_lightSpaceMatrix;

uniform vec3 vs_displacementLocation;
uniform float vs_isBorder;

out vec3 tcs_vertexPosition;
out vec2 tcs_textureCoord;
out vec3 tcs_vertexNormal0;
out vec3 tcs_vertexNormal;
out vec3 tcs_tangent0;
out vec3 tcs_tangent;
out vec3 tcs_bitangent0;
out vec3 tcs_bitangent;
out vec3 tcs_displacementLocation;
out float tcs_isBorder;
out vec3 tcs_shadow_Normal;
out vec4 tcs_shadow_FragPosLightSpace;

//out vec3 gs_vertexPosition;
//out vec2 gs_textureCoord;
//out vec3 gs_vertexNormal0;
//out vec3 gs_vertexNormal;
//out vec3 gs_tangent0;
//out vec3 gs_tangent;
//out vec3 gs_bitangent0;
//out vec3 gs_bitangent;
//out vec3 gs_displacementLocation;
//out float gs_isBorder;
//out float gs_height;
//out vec3 gs_shadow_FragPos;
//out vec3 gs_shadow_Normal;
//out vec4 gs_shadow_FragPosLightSpace;

void main(void) {
    tcs_vertexPosition = vs_vertexPosition;
    tcs_textureCoord = vs_textureCoord;
    tcs_vertexNormal0 = vs_vertexNormal;
    tcs_vertexNormal = (vs_WorldMatrix * vec4(vs_vertexNormal, 0.0)).xyz;
    tcs_tangent0 = vs_tangent;
    tcs_tangent = (vs_WorldMatrix * vec4(vs_tangent, 0.0)).xyz;
    tcs_bitangent0 = vs_bitangent;
    tcs_bitangent = (vs_WorldMatrix * vec4(vs_bitangent, 0.0)).xyz;
    tcs_displacementLocation = vs_displacementLocation;
    tcs_isBorder = vs_isBorder;
    tcs_shadow_Normal = transpose(inverse(mat3(shadow_model))) * vs_vertexNormal;
    tcs_shadow_FragPosLightSpace = shadow_lightSpaceMatrix * vec4(vec3(fs_ModelMatrix * vec4(vs_vertexPosition, 1.0)), 1.0);

//    gs_vertexPosition = vs_vertexPosition;
//    gs_textureCoord = vs_textureCoord;
//    gs_vertexNormal0 = vs_vertexNormal;
//    gs_vertexNormal = (vs_WorldMatrix * vec4(vs_vertexNormal, 0.0)).xyz;
//    gs_tangent0 = vs_tangent;
//    gs_tangent = (vs_WorldMatrix * vec4(vs_tangent, 0.0)).xyz;
//    gs_bitangent0 = vs_bitangent;
//    gs_bitangent = (vs_WorldMatrix * vec4(vs_bitangent, 0.0)).xyz;
//    gs_displacementLocation = vs_displacementLocation;
//    gs_isBorder = vs_isBorder;
//    gs_height = 1.0;
//    gs_shadow_FragPos = vec3(fs_ModelMatrix * vec4(vs_vertexPosition, 1.0));
//    gs_shadow_Normal = transpose(inverse(mat3(shadow_model))) * vs_vertexNormal;
//    gs_shadow_FragPosLightSpace = shadow_lightSpaceMatrix * vec4(vec3(fs_ModelMatrix * vec4(vs_vertexPosition, 1.0)), 1.0);

    gl_Position = vs_MVPMatrix * vec4(vs_vertexPosition, 1.0);
}
