import pygame
from network import Network
from heads_up.draw_tools.text_surface import Text
import threading
from pynput.mouse import Listener
import time

"""Method used with the listener function, the listener starts a thread that receives information on the mouse button. 
If the mouse button is clicked, variables are changed accordingly"""
def is_clicked(x1, y1, button, pressed):
    global player, btn2, btn1, btn3, x, y
    pos1, pos2, pos3 = player.pos['bet']
    if pressed and pos3[0] <= x < pos3[0] + 300 and pos1[1] <= y < pos2[1] + 300:
        btn3 = False

    elif pressed and pos1[0] <= x < pos2[0] and pos1[1] <= y < pos2[1] + 300:
        btn1 = False

    elif pressed and pos2[0] <= x < pos3[0] and pos1[1] <= y < pos2[1] + 300:
        btn2 = False


"""Function is run if the player chooses to raise"""
def raising(boolo, call_amnt):
    global opp, player, user_text, btn3, placeholder, erase

    raising = Text('Enter raise amount: ', size=20)
    back = Text('Click here to go back', size=20)

    pygame.Surface.blits(screen, blit_sequence = ((erase, player.pos['bet'][0]), (erase, player.pos['bet'][1]), (erase, player.pos['bet'][2]),
                                                  (raising.text, player.pos['bet'][0]), (back.text, player.pos['bet'][2])))
    while user_text is not None:
        if not btn3:
            btn3 = True
            return None

        user_t = Text(user_text, size=20)
        pygame.Surface.blits(screen, blit_sequence = (((erase, player.pos['bet'][1])), (user_t.text, player.pos['bet'][1])))

        if user_text == None:
            try:
                placeholder = int(placeholder)
                if (placeholder + player.raise_tot) - opp.raise_tot < raise_:
                    user_text = ''
                    continue

                if placeholder >= player.chips:
                    if boolo:
                        player.raise_sequence(call_amnt + opp.chips)
                        return (player, 'Raise')
                    elif not boolo:
                        player.raise_sequence(player.chips)
                    return (player, 'All_In')

                elif placeholder - opp.raise_tot >= opp.chips:
                    player.raise_sequence(call_amnt + opp.chips)
                    return (player, 'Raise')
                player.raise_sequence(placeholder)

                pygame.Surface.blits(screen, blit_sequence = ((erase, player.pos['bet'][0]), (erase, player.pos['bet'][1])))

            except:
                user_text = ''
    return (player, 'Raise')

"""Function is run when it is the players turn to bet"""
def betting():
    global player, opp, btn2, btn1, btn3, x, y, erase
    time.sleep(.5)
    call_amnt = opp.raise_tot - player.raise_tot
    check1 = False
    call = Text('Call', size=50)
    Fold = Text('Fold', size=50)
    check = Text('Check', size=50)
    """Checking to see if the player has enough chips to raise from the current bet"""
    if call_amnt < player.chips:
        raise2 = Text('Raise', size=50)
        pygame.Surface.blit(screen, raise2.text, player.pos['bet'][1])

    pygame.Surface.blit(screen, Fold.text, player.pos['bet'][2])

    """Checking to see if the player needs to call or if they can check"""
    if opp.raise_tot > player.raise_tot:
        pygame.Surface.blit(screen, call.text, player.pos['bet'][0])
    else:
        check1 = True
        pygame.Surface.blit(screen, check.text, player.pos['bet'][0])
    '''Edge cases for if the player goes all in, we need to know if the all in covers the opponent chips'''
    #FIXME needs better variable then boolo
    if player.chips - call_amnt <= opp.chips:
        boolo = False

    elif player.chips - call_amnt > opp.chips:
        boolo = True

    """Listener is here to locate the position and state of the mouse"""
    listener = Listener(on_click=is_clicked)
    listener.start()
    pos1, pos2, pos3 = player.pos['bet']

    while True:

        if not btn1:
            btn1 = True
            if check1 == False:
                listener.stop()
                return (player, 'Call')
            else:
                listener.stop()
                return (player, 'Check')

        if not btn2:
            btn2 = True
            raise_action = raising(boolo, call_amnt)
            if raise_action == None:

                pygame.Surface.blits(screen, blit_sequence=((erase, pos1), (erase, pos2), (erase, pos3)))
                pygame.Surface.blit(screen, Fold.text, pos2)

                if call_amnt < player.chips:
                    raise2 = Text('Raise', size=50)
                    pygame.Surface.blit(screen, raise2.text, pos1)

                if opp.raise_tot > player.raise_tot:
                    pygame.Surface.blit(screen, call.text, player.pos['bet'][0])
                else:
                    pygame.Surface.blit(screen, check.text, player.pos['bet'][0])
                continue

            else:
                listener.stop()
                return raise_action

        if not btn3:
            btn3 = True
            player.isTurn = False
            listener.stop()
            return (player, 'Fold')




"""Recieves constant and immediate information from the server on the cards on the board,
 the opponent player object, and the players attributes, then displays the information on the screen"""
def update_game():
    global raise_tot, player, opp, erase

    n2 = Network((player, 'opp'))
    board_pos = [(200, 300), (300, 300), (400, 300), (500, 300), (600, 300)]
    pot_pos = (900, 400)

    players = n2.send('opp')
    reset = pygame.Surface((200, 120))
    reset.fill((10, 50, 100))

    while players == False:
        players = n2.send('opp')


    while True:

        game_info = n2.send('opp')

        opp, player, pot, raise_, board = game_info[0], game_info[1], game_info[2], game_info[3], game_info[4]

        """displaying player cards on the screen"""
        try:
            for i in range(2):
                card = f'{player.cards[i].suit}{player.cards[i].number}'
                imgCard = f'/Users/chadgothelf/PycharmProjects/PGame/playing_cards/{card}.png'
                card = pygame.image.load(imgCard)
                card = pygame.transform.scale(card, (100, 150))
                pygame.Surface.blit(screen, card, player.pos['cards'][i])
        except:
            pass

        """Displaying the board on the screen"""
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
        pygame.Surface.blits(screen, blit_sequence= ((reset, player.pos['chips']), (player_chips.text, player.pos['chips'])))

        opp_chips = Text(str(opp.chips))
        pygame.Surface.blits(screen, blit_sequence=((reset, opp.pos['chips']), (opp_chips.text, opp.pos['chips'])))

        pot = Text(str(pot))
        pygame.Surface.blits(screen, blit_sequence=((reset, pot_pos), (pot.text, pot_pos)))


        if opp.show_cards == False:
            pygame.Surface.blits(screen, blit_sequence=((card, opp.pos['cards'][0]), (card, opp.pos['cards'][1])))

        pygame.display.update()
        time.sleep(.5)

"""Side thread resposnible for receiving information from the server in regards to its turn to bet.
 When it recieves information we intiate the betting sequence"""

def thread():
    global player
    pos1, pos2, pos3 = player.pos['bet']
    erase = pygame.Surface((200, 120))
    erase.fill((10, 50, 100))
    n = Network((player, 'main'))

    while True:
        n.receive()
        action = betting()
        pygame.Surface.blits(screen, blit_sequence=((erase, pos1), (erase, pos2), (erase, pos3)))

        n.send(action)


"""Intialzing the screen and connecting to the server"""
#FIXME There should be a better way to organize this data
pygame.init()
raise_ = 0
screen = pygame.display.set_mode((1280, 720))
screen.fill((10, 50, 100))
erase = pygame.Surface((200, 120))
erase.fill((10, 50, 100))
pygame.display.flip()
opp = x = y = None
btn1 = btn2 = btn3 = running = True
n3 = Network((None, 'player'))
player = n3.purpose
opp_thread = threading.Thread(target = update_game, daemon = True)
opp_thread.start()
time.sleep(2)
side_thread = threading.Thread(target = thread, daemon = True)
side_thread.start()
user_text = placeholder = ''


"""Main thread, responsible for tracking keyboard actions and state of the game window"""
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
                    placeholder = user_text
                    user_text = None

                else:
                    user_text += event.unicode
        except:
            pass
pygame.quit()
