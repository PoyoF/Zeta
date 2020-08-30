#coding: utf-8
from pygame import *
from pygame.locals import *
import sys
import pygame

dyv=1 #上下ほうこうののはやさ
SCREENRect = Rect(0, 0,640,400) # 画面の大きさ(x，y，w, h)
#   w：はば(width)、　h：高さ(height)
class ZetaMoveGame:
  def __init__(self):
    pygame.init() #initialize
    SCREEN = pygame.display.set_mode(SCREENRect.size)# 
    # 背景
    BG=pygame.image.load("SpringElmTree.jpg").convert_alpha()
    BG=pygame.transform.smoothscale(BG,SCREENRect.size)

    # Zetaのスプライト(サイズ：(50,50))
    #画像ファイル名:"inkscape.png"
    #スプライト、さいしょのいち:(100,200)
    #スプライト速さ:(5,0)
    Sprite.containers = self.all = pygame.sprite.RenderUpdates()
    self.Zeta = Sprite(
      "inkscape.png",(100,200),(50,50), (5,0)) 
    clock =pygame.time.Clock()
    # ループ部
    while True:
      clock.tick(60)                     # 画面更新間隔（m秒）
      SCREEN.blit(BG, SCREEN.get_rect()) # 背景画像の描画
      self.update()                      # Spriteアップデート
      self.draw(SCREEN)                  # Spriteを描く
      pygame.display.update() #画面全体のアップデート
      self.eventHandler() #　イベントハンドラ

  def update(self): #Spriteアップデート
    self.all.update()
    
  def draw(self, screen): #Spriteを描く 
    self.all.draw(screen)
    
  def eventHandler(self): #　イベントハンドラ
    for ev in pygame.event.get():
      if ev.type == pygame.QUIT:
        quit()
        sys.exit()
      if ev.type == pygame.KEYDOWN:       # キーを押したとき
        if ev.key == pygame.K_ESCAPE:   # Escキーが押されたとき
          quit()
          sys.exit()
        if ev.key == pygame.K_j:       # 「j」キーを押したとき
          self.Zeta.vy += dyv   # Y方向の速度を下向きに
        if ev.key == pygame.K_k:       # 「k」キーを押したとき
          self.Zeta.vy -= dyv   # Y方向の速度を上向きに
        if (ev.key == pygame.K_SPACE): # spaceキーを押したとき
          self.Zeta.vy=0        # Y方向の速度をゼロにする

class Sprite(pygame.sprite.Sprite):
  def __init__(self, filename, p, spriteSize, v):
    pygame.sprite.Sprite.__init__(self, self.containers)
    im = pygame.image.load(filename).convert_alpha()
    im = pygame.transform.smoothscale(im,spriteSize)
    im.set_colorkey(im.get_at((0,0)),pygame.RLEACCEL)

    self.leftImage = im # ←
    self.rightImage = pygame.transform.flip(im, 1, 0)# →
    self.image = self.rightImage

    self.rect = pygame.Rect(p[0], p[1], im.get_width(), im.get_height())
    self.vx = v[0]
    self.vy = v[1]
        
  def update(self):
    self.rect.move_ip(self.vx, self.vy)
  # 左右かべでのはねかえり
    if self.rect.left < 0:              # 左はしに着いたら
      self.vx = -self.vx                # はやさの向きを変える
      self.image = self.rightImage      # 右向きの画像
    if self.rect.right > SCREENRect.width: # 右端に着いたら
      self.vx = -self.vx                # はやさの向きを変える
      self.image = self.leftImage       # 左向きの画像
  # たて方向の　はやさの向きを変える
    if (self.rect.top < 0 or 
        self.rect.bottom > SCREENRect.height): 
      self.vy = -self.vy
  # 壁の中に入っていた時だけ描きなおす
    self.rect = self.rect.clamp(SCREENRect)

if __name__ == "__main__":
    ZetaMoveGame() # Gameプログラム本体の実行