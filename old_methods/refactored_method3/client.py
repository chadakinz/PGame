import pygame
from network import Network
from text_surface import Text
import threading
from player import Player
from pynput.mouse import Listener
import time
"""Intialzing the screen and connecting to the server"""
def is_clicked(x, y, button, pressed):
    global player, back2
    pos1, pos2, pos3 = player.pos['bet']
    if pressed and pos2[0] <= x < pos3[0] and pos2[1] <= y < pos3[1] + 300:
         #in your case, you can move it to some other pos
        back2 = False
        return False # to stop the thread after click

def betting():
    global user_text, placeholder, raise_, opp_raise, player, opp
    count = 0
    boolo = False
    boolo2 = True
    back2 = False
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
    while True:
        back2 = False
        pos1, pos2, pos3 = player.pos['bet']
        x, y = pygame.mouse.get_pos()

        if pos1[0] <= x < pos2[0] and pos1[1] <= y < pos2[1] + 300:
            one, two, three = pygame.mouse.get_pressed(num_buttons = 3)
            if one or two or three:
                if check1 == False:

                    return (player, 'Call')
                else:
                    return (player, 'Check')


        elif pos2[0] <= x < pos3[0] and pos2[1] <= y < pos3[1] + 300 and boolo2:

            user_text = ''
            one, two, three = pygame.mouse.get_pressed(num_buttons=3)
            if one or two or three:
                raising = Text('Enter raise amount: ', size = 20)
                back = Text('Click here to go back', size = 20)
                pygame.Surface.blit(screen, erase, player.pos['bet'][0])
                pygame.Surface.blit(screen, erase, player.pos['bet'][1])
                pygame.Surface.blit(screen, erase, player.pos['bet'][2])
                pygame.Surface.blit(screen, raising.text, player.pos['bet'][0])
                pygame.Surface.blit(screen, back.text, player.pos['bet'][1])
                while user_text is not None:

                    user_t = Text(user_text, size=20)
                    pygame.Surface.blit(screen, erase, player.pos['bet'][2])
                    pygame.Surface.blit(screen, user_t.text, player.pos['bet'][2])
                    listener = Listener(on_click= is_clicked)
                    listener.start()

                    if back2 == True:
                        print(f'breaking 2')
                        break
                    user_t = Text(user_text, size = 20)
                    pygame.Surface.blit(screen, erase, player.pos['bet'][2])
                    pygame.Surface.blit(screen, user_t.text, player.pos['bet'][2])

                    if user_text == None:


                        try:
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
                                    print(player.chips)
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
                if back2:
                    pygame.Surface.blit(screen, erase, player.pos['bet'][0])

                    pygame.Surface.blit(screen, erase, player.pos['bet'][1])
                    pygame.Surface.blit(screen, erase, player.pos['bet'][2])
                    if check1:
                        pygame.Surface.blit(screen, check.text, player.pos['bet'][0])
                    else:
                        pygame.Surface.blit(screen, call.text, player.pos['bet'][0])
                    if boolo2:
                        pygame.Surface.blit(screen, raise2.text, player.pos['bet'][1])
                    pygame.Surface.blit(screen, Fold.text, player.pos['bet'][2])
                    print(f'continuing')
                    back2 = False
                    continue
                else:
                    return (player, 'Raise')





        elif pos3[0] <= x < pos3[0] + 300 and pos1[1] <= y < pos2[1] + 300:

            one, two, three = pygame.mouse.get_pressed(num_buttons=3)
            if one or two or three:
                print(f'folded')
                player.isTurn = False
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

pygame.display.flip()
opp = None
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
        try:
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
        except:
            pass
pygame.quit()
