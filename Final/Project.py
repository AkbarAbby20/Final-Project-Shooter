import pygame
from random import randint, uniform
pygame.init()

#display
tinggi_layar = 900
lebar_layar = 1600
judul = "Space Shooter"

scene = pygame.display.set_mode((lebar_layar, tinggi_layar))
pygame.display.set_caption(judul)

#variabel utama
online = True
game_aktif = True
batas_kanan = 1200
batas_kiri = 400
#aset gambar
galaxy = "galaxy.jpg"

img_asteroid = pygame.image.load("asteroid.png")
img_bullet   = pygame.image.load("bullet.png")
img_roket    = pygame.image.load("rocket.png")
img_ufo      = pygame.image.load("ufo.png")

#aset suara
##musik
bg_music = "space.ogg"

##sfx
tembak = "fire.ogg"

#font tulisan
pygame.font.init()
font_utama = pygame.font.SysFont('Impact', 50)

#musik
pygame.mixer.init()
pygame.mixer.music.load(bg_music)
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()


# class 
class objek(pygame.sprite.Sprite):
    def __init__(self, gambar, x, y, lebar, tinggi):
        super().__init__()
        self.lebar = lebar
        self.tinggi = tinggi
        self.gambar = gambar
        #rect
        self.image = pygame.transform.scale(self.gambar,(self.lebar, self.tinggi))
        self.original = self.image
        self.rect = self.image.get_rect()
        ##posisi
        self.pos = pygame.math.Vector2(x,y) ##posisi akurat
        self.rect.center = self.pos
        
    def show(self):
        scene.blit(self.image, self.rect.topleft)

class player(objek):
    def __init__(self,gambar, x ,y, lebar, tinggi, kecepatan):
        super().__init__(gambar, x, y, lebar, tinggi)
        self.kecepatan = kecepatan

    def movement2(self, batas_kiri, batas_kanan):
        tombol =  pygame.key.get_pressed()
        if tombol[pygame.K_a] and self.pos.x > batas_kiri + self.lebar / 2:
            self.pos.x -= self.kecepatan
        if tombol[pygame.K_d] and self.pos.x < batas_kanan - self.lebar / 2:
        
            self.pos.x += self.kecepatan
        self.rect.center = self.pos

    def tembak(self):
        peluru = bullet(img_bullet, self.pos.x,self.pos.y, 50 ,50, 5, mode = 2)
        group_peluru_player.add(peluru)

class rintangan(objek):
    def __init__(self, gambar, x, y, lebar, tinggi, kecepatan, id):
        super().__init__(gambar, x, y, lebar, tinggi)
        self.kecepatan = kecepatan
        self.id = id
        self.rect.center = self.pos
        self.orientasi = randint(1, 360)
        self.vel = pygame.math.Vector2(1,1)
        self.rand = randint(1,2)
        self.rand2 = randint(1,2)
        if self.rand == 1:
            self.vel.x *= -1

    def update(self):
        if self.rand == 1 and self.rand2 == 1:
            self.orientasi -= 0.2
        elif self.rand == 2 and self.rand2 == 1:
            self.orientasi += 0.2
        self.image = pygame.transform.rotate(self.original, self.orientasi)
        acuan = self.pos
        self.rect = self.image.get_rect(center=acuan)
        if self.id % 2 == 0:
            self.pos.y += self.vel.y * self.kecepatan / 2
            step = self.pos.x + self.vel.x * self.kecepatan
            if self.pos.x > batas_kanan - self.lebar / 2:
                self.vel.x *= -1
                step = self.pos.x + self.vel.x * self.kecepatan
            if self.pos.x < batas_kiri + self.lebar / 2:
                self.vel.x *= -1
                step = self.pos.x + self.vel.x * self.kecepatan
            self.pos.x = step

        else:
            self.pos.y += self.vel.y * self.kecepatan
        
        if self.pos.y > 1000:
            self.kill()
        #membuat rect sama dengan posisi gambar
        self.rect.center = self.pos

class musuh(objek):
    def __init__(self, gambar, x, y, lebar, tinggi, kecepatan):
        super().__init__(gambar, x, y, lebar, tinggi)
        self.kecepatan = kecepatan
        self.rect.center = self.pos
        self.vel = pygame.math.Vector2(1,1)
        self.last_shot = pygame.time.get_ticks()
        self.interval = 2000

    def update(self, mode):
        global skor
        ## MODE 1 UNTUK PERGERAKAN UMUM KE BAWAH SEMENTARA LAINNYA spesial
        if mode == 1:
            self.pos.y += self.vel.y * self.kecepatan
            self.rect.center = self.pos
        elif mode == 2 and self.pos.y < 150:
            self.pos.y += self.vel.y * self.kecepatan
            self.rect.center = self.pos

        if self.pos.y > 100:
            self.logika_tembak()

        if self.pos.y > 1000:
            self.kill()
            skor -= 100

    def logika_tembak(self):
        kesempatan = randint(1,600)
        waktu_sekarang = pygame.time.get_ticks()
        if waktu_sekarang - self.last_shot > self.interval and kesempatan == 1:
            self.tembak()
            self.last_shot = waktu_sekarang

    def tembak(self):
        peluru = bullet(img_bullet, self.pos.x, self.pos.y, 50, 50, 5, mode = 1)
        group_peluru_musuh.add(peluru)

class bullet(objek):
    def __init__(self, gambar, x, y, lebar, tinggi, kecepatan, mode = None):
        super().__init__(gambar, x,y ,lebar, tinggi)
        self.kecepatan = kecepatan
        self.vel = pygame.math.Vector2(1,1)
        self.mode = mode ## 1 untuk mush dan apa saaj untuk player

        if self.mode == 1:
            self.orientasi = 180
            self.image = pygame.transform.rotate(self.original, self.orientasi)

    def update(self):
        #MODE ANTARA 1 DAN 2 SAJA
        ##mode 1 tembakan musuh
        if self.mode == 1:
            self.pos.y += self.vel.y * self.kecepatan
            if self.pos.y > 1000:
                self.kill()
        ## tembakan player
        else:
            self.pos.y -= self.vel.y * self.kecepatan
            if self.pos.y < -100:
                self.kill()
        
        self.rect.center = self.pos

##main 
bg = pygame.transform.scale(pygame.image.load(galaxy),(lebar_layar, tinggi_layar))
menang = font_utama.render("Kamu menang", True, (255,255,255))
kalah  = font_utama.render("Kamu kalah", True, (255,255,255))
##ui 
skor = 0
nyawa = 3
##pinggiran
tembok_kiri = pygame.Surface((400, 900))
tembok_kanan = pygame.Surface((400, 900))

##player
p1 = player(img_roket, 800, 850, 100, 100, 10)

##musuh
group_musuh_biasa = pygame.sprite.Group()
group_musuh_baris = pygame.sprite.Group()
group_rintangan  =pygame.sprite.Group()
group_peluru_musuh = pygame.sprite.Group()
group_peluru_player = pygame.sprite.Group()


#musuh baris
for i in range(4):
    enemy = musuh(img_ufo, 200 * i + 500 , -150, 150, 100, 1)
    group_musuh_baris.add(enemy)

tipe_musuh = 1


fps = pygame.time.Clock()
awal1 = pygame.time.get_ticks()
awal2 = pygame.time.get_ticks()
awal3 = pygame.time.get_ticks()

while online:
    scene.blit(bg, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            online = False
        
        if event.type == pygame.KEYDOWN:
            tombol = pygame.key.get_pressed()
            sedetik = pygame.time.get_ticks()
            if tombol[pygame.K_SPACE] and sedetik - awal2 > 200:
                p1.tembak()
                awal2 = sedetik  
        
    if nyawa < 1:
        game_aktif = False
        scene.blit(kalah, (600, 400))
        
    if skor > 3000:
        game_aktif = False
        scene.blit(menang, (600,400))
    if game_aktif:

        if pygame.sprite.spritecollide(p1,group_musuh_biasa, True) or pygame.sprite.spritecollide(p1, group_rintangan, True):
            nyawa -= 1
        elif pygame.sprite.spritecollide(p1, group_peluru_musuh, True):
            nyawa -= 1
        tabrak1 = pygame.sprite.groupcollide(group_peluru_player, group_musuh_biasa, True,True)
        tabrak2 = pygame.sprite.groupcollide(group_peluru_player, group_musuh_baris, True,True)
        tabrak3 = pygame.sprite.groupcollide(group_peluru_player, group_rintangan, True,True)

        for i in tabrak1:
            skor += 200
        
        for i in tabrak2:
            skor += 300

        scene.blit(tembok_kiri,(0,0))
        scene.blit(tembok_kanan,(1200, 0))
        #ui
        teks_skor  = font_utama.render("Skor: " +str(skor), True, (255,0,0))
        teks_nyawa = font_utama.render("Nyawa: " +str(nyawa), True, (255,0,0))
        scene.blit(teks_skor,(0,0))
        scene.blit(teks_nyawa,(0,100))
        p1.show()
        p1.movement2(batas_kiri, batas_kanan)

        if len(group_rintangan) < 10:
            ukuran = randint(50, 150)
            penghalang = rintangan(img_asteroid, randint(500, 1100), randint(-200, -50), ukuran, ukuran, randint(1,2), randint(1,2))
            group_rintangan.add(penghalang)


        detik_10 = pygame.time.get_ticks()
        if detik_10 - awal1 > 10000:
            awal1 = detik_10

            tipe_musuh += 1
            if tipe_musuh > 2:
                if len(group_musuh_baris) == 0:
                    tipe_musuh = 1
                else:
                    tipe_musuh = 2

        group_peluru_player.update()
        group_peluru_musuh.update()
        group_rintangan.update()

        group_peluru_player.draw(scene)
        group_peluru_musuh.draw(scene)
        group_rintangan.draw(scene)

        if tipe_musuh == 2:
            group_musuh_biasa.update(1)
            group_musuh_baris.update(2) 
            group_musuh_baris.draw(scene)
            group_musuh_biasa.draw(scene)

        else:
            if len(group_musuh_biasa) < 4:
                ukuran = randint(50, 150)
                enemy = musuh(img_ufo, randint(500,1100), randint(-200, -50), ukuran, ukuran / 1.5, randint(1,3))
                group_musuh_biasa.add(enemy)
            group_musuh_biasa.update(1)
            group_musuh_biasa.draw(scene)


    fps.tick(60)
    pygame.display.update()