import sys
import os

# パスを追加
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.robot_simulator import Robot1D
from src.visualizer import plot_position


def main():
    
    # 初期位置0m
    robot = Robot1D(initial_position=0.0)
    print(f"\n初期位置: {robot.get_position():.1f}m")
    
    # 位置を記録
    positions = [robot.get_position()]
    
    # ロボットを10回動かす
    print("\n--- ロボットを動かす ---")
    for step in range(1, 11):
        # 1m前進
        new_position = robot.move(distance=1.0)
        positions.append(new_position)
        
        print(f"ステップ {step}: 1m前進 → 現在位置 {new_position:.1f}m")
    
    # 結果
    print("\n--- 結果 ---")
    print(f"最終位置: {robot.get_position():.1f}m")
    print(f"予想: {robot.get_position() == 10.0}")
    
    # グラフ表示
    print("\nグラフを表示中...")
    plot_position(positions)

if __name__ == "__main__":
    main()
    