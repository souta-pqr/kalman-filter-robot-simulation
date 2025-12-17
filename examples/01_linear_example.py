import sys
import os
import numpy as np

# パスを追加
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.robot_simulator import Robot1D
from src.visualizer import plot_with_observations


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
    
    # ロボットを10回動かす
    print("\n--- シミュレーション ---")
    for step in range(1, 11):
        # 1m前進
        true_pos = robot.move(distance=1.0)
        obs = robot.observe()
        
        true_positions.append(true_pos)
        observations.append(obs)
        
        print(f"ステップ {step}: 真の位置={true_pos:.1f}m, 観測値={obs:.2f}m, 誤差={obs-true_pos:.2f}m")
    
    # 結果
    print("\n--- 結果 ---")
    print(f"最終の真の位置: {robot.get_position():.1f}m")
    print(f"最後の観測値: {observations[-1]:.2f}m")
    print(f"観測誤差: {observations[-1] - robot.get_position():.2f}m")
    
    # グラフ表示
    print("\nグラフを表示中...")
    plot_with_observations(true_positions, observations)


if __name__ == "__main__":
    main()
    