import pygame
from text_surface import Text
from network import Network


class Client:
    def __init__(self):
        pass


def pre_flop():

    pass


def round_start():
    pass

def betting(player):
    global state
    if state == 'PREFLOP':
        if player.isdealer == True:

            call = Text('Call', size = 50)
            raise2 = Text('Raise', size = 50)
            Fold = Text('Fold', size = 50)
            pygame.Surface.blit(screen, call.text, player.pos['bet'][0])
            pygame.Surface.blit(screen, raise2.text, player.pos['bet'][1])
            pygame.Surface.blit(screen, Fold.text, player.pos['bet'][2])

            state = 'FLOP'




    pass




def update_opps(players):

    face_down_card = f'/Users/chadgothelf/PycharmProjects/PGame/playing_cards/face_down.png'
    card = pygame.image.load(face_down_card)
    card = pygame.transform.scale(card, (100, 150))

    for x, i in players.items():

        opp_chips = Text(str(i.chips))
        reset = pygame.Surface((200, 120))
        reset.fill((10, 50, 100))
        pygame.Surface.blit(screen, reset, i.pos['chips'])
        pygame.Surface.blit(screen, opp_chips.text, i.pos['chips'])


        if i.show_cards == False:

            pygame.Surface.blit(screen, card, (i.pos['cards'][0], i.pos['cards'][1]))
            pygame.Surface.blit(screen, card, (i.pos['cards'][2], i.pos['cards'][3]))

        pygame.display.update()







def deal_cards(player):

    global state
    x, y, x1, y1 = player.pos['cards']
    cards = player.cards
    print(f'inside deal cards')
    card1 = f'{cards[0].suit}{cards[0].number}'
    card2 = f'{cards[1].suit}{cards[1].number}'
    imgCard1 = f'/Users/chadgothelf/PycharmProjects/PGame/playing_cards/{card1}.png'
    imgCard2 = f'/Users/chadgothelf/PycharmProjects/PGame/playing_cards/{card2}.png'

    card1 = pygame.image.load(imgCard1)
    card2 = pygame.image.load(imgCard2)

    print('loaded images...')

    card1 = pygame.transform.scale(card1, (100, 150))
    card2 = pygame.transform.scale(card2, (100, 150))

    #pygame.Surface.blit(screen, card1, (150,  500))
    #pygame.Surface.blit(screen, card2, (200, 500))
    pygame.Surface.blit(screen, card1, (x, y))
    pygame.Surface.blit(screen, card2, (x1, y1))
    print('RAN')

    pygame.display.flip()

pygame.init()

screen = pygame.display.set_mode((1280, 720))

running = True

#myTable = Table()
state = 'PREFLOP'

screen.fill((10, 50, 100))

pygame.display.flip()

n = Network()

#start_new_thread(thread, ())

while running:

    player = n.send('player')
    print(player.chips)
    chips = Text(str(player.chips))
    opps = n.send("update")

    if opps == False:
        pass
    else:
        update_opps(opps)
    #print(f'GO')



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    if state == 'PREFLOP':



        player = n.send("PREFLOP")

        print(f'I recieved the cards: {player.cards}')
        deal_cards(player)
        if player.isdealer == True:
            player.chips -= 50

        else:

            player.chips -= 100
        n.send(player)
    if player.isdealer == True:
        pass
    reset = pygame.Surface((200,120))
    reset.fill((10, 50, 100))

    #pygame.Surface.blit(screen, chips.render(str.encode(str(chips))), (300, 500))
    pygame.Surface.blit(screen, reset, player.pos['chips'])
    pygame.Surface.blit(screen, chips.text, player.pos['chips'])
    betting(player)
    pygame.display.update()

pygame.quit()
