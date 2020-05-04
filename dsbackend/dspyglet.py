import pyglet
import logging

logging.basicConfig(format='%(asctime)s %(message)s')

class DSpygletBackend:
    def get_tablet(self):
        return pyglet.input.get_tablets()

    def open_tablet(self, window):
        tablets = self.get_tablet()
        
        if not tablets:
            logging.error("tablet is not detected, please retry")
            return None

        name = tablets[0].name

        try:
            canvas = tablets[0].open(window)
        except pyglet.input.DeviceException:
            logging.error("Failed to open tablet")

        logging.info("Opened %s" % name)

        return canvas

        
    def __init__(self):
        window = pyglet.window.Window()

        @window.event
        def on_mouse_motion(x, y, button, modifiers):
            canvas = self.open_tablet(window)
            if not canvas:
                return
            
            @canvas.event
            def on_motion(cursor, x, y, pressure, a, b):
                self.motion_reporter(x, y, pressure, a, b)


    def motion_reporter(self, x, y, pressure, a, b):
        #msg = "on_motion(x=%s, y=%s, pressure=%s, a=%s, b=%s)" % (x, y, pressure, a, b)
        #logging.info(msg)
        #logging.info("on_motion(x=%s, y=%s, pressure=%s, a=%s, b=%s)", x, y, pressure, a, b)
        print("on_motion(x=%s, y=%s, pressure=%s, a=%s, b=%s)" % (x, y, pressure, a, b))
    

    def run(self):
        pyglet.app.run()