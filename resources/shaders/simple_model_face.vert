#version 410 core

layout (location = 0) in vec3 vs_vertexPosition;
layout (location = 1) in vec3 vs_vertexNormal;
layout (location = 2) in vec2 vs_textureCoord;

uniform mat4 vs_MVPMatrix;

void main(void) {
    gl_Position = vs_MVPMatrix * vec4(vs_vertexPosition, 1.0);
}
