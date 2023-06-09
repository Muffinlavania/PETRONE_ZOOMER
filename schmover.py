import pygame,sys,math,os,time,random,json
from pygame.locals import *
#window stuff
import ctypes
from ctypes import POINTER, WINFUNCTYPE, windll
from ctypes.wintypes import BOOL, HWND, RECT


#close to working


#PETRONE ZOOMER
#petrones zooms from one screen the the next, using the entire width of each screen, synced DE file system, a dictionary with keys which are:
#amount of screens alive: use an id number that when assigned to one screen becomes +1
#current screen max: resets to amount of screens alive 
#other stuff thasts needed

#petrone zooming, use default petrone pic, add fire petrone (press f for it, secret in a text file in github upload)
#make proportional to screen width etc

#todo: maths for calculations as where petrone should start on each screen, make the zooming (not bad lol)
#this is probably broken rn just normally lol

#1 first, 0 2nd etc

loaded = False
ID = 1

def save():
  global thedict
  with open("petrone-data.json","w") as i:
    i.write(json.dumps(thedict))
  i.close()

def load(over=True):
  global thedict
  with open("petrone-data.json",'r') as j:
    if over:
      thedict = json.load(j)
    else:
      q = json.load(j)
      j.close()
      return q
def recheck_first():
  global ID,loaded
  load()
  
  #change things
  if 'id' in thedict.keys():
    loaded = True
    ID = thedict['id']+1
    thedict['id']+=1
  
  save()

thedict = {}
if "petrone-data.json" not in os.listdir():
  save()
else:
  thedict['die'] = False
  recheck_first()

class pet:
  def __init__(self, image, starting_cords = (0,0)):
    self.image = image
    self.height = self.image.get_height()
    self.pos = image.get_rect().move(starting_cords[0], starting_cords[1])
    self.width = self.image.get_width()


clock = pygame.time.Clock()

#window stuff
user32 = ctypes.windll.user32
maxSS = (user32.GetSystemMetrics(78), user32.GetSystemMetrics(79))
def move_window(x, y):
    hwnd = pygame.display.get_wm_info()["window"]
    user32.SetWindowPos(hwnd, 0, round(x), round(y), 0, 0, 0x0001)  # 0x0001 is SWP_NOSIZE flag
def screensize(size,size2):
  global screen,WIDTH,HEIGHT
  screen = pygame.display.set_mode(((WIDTH:=round(size)),(HEIGHT:=round(size2))))
screensize(maxSS[0]//2,400)

def title(thi):
  pygame.display.set_caption(thi)
def fill(color,default=screen):
  default.fill(color)
def current_pos():
  prototype = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
  paramflags = (1, "hwnd"), (2, "lprect")

  GetWindowRect = prototype(("GetWindowRect", windll.user32), paramflags)
  POS = GetWindowRect(pygame.display.get_wm_info()["window"]) 
  return (POS.left,POS.top)
def check_events():
  for event in pygame.event.get():
    if event.type == pygame.QUIT: #will need to change this later so you cant just 
      quit()
def file(name):
  return pygame.image.load(f"zoom_files/{name}")
def up():
  pygame.display.update()
def color(colo,wid=WIDTH,hei=HEIGHT):
  surf = pygame.Surface((wid,hei))
  surf.fill(colo)
  return surf
def quit():
  pygame.quit()
  
  #if first kill them all
  if ID==1 or quiter>5:
    with open("petrone-data.json",'w') as j:
      j.write(json.dumps({'die':True}))
  else:
    #if current ID saved is its own ID, aka you just opened and closed, minus one
    load()
    if ID==thedict['id']:
      thedict['id']-=1
    save()
  sys.exit()
def scale(thing,coors):
  return pygame.transform.scale(thing,coors)
def show(thing,where=(0,0)):
  screen.blit(thing,where if type(where[0])==int else (where[1][0]-width_dict[where[0]],where[1][1]))
def sleep(tim=1000):
  tim2 = round(tim,-1)
  li = list(i for i in range(5,500,5) if tim2/i < 50)[0] #.01% chance this errors
  #tim1 = time.time()
  NUM = round(tim)
  for i in range(round(li)):
    key = pygame.key.get_pressed()
    check_events()
    pygame.time.delay((e:=round(tim2/li)) if i!=round(li)-1 else NUM-1)
    NUM -= e

def cos(num):
  return math.cos(math.radians(num))
def sin(num):
  return math.sin(math.radians(num))
def font(size:int):
  return pygame.font.Font('zoom_files/determination.ttf', size)
def text(text,font,color=(0,0,0)):
  return font.render(text, True, color)
def MID(surf):
  return surf.get_rect().width//2
def flip(thi,x_flip=True,y_flip=False):
  return pygame.transform.flip(thi,x_flip,y_flip)

ded_sync = False
if not loaded:
  thedict = {'id':1,'target':1}
  save()
else:
  if thedict.get("death_sync",False):
    ded_sync = True
#death cutscene
def DIE(petrone):
  global thedict
  black = color((0,0,0))
  RAHH = pygame.mixer.Sound("zoom_files/rahh.mp3")
  RAHH.set_volume(.5)
  show(black)
  show(petrone.image,(WIDTH//2-MID(petrone.image),HEIGHT//2))
  up()
  load()
  if thedict.get("TIME_JUMP",False)!=False:
    sleep((thedict["TIME_JUMP"]-time.time())*1000)
  else:
    thedict['TIME_JUMP'] = time.time()+5
    save()
    sleep(5000)
  move_window(0,0)
  screensize(maxSS[0],maxSS[1])
  show(color((0,0,0)))
  show(scale(petrone.image,(maxSS[0],maxSS[1])))
  up()
  pygame.mixer.Sound.play(RAHH)
  sleep(1000)
  thedict = {}
  save()
  quit()


def main():
  global screen,HEIGHT,WIDTH,width_dict,quiter,ded_sync,thedict
  pygame.init()
  #HURT = pygame.mixer.Sound("FILES/hurt.wav")
  #dont = pygame.font.Font('zoom_files/determination.ttf', 20).render(random.choice(['dont be party poop >:(','why are you like this','im invincible easy','hey no','get me to do it lol','nah b']), True, (255,255,255))
  press = font(50)
  press2 = font(30)
  
  width_dict = {"press_mid":MID(text(("Press s to join the chain!" if loaded else "Press s to start the chain!"),press)),"other_mid":MID(text(f"Screen ID: {ID}",press2)),"waiting":MID(text("Syncing Petrones... (itll start soonish)",press)),"show":MID(text(f"Synced, running in 10.0 seconds..",press2))}
  
  colour = (111, 167, 227)
  title(random.choice(["hi :)","the zoooooooomer","petroleum power","petrone > sogoian sorry","made by not lucas stop beating everything i do lucas god damn it","anyway todays weather is cloudy with a chance of uncloudyness","i wonder how many random messages there are","im not the maker of this thing game thing","bbbbbbbbbbbbbbbbbbbbbbb aaaaaaaaaa W programming rn","how much wood could a woodchuck chuck at a toddler","3.141592652589 thats all i know","*boolean algebra* (i forgot to laugh)","bububmbbbubmbbbbmmbbumbb baaaaaaaaaaaaa","you reached the end of this ranomness wait you probably didnt nvm lol","i do this whenever i forget what im doing","wait what am i doing","you read the text file that came with this too right >:(","im so angry right now rrrrrRRRRRRRRRRRR"]))
  
  ending = maxSS[0]+10 + (maxSS[0]*(ID-1))
  
  petrone = pet(file("PETRONE.jpeg"),(ending,200-MID(file("PETRONE.jpeg"))))
  
  petrone_norm = file("PETRONE.jpeg")
  petrone_norm_flipped = flip(petrone_norm)
  petrone_fire = file("PETRONE_FLAME.png")
  petrone_fire_flipped = flip(petrone_fire)
  
  activated = False
  goodie = False
  FIRE = False
  numb = 90
  quiter = 0
  frame = 0
  Pmult = -1
  P_cos_num = 0
  Pnum = -69
  Pos = current_pos()
  targY = maxSS[1]//2 - 200
  targtime = -1
  SCREEN = 1
  POS = 1280
  numbi = 254
  alp2 = 0
  alp3 = 0
  confirmed = False
  confirmed2 = False
  values = (255,56,56, 255,162,56, 255,252,56, 103,250,56, 56,150,250, 117,56,250)
  thing2 = text("Exiting synced to new screens!",press2)
  #start real
  def resetie():
    nonlocal Pmult,P_cos_num,petrone
    petrone.image = petrone_norm if not FIRE else petrone_fire
    if ID==1: #resetie spageti thing
      load()
      thedict['time'] = time.time()+3
      save()
      sleep(3000)
      load()
      thedict['time'] = -1
      save()
    else:
      Q = 0
      while Q<=2:
        sleep(1000)
        Q+=1
        load()
        if thedict['time']>time.time():
          Q = thedict['time']
      if Q>time.time():
        sleep((Q-time.time())*1000)
      load()
        
    Pmult = -1 #used for left/right movement
    P_cos_num = 0 #used for the target screen movement, increment to 360 (amplify by 20?) then stop it and move normally
    petrone.pos.left = ending
  def zoom():
    nonlocal Pmult,P_cos_num,petrone,Pnum,SCREEN,POS
    if Pnum==-69 and ID==1: #resetie spageti thing
      resetie()
    Pnum = 69
    SCREEN = petrone.pos.left//maxSS[0] + (2-ID) 
    POS = petrone.pos.left - (maxSS[0]*(petrone.pos.left//maxSS[0]))
    if (2-thedict['target']) == SCREEN and POS<500 and P_cos_num<180:
      petrone.pos.left += cos(P_cos_num)*5*Pmult
      P_cos_num+=1
      if P_cos_num == 91:
        petrone.image = petrone_norm_flipped if not FIRE else petrone_fire_flipped 
      if P_cos_num == 180:
        Pmult = 1
      
    elif SCREEN>1 and petrone.pos.left!=ending:
      show(backing)
      up()
      resetie()
    else:
      petrone.pos.left += 15*Pmult
  
  
  while True:
    if numb<-300 or not activated:
      pass
    elif numb>0:
      numb-=.5
      move_window(Pos[0]-Pos[0]*cos(numb)-(7*cos(numb)),targY + (targY-Pos[1])*(1 if targY>Pos[1] else -1)*cos(numb+90))
      screensize((maxSS[0]-maxSS[0]//2)*cos(numb)+maxSS[0]//2,400)
    elif numb>-300:
      title('lets get to zooming')
      numb=-6969
    thing = text(str(SCREEN)+","+str(POS),press)
    thing.set_alpha(numbi if numbi>0 else 0)
    thing2.set_alpha(alp2 if alp2>0 else 0)
    backing = color(colour,WIDTH,HEIGHT)
    show(backing)
    show(thing,(10,10))
    show(thing2,(WIDTH-360,10))
    if confirmed:
      idtext1[0].set_alpha(numbi)
      idtext1[1].set_alpha(numbi)
      show(idtext1[0],(WIDTH//2-275,350))
      show(idtext1[1],(WIDTH//2,350))
    if confirmed2:
      changed.set_alpha(alp3)
      show(changed,(WIDTH-100,350))
    show(petrone.image,petrone.pos)
    if not activated:
      q = sin(frame)
      show(press.render("Press s to join the chain!" if loaded else "Press s to start the chain!", True, (abs(q)*143+20,abs(q)*71+20,abs(q)*191+20)),("press_mid",(maxSS[0]//4,50+q*10)))
      if loaded:
        show(press2.render(f"Screen ID: {ID}", True, (0,0,0)),("other_mid",(maxSS[0]//4,100+q*10)))
    
    if numb==-6969:
      if not loaded:
        zoom()
      else:
        if not goodie:
          show(text("Syncing Petrones... (itll start soonish)",press),("waiting",(maxSS[0]//2,180)))
          if targtime==-1 and frame%10==0:
            load()
            if thedict.get('time',-1)!=-1:
              targtime = thedict['time']
          elif targtime!=-1:
            if targtime-time.time()>0:
              if thedict.get('target',2)!=2-ID and thedict['id'] == ID:
                load()
                if thedict['id'] == ID:
                  thedict['target'] = ID
                save()
              show(text(f"Synced, running in {round(targtime-time.time(),1)} seconds..",press2),("show",(maxSS[0]//2,220)))
            else:
              goodie = True
              zoom()
        else:
          zoom()
    k = pygame.key.get_pressed()
    
    if k[K_s]:
      if Pos[0] != current_pos()[0]:
        Pos = current_pos()
        targY = Pos[1]
      activated = True
    
    if k[K_z]:
      quiter +=1
    
    if k[K_q]:
      numbi = 254
      idtext1 = (text(f"Next ID: {thedict['id']}, Target: {thedict['target']}",press2),text("Press e to change -1!",press2))
      confirmed = True

    if k[K_f]:
      FIRE = True
    
    if k[K_l]:
      load()
    
    if k[K_d] and ID==1:
      alp2 = 254
      temp = thedict.copy()
      load()
      thedict['death_sync'] = True
      save()
      thedict = temp.copy()
    if k[K_e] and confirmed and alp3<220 and thedict['id']>1:
      confirmed2 = True
      alp3 = 254
      thedict['id'] -= 1
      thedict['target'] -= 1
      changed = text("Changed!",press2,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
      save()
    
    if k[K_r]:
      temp = ((ID-1)%6)*3
      colour = (values[temp],values[temp+1],values[temp+2])
    check_events()
        
    up() 
    
    if frame%60 and ded_sync and ID!=1:
      thedict2 = load(False)
      if thedict2.get("die",False):
        DIE(petrone)
    
    clock.tick(60) #60 fps
    frame += 1
    numbi -= 2
    alp2 -= 2
    alp3 -= 2
    if numbi==0:
      confirmed = False
    if alp3==0:
      confirmed2 = False
main()