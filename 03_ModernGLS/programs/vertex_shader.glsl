#version 430 // GLSL languahe version used

// screen plane vertex coordinates (transferred from the vertex buffer)
in vec3 in_position;

void main(){
    gl_Position = vec4(in_position, 1);
}