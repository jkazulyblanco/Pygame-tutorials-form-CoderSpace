import moderngl_window as mglw

class App(mglw.WindowConfig):
    window_size = 1280, 720
    resource_dir = 'programs'

    def __init__(self, **kwargs):
        # calling super() will automatically create:
        # self.ctx - OpenGL context
        # self.wnd - the window instance
        # self.timer - the timer instance
        super().__init__(**kwargs)
        # create screen aligned quad
        self.quad = mglw.geometry.quad_fs()
        #load shader program
        self.prog = self.load_program(vertex_shader='vertex_shader.glsl',
                                      fragment_shader='fragment_shader.glsl')
        self.set_uniform('resolution', self.window_size)

    def set_uniform(self, u_name, u_value):
        try:
            self.prog[u_name] = u_value
        except KeyError:
            print(f'uniform: {u_name} - not used in shader')

    def render(self, time, frame_time):
        self.ctx.clear()
        self.set_uniform('time', time)
        self.quad.render(self.prog)

if __name__ == '__main__':
    mglw.run_window_config(App)

