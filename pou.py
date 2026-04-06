import pygame
from sys import exit
from random import randint
from pygame import mixer

# --- FUNKCJA ---
def draw_score(w, w_z):
    score = my_font.render(str(w), False, (166,3,4))
    score_surface = score.get_rect(midbottom=(WIDTH/2, 160))
    screen.blit(score, score_surface)
    cyfra = 0

    if w_z >= 1 and w_z < 6:
        cyfra = 1
        zegar = my_font.render(str(cyfra), False, (166,3,4))
        wynik_rect = zegar.get_rect(midbottom=(WIDTH/2, 60))
        screen.blit(zegar, wynik_rect)

    if w_z >= 2 and w_z < 6:
        cyfra = 2
        zegar_dwa = my_font.render(str(cyfra), False, (166,3,4))
        zegar_dwa_rect = zegar_dwa.get_rect(midbottom=(240, 142))
        screen.blit(zegar_dwa, zegar_dwa_rect)

    if w_z >= 3 and w_z < 6:
        cyfra = 3
        zegar_dwa = my_font.render(str(cyfra), False, (166,3,4))
        zegar_dwa_rect = zegar_dwa.get_rect(midbottom=(203, 255))
        screen.blit(zegar_dwa, zegar_dwa_rect)

    if w_z >= 4 and w_z < 6:
        cyfra = 4
        zegar_dwa = my_font.render(str(cyfra), False, (166,3,4))
        zegar_dwa_rect = zegar_dwa.get_rect(midbottom=(94, 255))
        screen.blit(zegar_dwa, zegar_dwa_rect)

    if w_z == 5 and w_z < 6:
        cyfra = 5
        zegar_dwa = my_font.render(str(cyfra), False, (166,3,4))
        zegar_dwa_rect = zegar_dwa.get_rect(midbottom=(60, 142))
        screen.blit(zegar_dwa, zegar_dwa_rect)        



# --- INIT ---
pygame.init()
mixer.init()

szczekanie = [
    pygame.mixer.Sound('dzwieki/nia1.wav'),
    pygame.mixer.Sound('dzwieki/nia2.wav'),
    pygame.mixer.Sound('dzwieki/rawr1.wav'),
    pygame.mixer.Sound('dzwieki/rawr2.wav'),
    pygame.mixer.Sound('dzwieki/Dunkelheit.mp3')
]

szczekanie[4].set_volume(0.1)
for i in szczekanie[:4]:
    i.set_volume(2)

WIDTH, HEIGHT = 300, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('moshpit pou')
clock = pygame.time.Clock()
my_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# --- ZMIENNE ---
sciana = pygame.image.load('zdjencia/sciana/sciana.jpg').convert_alpha()
podloga = pygame.image.load('zdjencia/sciana/podloga.png').convert_alpha()
twarze = [
    pygame.image.load('zdjencia/pou/image.png').convert_alpha(),
    pygame.image.load('zdjencia/pou/pou_krzyk.png').convert_alpha()
]
itemki = [
    pygame.image.load('zdjencia/itemki/wino.png').convert_alpha(),
    pygame.image.load('zdjencia/itemki/piwo.png').convert_alpha(),
    pygame.image.load('zdjencia/itemki/glany.png').convert_alpha()
]

play_again_button = my_font.render('Play again', False, (0,0,0))
play_again_button_rect = play_again_button.get_rect(midbottom=(WIDTH/2,HEIGHT/2))
aktywne_itemki = []
play_button = my_font.render('play', False, (0,0,0))
play_button_rect = play_button.get_rect(midbottom=(WIDTH/2,HEIGHT/2))

pou = pygame.image.load('zdjencia/pou/imagee.png').convert_alpha()
pou_rect = pou.get_rect(midtop=(80,500)).inflate(-94, -114)

pou_speed = 5
a_pressed = False
d_pressed = False
c_pressed = False
player_surface = twarze[0]

rawr = 1000
action = False
action_time = 0

itemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(itemy_timer, 1200)

wynik = 0
wynik_zegar = 0

base_speed = 3
current_speed = 0
game_aktive = False


play_again_TF = 0

# --- PĘTLA GŁÓWNA ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # Sterowanie myszką w menu
        if not game_aktive and event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                game_aktive = True
                play_again_TF += 1
                wynik = 0
                wynik_zegar = 0
                
                # Opcjonalnie: tu możesz wyzerować wynik przy restarcie
        
        # Sterowanie klawiszami (tylko w grze)
        if game_aktive:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d: d_pressed = True
                elif event.key == pygame.K_a: a_pressed = True
                elif event.key == pygame.K_c:
                    szczekanie[randint(0,3)].play()
                    c_pressed = True
                    action = True
                    action_time = pygame.time.get_ticks()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d: d_pressed = False
                elif event.key == pygame.K_a: a_pressed = False
            
            # Timer itemków (tylko w grze)
            if event.type == itemy_timer:
                losowy_index = randint(0, len(itemki)-1)
                dany_item = itemki[losowy_index]
                x_pos = randint(20, WIDTH-20)
                new_rect = dany_item.get_rect(midbottom=(x_pos,-10))
                aktywne_itemki.append({'obrazek':dany_item,'rect':new_rect, 'typ':losowy_index})

    if game_aktive:
        # LOGIKA GRY
        if c_pressed: player_surface = twarze[1]
        else: player_surface = twarze[0]

        if a_pressed: pou_rect.x -= pou_speed
        if d_pressed: pou_rect.x += pou_speed

        if pou_rect.right >= WIDTH: pou_rect.right = WIDTH
        if pou_rect.left <= 0: pou_rect.left = 0
        if pou_rect.bottom >= 500: pou_rect.bottom = 500

        if action:
            current_time = pygame.time.get_ticks()
            if current_time - action_time >= rawr:
                action = False
                c_pressed = False

        if wynik_zegar == 6:
            wynik_zegar = 0

        current_speed = base_speed + (wynik//5)

        # RYSOWANIE GRY
        screen.blit(sciana, (-99,-140))
        screen.blit(podloga,(0, 500))
        screen.blit(player_surface, pou_rect)
        draw_score(wynik, wynik_zegar)  

        for item in aktywne_itemki[:]:
            item['rect'].y += current_speed
            screen.blit(item['obrazek'],item['rect'])

            if pou_rect.colliderect(item['rect']):
                if item['typ'] != 2:
                    aktywne_itemki.remove(item)
                    wynik += 1
                    wynik_zegar += 1
                if item['typ'] == 2:
                    game_aktive = False
                    
            elif item['rect'].top > HEIGHT:
                aktywne_itemki.remove(item)
                if item['typ'] != 2:
                    wynik -= 1  
                    wynik_zegar -= 1
            if game_aktive == False:
                aktywne_itemki.remove(item)
                    
    else:
        # MENU

        screen.fill((166,3,4))
        if play_again_TF:
            screen.blit(play_again_button,play_again_button_rect)
        else:
            screen.blit(play_button, play_button_rect)
        
        
        if wynik:
            wynik_font = my_font.render(f'Twoj wynik: {wynik}', False, (0,0,0))
            wynik_font_rect = wynik_font.get_rect(midbottom=(WIDTH/2,(HEIGHT/2)+50))
            screen.blit(wynik_font,wynik_font_rect)
            

        

    pygame.display.update()
    clock.tick(60)