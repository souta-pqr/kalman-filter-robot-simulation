import numpy as np

class LinearKalmanFilter:
    """
    1次元線形カルマンフィルタ
    
    状態方程式: x_k = x_{k-1} + u_k + w_k  (w_k ~ N(0, Q))
    観測方程式: z_k = x_k + v_k  (v_k ~ N(0, R))
    """
    
    def __init__(self, Q, R, x0=0.0, P0=1.0):
        """
        Parameters
        ----------
        Q : float
            プロセスノイズの共分散
        R : float
            観測ノイズの共分散
        x0 : float
            初期状態推定値
        P0 : float
            初期誤差共分散
        """
        self.Q = Q
        self.R = R
        self.x = x0  # 現在の推定値
        self.P = P0  # 現在の誤差共分散
        
    def predict(self, u=0):
        """
        予測ステップ
        
        Parameters
        ----------
        u : float
            制御入力（移動量）
        """
        # 状態予測: x = x + u
        self.x = self.x + u
        
        # 誤差共分散予測: P = P + Q
        self.P = self.P + self.Q
    
    def update(self, z):
        """
        更新ステップ
        
        Parameters
        ----------
        z : float
            観測値
            
        Returns
        -------
        K : float
            カルマンゲイン
        """
        # カルマンゲイン: K = P / (P + R)
        K = self.P / (self.P + self.R)
        
        # 状態更新: x = x + K * (z - x)
        self.x = self.x + K * (z - self.x)
        
        # 誤差共分散更新: P = (1 - K) * P
        self.P = (1 - K) * self.P
        
        return K
    
    def filter_step(self, z, u=0):
        """
        予測と更新を実行
        
        Parameters
        ----------
        z : float
            観測値
        u : float
            制御入力
            
        Returns
        -------
        x : float
            推定値
        K : float
            カルマンゲイン
        """
        self.predict(u)
        K = self.update(z)
        return self.x, K
        