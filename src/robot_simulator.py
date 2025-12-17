class Robot1D:
    
    def __init__(self, initial_position=0.0):
        """
        Parameters
        ----------
        initial_position : float
            初期位置
        """
        self.position = initial_position
        
    def move(self, distance):
        """
        Parameters
        ----------
        distance : float
            移動距離（正で右、負で左）
            
        Returns
        -------
        position : float
            移動後の位置
        """
        self.position += distance
        return self.position
    
    def get_position(self):
        """
        Returns
        -------
        position : float
            現在の位置
        """
        return self.position
    