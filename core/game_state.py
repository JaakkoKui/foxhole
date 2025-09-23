class SceneManager:
    """
    Manages the current scene and delegates event handling, updating, and drawing.
    """

    def __init__(self):
        self.current_scene = None

    def set_scene(self, scene):
        self.current_scene = scene

    def handle_events(self, events):
        if self.current_scene:
            self.current_scene.handle_events(events)

    def update(self, dt):
        if self.current_scene:
            self.current_scene.update(dt)

    def draw(self, screen, dt):
        """
        Draw the current scene. Pass both screen and dt to the scene's draw method.
        """
        if self.current_scene:
            self.current_scene.draw(screen, dt)