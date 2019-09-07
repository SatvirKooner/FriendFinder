from PIL import Image


class Camera_effects(object):
    def __init__(self):
        pass

    def transform(self, img):
        return img.transpose(Image.FLIP_LEFT_RIGHT)