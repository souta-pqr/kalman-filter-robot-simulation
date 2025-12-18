import sys
import os
import numpy as np

# パスを追加
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.robot_simulator import Robot1D
from src.linear_kf import LinearKalmanFilter
from src.visualizer import plot_with_estimates, plot_kalman_gain


def main():
    
    # 乱数シード
    np.random.seed(42)
    
    # ロボットを作成（プロセスノイズあり）
    process_noise = 0.1
    observation_noise = 0.5
    robot = Robot1D(initial_position=0.0,
                    process_noise_std=process_noise,
                    observation_noise_std=observation_noise)
    
    # カルマンフィルタの初期化
    Q = process_noise**2  # プロセスノイズの共分散
    R = observation_noise**2  # 観測ノイズの共分散
    kf = LinearKalmanFilter(Q=Q, R=R, x0=0.0, P0=1.0)
    
    print(f"\nプロセスノイズ Q: {Q:.4f}")
    print(f"観測ノイズ R: {R:.2f}")
    print(f"初期位置: {robot.get_position():.1f}m")
    print(f"初期予測誤差 P: {kf.P}")
    
    # データ記録
    true_positions = [robot.get_position()]
    observations = [robot.observe()]
    estimates = [kf.x]
    kalman_gains = []
    
    # ロボットを10回動かす
    print("\n--- シミュレーション ---")
    for step in range(1, 11):
        # 1m前進（ノイズあり）
        true_pos = robot.move(distance=1.0)
        obs = robot.observe()
        
        true_positions.append(true_pos)
        observations.append(obs)
        
        # カルマンフィルタで推定
        estimate, K = kf.filter_step(z=obs, u=1.0)
        
        estimates.append(estimate)
        kalman_gains.append(K)
        
        # 実際の移動量
        actual_move = true_pos - true_positions[-2]
        print(f"ステップ {step}: 真値={true_pos:.2f}m(移動{actual_move:.2f}m), "
              f"観測={obs:.2f}m, 推定={estimate:.2f}m, K={K:.3f}")
    
    # 結果
    print("\n--- 結果 ---")
    print(f"最終の真の位置: {robot.get_position():.2f}m")
    print(f"最後の観測値: {observations[-1]:.2f}m")
    print(f"最後の推定値: {estimates[-1]:.2f}m")
    print(f"最終カルマンゲイン: {kalman_gains[-1]:.3f}")
    print(f"最終予測誤差: {kf.P:.4f}")
    
    # 誤差計算
    errors = [abs(t - e) for t, e in zip(true_positions[1:], estimates[1:])]
    mean_error = np.mean(errors)
    print(f"\n平均推定誤差: {mean_error:.2f}m")
    
    # グラフ表示
    print("\nグラフを表示中...")
    plot_with_estimates(true_positions, observations, estimates)
    plot_kalman_gain(kalman_gains)

if __name__ == "__main__":
    main()
    