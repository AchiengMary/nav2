from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
import xacro

def generate_launch_description():
    # Paths
    panda_description_pkg = get_package_share_directory('moveit_resources_panda_description')
    panda_moveit_pkg = get_package_share_directory('moveit_resources_panda_moveit_config')
    gazebo_ros_pkg = get_package_share_directory('gazebo_ros')

    # Process xacro
    xacro_file = os.path.join(panda_description_pkg, 'urdf', 'panda_arm_hand.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    robot_description = {'robot_description': robot_description_config.toxml()}

    return LaunchDescription([
        # Start Gazebo
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(gazebo_ros_pkg, 'launch', 'gazebo.launch.py')
            )
        ),

        # Spawn robot in Gazebo
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-topic', 'robot_description',
                '-entity', 'panda'
            ],
            output='screen'
        ),

        # Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[robot_description],
            output='screen'
        ),

        # Start MoveIt (RViz, move_group, etc.)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(panda_moveit_pkg, 'launch', 'demo.launch.py')
            )
        ),
    ])

