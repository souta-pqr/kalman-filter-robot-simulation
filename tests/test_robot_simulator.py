"""Tests for Robot Simulators"""
import sys
from pathlib import Path

import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from robot_2d_simulator import Robot2D
from robot_simulator import Robot1D


def test_robot1d_initialization():
    """Test 1D robot initialization"""
    robot = Robot1D(initial_position=0.0, process_noise_std=0.01, observation_noise_std=0.25)
    assert robot.position == 0.0


def test_robot1d_move():
    """Test 1D robot movement"""
    robot = Robot1D(initial_position=0.0, process_noise_std=0.0, observation_noise_std=0.0)
    new_pos = robot.move(distance=1.0)
    assert abs(new_pos - 1.0) < 0.01


def test_robot1d_observe():
    """Test 1D robot observation"""
    robot = Robot1D(initial_position=5.0, process_noise_std=0.0, observation_noise_std=0.0)
    obs = robot.observe()
    assert obs == 5.0


def test_robot2d_initialization():
    """Test 2D robot initialization"""
    robot = Robot2D(
        initial_state=[0.0, 0.0, 0.0],
        process_noise_std=[0.01, 0.01, 0.001],
        observation_noise_std=[0.1, 0.1, 0.01],
    )
    assert np.allclose(robot.state, [0.0, 0.0, 0.0])


def test_robot2d_move():
    """Test 2D robot movement"""
    robot = Robot2D(
        initial_state=[0.0, 0.0, 0.0],
        process_noise_std=[0.0, 0.0, 0.0],
        observation_noise_std=[0.0, 0.0, 0.0],
    )
    
    state = robot.move(control_input=[1.0, 0.0])
    
    # Moving straight with theta=0 should increase x
    assert robot.state[0] > 0.0


def test_robot2d_observe():
    """Test 2D robot observation"""
    robot = Robot2D(
        initial_state=[1.0, 2.0, 0.5],
        process_noise_std=[0.0, 0.0, 0.0],
        observation_noise_std=[0.0, 0.0, 0.0],
    )
    
    obs = robot.observe()
    
    assert len(obs) == 3
    assert obs[0] == 1.0
    assert obs[1] == 2.0
    assert obs[2] == 0.5


def test_robot2d_rotation():
    """Test 2D robot rotation"""
    robot = Robot2D(
        initial_state=[0.0, 0.0, 0.0],
        process_noise_std=[0.0, 0.0, 0.0],
        observation_noise_std=[0.0, 0.0, 0.0],
    )
    
    # Pure rotation
    robot.move(control_input=[0.0, np.pi / 2])
    
    assert np.isclose(robot.state[0], 0.0, atol=1e-5)
    assert np.isclose(robot.state[1], 0.0, atol=1e-5)
    assert np.isclose(robot.state[2], np.pi / 2, atol=1e-5)
