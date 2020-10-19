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


