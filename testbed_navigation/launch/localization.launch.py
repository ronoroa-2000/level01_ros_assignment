#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    pkg_testbed_navigation = get_package_share_directory('testbed_navigation')

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true',
    )

    map_arg = DeclareLaunchArgument(
        'map',
        default_value=os.path.join(
            get_package_share_directory('testbed_bringup'), 'maps', 'testbed_world.yaml'),
        description='Full path to the map yaml file to load',
    )

    amcl_params_file_arg = DeclareLaunchArgument(
        'amcl_params_file',
        default_value=os.path.join(pkg_testbed_navigation, 'config', 'amcl_params.yaml'),
        description='Full path to the AMCL parameters file',
    )

    # Reuse the existing map server bring-up so localization.launch.py is self-contained
    map_loader = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_testbed_navigation, 'launch', 'map_loader.launch.py'),
        ),
        launch_arguments={
            'map': LaunchConfiguration('map'),
            'use_sim_time': LaunchConfiguration('use_sim_time'),
        }.items(),
    )

    amcl_node = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[
            LaunchConfiguration('amcl_params_file'),
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
        ],
    )

    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_localization',
        output='screen',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'autostart': True,
            'node_names': ['amcl'],
        }],
    )

    return LaunchDescription([
        use_sim_time_arg,
        map_arg,
        amcl_params_file_arg,
        map_loader,
        amcl_node,
        lifecycle_manager_node,
    ])
