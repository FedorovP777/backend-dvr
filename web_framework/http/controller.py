class Controller:
    middleware = []

    def __init__(self, tornado_instance):
        self.tornado_instance = tornado_instance


class RestController(Controller):
    pass
