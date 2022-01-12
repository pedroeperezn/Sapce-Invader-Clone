import pygame
import random
import math
from pygame import mixer
#Initialize pygame librarie, if not it will not work
pygame.init()
#Create first screen
screen = pygame.display.set_mode((800,600))

#At this point, the window is created but immediately closed. We need to create a quit event so we can maintain it open until the quit event is called
running = True
#para poder mantener abierta la ventana el tiempo que queremos, necesitamos pedir que la ventana permanezca abierta siempre que no se precione
#el boton quit
#la variable "running" va a ser la que se va a encargar de esto

#Title and icon change. First we change the caption, then we load the icon as the "icon" variable, and finally we set it as the icon of the window
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
bgimg = pygame.image.load("bg_img.png")

#Music
mixer.music.load("space_music.wav")
mixer.music.play(-1)

#Add player

#Player
playerImg = pygame.image.load("play_craft.png")
playerX = 370
playerY = 480
playerX_change = 0
#load player image and tell that starter position should be the center of the display

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

#Para tener multiples enemigos, debemos enlistarlos a todos, ya que si no el programa no sabra a que enemigo me estoy refiriendo cuando ocurre cualquier
#evento. Comienzo declarando todo lo que era una variable fija ahora como listas

for i in range(num_of_enemies):


    enemyImg.append(pygame.image.load("enemy1.png"))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2)
    enemyY_change.append(40)

#aqui digo que para cada lista, en el rango de enemigos que elegi, agregue un elemento (imagen, posicion en X, en Y y su movimiento)

#Laser
laserImg = pygame.image.load("laser.png")
laserX = 0
laserY = 480
#Es restando la altura de la nave por que debe salir de su punta
laserX_change = 0
laserY_change = -10
laser_state = "ready"
#Ready state means you cant se laser
#Fire - The laser is moving
#state make us know when it is moving

#SCORE

score_value = 0
font = pygame.font.Font("ARCADE_N.TTF",32)

textX = 10
textY = 10

def showScore(x,y):

    global score
    score = font.render("Score:" + str(score_value),True,(255,255,255))
    
    screen.blit(score,(x,y))

def player(x,y):

    screen.blit(playerImg, (x,y))

#blit is a draw method, you tell which image and where you want it to be draw to
#We defined a function just for drawing the player in the medium

#ENEMIGOS MULTIPLES

#Inicialmente, la funcion enemy solo necesitaba los valores de X y Y para dibujar al enemigo, ahora necesita tambien conocer de que enemigo
#estamos hablando cuando llamemos la funcion en el for loop (eso se logra a traves de enviarle la variable "i" dentro del ciclo)

def enemy(x,y,i):

    screen.blit(enemyImg[i], (x,y))

#todo lo que ocurre en el juego debe estar dentro del loop, que es lo que pasa siempre y cuando el juego siga activo

def laser_shoot(x,y):

    global laser_state
    laser_state = "fire"
    screen.blit(laserImg,(x+16,y + 16))
#that sums are to make sure the laser appears to be shot from the top of the spaceship
#esta funcion solamente setea el estado del laser a "fire" y dibuja el laser arriba de la nave. El movimiento va despues

def isCollision(enemyX,enemyY,laserX,laserY):

    distance = math.sqrt((math.pow(enemyX-laserX,2)) + (math.pow(enemyY-laserY,2)))
    if distance < 27:
        return True
    else:
        return False

#La función de isCollision lo unico que hace es revisar si el laser esta a una distancia de colision con el enemigo
#para esto calculamos la distancia (formula de distancia entre dos coordenadas) y, si está a menos de ciertos pixeles, entonces la colision es cierta

#Game over function

def game_over_text():

    GOT = font.render("GAME OVER",True,(255,255,255))
    screen.blit(GOT,(200,250))
    screen.blit(score,(200,300))


while running:
    for event in pygame.event.get():
#en este ciclo, escaneo todos los eventos que estan ocurriendo en la ventana
        if event.type == pygame.QUIT:
#aqui digo que, si el boton de quit es accionado, entonces running será false y se cerrara el juego
            running = False

        if event.type == pygame.KEYDOWN:

#Para programar el movimiento de la nave, primero debemos verificar si se presiono una tecla

            if event.key == pygame.K_LEFT:
                print("Left arrow is pressed")
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
                print("Right arrow is pressed")

            if event.key == pygame.K_SPACE:

                if laser_state == "ready":
                    laser_shoot(playerX,laserY)
                    laserX = playerX
                    laser_sound = mixer.Sound("shoot.wav")
                    laser_sound.play()

        

#Aqui en esta seccion del codigo es donde estare poniendo los eventos en teclado que desencadenan la accion.
#como vimos antes, el primer for que anida a los ifs esta buscando eventos. despues otro if pregunta si se presiono una tecla
#y por ultimo pregunto que, si fue espacio, entonces dispare el laser

#debemos agregar una condicion al disparo para que solamente podamos disparar una vez que se desaparecio el laser anterior, lo cual significa que
#solamente podemos disparar cuando el estado del laser sea "ready", no se puede disparar mientras este en "fire". Igual debemos setear la posicion 
#en X del laser para que no se mueva junto con el jugador, sino que siga su trayectoria en un valor en X y solamente variando en Y

#una ves que sabemos si se presiono una tecla, debemos saber si fue la tecla que queremos utilizar
#en este caso, si las flechas derecha o izquierda se accionan, entonces la variable que dicta el cambio de posicion va a cambiar
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print("Key unpressed")
                playerX_change = 0

#aqui indicamos que si la tecla es soltada, entonces no habra movimiento

#para programar el cambio de posicion del asset, es muy similar que el quit button.

            

    screen.fill((0,0,0))
    screen.blit(bgimg,(0,0))

#set bg color on the screen displayed

    playerX += playerX_change
#añadimos a la posicion de la nave la variable de cambio (que se modifica presionando las teclas derecha o izquierda)

    if playerX <= 0:
        playerX = 0

    elif playerX >= 736:
        playerX = 736

#estas condiciones son para poner una frontera. la nave no puede pasar de la medida de la pantalla. 769 es por que debemos considerar el tamaño
#de la nave (64 px). Lo que ocurre es que no permite que la nave pueda ser dibujada fuera de ese rango, siempre se va a trabar ahi

    
#MOVIMIENTO Y COLISIONES DE ENEMIGOS MULTIPLES

#Despues de que lo declare como lista, debo indicar como se va a mover cada uno de los elementos de la lista (o sea, los enemigos)
#aqui simplemente estoy tomando el codigo que ya teniamos de su movimiento y lo estoy ahora anidando en un for loop para el rango de enemigos
#que tengo

    for i in range(num_of_enemies):

        #Game Over

        if enemyY[i] > 450:

            for j in range(num_of_enemies):

                enemyY[j] = 2000

            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

    #Collision

#Igualmente, el comportamiento de la colision debe ser asignado para cada uno de los enemigos presentes, asi no importa que enemigo sea, va a respawnear

        collision = isCollision(enemyX[i],enemyY[i],laserX,laserY)

        if collision:

            laserY = 480
            laser_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
            exp_sound = mixer.Sound("explosion.wav")
            exp_sound.play()

        enemy(enemyX[i],enemyY[i],i)

#Si el estado del laser es fire (o sea, se presiono espacio y se desencadeno la funcion de disparar)

    if laser_state is "fire":

        laser_shoot(laserX,laserY)
        laserY += laserY_change

    if laserY <= 0:
        laserY = 480
        laser_state = "ready"

#ahora si, dicto el movimiento que debe seguir mi laser. Hay que poner una condicion extra para que podamos disparar de nuevo en cuanto el
#laser desaparezca, para esto debemos resetear la posicion en Y y volver a poner el estado en ready



#despues de haber definido la función de colisión, ahora revisamos si ocurre una. si si ocurre, voy a resetear la posicion de mi laser 
#y su estado de nuevo a ready para que podamos disparar de nuevo
#posteriormente, añadimos una variable de score para que cada que le demos un disparo a un enemigo, se nos agregue un punto
#finalmente, hacemos que el enemigo vuelva a aparecer en un punto de origen para dar la ilusion de que fue derribado 

    player(playerX,playerY)
    showScore(textX,textY)
    
#we call the function that draws the player in the middle (AFTER THE BG COLOR)
    pygame.display.update()
#pygame.display.update() SIEMPRE debe ser escrito al final de todo codigo. Eso es para actualizar la pantalla y que se realicen cambios







