import os.path
import constants


class FilesMenu:
    def __init__(self, window):
        self.index = 0

        self.window = window

    def read_next(self):
        files = os.listdir(constants.SAVE_DIR)
        if len(files) > 0:
            data = self.load(files[self.index % len(files)])
            self.index += 1
            return data

    def read_prev(self):
        files = os.listdir(constants.SAVE_DIR)
        data = self.load(files[self.index % len(files)])
        self.index -= 1
        return data

    def save(self, map, passes, name=constants.SAVE_NAME):
        add_number = 0
        while os.path.isfile(constants.SAVE_DIR + '/' + name):
            if not add_number:
                add_number += 1
                name += str(add_number)
            else:
                add_number += 1
                name = name[0:len(name) - len(str(add_number))] + str(add_number)
        with open(constants.SAVE_DIR + "/" + name, "w") as file:
            file.write(str(map) + "\n" + str(passes))

    def load(self, name):
        with open(constants.SAVE_DIR + '/' + name, "r") as file:
            map = file.readline()
            passes = file.readline()
        return eval(map), eval(passes)
