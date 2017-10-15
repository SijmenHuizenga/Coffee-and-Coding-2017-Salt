class CustomFrameError(Exception):
    def __init__(self, frame_url):
        self.frame_url = frame_url

    def get_url(self):
        return self.frame_url
