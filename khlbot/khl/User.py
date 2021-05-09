class User:
    def __init__(self, body: dict):
        self.__data = body

    def __getattr__(self, item):
        if item in self.__data:
            return self.__data[item]
        return None

    def __getitem__(self, item):
        if item in self.__data:
            return self.__data[item]

        return None
