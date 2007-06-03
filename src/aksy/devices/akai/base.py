class SamplerException(Exception):
    """ Exception raised by the sampler
    """
    def __init(self, msg, code):
        Exception.__init__(self, msg)
        self.code = code

    def get_code(self):
        return self.code
