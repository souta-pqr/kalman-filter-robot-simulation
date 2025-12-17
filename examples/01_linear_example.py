import sys
import os
import numpy as np

# パスを追加
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.robot_simulator import Robot1D
from src.visualizer import plot_with_estimates


def main():
    
    # 乱数シード
    np.random.seed(42)
    
    # ロボットを作成
    observation_noise = 0.5
    robot = Robot1D(initial_position=0.0, observation_noise_std=observation_noise)
    print(f"\n観測ノイズ: 標準偏差 {observation_noise}m")
    print(f"初期位置: {robot.get_position():.1f}m")
    
    # データ記録
    true_positions = [robot.get_position()]
    observations = [robot.observe()]
    estimates = [observations[0]]  # 最初は観測値をそのまま使う
    
    # 重み（観測値をどれだけ信じるか）
    alpha = 0.7  # 0.7 = 観測値を70%信じる
    
    print(f"\n重み α = {alpha} (観測値を{alpha*100:.0f}%信じる)")
    
    # ロボットを10回動かす
    print("\n--- シミュレーション ---")
    for step in range(1, 11):
        # 1m前進
        true_pos = robot.move(distance=1.0)
        obs = robot.observe()
        
        true_positions.append(true_pos)
        observations.append(obs)
        
        # 推定: 前回の推定値 + 移動量 と 観測値を組み合わせる
        prediction = estimates[-1] + 1.0  # 前回の推定 + 1m移動
        estimate = (1 - alpha) * prediction + alpha * obs
        estimates.append(estimate)
        
        print(f"ステップ {step}: 真値={true_pos:.1f}m, 予測={prediction:.2f}m, 観測={obs:.2f}m, 推定={estimate:.2f}m")
    
    # 結果
    print("\n--- 結果 ---")
    print(f"最終の真の位置: {robot.get_position():.1f}m")
    print(f"最後の観測値: {observations[-1]:.2f}m")
    print(f"最後の推定値: {estimates[-1]:.2f}m")
    
    # 誤差計算
    obs_error = abs(observations[-1] - robot.get_position())
    est_error = abs(estimates[-1] - robot.get_position())
    print(f"\n観測値の誤差: {obs_error:.2f}m")
    print(f"推定値の誤差: {est_error:.2f}m")
    
    if obs_error > 0:
        print(f"改善率: {(1 - est_error/obs_error)*100:.1f}%")
    
    # グラフ表示
    print("\nグラフを表示中...")
    plot_with_estimates(true_positions, observations, estimates)


if __name__ == "__main__":
    main()
    