import pygame
import random
import math

pygame.init()

ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Batalla Espacial")

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

class Jugador:
    def __init__(self):
        self.ancho = 50
        self.alto = 50
        self.x = ANCHO // 2
        self.y = ALTO - 70
        self.velocidad = 5
        self.vida = 100
        self.disparos = []

    def dibujar(self, superficie):
        pygame.draw.polygon(superficie, BLANCO, [
            (self.x, self.y),
            (self.x - 25, self.y + 50),
            (self.x + 25, self.y + 50)
        ])
        for disparo in self.disparos:
            pygame.draw.rect(superficie, BLANCO, (disparo[0], disparo[1], 3, 10))

    def mover(self, direccion):
        if direccion == "izquierda" and self.x > 30:
            self.x -= self.velocidad
        if direccion == "derecha" and self.x < ANCHO - 30:
            self.x += self.velocidad

    def disparar(self):
        self.disparos.append([self.x, self.y])

    def actualizar_disparos(self):
        for disparo in self.disparos[:]:
            disparo[1] -= 10
            if disparo[1] < 0:
                self.disparos.remove(disparo)

# Clase para los enemigos
class Enemigo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 30
        self.alto = 30
        self.velocidad = 2
        self.direccion = 1

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, ROJO, (self.x, self.y, self.ancho, self.alto))

    def mover(self):
        self.x += self.velocidad * self.direccion
        if self.x <= 0 or self.x >= ANCHO - self.ancho:
            self.direccion *= -1
            self.y += 40

def mostrar_menu():
    menu = True
    while menu:
        pantalla.fill(NEGRO)
        dibujar_texto("BATALLA ESPACIAL", 64, ANCHO//2, ALTO//4)
        dibujar_texto("Presiona ESPACIO para jugar", 32, ANCHO//2, ALTO//2)
        dibujar_texto("Presiona Q para salir", 32, ANCHO//2, ALTO*3//4)
        
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return True
                if evento.key == pygame.K_q:
                    return False

def dibujar_texto(texto, tamaño, x, y):
    fuente = pygame.font.Font(None, tamaño)
    superficie = fuente.render(texto, True, BLANCO)
    rect = superficie.get_rect()
    rect.midtop = (x, y)
    pantalla.blit(superficie, rect)

def juego_principal():
    jugador = Jugador()
    enemigos = [Enemigo(x * 100, 50) for x in range(1, 7)]
    puntuacion = 0
    reloj = pygame.time.Clock()
    jugando = True

    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jugador.disparar()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            jugador.mover("izquierda")
        if teclas[pygame.K_RIGHT]:
            jugador.mover("derecha")

        jugador.actualizar_disparos()
        for enemigo in enemigos[:]:
            enemigo.mover()
            for disparo in jugador.disparos[:]:
                if (disparo[0] > enemigo.x and disparo[0] < enemigo.x + enemigo.ancho and
                    disparo[1] > enemigo.y and disparo[1] < enemigo.y + enemigo.alto):
                    jugador.disparos.remove(disparo)
                    enemigos.remove(enemigo)
                    puntuacion += 100
                    break

            if enemigo.y + enemigo.alto > ALTO - 100:
                return False
        pantalla.fill(NEGRO)
        jugador.dibujar(pantalla)
        for enemigo in enemigos:
            enemigo.dibujar(pantalla)
        dibujar_texto(f"Puntuación: {puntuacion}", 32, ANCHO//2, 10)
        
        pygame.display.flip()
        reloj.tick(60)

        if len(enemigos) == 0:
            return True

def main():
    jugando = True
    while jugando:
        jugando = mostrar_menu()
        if jugando:
            resultado = juego_principal()
            if resultado:
                pantalla.fill(NEGRO)
                dibujar_texto("¡VICTORIA!", 64, ANCHO//2, ALTO//2)
                pygame.display.flip()
                pygame.time.wait(2000)
            else:
                pantalla.fill(NEGRO)
                dibujar_texto("GAME OVER", 64, ANCHO//2, ALTO//2)
                pygame.display.flip()
                pygame.time.wait(2000)

    pygame.quit()

if __name__ == "__main__":
    main()