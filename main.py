
#Import modul yang dibutuhkan
try:
    import time, random, sys, os, math
except ImportError:
    print("Pastikan Anda memiliki modul waktu")
    sys.exit()
try:
    import pygame
except ImportError:
    print("Pastikan Anda memiliki python 3 dan pygame.")
    sys.exit()
try:
    import MainMenu
except ImportError:
    print("Pastikan Anda memiliki semua file tambahan")
from pygame import freetype

    
# Inisialisasi awal terdiri dari ruang game/tempat dan inisialisasi musik game
pygame.init()
pygame.mixer.init()


DisplayWidth,DisplayHeight = 1000, 800
clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((DisplayWidth,DisplayHeight))
pygame.display.set_caption("Fruit Ninja kelompok 4")


#Menambahkan modul musik dan lokasi foldernya
slice_sound = pygame.mixer.Sound("sounds_FruitSlice.wav")
explosion_sound = pygame.mixer.Sound("sound bomb.mp3")
backsoudgame = pygame.mixer.Sound("backsound_play_game.mp3")


#fungsi memuat gambar
def load_images(path_to_directory):
    images = {}
    for dirpath, dirnames, filenames in os.walk(path_to_directory):
        for name in filenames:
            if name.endswith('.png'):
                key = name[:-4]
                if key != "background":
                    img = pygame.image.load(os.path.join(dirpath, name)).convert_alpha()
                else:
                    img = pygame.image.load(os.path.join(dirpath, name)).convert()
                images[key] = img
    return images


#Menghitung dan menggambar segala sesuatu untuk buah-buahan
class Fruit():
    def __init__(self, Image, x=None, y=None, Vx=None, gravity=None, width=200,height=200):
        """Mendeklarasikan semua Variabel awal."""
        self.Image = Image
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.Vx = Vx
        self.gravity = gravity
        if x == None:
            self.x = 500
        if y == None:
            self.y = 800
        if Vx == None:
            self.Vx = random.randint(-20,20)
        if gravity == None:
            self.gravity = random.randint(-22,-20)
        self.image = pygame.Surface([self.width,self.height])
        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.bottom = self.y + self.height
        self.rect.left = self.x
        self.rect.right = self.x + self.width
        self.angle = random.randint(0,355)
        self.split = False
 

    def draw(self):
        """Menggambar Buah."""
        gameDisplay.blit(pygame.transform.rotate(pygame.transform.scale(self.Image,(self.width,self.height)),self.angle).convert_alpha(),(self.x,self.y))

    def Physics(self):
        """Menghitung fisika dan sudut setiap buah."""
        self.x += self.Vx
        self.y += self.gravity
        self.gravity += 0.35
        if self.Vx > 0:
            self.Vx -= 0.25
        if self.Vx < 0:
            self.Vx += 0.25
        if self.x + self.width >= 1000 or self.x <= 0:
            self.Vx *= -1

        #Update arah buah
        self.angle += 1
        self.angle %= 360

    def update(self):
        """Memanggil setiap fungsi untuk memperbarui setiap buah."""
        self.draw()
        self.Physics()
        #Memperbarui hitbox
        self.rect.top = self.y
        self.rect.bottom = self.y + self.height
        self.rect.left = self.x
        self.rect.right = self.x + self.width

class Player():
    def __init__(self):
        """mendeklarasikan kelompok variable"""
        pos = pygame.mouse.get_pos()
        self.x = pos[0]
        self.y = pos[1]
        self.width = 5
        self.height = 5
        self.image = pygame.Surface([self.width,self.height])
        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.bottom = self.y + self.height
        self.rect.left = self.x
        self.rect.right = self.x + self.width
        self.drag = False
        self.Past = []

    def draw(self, Colors):
        """gambar garis slash pemotong buah"""
        pygame.draw.rect(gameDisplay,(0,255,0),(self.x,self.y,self.width,self.height),0)
        
        for i in range(len(self.Past)-2):
            self.Past[i][1] -= 1
            if self.Past[i][1] >= 1:
                pygame.draw.line(gameDisplay, Colors[1],(self.Past[i][0]),(self.Past[i+1][0]),self.Past[i][1]+10)
                pygame.draw.line(gameDisplay, Colors[0],(self.Past[i][0]),(self.Past[i+1][0]),self.Past[i][1])
        

    def update(self, Colors):
        """Memanggil setiap fungsi untuk memperbarui"""
        self.draw(Colors)
        #update garis
        pos = pygame.mouse.get_pos()
        change = pygame.mouse.get_rel()
        self.Past.insert(0, [pos, (change[1]+10) % 30, (abs(change[0])*3) % 100])
        if len(self.Past) >= 21:
            self.Past.pop(20)
        #update kotak hit
        self.x = pos[0]
        self.y = pos[1]
        self.rect.top = self.y
        self.rect.bottom = self.y + self.height
        self.rect.left = self.x
        self.rect.right = self.x + self.width

class Explosion():
    """Kelas yang membuat ledakan setiap kali memotong bomb"""
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.Life = 20

    def draw(self, Images):
        gameDisplay.blit(pygame.transform.scale(Images["Explosions"],(150,150)),(self.x,self.y))

    def update(self, Images):
        self.draw(Images)
        self.x += random.randint(-5,5)
        self.y += random.randint(-5,5)
        self.Life -= 1


#BAGIAN GAME OVER
def GameOverScreen(score):
    Images = load_images("Images")#fungsi untuk mengakses gambar di folder "images"
    game_over = True
    game_over_logo = pygame.image.load("game-over.png").convert_alpha()
    game_over_sound = pygame.mixer.Sound("game_over_sound.mp3")
    game_over_sound_played = False
    font_path = "gang-of-three.ttf"  # Ganti dengan nama file font yang sesuai
    font_size = 30
    font_50 = 70
    font = pygame.font.Font(font_path, font_size)
    font1 = pygame.font.Font(font_path, font_50)


    while game_over:
        gameDisplay.fill((0, 0, 0))  # Ganti warna latar belakang sesuai kebutuhan
        gameDisplay.blit(pygame.transform.scale(Images["background"],(DisplayWidth,DisplayHeight)),(0,0))

        # Tampilkan skor akhir
        # font = pygame.font.SysFont(None, 75)
        text = font1.render("Score: {}".format(score), True, (255, 255, 255))
        gameDisplay.blit(text, ((DisplayWidth - text.get_width()) // 2, (DisplayHeight - text.get_height()) // 2))
        gameDisplay.blit(game_over_logo, ((DisplayWidth - game_over_logo.get_width()) // 2, 275))
        
        # Tampilkan opsi untuk mengulang permainan atau kembali ke layar utama
        # font = pygame.font.SysFont(None, 30)
        retry_text = font.render("Press 'R' to try again", True, (255, 255, 255))
        main_menu_text = font.render("Press 'M' for back to Main Menu", True, (255, 255, 255))
        gameDisplay.blit(retry_text, ((DisplayWidth - retry_text.get_width()) // 2, (DisplayHeight // 2) + 50))
        gameDisplay.blit(main_menu_text, ((DisplayWidth - main_menu_text.get_width()) // 2, (DisplayHeight // 2) + 100))

        pygame.display.flip()

        # memainkan sound game over 1x
        if not game_over_sound_played:
           game_over_sound.play()
           game_over_sound_played = True


        # pilihan untuk try again atau back to menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Memulai ulang permainan
                    game_over_sound.stop()
                    game_over = False
                    game_loop()
                elif event.key == pygame.K_m:
                    # Kembali ke layar utama
                    game_over_sound.stop()
                    game_over = False
                    MainMenu.HomeScreen()
                    

        clock.tick(60)


def game_loop(Colors=[(0,255,0),(0,150,0)]):
    backsoudgame.play(-1)
    game_run = True
    Images = load_images("Images")#fungsi untuk mengakses gambar di folder "images"
    Choices = ["Grapes", "Orange", "Apple","Lemon", "Strawberry"]
    player = Player()
    Fruits = []
    Lives = 3
    score = 0


    for i in range(random.randint(2,5)):
        choice = random.choice(Choices)
        if choice == "Strawberry": 
            Fruits.append(Fruit(Images[choice],500,800,random.randint(-20,20),random.randint(-22,-20),125,125))
        else:
            Fruits.append(Fruit(Images[choice]))
    if random.randint(1,4) <= 3:
        Bombs = [Fruit(Images["Bomb"], 500,1000,random.randint(-30,30),-25,100,100)]
    else:
        Bombs = []
    # SplitFruit = []
    Explosions = []

    #LOOP GAME
    while game_run == True:
        gameDisplay.fill((210,140,42))
        gameDisplay.blit(pygame.transform.scale(Images["background"],(DisplayWidth,DisplayHeight)),(0,0))
        font = pygame.font.Font("gang-of-three.ttf", 50) 
        score_text = font.render("Score: {}".format(score), True, (255, 255, 255))
        text_rect = score_text.get_rect(center=(DisplayWidth // 2, 30))  # Menyesuaikan posisi skor di tengah atas
        gameDisplay.blit(score_text, text_rect)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.drag = True
            if event.type == pygame.MOUSEBUTTONUP:
                player.Past = []
                player.drag = False

        #menampilkan gambar nyawa di kiri atas 
        if Lives > 0:
            for i in range(Lives):
                pygame.draw.rect(gameDisplay,(250,0,0),(25+(i*55),10,50,50),0)
                pygame.draw.rect(gameDisplay,(150,0,0),(25+(i*55),10,50,50),5)
        else:
            backsoudgame.stop()# backsound musik berhenti
            GameOverScreen(score)
            

        #fungsi menampilkan gambar semua buah dan kedua potongan buah
        stop = False
        for fruit in Fruits:
            fruit.update()
            if fruit.y <= 800:
                stop = True
            if pygame.sprite.collide_rect(player, fruit) == True and player.drag and not fruit.split:
                fruit.split = True
                if fruit.Image == Images["Grapes"]:
                    fruit.Image = Images["GrapeTop"]
                    Fruits.append(Fruit(Images["GrapeBottom"],fruit.x,fruit.y,fruit.Vx*-2,fruit.gravity*1.5))
                elif fruit.Image == Images["Orange"]:
                    fruit.Image = Images["OrangeTop"]
                    Fruits.append(Fruit(Images["OrangeBottom"],fruit.x,fruit.y,fruit.Vx*-2,fruit.gravity*1.5))
                elif fruit.Image == Images["Apple"]:
                    fruit.Image = Images["AppleTop"]
                    Fruits.append(Fruit(Images["AppleBottom"],fruit.x,fruit.y,fruit.Vx*-2,fruit.gravity*1.5))
                elif fruit.Image == Images["Lemon"]:
                    fruit.Image = Images["LemonTop"]
                    Fruits.append(Fruit(Images["LemonBottom"],fruit.x,fruit.y,fruit.Vx*-2,fruit.gravity*1.5))
                elif fruit.Image == Images["Strawberry"]:
                    fruit.Image = Images["StrawberryTop"]
                    Fruits.append(Fruit(Images["StrawberryBottom"],fruit.x,fruit.y,fruit.Vx*-2,fruit.gravity*1.5,125,125))
                slice_sound.play()#MAINKAN MUSIKKKK
                Fruits[-1].split = True
                score += 10
        for fruit in Bombs:
            fruit.update()
            if fruit.y <= 800:
                stop = True
            if pygame.sprite.collide_rect(player, fruit) == True and player.drag:
                Explosions.append(Explosion(fruit.x,fruit.y))
                Lives -= 1
                fruit.x = -100
                fruit.y = 900
                explosion_sound.play()#MAINKAN MUSIK BOSSSS

                               
        if stop == False:#BUAH YANG JATUH TIDAK MENGURANGI NYAWA
            for fruit in Fruits:
                if fruit.split == False:
                   Fruits = []
            for i in range(random.randint(2,5)):
                choice = random.choice(Choices)
                if choice == "Strawberry": 
                    Fruits.append(Fruit(Images[choice],500,800,random.randint(-20,20),random.randint(-22,-20),125,125))
                else:
                    Fruits.append(Fruit(Images[choice]))
            if random.randint(1,4) <= 3:
                Bombs = [Fruit(Images["Bomb"],500,800,random.randint(-40,40),-20,100,100)]
            else:
                Bombs = []
        for explosion in Explosions:
            explosion.update(Images)
            if explosion.Life <= 0:
                Explosions.pop(Explosions.index(explosion))
               
     
        #Menggambar slash cursor
        if player.drag == True:
            player.update(Colors)
                

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
     MainMenu.HomeScreen()





