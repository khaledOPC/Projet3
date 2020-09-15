import pygame
from models import Game

rect = pygame.Rect(20, 20, 20, 20)
OFFSET = 20
FPS = 10
FPSCLDCK = pygame.time.Clock()


class GameView:
    """"""

    def __init__(self):
        self.game = Game()
        self.box_image = self.get_image("floor-tiles-20x20.png")
        self.player_image = self.get_image("MacGyver.png", True)
        self.ether_image = self.get_image("ether.png", True)
        self.tube_plastic = self.get_image("tube_plastic.png", True)
        self.aiguille_image = self.get_image("aiguille.png", True)
        self.boss_image = self.get_image("Gardien.png", True)
        pygame.init()
        pygame.display.set_caption("Help Mcgyver")
        self.screen = pygame.display.set_mode(
            (self.game.width * OFFSET, self.game.width * OFFSET + 25)
        )  # noqa
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((41, 36, 33))
        self.background = background

    def get_image(self, file, scale=False):
        """
        get_image function for add a image
        """
        file = f"src/macgyver_ressources/ressource/{file}"
        image = pygame.image.load(file)
        if scale:
            image = pygame.transform.scale(image, (20, 20))
        return image

    def display_game(self):
        self.screen.blit(self.background, (0, 0))
        blue = (255, 255, 255)
        arial_font = pygame.font.SysFont("arial", 20)

        for i, box in enumerate(self.game.list_box):
            if box.is_black():
                self.screen.blit(
                    self.box_image, self.game.position_to_coordinate(
                        i, OFFSET
                    ), rect
                )

            if i == self.game.items[0].position and not self.game.items[0].is_taken: # noqa
                self.screen.blit(
                    self.ether_image, self.game.position_to_coordinate(
                        i, OFFSET
                    )
                )

            elif i == self.game.items[1].position and not self.game.items[1].is_taken: # noqa
                self.screen.blit(
                    self.tube_plastic, self.game.position_to_coordinate(
                        i, OFFSET
                    )
                )

            elif i == self.game.items[2].position and not self.game.items[2].is_taken: # noqa
                self.screen.blit(
                    self.aiguille_image, self.game.position_to_coordinate(
                        i, OFFSET
                    )
                )

        self.screen.blit(
            self.player_image,
            self.game.position_to_coordinate(
                self.game.player.position, OFFSET
            ),
        )
        self.screen.blit(
            self.boss_image,
            self.game.position_to_coordinate(self.game.boss.position, OFFSET),
        )

        items_display = arial_font.render(
            str(self.game.count_missing_items()), True, blue
        )
        self.screen.blit(items_display, (55, 300))

        message_display = arial_font.render(
            str(self.game.message()), True, blue
        )
        self.screen.blit(
            message_display, self.game.position_to_coordinate(15, 300)
        )

        message_2_display = arial_font.render(
            str(self.game.message_2()), True, blue
        )  # noqa
        self.screen.blit(message_2_display, (75, 300))

        and_message_display = arial_font.render(
            self.game.and_message(), True, blue
        )  # noqa
        self.screen.blit(and_message_display, (125, 300))


def main():
    game_view = GameView()
    game = game_view.game
    running = True

    while running:
        """
        infinite loop as long as this condition is true
        """
        game_view.display_game()
        """
        apply the background of the surface and display the game
        """
        for event in pygame.event.get():
            """
            if the player closes the window
            """
            if event.type == pygame.QUIT:
                """
                if event is closing
                """
                running = False
                pygame.quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] != 0:
            game.move_up()
        if keys[pygame.K_DOWN] != 0:
            game.move_down()
        if keys[pygame.K_LEFT] != 0:
            game.move_left()
        if keys[pygame.K_RIGHT] != 0:
            game.move_right()

        response = game.check_game()
        if response:
            response
        FPSCLDCK.tick(FPS)

        pygame.display.flip()
