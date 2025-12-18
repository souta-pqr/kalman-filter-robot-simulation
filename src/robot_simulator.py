import numpy as np

class Robot1D:
    
    def __init__(self, initial_position=0.0, process_noise_std=0.0, observation_noise_std=0.0):
        """
        Parameters
        ----------
        initial_position : float
            初期位置
        process_noise_std : float
            プロセスノイズの標準偏差
        observation_noise_std : float
            観測ノイズの標準偏差
        """
        self.position = initial_position
        self.process_noise_std = process_noise_std
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
        noise = np.random.randn() * self.process_noise_std
        self.position += distance + noise
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
    