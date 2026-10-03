#!/usr/bin/python3
# -*- coding: utf-8 -*-
from launch_ros.actions import Node
from launch import LaunchDescription


# this is the function launch system will look for
def generate_launch_description():

    # Position and orientation
    # [X, Y, Z]
    position = [0.0, 5.0, 0.0]
    # [Roll, Pitch, Yaw]
    orientation = [0.0, 0.0, 0.0]
    # Base Name or robot
    robot_base_name = "testbed"

    entity_name = robot_base_name

    # Spawn ROBOT in Gazebo (Harmonic / ros_gz)
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_entity',
        output='screen',
        arguments=['-name',
                   entity_name,
                   '-x', str(position[0]), '-y', str(position[1]
                                                     ), '-z', str(position[2]),
                   '-R', str(orientation[0]), '-P', str(orientation[1]
                                                        ), '-Y', str(orientation[2]),
                   '-topic', '/robot_description'
                   ]
    )

    # Bridge topics between ROS 2 and Gazebo Transport
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_bridge',
        output='screen',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            '/imu@sensor_msgs/msg/Imu[gz.msgs.IMU',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
        ],
    )

    # gz-sim collapses the URDF's fixed joints into 'base_footprint' for physics,
    # so sensor messages carry a gz-scoped frame_id (<model>/base_footprint/<sensor_name>)
    # instead of the original URDF link name that robot_state_publisher broadcasts.
    # These zero-offset static transforms alias the gz-scoped sensor frames onto
    # their real URDF links so consumers (RViz, AMCL, etc.) can resolve the TF chain.
    lidar_frame_bridge = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='lidar_frame_bridge',
        arguments=['--frame-id', 'lidar_link_1',
                   '--child-frame-id', f'{entity_name}/base_footprint/head_hokuyo_sensor'],
    )

    imu_frame_bridge = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='imu_frame_bridge',
        arguments=['--frame-id', 'imu_link_1',
                   '--child-frame-id', f'{entity_name}/base_footprint/imu_link_1'],
    )

    # create and return launch description object
    return LaunchDescription(
        [
            spawn_robot,
            bridge,
            lidar_frame_bridge,
            imu_frame_bridge,
        ]
    )
