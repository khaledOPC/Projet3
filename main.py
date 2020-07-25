import pygame
from models import Game

rect = pygame.Rect(20, 20, 20, 20)


# get_image function for add a image without repeat everytime the same sentence
def get_image(file, scale=False):
    file = f"macgyver_ressources/ressource/{file}"
    image = pygame.image.load(file)
    if scale:
        image = pygame.transform.scale(image, (20, 20))
    return image


box_image = get_image("floor-tiles-20x20.png")

player_image = get_image("MacGyver.png", True)

ether_image = get_image("ether.png", True)

tube_plastic = get_image("tube_plastic.png", True)

aiguille_image = get_image("aiguille.png", True)

boss_image = get_image("Gardien.png", True)


OFFSET = 20
FPS = 10
FPSCLDCK = pygame.time.Clock()


def display_game(game, screen):

    for i, box in enumerate(game.list_box):
        if box.is_black():
            screen.blit(box_image, game.position_to_coordinate(i, OFFSET), rect) # noqa

        if i == game.items[0].position and not game.items[0].is_taken:
            screen.blit(ether_image, game.position_to_coordinate(i, OFFSET))

        elif i == game.items[1].position and not game.items[1].is_taken:
            screen.blit(tube_plastic, game.position_to_coordinate(i, OFFSET))

        elif i == game.items[2].position and not game.items[2].is_taken:
            screen.blit(aiguille_image, game.position_to_coordinate(i, OFFSET))


def main():
    game = Game()

    pygame.init()

    pygame.display.set_caption("Help Mcgyver")
    screen = pygame.display.set_mode((game.width*OFFSET, game.width*OFFSET + 25)) # noqa

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((41, 36, 33))
    blue = (255, 255, 255)
    arial_font = pygame.font.SysFont("arial", 20)
    running = True
    # infinite loop as long as this condition is true
    while running:
        screen.blit(background, (0, 0))
        display_game(game, screen)
    # apply the background of the surface
        screen.blit(player_image, game.position_to_coordinate(game.player.position, OFFSET)) # noqa
        screen.blit(boss_image, game.position_to_coordinate(game.boss.position, OFFSET)) # noqa
    # screen.blit(box_image, (200, 100), rect) # blit superimposes an image
        items_display = arial_font.render(str(game.count_missing_items()), True, blue) # noqa
        screen.blit(items_display, (55, 300))

        message_display = arial_font.render(str(game.message()), True, blue)
        screen.blit(message_display, game.position_to_coordinate(15, 300))

        message_2_display = arial_font.render(str(game.message_2()), True, blue) # noqa
        screen.blit(message_2_display, (75, 300))

        and_message_display = arial_font.render(game.and_message(), True, blue) # noqa
        screen.blit(and_message_display, (125, 300))

    # if the player closes the window
        for event in pygame.event.get():
            # if event is closing
            if event.type == pygame.QUIT:
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
            print(response)
            # running = False
        FPSCLDCK.tick(FPS)

        pygame.display.flip()


if __name__ == "__main__":
    # execute only if run as a script
    main()
