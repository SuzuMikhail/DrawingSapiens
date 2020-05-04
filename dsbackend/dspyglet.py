import pyglet

class DSpygletBackend:
    def getTablet(self):
        return pyglet.input.get_tablets()
        
    def __init__(self):
        window = pyglet.window.Window()

        @window.event
        def on_mouse_press(x, y, button, modifiers):
            tablets = self.getTablet()
            
            if not tablets:
                print("tablet is not detected, please retry")
                return None

            name = tablets[0].name

            try:
                canvas = tablets[0].open(window)
            except pyglet.input.DeviceException:
                print("Failed to open tablet %d on window" % index)

            print("Opened %s" % name)

            @canvas.event
            def on_enter(cursor):
                print("%s: on_enter(%r)" % (name, cursor))

            @canvas.event
            def on_leave(cursor):
                print("%s: on_leave(%r)" % (name, cursor))

            @canvas.event
            def on_motion(cursor, x, y, pressure, a, b):
                print("%s: on_motion(%r, x=%r, y=%r, pressure=%r, a=%s, b=%s)" % (name, cursor, x, y, pressure, a, b))


        @window.event
        def on_mouse_release(x, y, button, modifiers):
            #print("on_mouse_release(%r, %r, %r, %r)" % (x, y, button, modifiers))
            return
            
        pyglet.app.run()