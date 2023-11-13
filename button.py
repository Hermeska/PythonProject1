import pygame.draw


class Button(pygame.sprite.Sprite):
    def __init__(self, window, coords, text, func=lambda: True):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(coords)
        self.image = pygame.Surface((coords[2], coords[3]))
        self.func = func
        self.window = window
        font = pygame.font.Font(None, coords[3])
        self.text = font.render(
            text, True, (0, 0, 0))
        self.place = self.text.get_rect(
            center=(coords[0] + coords[2] / 2, coords[1] + coords[3] / 2))
        self.draw_button()

    def draw_button(self):
        pygame.draw.rect(self.window, (255, 255, 255), self.rect, 0)
        self.window.blit(self.text, self.place)
        pygame.display.update()
        pygame.display.flip()

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    return self.func()
