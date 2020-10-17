# Is in Jaque (color)
# Is ahogado
# Enroque
# Coronacion



from math import floor

NEGRO=False
BLANCO=True

A=1
B=2
C=3
D=4
E=5
F=6
G=7
H=8

columna={1:"A",2:"B",3:"C",4:"D",5:"E",6:"F",7:"G",8:"H"}
color_dic={True:"Blanco",False:"Negro"}

class Pieza:
  def __init__(self,color,pieza,x,y):
    self.color=color
    self.setPieza(pieza)
    self.setPosition(x,y)
    if self.pieza=="Peon" or self.pieza=="Rey" or self.pieza=="Torre":
      self.ismoved=False

  def setPieza(self,pieza):
    if pieza not in ["Peon","Torre","Alfil","Caballo","Dama","Rey"]:
      raise PiezaIncorrecta
    else:
      self.pieza=pieza

  def getPieza(self):
    return self.pieza

  def getPosition(self):
    return [self.x,self.y]

  def getColor(self):
    return self.color

  def __repr__(self):
    return 'Pieza: %s | Color: %s | Posicion: %s %d' % (self.pieza, color_dic[self.color], columna[self.x], self.y)


  def setPosition(self,x,y):
    if y < 1 or y > 8 or x < A or x > H:
      raise PosicionIncorecta
    else:
      self.x=x
      self.y=y
      if self.pieza=="Peon" or self.pieza=="Rey" or self.pieza=="Torre":
        self.ismoved=True
  
  def moverPieza(self,x,y,tablero):
    """Mueve la piezas hacia esa posicion"""
    availablepos=self.AvailablePositionsinTablero(tablero)
    found=False
    for p in availablepos:
      if x == p[0] and y == p[1]:
        found=True
        if p[2]:
          tablero.remove(tablero.GetPieza(x,y)) #Como la pieza
        self.setPosition(x,y)
    if not found:
      raise PiezaNoEncontrada

  def isin(self,x,y):
    """Permite saber si la pieza esta en un casillero determinado"""
    return True if (self.x==x and self.y==y) else False
  @staticmethod
  def _isinTablero(x,y):
    """Devuelve si una posicion esta adentro del tablero"""
    if y < 1 or y > 8 or x < A or x > H:
      return False
    else:
      return True

  def _AvailablePositionsinTablero_Peon(self,tablero):
      _avail=[]
      if self.color==BLANCO:
        direction=1
      else:
        direction=-1

      p=[self.x,self.y+1*direction]
      if Pieza._isinTablero(p[0],p[1]) and not tablero.CasilleroOcupado(p[0],p[1]):
        _avail.append([p[0],p[1],False])
        p=[self.x,self.y+2*direction]
        if Pieza._isinTablero(p[0],p[1]) and not self.ismoved and not tablero.CasilleroOcupado(p[0],p[1]):
          _avail.append([p[0],p[1],False])

      for p in [[self.x+1,self.y+1*direction],[self.x-1,self.y+1*direction]]:
        if Pieza._isinTablero(p[0],p[1]) and tablero.CasilleroOcupado(p[0],p[1]) and tablero.GetPieza(p[0],p[1]).getColor()!=self.getColor():
            _avail.append([p[0],p[1],tablero.GetPieza(p[0],p[1])])
      return _avail

  def _AvailablePositionsinTablero_AlfilTorreDama(self,tablero):
    _avail=[]
    if self.getPieza()=="Alfil":
      mov=[[1,1],[1,-1],[-1,1],[-1,-1]]
    if self.getPieza()=="Torre":
      mov=[[1,0],[-1,0],[0,1],[0,-1]]
    if self.getPieza()=="Dama":
      mov=[[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
    for p in mov:
      for i in range(1,8):
        pos=[ self.x+p[0]*i , self.y+p[1]*i ]
        if not Pieza._isinTablero(pos[0],pos[1]):
          break
        if not tablero.CasilleroOcupado(pos[0],pos[1]):
          _avail.append([pos[0],pos[1],False])
          continue
        #Si hay pieza pero es del otro color, la meto
        if self.getColor()!=tablero.GetPieza(pos[0],pos[1]).getColor():
          _avail.append([pos[0],pos[1],tablero.GetPieza(pos[0],pos[1])])
          break
        if self.getColor()==tablero.GetPieza(pos[0],pos[1]).getColor():
          break
    return _avail

  def _AvailablePositionsPieza(self):
    """Devuelva las posiciones disponibles para esa pieza"""
    ##############
    #Caballo
    if self.pieza=="Caballo":
      _avail=[]
      #Voy por las posiciones del Rey sacando las tablero
      for pos in [[self.x+2,self.y+1],
                  [self.x+2,self.y-1],
                  [self.x-2,self.y+1],
                  [self.x-2,self.y-1],
                  [self.x+1,self.y+2],
                  [self.x+1,self.y-2],
                  [self.x-1,self.y+2],
                  [self.x-1,self.y-2]]:
        if Pieza._isinTablero(pos[0],pos[1]):
          _avail.append([pos[0],pos[1],False])
      return _avail
    ##############
    #Rey
    if self.pieza=="Rey":
      _avail=[]
      #Voy por las posiciones del Rey sacando las tablero
      for pos in [[self.x+1,self.y+1],[self.x+1,self.y-1],[self.x-1,self.y+1],[self.x-1,self.y-1],[self.x-1,self.y],[self.x+1,self.y],[self.x,self.y-1],[self.x,self.y+1]]:
        if Pieza._isinTablero(pos[0],pos[1]):
          _avail.append(pos)
      return _avail


  def AvailablePositionsinTablero(self,tablero):
    """Devuelva las posiciones disponible spara esa pieza dado el tablero """
    #Falta Peon, Alfil, Dama, Torre

    if self.getPieza()in ["Alfil","Torre","Dama"]:
      return self._AvailablePositionsinTablero_AlfilTorreDama(tablero)

    if self.getPieza()== "Peon":
      return self._AvailablePositionsinTablero_Peon(tablero)

    _avail=self._AvailablePositionsPieza()
    __avail=[]
    #Se fija que no haya otra pieza"
    for pos in _avail:
      #Si no hay pieza, la meto
      if not tablero.CasilleroOcupado(pos[0],pos[1]): 
        __avail.append([pos[0],pos[1],False])
      #Si hay pieza pero es del otro color, la meto
      elif self.getColor()!=tablero.GetPieza(pos[0],pos[1]).getColor():
        __avail.append([pos[0],pos[1],tablero.GetPieza(pos[0],pos[1])])
    return __avail



class Tablero(list):
  def CasilleroOcupado(self,x,y):
    for p in self:
      if p.isin(x,y):
        return True
    return False

  def GetPieza(self,x,y):
    for p in self:
      if [x,y]==p.getPosition():
        return p
    return False


#############################################
#############################################
#############################################
#############################################

tablero=Tablero()

tablero.append(Pieza(BLANCO,"Peon",A,2))
tablero.append(Pieza(BLANCO,"Peon",B,2))
tablero.append(Pieza(BLANCO,"Peon",C,2))
tablero.append(Pieza(BLANCO,"Peon",D,2))
tablero.append(Pieza(BLANCO,"Peon",E,2))
tablero.append(Pieza(BLANCO,"Peon",F,2))
tablero.append(Pieza(BLANCO,"Peon",G,2))
tablero.append(Pieza(BLANCO,"Peon",H,2))

tablero.append(Pieza(BLANCO,"Torre",A,1))
tablero.append(Pieza(BLANCO,"Caballo",B,1))
tablero.append(Pieza(BLANCO,"Alfil",C,1))
tablero.append(Pieza(BLANCO,"Dama",D,1))
tablero.append(Pieza(BLANCO,"Rey",E,1))
tablero.append(Pieza(BLANCO,"Alfil",F,1))
tablero.append(Pieza(BLANCO,"Caballo",G,1))
tablero.append(Pieza(BLANCO,"Torre",H,1))

tablero.append(Pieza(NEGRO,"Peon",A,7))
tablero.append(Pieza(NEGRO,"Peon",B,7))
tablero.append(Pieza(NEGRO,"Peon",C,7))
tablero.append(Pieza(NEGRO,"Peon",D,7))
tablero.append(Pieza(NEGRO,"Peon",E,7))
tablero.append(Pieza(NEGRO,"Peon",F,7))
tablero.append(Pieza(NEGRO,"Peon",G,7))
tablero.append(Pieza(NEGRO,"Peon",H,7))

tablero.append(Pieza(NEGRO,"Torre",A,8))
tablero.append(Pieza(NEGRO,"Caballo",B,8))
tablero.append(Pieza(NEGRO,"Alfil",C,8))
tablero.append(Pieza(NEGRO,"Dama",D,8))
tablero.append(Pieza(NEGRO,"Rey",E,8))
tablero.append(Pieza(NEGRO,"Alfil",F,8))
tablero.append(Pieza(NEGRO,"Caballo",G,8))
tablero.append(Pieza(NEGRO,"Torre",H,8))

#tablero.GetPieza(B,2).moverPieza(B,3,tablero)

#For Testing
#p=tablero.GetPieza(C,7)
#print(p)
#p.AvailablePositionsinTablero(tablero)


#############################################
#############################################
#############################################
#############################################
########################### Arranca GUI


import pygame

#Screen
pygame.init()
screen=pygame.display.set_mode((6 00,600))
pygame.display.set_caption("Ajedrez")

#Piezas

x0=0
y0=0
a=60


dic_white =  {
  "Peon": pygame.image.load("images/Chess_plt60.png"),
  "Dama": pygame.image.load("images/Chess_qlt60.png"),
  "Rey": pygame.image.load("images/Chess_klt60.png"),
  "Caballo": pygame.image.load("images/Chess_nlt60.png"),
  "Torre": pygame.image.load("images/Chess_rlt60.png"),
  "Alfil": pygame.image.load("images/Chess_blt60.png")
}

dic_black =  {
  "Peon": pygame.image.load("images/Chess_pdt60.png"),
  "Dama": pygame.image.load("images/Chess_qdt60.png"),
  "Rey": pygame.image.load("images/Chess_kdt60.png"),
  "Caballo": pygame.image.load("images/Chess_ndt60.png"),
  "Torre": pygame.image.load("images/Chess_rdt60.png"),
  "Alfil": pygame.image.load("images/Chess_bdt60.png")
}

dic_img =  {
  BLANCO: dic_white,
  NEGRO: dic_black
}

escaqueblack=pygame.image.load("images/black.png")
escaquewhite=pygame.image.load("images/white.png")
selected=pygame.image.load("images/selected.png")


def displayEscaques():
  for x in range(1,9):
    for y in range(1,9):
      if (x+y)%2:
        screen.blit(escaqueblack,(x*a+x0,y*a+y0))
      else:
        screen.blit(escaquewhite,(x*a+x0,y*a+y0))

def displayPiezas():
  for pieza in tablero:
    screen.blit(dic_img[pieza.getColor()][pieza.getPieza()],(pieza.getPosition()[0]*a+x0,pieza.getPosition()[1]*a+y0))


def displaySelected(availableEscaques):
  for p in availableEscaques:
    screen.blit(selected,(p[0]*a+x0,p[1]*a+y0))


def getescaque_from_mousexy(xy):
  """Le das las el escaque, de la posicion xy"""
  return (
          floor((xy[0]-x0)/a),
          floor((xy[1]-y0)/a)
         )


running=True

#Seteo el turno del juegador
turno=BLANCO        #DE quien es el turno
drag=False          #Si esta agarrada la pieza
selectedEscaque=[False,False]  #Escaque seleccionado
selectedPieza=False      #Pieza seleccionada
availableEscaques=[]    #Variables que tienen que ser pintadas

while running:

  screen.fill((0,0,0))

  for event in pygame.event.get():
    if event.type== pygame.QUIT:
      running=False
    if event.type== pygame.MOUSEBUTTONDOWN:
      selectedEscaque=getescaque_from_mousexy(pygame.mouse.get_pos())
      piez=tablero.GetPieza(selectedEscaque[0],selectedEscaque[1])
 
      if not drag:
        if piez and piez.getColor()==turno:
            availableEscaques=piez.AvailablePositionsinTablero(tablero)
            selectedPieza=piez
            drag=True
        else:
          availableEscaques=[]
      else:
        for p in availableEscaques:
          if [selectedEscaque[0],selectedEscaque[1]]==[p[0],p[1]]:
            selectedPieza.moverPieza(selectedEscaque[0],selectedEscaque[1],tablero)
            drag=False
            turno=NEGRO if turno==BLANCO else BLANCO
            availableEscaques=[]
            break
        if drag and piez and piez.getColor()==turno: #Solo entramos si es draf, evaluamos de nuevo eso en caso de que el for de arriba mueza pieza
          availableEscaques=piez.AvailablePositionsinTablero(tablero)
          drag=True
        else:
          availableEscaques=[]
          drag=False



  displayEscaques()
  displaySelected(availableEscaques)
  displayPiezas()

  if turno==BLANCO:
    pass
    if drag:
        pass
    else:
        pass
  else:
    pass
    if drag:
      pass
    else:
        pass

  pygame.display.update()
