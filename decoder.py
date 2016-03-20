from json import JSONDecoder

__author__ = 'Victor'


class BaseDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(BaseDecoder, self).__init__(object_hook = self.dictToObj, *args, **kwargs)

    def dictToObj(self, d):
        raise NotImplementedError("This method must be reimplemented")