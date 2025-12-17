import numpy as np

class Robot1D:
    
    def __init__(self, initial_position=0.0, observation_noise_std=0.0):
        """
        Parameters
        ----------
        initial_position : float
            初期位置
        observation_noise_std : float
            観測ノイズの標準偏差
        """
        self.position = initial_position
        self.observation_noise_std = observation_noise_std
        
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
            現在の位置（真の値）
        """
        return self.position
    
    def observe(self):
        """
        Returns
        -------
        observation : float
            観測値（ノイズあり）
        """
        noise = np.random.randn() * self.observation_noise_std
        return self.position + noise
    