import numpy as np


class Robot2D:
    """2D平面上を移動するロボット
    状態: [x, y, theta]
    制御入力: [v, omega]
    """
    
    def __init__(self, initial_state, process_noise_std, observation_noise_std, dt=1.0):
        self.state = np.array(initial_state, dtype=float)
        self.process_noise_std = np.array(process_noise_std, dtype=float)
        self.observation_noise_std = np.array(observation_noise_std, dtype=float)
        self.dt = dt
        
        self.state_history = [self.state.copy()]
        self.observation_history = [self.observe()]
    
    def move(self, control_input):
        """制御入力 [v, omega] で移動"""
        v, omega = control_input
        x, y, theta = self.state
        
        # 運動モデル
        x_new = x + v * np.cos(theta) * self.dt
        y_new = y + v * np.sin(theta) * self.dt
        theta_new = theta + omega * self.dt
        
        # プロセスノイズ
        process_noise = np.random.randn(3) * self.process_noise_std
        self.state = np.array([x_new, y_new, theta_new]) + process_noise
        self.state[2] = self._normalize_angle(self.state[2])
        
        self.state_history.append(self.state.copy())
        self.observation_history.append(self.observe())
        
        return self.state.copy()
    
    def observe(self):
        """観測値を取得"""
        observation_noise = np.random.randn(3) * self.observation_noise_std
        observation = self.state + observation_noise
        observation[2] = self._normalize_angle(observation[2])
        return observation
    
    def get_state(self):
        """現在の真の状態を取得"""
        return self.state.copy()
    
    def _normalize_angle(self, angle):
        """角度を [-pi, pi] に正規化"""
        while angle > np.pi:
            angle -= 2 * np.pi
        while angle < -np.pi:
            angle += 2 * np.pi
        return angle
