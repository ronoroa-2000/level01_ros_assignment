#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    pkg_testbed_gazebo = get_package_share_directory('testbed_gazebo')

    # Gazebo (Harmonic / ros_gz) launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py'),
        ),
        launch_arguments={
            'gz_args': [LaunchConfiguration('world'), ' -r'],
        }.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument(
          'world',
          default_value=os.path.join(pkg_testbed_gazebo, 'worlds', 'testbed_playground.world'),
          description='SDF world file'),
        gazebo,
    ])
