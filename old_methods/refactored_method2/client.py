import pygame
from network import Network
from text_surface import Text
import threading
from player import Player
import time
"""Intialzing the screen and connecting to the server"""

def betting(player, first_act):
    global user_text, placeholder, raise_tot, opp_raise
    print(f'inside betting')
    erase = pygame.Surface((200, 120))
    erase.fill((10, 50, 100))
    while True:

        pos1, pos2, pos3 = player.pos['bet']
        x, y = pygame.mouse.get_pos()

        if pos1[0] <= x < pos2[0] and pos1[1] <= y < pos2[1] + 300:
            one, two, three = pygame.mouse.get_pressed(num_buttons = 3)
            if one or two or three:
                player.isTurn = False
                return (player, 'Call')
        elif pos2[0] <= x < pos3[0] and pos2[1] <= y < pos3[1] + 300:
            user_text = ''
            one, two, three = pygame.mouse.get_pressed(num_buttons=3)
            if one or two or three:
                raising = Text('Enter raise amount: ', size = 20)
                pygame.Surface.blit(screen, erase, player.pos['bet'][0])
                pygame.Surface.blit(screen, erase, player.pos['bet'][1])
                pygame.Surface.blit(screen, erase, player.pos['bet'][2])
                pygame.Surface.blit(screen, raising.text, player.pos['bet'][0])
                while user_text is not None:

                    user_t = Text(user_text, size = 20)
                    pygame.Surface.blit(screen, erase, player.pos['bet'][1])
                    pygame.Surface.blit(screen, user_t.text, player.pos['bet'][1])

                    if user_text == None:
                        print(f'user text is none')
                        call_amnt = opp_raise - player.raise_amnt
                        try:
                            placeholder = int(placeholder)
                            if (placeholder - call_amnt) < raise_tot:
                                print(f'Placeholder: {placeholder}, Call Amount: {call_amnt}, Raise: {raise_tot}')

                                user_text = ''
                                continue

                            player.new_raise = placeholder - call_amnt
                            player.raise_amnt += placeholder
                            player.raise_amnt2 = placeholder
                            player.isTurn = False
                            pygame.Surface.blit(screen, erase, player.pos['bet'][0])
                            pygame.Surface.blit(screen, erase, player.pos['bet'][1])



                        except:
                            print(f'Error with input')
                            user_text = ''








                return (player, 'Raise')

        elif pos3[0] <= x < pos3[0] + 300 and pos1[1] <= y < pos2[1] + 300:

            one, two, three = pygame.mouse.get_pressed(num_buttons=3)
            if one or two or three:
                print(f'folded')
                player.isTurn = False
                return (player, 'Fold')

def preflop(n, player):
    screen.fill((10, 50, 100))
    result = None
    print(f'inside preflop')

    n.send('betting')
    first_act = False
    x1, y1 = player.pos['cards'][0]
    x2, y2 = player.pos['cards'][1]

    erase = pygame.Surface((200, 120))
    erase.fill((10, 50, 100))

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
    pygame.Surface.blit(screen, None, (x2, y2))

    print(f'cards shown')
    call = Text('Call', size=50)
    raise2 = Text('Raise', size=50)
    Fold = Text('Fold', size=50)
    check = Text('Check', size= 50)

    while True:


        while not player.isTurn:
            pygame.Surface.blit(screen, erase, player.pos['bet'][0])
            pygame.Surface.blit(screen, erase, player.pos['bet'][1])
            pygame.Surface.blit(screen, erase, player.pos['bet'][2])

            print(f'recieve info')
            result = n.receive()
            print(f'info recieved')
            if result == 'Reset':
                print(f'Recieved information of a fold')

                return
            first_act = True
            if result == 'Call':
                if first_act == True:
                    return
                player.isTurn = True
                break
            if result == 'Raise':
                player.isTurn = True
                break

        pygame.Surface.blit(screen, raise2.text, player.pos['bet'][1])
        pygame.Surface.blit(screen, Fold.text, player.pos['bet'][2])
        if result == 'Call' and first_act == False:
            pygame.Surface.blit(screen, check.text, player.pos['bet'][0])
        else:
            pygame.Surface.blit(screen, call.text, player.pos['bet'][0])

        pygame.display.update()
        print(f'Display Updated')
        action = betting(player, first_act)
        if action == 'Call' and first_act == True:
            return
        player = action[0]
        print(f'action: {action}')
        first_act = True
        result = n.send(action)

        print(result)
        if result == 'Reset':
            return
def flop(n, player):
    global board
    lis = [(200, 400), (400, 400), (600, 400)]
    for i in range(3):
        card = f'{board[i].suit}{board[i].number}'
        imgCard = f'/Users/chadgothelf/PycharmProjects/PGame/playing_cards/{card}.png'
        card = pygame.image.load(imgCard)
        card = pygame.transform.scale(card, (100, 150))
        pygame.Surface.blit(screen, card, lis[i])

    while True:
        pass






    pass
def update_opp():
    global raise_tot, opp_raise, player, board

    print(f'INside opp')
    n2 = Network((player, 'opp'))
    pot_pos = (900, 400)

    while True:
        players = n2.send('opp')


        if players == False:
            continue

        opp, player, pot, raise_tot, board = players[0], players[1], players[2], players[3], players[4]
        opp_raise = opp.raise_amnt
        pot = Text(str(pot))
        chips = Text(str(player.chips))
        face_down_card = f'/Users/chadgothelf/PycharmProjects/PGame/playing_cards/face_down.png'
        card = pygame.image.load(face_down_card)
        card = pygame.transform.scale(card, (100, 150))
        opp_chips = Text(str(opp.chips))
        reset = pygame.Surface((200, 120))
        reset.fill((10, 50, 100))
        pygame.Surface.blit(screen, reset, opp.pos['chips'])
        pygame.Surface.blit(screen, opp_chips.text, opp.pos['chips'])

        pygame.Surface.blit(screen, reset, pot_pos)
        pygame.Surface.blit(screen, pot.text, pot_pos)

        pygame.Surface.blit(screen, reset, player.pos['chips'])
        pygame.Surface.blit(screen, chips.text, player.pos['chips'])

        if opp.show_cards == False:
            pygame.Surface.blit(screen, card, (opp.pos['cards'][0]))
            pygame.Surface.blit(screen, card, (opp.pos['cards'][1]))

        pygame.display.update()
        time.sleep(.5)

def thread():
    global player
    n = Network((player, 'main'))
    print('')
    check_players = n.send('check_players')



    while check_players:
        check_players = n.send('check_players')

    while True:

        game_state = n.send('state')
        n.send('transition')

        if game_state == 'PREFLOP':
            player = n.send('player')
            print(f'player is turn: {player.isTurn}')
            preflop(n, player)
            n.send((None, 'Reset'))



        elif game_state == 'FLOP':
            player = n.send('player')
            flop(n, player)
            pass
        elif game_state == 'TURN':
            pass
        elif game_state == 'RIVER':
            pass
        pass


pygame.init()
raise_tot = 0
screen = pygame.display.set_mode((1280, 720))
board = None
running = True

screen.fill((10, 50, 100))

pygame.display.flip()

n3 = Network((None, 'player'))
player = n3.purpose

opp_raise = None

opp_thread = threading.Thread(target = update_opp, daemon = True)
opp_thread.start()
time.sleep(2)
side_thread = threading.Thread(target = thread, daemon = True)
side_thread.start()

user_text = ''
placeholder = ''

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            elif event.key == pygame.K_RETURN:
                placeholder = user_text
                user_text = None

            else:
                user_text += event.unicode

pygame.quit()
