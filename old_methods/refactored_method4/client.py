import pygame
from network import Network
from text_surface import Text
import threading
from player import Player
from pynput.mouse import Listener
import time
"""Intialzing the screen and connecting to the server"""
def is_clicked(x1, y1, button, pressed):
    global player, btn2, btn1, back3, x, y
    pos1, pos2, pos3 = player.pos['bet']
    if pressed and pos3[0] <= x < pos3[0] + 300 and pos1[1] <= y < pos2[1] + 300:
        print(f'pressed back3')
        back3 = False

    elif pressed and pos1[0] <= x < pos2[0] and pos1[1] <= y < pos2[1] + 300:
        print(f'pressed back1')
        back1 = False

    elif pressed and pos2[0] <= x < pos3[0] and pos1[1] <= y < pos2[1] + 300:
        print(f'pressed back2')
        back2 = False



def raising(boolo, call_amnt):
    global opp_raise, opp, player, btn2, user_text, btn1, back3, placeholder
    print('inside raise')
    erase = pygame.Surface((200, 120))
    erase.fill((10, 50, 100))
    pos1, pos2, pos3 = player.pos['bet']

    raising = Text('Enter raise amount: ', size=20)
    back = Text('Click here to go back', size=20)
    pygame.Surface.blit(screen, erase, player.pos['bet'][0])
    pygame.Surface.blit(screen, erase, player.pos['bet'][1])
    pygame.Surface.blit(screen, erase, player.pos['bet'][2])
    pygame.Surface.blit(screen, raising.text, player.pos['bet'][0])
    pygame.Surface.blit(screen, back.text, player.pos['bet'][2])

    while user_text is not None:
        x, y = pygame.mouse.get_pos()

        if not back3:
            print(back3)
        if not back3:
            back3 = True
            print(f'returning none')
            return None
        user_t = Text(user_text, size=20)
        pygame.Surface.blit(screen, erase, player.pos['bet'][1])
        pygame.Surface.blit(screen, user_t.text, player.pos['bet'][1])


        if user_text == None:

            try:
                print(f'placeholder: {placeholder}')
                placeholder = int(placeholder)

                if (placeholder + player.raise_tot) - opp_raise < raise_:

                    user_text = ''
                    continue
                if placeholder >= player.chips:
                    if boolo:
                        player.chips -= call_amnt + opp.chips
                        player.raise_tot += call_amnt + opp.chips
                        player.raise_amnt = call_amnt + opp.chips
                        return (player, 'Raise')
                    elif not boolo:
                        player.raise_tot += player.chips
                        player.raise_amnt = player.chips
                        player.chips = 0

                    return (player, 'All_In')

                elif placeholder - opp_raise >= opp.chips:
                    player.chips -= call_amnt + opp.chips
                    player.raise_tot += call_amnt + opp.chips
                    player.raise_amnt = call_amnt + opp.chips
                    return (player, 'Raise')

                player.raise_tot += placeholder
                print(f'Player raise total after raise: {player.raise_tot} with raise:{placeholder}')
                player.chips -= placeholder

                player.raise_amnt = placeholder

                pygame.Surface.blit(screen, erase, player.pos['bet'][0])
                pygame.Surface.blit(screen, erase, player.pos['bet'][1])



            except:
                user_text = ''



    return (player, 'Raise')


def betting():
    global user_text, placeholder, raise_, opp_raise, player, opp, btn2, btn1, back3


    boolo2 = True

    time.sleep(.5)
    call_amnt = opp_raise - player.raise_tot
    print(f'Opp_raise: {opp_raise}')
    check1 = False
    call = Text('Call', size=50)
    Fold = Text('Fold', size=50)
    check = Text('Check', size=50)
    if call_amnt >= player.chips:
        boolo2 = False
    else:
        raise2 = Text('Raise', size=50)
        pygame.Surface.blit(screen, raise2.text, player.pos['bet'][1])

    pygame.Surface.blit(screen, Fold.text, player.pos['bet'][2])
    if opp_raise > player.raise_tot:
        print(f'Player raise {player.raise_tot}')
        pygame.Surface.blit(screen, call.text, player.pos['bet'][0])
    else:
        check1 = True
        print(f'Player raise {player.raise_tot}')
        pygame.Surface.blit(screen, check.text, player.pos['bet'][0])

    print(f'inside betting')
    erase = pygame.Surface((200, 120))
    erase.fill((10, 50, 100))

    if player.chips - call_amnt < opp.chips:
        boolo = False
    elif player.chips - call_amnt > opp.chips:
        boolo = True
    else:
        boolo = False
    listener = Listener(on_click=is_clicked)
    listener.start()
    print(f'did this run?')
    while True:

        pos1, pos2, pos3 = player.pos['bet']
        x, y = pygame.mouse.get_pos()

        if pos1[0] <= x < pos2[0] and pos1[1] <= y < pos2[1] + 300:
            one, two, three = pygame.mouse.get_pressed(num_buttons = 3)
            if not back1:
                back1 = True
                if check1 == False:
                    listener.stop()
                    return (player, 'Call')
                else:
                    listener.stop()
                    return (player, 'Check')


        elif pos2[0] <= x < pos3[0] and pos2[1] <= y < pos3[1] + 300 and boolo2:
            #print('Trying to raise')
            user_text = ''

            if not back2:
                back2 = True
                #print(f'condition checked')

                raise_action = raising(boolo, call_amnt)
                if raise_action == None:
                    pygame.Surface.blit(screen, erase, player.pos['bet'][0])
                    pygame.Surface.blit(screen, erase, player.pos['bet'][1])
                    pygame.Surface.blit(screen, erase, player.pos['bet'][2])

                    if call_amnt >= player.chips:
                        boolo2 = False
                    else:
                        raise2 = Text('Raise', size=50)
                        pygame.Surface.blit(screen, raise2.text, player.pos['bet'][1])

                    pygame.Surface.blit(screen, Fold.text, player.pos['bet'][2])
                    if opp_raise > player.raise_tot:
                        print(f'Player raise {player.raise_tot}')
                        pygame.Surface.blit(screen, call.text, player.pos['bet'][0])
                    else:
                        check1 = True
                        print(f'Player raise {player.raise_tot}')
                        pygame.Surface.blit(screen, check.text, player.pos['bet'][0])
                    continue
                else:
                    listener.stop()
                    print(f'recieved action from player')
                    return raise_action






        elif pos3[0] <= x < pos3[0] + 300 and pos1[1] <= y < pos2[1] + 300:

            one, two, three = pygame.mouse.get_pressed(num_buttons=3)
            if not back3:
                back3 = True
                print(f'folded')
                player.isTurn = False
                listener.stop()
                return (player, 'Fold')





def update_opp():
    global raise_tot, opp_raise, player, board, opp

    n2 = Network((player, 'opp'))
    board_pos = [(200, 300), (300, 300), (400, 300), (500, 300), (600, 300)]
    pot_pos = (900, 400)
    players = n2.send('opp')
    reset = pygame.Surface((200, 120))
    erase = pygame.Surface((100, 150))
    reset.fill((10, 50, 100))
    erase.fill((10, 50, 100))
    while players == False:
        players = n2.send('opp')



    while True:

        players = n2.send('opp')

        opp, player, pot, raise_, board = players[0], players[1], players[2], players[3], players[4]
        opp_raise = opp.raise_tot



        try:

            for i in range(2):

                card = f'{player.cards[i].suit}{player.cards[i].number}'
                imgCard = f'/Users/chadgothelf/PycharmProjects/PGame/playing_cards/{card}.png'
                card = pygame.image.load(imgCard)
                card = pygame.transform.scale(card, (100, 150))
                pygame.Surface.blit(screen, card, player.pos['cards'][i])
        except:
            #print(f'player cards: {player.cards[0].number}{player.cards[1].number}')
            pass

        try:


            for i in range(len(board)):

                card = f'{board[i].suit}{board[i].number}'
                imgCard = f'/Users/chadgothelf/PycharmProjects/PGame/playing_cards/{card}.png'
                card = pygame.image.load(imgCard)
                card = pygame.transform.scale(card, (100, 150))
                pygame.Surface.blit(screen, card, board_pos[i])

            for i in range(-1, -(6 - len(board)), -1):

                pygame.Surface.blit(screen, erase, board_pos[i])

        except:
            pass
        face_down_card = f'/Users/chadgothelf/PycharmProjects/PGame/playing_cards/face_down.png'
        card = pygame.image.load(face_down_card)
        card = pygame.transform.scale(card, (100, 150))



        player_chips = Text(str(player.chips))
        pygame.Surface.blit(screen, reset, player.pos['chips'])
        pygame.Surface.blit(screen, player_chips.text, player.pos['chips'])




        opp_chips = Text(str(opp.chips))
        pygame.Surface.blit(screen, reset, opp.pos['chips'])
        pygame.Surface.blit(screen, opp_chips.text, opp.pos['chips'])



        pot = Text(str(pot))
        pygame.Surface.blit(screen, reset, pot_pos)
        pygame.Surface.blit(screen, pot.text, pot_pos)



        if opp.show_cards == False:
            pygame.Surface.blit(screen, card, (opp.pos['cards'][0]))
            pygame.Surface.blit(screen, card, (opp.pos['cards'][1]))

        pygame.display.update()
        time.sleep(.5)


def thread():
    global player
    erase = pygame.Surface((200, 120))
    erase.fill((10, 50, 100))
    n = Network((player, 'main'))
    while True:

        print('')
        n.receive()
        action = betting()

        pygame.Surface.blit(screen, erase, player.pos['bet'][0])
        pygame.Surface.blit(screen, erase, player.pos['bet'][1])
        pygame.Surface.blit(screen, erase, player.pos['bet'][2])

        n.send(action)






pygame.init()
raise_ = 0
screen = pygame.display.set_mode((1280, 720))
board = None
running = True
screen.fill((10, 50, 100))
x = y = None
pygame.display.flip()
opp = None
n3 = Network((None, 'player'))
player = n3.purpose

opp_raise = None
btn1 = True
btn2 = True
back3 = True
opp_thread = threading.Thread(target = update_opp, daemon = True)
opp_thread.start()
time.sleep(2)
side_thread = threading.Thread(target = thread, daemon = True)
side_thread.start()

user_text = ''
placeholder = ''

while running:
    x, y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        try:
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    print(f'user_text is none')
                    placeholder = user_text
                    user_text = None

                else:
                    user_text += event.unicode
        except:
            pass
pygame.quit()
