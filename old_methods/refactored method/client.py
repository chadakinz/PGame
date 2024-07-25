import pygame
from network import Network
from text_surface import Text
import threading
import time
"""Intialzing the screen and connecting to the server"""
def update_opp():
    print(f'INside opp')
    n2 = Network()
    while True:

        opp = n2.send('opp')

        face_down_card = f'/Users/chadgothelf/PycharmProjects/PGame/playing_cards/face_down.png'
        card = pygame.image.load(face_down_card)
        card = pygame.transform.scale(card, (100, 150))
        opp_chips = Text(str(opp.chips))
        reset = pygame.Surface((200, 120))
        reset.fill((10, 50, 100))
        pygame.Surface.blit(screen, reset, opp.pos['chips'])
        pygame.Surface.blit(screen, opp_chips.text, opp.pos['chips'])

        if opp.show_cards == False:
            pygame.Surface.blit(screen, card, (opp.pos['cards'][0]))
            pygame.Surface.blit(screen, card, (opp.pos['cards'][1]))

        pygame.display.update()
        time.sleep(.5)

def preflop(player):
    print(f'inside preflop')
    x1, y1 = n.id['cards'][0]
    x2, y2 = n.id['cards'][1]

    cards = player.cards
    card1 = f'{cards[0].suit}{cards[0].number}'
    card2 = f'{cards[1].suit}{cards[1].number}'

    imgCard1 = f'/Users/chadgothelf/PycharmProjects/PGame/playing_cards/{card1}.png'
    imgCard2 = f'/Users/chadgothelf/PycharmProjects/PGame/playing_cards/{card2}.png'

    card1 = pygame.image.load(imgCard1)
    card2 = pygame.image.load(imgCard2)

    card1 = pygame.transform.scale(card1, (100, 150))
    card2 = pygame.transform.scale(card2, (100, 150))

    pygame.Surface.blit(screen, card1, (x1, y1))
    pygame.Surface.blit(screen, card2, (x2, y2))

    print(f'cards shown')
    call = Text('Call', size=50)
    raise2 = Text('Raise', size=50)
    Fold = Text('Fold', size=50)



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while not player.isTurn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    player = n.send('player')

        pygame.Surface.blit(screen, call.text, n.id['bet'][0])
        pygame.Surface.blit(screen, raise2.text, n.id['bet'][1])
        pygame.Surface.blit(screen, Fold.text, n.id['bet'][2])
        pygame.display.update()
        break
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False











pygame.init()

screen = pygame.display.set_mode((1280, 720))

running = True


screen.fill((10, 50, 100))

print('screen filled')
pygame.display.flip()

n = Network()


#player = n.receive()
check_players = True
"""Checking if there are two players connected to the server so that the game can start"""


while check_players:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    check_players = n.send('check_player')


print("all players in!")
"""Client loops through all checkpoints until game ends"""


n.send('transition')

time.sleep(2)

oppUpdate = threading.Thread(target = update_opp)
oppUpdate.start()
while running:
    print('running!')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    game_state = n.send('state')

    if game_state == 'PREFLOP':
        player = n.send('player')
        preflop(player)


    elif game_state == 'FLOP':
        pass
    elif game_state == 'TURN':
        pass
    elif game_state == 'RIVER':
        pass
    pass

pygame.quit()
