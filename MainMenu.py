#Importing all the modules
try:
    import time, random, sys, os
except ImportError:
    print("pastikan anda memiliki modul waktu")
    sys.exit()
try:
    import pygame
except ImportError:
    print("pastikan anda memiliki modul pygame")
    sys.exit()
try:
    import main
except ImportError:
    print("Pastikan Anda memiliki semua file tambahan")
from pygame import freetype




# INISIALISASI GAME (WAJIB SEBELUM MEMASUKKAN PERINTAH YANG LAIN)
pygame.init()


DisplayWidth,DisplayHeight = 1000, 800
clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((DisplayWidth,DisplayHeight))
pygame.display.set_caption("Fruit Ninja Anjayyyyy")

font_100 = pygame.freetype.Font("gang-of-three.ttf", 100)
font_50 = pygame.freetype.Font("gang-of-three.ttf", 50)
font_75 = pygame.freetype.Font("gang-of-three.ttf", 75) 
SizeCheck = pygame.font.Font("gang-of-three.ttf", 50)
SizeCheck_75 = pygame.font.Font("gang-of-three.ttf", 75)
font_35 = pygame.freetype.Font("gang-of-three.ttf", 35)

#LOAD GAMBAR DIRECTORY
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

#TOMBOL
class Button():
    def __init__(self, x, y, width, height, Text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = Text

    def draw(self):
        pos = pygame.mouse.get_pos()
        if self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height:
            pygame.draw.rect(gameDisplay,(150,0,0),(self.x,self.y,self.width,self.height),0)
        else:
            pygame.draw.rect(gameDisplay,(250,0,0),(self.x,self.y,self.width,self.height),0)
        pygame.draw.rect(gameDisplay,(100,100,100),(self.x,self.y,self.width,self.height),5)

        if self.text != "Change Color":
            text_surface, rect = font_50.render(str(self.text), (0, 0, 0))
            gameDisplay.blit(text_surface, (self.x + int(self.width/2)+55 - int(SizeCheck.size(str(self.text))[0]), self.y + int(self.height/2) - 20))
        else:
            text_surface, rect = font_35.render(str("Change"), (0, 0, 0))
            gameDisplay.blit(text_surface,(560,625))
            text_surface, rect = font_35.render(str("Color"), (0, 0, 0))
            gameDisplay.blit(text_surface,(575,655))

def shorten(Num):
    count = 0
    let = ""
    while Num >= 1000:
        Num /= 1000
        count += 1
    Num = str(Num)
    Num2 = ""
    if count >= 1:
        for i in range(Num.index(".")+2):
            Num2 += Num[i]
        Num = Num2
    if count == 1:
        Num += "K"
    if count == 2:
        Num += "M"
    if count == 3:
        Num += "B"
    if count == 4:
        Num += "T"
    if count == 5:
        Num += "q"
    if count == 6:
        Num += "Q"
    if count == 7:
        Num += "s"
    if count == 8:
        Num += "S"
    return Num


def HomeScreen(score=0):
    game_run = True
    Images = load_images("Images")
    Buttons = [Button(275,600,200,100,"Play"),Button(525,600,200,100,"Change Color")]
    CcButtons = [Button(750,650,200,100,"Exit"),Button(150,250,50,50,""),Button(800,250,50,50,"")]
    screen = "Main"
    Colors = [(0,250,0),(250,0,0),(0,0,250),(255,255,0),(0,255,255)]
    SubColors = [(0,150,0),(150,0,0),(0,0,150),(150,150,0),(0,150,150)]
    ColorSelection = 0
    logo_fruit = pygame.image.load(os.path.join(os.getcwd(), 'logo.png'))  # udah 'fruit_ninja_logo.png' sesuai dengan format nama gambar
    logo_fruit = pygame.transform.scale(logo_fruit, (700, 500))
    # Images = load_images("Images")


    while game_run == True:

        gameDisplay.fill((210,140,42))
        gameDisplay.blit(pygame.transform.scale(Images["background"],(DisplayWidth,DisplayHeight)),(0,0))
        pos = pygame.mouse.get_pos()
        if screen == "Main":
            gameDisplay.blit(logo_fruit, (160, 20))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if screen == "Main":
                    for i, button in enumerate(Buttons):
                        if button.x <= pos[0] <= button.x + button.width and button.y <= pos[1] <= button.y + button.height:
                            if i == 0:
                                main.game_loop([Colors[ColorSelection],SubColors[ColorSelection]])
                            if i == 1:
                                screen = "Change Color"
                if screen == "Change Color":
                    for i, button in enumerate(CcButtons):
                        if button.x <= pos[0] <= button.x + button.width and button.y <= pos[1] <= button.y + button.height:
                            if i == 0:
                                screen = "Main"
                            if i == 1:
                                ColorSelection += 1
                                ColorSelection %= (len(Colors))
                            if i == 2:
                                ColorSelection -= 1
                                if ColorSelection < 0:
                                    ColorSelection = len(Colors)-1
                                

        if screen == "Main":
            if score != 0:
                text_surface, rect = font_75.render(("Score: " + shorten(score)), (0, 0, 0))
                gameDisplay.blit(text_surface, (440 - SizeCheck_75.size(shorten(score))[0], 300))


            #UPDATE TOMBOL
            for button in Buttons:
                button.draw()

               
        if screen == "Change Color":
            for button in CcButtons:
                button.draw()
            pygame.draw.rect(gameDisplay,Colors[ColorSelection],(350,200,300,150),0)
            pygame.draw.rect(gameDisplay,SubColors[ColorSelection],(350,200,300,150),5)
            pygame.draw.polygon(gameDisplay,(150,150,150),[(808,259),(808,289),(838,274)],0)
            pygame.draw.polygon(gameDisplay,(150,150,150),[(192,259),(192,289),(162,274)],0)


        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    HomeScreen()
    
