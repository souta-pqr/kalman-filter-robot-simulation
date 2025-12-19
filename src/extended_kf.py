import numpy as np


class ExtendedKalmanFilter:
    """
    2Dロボット用の拡張カルマンフィルタ

    状態: [x, y, theta]
    制御入力: [v, omega]
    """

    def __init__(self, Q, R, x0, P0, dt=1.0):
        """
        Parameters
        ----------
        Q : ndarray, shape (3, 3)
            プロセスノイズ共分散行列
        R : ndarray, shape (3, 3)
            観測ノイズ共分散行列
        x0 : ndarray, shape (3,)
            初期状態 [x, y, theta]
        P0 : ndarray, shape (3, 3)
            初期誤差共分散行列
        dt : float
            時間ステップ (s)
        """
        self.Q = np.array(Q)
        self.R = np.array(R)
        self.x = np.array(x0)
        self.P = np.array(P0)
        self.dt = dt

    def predict(self, u):
        """
        予測ステップ

        Parameters
        ----------
        u : array-like, shape (2,)
            制御入力 [v, omega]
        """
        v, omega = u
        x, y, theta = self.x

        # 状態予測（非線形運動モデル）
        x_pred = x + v * np.cos(theta) * self.dt
        y_pred = y + v * np.sin(theta) * self.dt
        theta_pred = theta + omega * self.dt

        # 角度を [-pi, pi] に正規化
        theta_pred = self._normalize_angle(theta_pred)

        self.x = np.array([x_pred, y_pred, theta_pred])

        # ヤコビアン行列 F（状態遷移の線形化）
        # F = ∂f/∂x
        F = np.array(
            [[1, 0, -v * np.sin(theta) * self.dt], [0, 1, v * np.cos(theta) * self.dt], [0, 0, 1]]
        )

        # 誤差共分散予測: P = F*P*F^T + Q
        self.P = F @ self.P @ F.T + self.Q

    def update(self, z):
        """
        更新ステップ

        Parameters
        ----------
        z : array-like, shape (3,)
            観測値 [x_obs, y_obs, theta_obs]

        Returns
        -------
        K : ndarray, shape (3, 3)
            カルマンゲイン行列
        """
        z = np.array(z)

        # 観測モデル（線形）: h(x) = x
        # H = ∂h/∂x = I
        H = np.eye(3)

        # イノベーション: y = z - h(x)
        innovation = z - self.x
        innovation[2] = self._normalize_angle(innovation[2])

        # イノベーション共分散: S = H*P*H^T + R
        S = H @ self.P @ H.T + self.R

        # カルマンゲイン: K = P*H^T*S^(-1)
        K = self.P @ H.T @ np.linalg.inv(S)

        # 状態更新: x = x + K*y
        self.x = self.x + K @ innovation
        self.x[2] = self._normalize_angle(self.x[2])

        # 誤差共分散更新: P = (I - K*H)*P
        I_ = np.eye(3)
        self.P = (I_ - K @ H) @ self.P

        return K

    def filter_step(self, z, u):
        """
        予測と更新を実行

        Parameters
        ----------
        z : array-like, shape (3,)
            観測値 [x_obs, y_obs, theta_obs]
        u : array-like, shape (2,)
            制御入力 [v, omega]

        Returns
        -------
        x : ndarray, shape (3,)
            更新後の状態推定値
        K : ndarray, shape (3, 3)
            カルマンゲイン行列
        """
        self.predict(u)
        K = self.update(z)
        return self.x.copy(), K

    def _normalize_angle(self, angle):
        """
        角度を [-pi, pi] の範囲に正規化

        Parameters
        ----------
        angle : float
            角度 (rad)

        Returns
        -------
        normalized_angle : float
            正規化された角度 (rad)
        """
        while angle > np.pi:
            angle -= 2 * np.pi
        while angle < -np.pi:
            angle += 2 * np.pi
        return angle
