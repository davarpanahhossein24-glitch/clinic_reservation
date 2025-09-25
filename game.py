from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# ایجاد زمین
ground = Entity(model='plane', scale=(100, 1, 100), texture='grass', collider='box')

# ایجاد آسمان آبی
Sky(color=color.azure)

# ایجاد بازیکن
player = FirstPersonController()
player.speed = 5
player.gravity = 0.5
player.health = 100

# ایجاد درختان
for i in range(20):
    Entity(model='cube', color=color.green, scale=(1, 3, 1),
           position=(random.randint(-45, 45), 1.5, random.randint(-45, 45))))

    # ایجاد دشمنان
    enemies = []
    for i in range(5):
        enemy = Entity(model='cube', color=color.red, scale=2,
                       position=(random.randint(-40, 40), 1, random.randint(-40, 40)), collider='box')
    enemy.health = 50
    enemies.append(enemy)

    # تیراندازی
    bullets = []


def shoot():
    bullet = Entity(model='sphere', color=color.yellow, scale=0.2, position=player.position + Vec3(0, 1.5, 0))
    bullet.direction = player.forward
    bullets.append(bullet)


def update():
    # حرکت گلوله‌ها
    for bullet in bullets:
        bullet.position += bullet.direction * 20 * time.dt
        # برخورد با دشمن
        for enemy in enemies:
            if bullet.intersects(enemy).hit:
                enemy.health -= 25
                bullets.remove(bullet)
                destroy(bullet)
                if enemy.health <= 0:
                    destroy(enemy)
                    enemies.remove(enemy)

    # برخورد دشمن با بازیکن
    for enemy in enemies:
        if player.intersects(enemy).hit:
            player.health -= 10 * time.dt
            if player.health <= 0:
                print("شما مردید!")
                application.quit()


# کلید تیراندازی
def input(key):
    if key == 'left mouse down':
        shoot()


app.run()
