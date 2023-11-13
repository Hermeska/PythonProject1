import pygame
import map_gen
import map_graphics
import map_solver
import constants
import button
import map_data
import sys


class Game:
    def __init__(self, is_console):
        self.is_console = is_console
        self.window = ''

        self.window_width = constants.WIDTH
        self.window_height = constants.HEIGHT + constants.MARGIN_TOP
        self.amount_of_cells_x = constants.CELLS_X
        self.amount_of_cells_y = constants.CELLS_Y

        if not self.is_console:
            pygame.init()
            self.window = pygame.display.set_mode((self.window_width, self.window_height))
        else:
            self.load_name = ""
            self.saving_name = ""
            self.mode = ""
            self.is_saving = False
            self.is_loading = False
            for i in range(1, len(sys.argv)):
                param = sys.argv[i]
                if param == "-a":
                    self.mode = sys.argv[i + 1]
                if param == "-s":
                    self.is_saving = True
                    self.saving_name = sys.argv[i + 1]
                if param == "-sd":
                    self.is_saving = True
                if param == "-l":
                    self.is_loading = True
                    self.load_name = sys.argv[i + 1]

        self.graphics = map_graphics.MapGraphics(self.window_width, self.window_height, self.amount_of_cells_x,
                                                 self.amount_of_cells_y, self.window, is_console)
        self.map = []
        self.passes = {}

        self.files_menu = map_data.FilesMenu(self.window)

        self.is_playing = True
        self.ready_to_solve = False

        self.button_width = 100
        self.button_height = 20
        if not self.is_console:
            dfs_button = button.Button(self.window, (
                constants.MARGIN_TOP / 4, constants.MARGIN_TOP / 4, self.button_width, self.button_height), "dfs",
                                       self.map_with_dfs)
            aldous_button = button.Button(self.window, (
                constants.MARGIN_TOP / 2 + self.button_width, constants.MARGIN_TOP / 4, self.button_width,
                self.button_height), "aldous", self.map_with_aldous)
            kruskal_button = button.Button(self.window, (
                (3 * constants.MARGIN_TOP) / 4 + 2 * self.button_width, constants.MARGIN_TOP / 4, self.button_width,
                self.button_height), "kruskal", self.map_with_kruskal)
            next_map_button = button.Button(self.window, (
                constants.WIDTH - (3 * constants.MARGIN_TOP) / 4, constants.MARGIN_TOP / 4, self.button_height,
                self.button_height), ">", self.load_next)
            prev_map_button = button.Button(self.window, (
                constants.WIDTH - (6 * constants.MARGIN_TOP) / 4, constants.MARGIN_TOP / 4,
                self.button_height, self.button_height), "<", self.load_next)
            save_button = button.Button(self.window, (
                constants.WIDTH - (7 * constants.MARGIN_TOP) / 4 - self.button_width, constants.MARGIN_TOP / 4,
                self.button_width, self.button_height), "save", self.save)
            solve_button = button.Button(self.window, (
                constants.WIDTH / 2 - self.button_width / 2, constants.MARGIN_TOP / 4, self.button_width,
                self.button_height),
                                         "solve", self.solve)
            self.buttons = [dfs_button,
                            aldous_button, kruskal_button, next_map_button,
                            prev_map_button, save_button, solve_button]

    def run(self):
        if not self.is_console:
            while self.is_playing:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.click_buttons(event)
                pygame.display.flip()
        else:
            if not self.is_loading:
                if self.mode == "dfs":
                    self.map_with_dfs()
                elif self.mode == "aldous":
                    self.map_with_aldous()
                elif self.mode == "kruskal":
                    self.map_with_kruskal()
                else:
                    print("No algorithm found!")
            else:
                files = self.files_menu.load(self.load_name)
                self.load(files)
            if self.is_saving:
                if self.saving_name == "":
                    self.save()
                else:
                    self.save(self.saving_name)
            self.solve()

    def map_with_dfs(self):
        self.graphics.cell = 0
        self.clear()
        generated_map = map_gen.Generator(self.amount_of_cells_x, self.amount_of_cells_y)
        generated_map.dfs()
        generated_map.generate_map()
        self.map, self.passes = generated_map.map, generated_map.passes
        self.graphics.draw_map(generated_map.map, generated_map.passes, self.is_console)
        self.ready_to_solve = True

    def map_with_aldous(self):
        self.graphics.cell = 0
        self.clear()
        dfs = map_gen.Generator(self.amount_of_cells_x, self.amount_of_cells_y)
        dfs.aldous_broder()
        dfs.generate_map()
        self.graphics.draw_map(dfs.map, dfs.passes, self.is_console)
        self.ready_to_solve = True

    def map_with_kruskal(self):
        self.graphics.cell = 0
        self.clear()
        dfs = map_gen.Generator(self.amount_of_cells_x, self.amount_of_cells_y)
        dfs.kruskal()
        dfs.generate_map()
        self.graphics.draw_map(dfs.map, dfs.passes, self.is_console)
        self.ready_to_solve = True

    def solve(self):
        if not self.ready_to_solve:
            return 0
        solve = map_solver.Solver(self.graphics.passes, self.amount_of_cells_x, self.amount_of_cells_y)
        if not self.is_console:
            pygame.display.flip()
        self.graphics.draw_path(solve.path, self.is_console)

    def clear(self):
        if not self.is_console:
            self.graphics.clear_display()

    def click_buttons(self, event):
        for but in self.buttons:
            but.click(event)

    def load_next(self):
        files = self.files_menu.read_next()
        self.load(files)

    def load_prev(self):
        files = self.files_menu.read_prev()
        self.load(files)

    def load(self, files):
        if files is not None:
            map, passes = files[0], files[1]
            self.clear()
            self.amount_of_cells_x = len(map[0]) // 3
            self.amount_of_cells_y = len(map) // 3
            self.graphics = map_graphics.MapGraphics(self.window_width, self.window_height, self.amount_of_cells_x,
                                                     self.amount_of_cells_y, self.window, self.is_console)
            self.graphics.draw_map(map, passes, self.is_console)
            solve = map_solver.Solver(self.graphics.passes, self.amount_of_cells_x, self.amount_of_cells_y)
            if not self.is_console:
                pygame.display.flip()
            self.graphics.draw_path(solve.path, self.is_console)

    def save(self, name=constants.SAVE_NAME):
        self.files_menu.save(self.graphics.field, self.graphics.passes, name)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        game = Game(True)
        game.run()
    else:
        game = Game(False)
        game.run()
