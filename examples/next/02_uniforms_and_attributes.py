'''
    Renders a rotating and scaling traignle
'''

import moderngl.next as mgl
import numpy as np

from example_window import Example, run_example


class UniformsAndAttributes(Example):
    def __init__(self):
        self.ctx = mgl.create_context()

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330
                in vec2 vert;

                uniform vec2 scale;
                uniform float rotation;

                void main() {

                    mat2 rot = mat2(
                        cos(rotation), sin(rotation),
                        -sin(rotation), cos(rotation)
                    );
                    gl_Position = vec4((rot * vert) * scale, 0.0, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330

                out vec4 color;
                void main() {
                    color = vec4(0.3, 0.5, 1.0, 1.0);
                }
            ''',
        )

        width, height = self.wnd.size

        vertices = np.array([
            1.0, 0.0,
            -0.5, 0.86,
            -0.5, -0.86,
        ])

        self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'vert')

    def render(self):
        sin_scale = np.sin(np.deg2rad(self.wnd.time * 60))

        self.ctx.screen.viewport = self.wnd.viewport
        self.ctx.clear(1.0, 1.0, 1.0)
        self.vao.render()
        self.prog['rotation'] = self.wnd.time

        # Change the scale of the triangle sin-ly
        self.prog['scale'] = (sin_scale * 0.75, 0.75)


run_example(UniformsAndAttributes)
