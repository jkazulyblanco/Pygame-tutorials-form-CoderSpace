#version 430

out vec4 fragColor;

uniform vec2 resolution;
uniform float time;

// rotate function
vec2 rotate2D(vec2 uv, float a) {
    float s = sin(a);
    float c = cos(a);
    return mat2(c, -s, s, c) * uv;
}

vec2 hash12(float t){
    float x = fract(sin(t * 3453.329));
    float y = fract(sin(t + x) * 8532.732);
    return vec2(x, y);
}

void main(){
    vec2 uv = (gl_FragCoord.xy - 0.5 * resolution.xy) / resolution;
    vec3 col = vec3(0.0);

    uv = rotate2D(uv, 3.14 / 2.0);

    float r = 0.17;

    for (float i=0.0; i<60.0; i++) {
        float factor = (sin(time) * 0.5 + 0.5) + 0.3;
        i += factor;
        // parametric equations cardioid
        float a = i / 3;
        float dx = 2 * r * cos(a) - r * cos(2 * a);
        float dy = 2 * r * sin(a) - r * sin(2 * a);

        col += 0.005 * factor / length(uv - vec2(dx + 0.1, dy) - 0.02 * hash12(i));
    }
    col *= sin(vec3(0.2, 0.8, 0.9) * time) * 0.15 + 0.25;

    fragColor = vec4(col, 1.0);
}