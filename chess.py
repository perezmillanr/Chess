#Author: Perez Millan Rodrigo
#2020
from math import floor
import copy

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
    self.ismoved=False
    self.coronado=False

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
      self.ismoved=True
  
  def moverPieza(self,x,y,tablero):
    """Mueve la piezas hacia esa posicion"""
    availablepos=self.AvailablePositionsinTablero2(tablero)
    found=False
    for p in availablepos:
      if x == p[0] and y == p[1]:
        found=True
        if p[2]:
          tablero.remove(tablero.GetPieza(x,y)) #Como la pieza

        if self.getPieza()=="Rey" and [x,y] in self._addEnroque(tablero):
          #Aca tenemos que mover la torre tambien porque es un enroque
          self._moverTorreEnrocada (x,y,tablero)
        self.setPosition(x,y)

        if self.getPieza()=="Peon":
          if self.getColor()==NEGRO and self.getPosition()[1]==1:
            self.coronado=True
          if self.getColor()==BLANCO and self.getPosition()[1]==8:
            self.coronado=True

    if not found:
      raise PiezaNoEncontrada

  def _moverTorreEnrocada(self,x,y,tablero):
    """Mueve la torre en el marco del enroque"""
    if [x,y] == [G,1]:
      tablero.GetPieza(H,1).moverPieza(F,1,tablero)
    if [x,y] == [C,1]:
      tablero.GetPieza(A,1).moverPieza(D,1,tablero)
    if [x,y] == [G,8]:
      tablero.GetPieza(H,8).moverPieza(F,8,tablero)
    if [x,y] == [C,8]:  
      tablero.GetPieza(A,8).moverPieza(D,8,tablero)

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

  def _AvailablePositionsPieza(self,tablero,EvaluateEnroque=True):
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

      return _avail+(self._addEnroque(tablero) if EvaluateEnroque else [])


  def _addEnroque(self,tablero):
    """Suma las posiciones de enroque si aplica"""

    #Este es el unico lugar del codigo donde uso isinjacque con EvaluateEnroque en false
    #Esto es para evitar la recursion, evaluar enroque -> envaluo jaque -> evalua las availablepos de cada pieza contraria -> evaluo el enroque del otro rey -> etc etc
    _available=[]
    if self.getColor()==BLANCO and not Pieza.isinJaque(BLANCO,tablero,EvaluateEnroque=False) and tablero.GetPieza(H,1) and not tablero.GetPieza(G,1) and not tablero.GetPieza(F,1):
      if tablero.GetPieza(H,1).getPieza()=="Torre":
       if not tablero.GetPieza(H,1).ismoved:
        if not self.ismoved:
            _available.append([G,1])

    if self.getColor()==BLANCO and not Pieza.isinJaque(BLANCO,tablero,EvaluateEnroque=False) and tablero.GetPieza(A,1) and not tablero.GetPieza(B,1) and not tablero.GetPieza(C,1) and not tablero.GetPieza(D,1):
      if tablero.GetPieza(A,1).getPieza()=="Torre":
       if not tablero.GetPieza(A,1).ismoved:
        if not self.ismoved:
            _available.append([C,1])

    if self.getColor()==NEGRO and not Pieza.isinJaque(NEGRO,tablero,EvaluateEnroque=False) and tablero.GetPieza(H,8) and not tablero.GetPieza(G,8) and not tablero.GetPieza(F,8):
      if tablero.GetPieza(H,8).getPieza()=="Torre":
       if not tablero.GetPieza(H,8).ismoved:
        if not self.ismoved:
            _available.append([G,8])

    if self.getColor()==NEGRO and not Pieza.isinJaque(NEGRO,tablero,EvaluateEnroque=False) and tablero.GetPieza(A,8) and not tablero.GetPieza(B,8) and not tablero.GetPieza(C,8) and not tablero.GetPieza(D,8):
      if tablero.GetPieza(A,8).getPieza()=="Torre":
       if not tablero.GetPieza(A,8).ismoved:
        if not self.ismoved:
            _available.append([C,8])
    return _available

  def AvailablePositionsinTablero2(self,tablero):  #TO FIX
    _avail=[]
    for available in self.AvailablePositionsinTablero(tablero):
      _tablero=Tablero() 
      #tablero auxiliar
      for p in tablero:
          _tablero.append(copy.copy(p))
      if available[2]:
        _tablero.remove(_tablero.GetPieza(available[0],available[1])) #Como la pieza
      if self.getPieza()=="Rey" and self.getPosition() in self._addEnroque(_tablero):
        #Aca tenemos que mover la torre tambien porque es un enroque
        _tablero.GetPieza(self.getPosition()[0],self.getPosition()[1])._moverTorreEnrocada (available[0],available[1],_tablero)
      _tablero.GetPieza(self.getPosition()[0],self.getPosition()[1]).setPosition(available[0],available[1])
      
      if not Pieza.isinJaque(self.getColor(),_tablero):
        _avail.append(available)
    return _avail

  def AvailablePositionsinTablero(self,tablero,EvaluateEnroque=True):
    """Devuelva las posiciones disponible spara esa pieza dado el tablero """
    #Falta Peon, Alfil, Dama, Torre

    if self.getPieza() in ["Alfil","Torre","Dama"]:
      return self._AvailablePositionsinTablero_AlfilTorreDama(tablero)

    if self.getPieza()== "Peon":
      return self._AvailablePositionsinTablero_Peon(tablero)

    _avail=self._AvailablePositionsPieza(tablero,EvaluateEnroque) #esta es para el rey y el caballo
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


  @staticmethod
  def isinJaque(color,tablero,EvaluateEnroque=True):
    """Te dice si un Rey de un color determinado esta en Jacuqe"""
    for p in tablero:
      if p.color != color:
        for pos in p.AvailablePositionsinTablero(tablero,EvaluateEnroque): #Uso la version uno de la funcion porque no quiero que me saque los escaques que pudiesen dejar al rey contrario en jacque porque estamos evaluando si ya estmaos en jaque
          if pos[2] and pos[2].getPieza()=="Rey":
            return True
    return False

  @staticmethod
  def isinMate(color,tablero):
    """Te dice si esta en mate"""
    if Pieza.isinJaque(color,tablero):
      for p in tablero:
        if p.color == color:
          for pos in p.AvailablePositionsinTablero2(tablero): #Uso la version uno de la funcion porque no quiero que me saque los escaques que pudiesen dejar al rey contrario en jacque porque estamos evaluando si ya estmaos en jaque
            return False
      return True
    return False

  @staticmethod
  def isAhogado(color,tablero):
    """Te dice siel rey esta ahogado"""
    _available=[]
    for p in tablero:
        if p.color == color:
          for pos in p.AvailablePositionsinTablero2(tablero): #Uso la version uno de la funcion porque no quiero que me saque los escaques que pudiesen dejar al rey contrario en jacque porque estamos evaluando si ya estmaos en jaque
            _available.append(pos)
    return True if _available==[] and not Pieza.isinJaque(color,tablero) else False

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
screen=pygame.display.set_mode((600,600))
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
            availableEscaques=piez.AvailablePositionsinTablero2(tablero)
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

            if Pieza.isinJaque(BLANCO,tablero): 
              if Pieza.isinMate(BLANCO,tablero):
                print("Blanco en Jaque Mate")              
              else:
                print("Blanco en Jaque")
            else:
              if Pieza.isAhogado(BLANCO,tablero) and turno==BLANCO:
                print("Blanco Ahogado")
            if Pieza.isinJaque(NEGRO,tablero): 
              if Pieza.isinMate(NEGRO,tablero):
                print("Negro en Jaque Mate")              
              else:
                print("Negro en Jaque")
            else:
              if Pieza.isAhogado(NEGRO,tablero) and turno==NEGRO:
                print("Negro Ahogado")


            for p in tablero:
              if p.coronado:
                p.coronado=False
                option=""
                while option not in ["a","b","c","d"]:
                  if option!="":
                    print("Opcion equivocada, pruebe de nuevo.")
                  option=input("El peon ha sido coronado. Por favor, seleccione una pieza: (a) Dama ; (b) Alfil; (c) Caballo; (d) Torre ")
                d={
                "a":"Dama",
                "b":"Alfil",
                "c":"Caballo",
                "d":"Torre"
                }                  
                p.setPieza(d[option])
            break
        if drag and piez and piez.getColor()==turno: #Solo entramos si es draf, evaluamos de nuevo eso en caso de que el for de arriba mueza pieza
          availableEscaques=piez.AvailablePositionsinTablero2(tablero)
          selectedPieza=piez
          drag=True
        else:
          availableEscaques=[]
          drag=False



  displayEscaques()
  displaySelected(availableEscaques)
  displayPiezas()

  pygame.display.update()
