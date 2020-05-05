import pyglet
import logging

logging.basicConfig(format='%(asctime)s %(message)s')

class DSpygletBackend:
    def __init__(self):
        win = pyglet.window.Window()
        self.batch = pyglet.graphics.Batch()
        self.i = 0

        @win.event
        def on_mouse_motion(x, y, button, modifiers):
            
            canvas = self.open_tablet(win)
            self.canvas_reporter(canvas)
            return

        @win.event
        def on_mouse_press(x, y, button, modifiers):
            self.draw(x, y)
            return

        @win.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            return

        @win.event
        def on_mouse_enter(x, y):
            return

        @win.event
        def on_mouse_leave(x, y):
            return

        @win.event
        def on_draw():
            self.batch.draw()


    def motion_reporter(self, x, y, pressure, a, b):
        #msg = "on_motion(x=%s, y=%s, pressure=%s, a=%s, b=%s)" % (x, y, pressure, a, b)
        #logging.info(msg)
        #logging.info("on_motion(x=%s, y=%s, pressure=%s, a=%s, b=%s)", x, y, pressure, a, b)
        print("on_motion(x=%s, y=%s, pressure=%s, a=%s, b=%s)" % (x, y, pressure, a, b))


    def get_tablet(self):
        return pyglet.input.get_tablets()

    def open_tablet(self, win):
        tablets = self.get_tablet()
        
        if not tablets:
            logging.error("tablet is not detected, please retry")
            return None

        name = tablets[0].name

        try:
            canvas = tablets[0].open(win)
        except pyglet.input.DeviceException:
            logging.error("Failed to open tablet")

        logging.info("Opened %s" % name)

        return canvas

    def canvas_reporter(self, canvas):
        if not canvas:
            return
        
        @canvas.event
        def on_motion(cursor, x, y, pressure, a, b):
            #self.motion_reporter(x, y, pressure, a, b)
            if pressure > 0:
                self.draw(x, y)

            return
        
        return
        
    def draw(self, x, y):
        print('drawing: %s %s' % (x, y))
        pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,
             ('v2i', (x, y)),
             ('c3B', (0, 255, 0))
             )
        return

    def update(self, dt):
        print('updated %s' % self.i)
        self.i += 1
        self.batch.draw()

    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/60.0)
        pyglet.app.run()