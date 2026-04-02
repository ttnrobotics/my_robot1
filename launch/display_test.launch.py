# import os

# from ament_index_python.packages import get_package_share_directory
# from launch import LaunchDescription
# from launch_ros.actions import Node


# def generate_launch_description():
#     package_name = 'my_robot1'

#     package_share = get_package_share_directory(package_name)

#     urdf_file = os.path.join(package_share, 'urdf', 'panda_collision.urdf')
#     rviz_file = os.path.join(package_share, 'rviz', 'display.rviz')

#     with open(urdf_file, 'r') as infp:
#         robot_description = infp.read()

#     return LaunchDescription([
#         Node(
#             package='robot_state_publisher',
#             executable='robot_state_publisher',
#             name='robot_state_publisher',
#             output='screen',
#             parameters=[{'robot_description': robot_description}],
#         ),
#         Node(
#             package='joint_state_publisher_gui',
#             executable='joint_state_publisher_gui',
#             name='joint_state_publisher_gui',
#             output='screen',
#         ),
#         Node(
#             package='rviz2',
#             executable='rviz2',
#             name='rviz2',
#             output='screen',
#             arguments=['-d', rviz_file],
#         ),
#     ])


from launch import LaunchDescription
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare
from launch.substitution import FindExecutable

def generate_launch_description():
    xacro_file = PathJoinSubstitution(
        [FindPackageShare("my_robot1"),
         "urdf", "my_first_arm.urdf.xacro"])
    
    robot_description = ParameterValue(
        Command([FindExecutable(name="xacro"), " ", xacro_file]),
        value_type=str
    )

    rviz_config = PathJoinSubstitution(
        [FindPackageShare("my_robot1"),
         "rviz", "view_arm.rviz"]
    )

    return LaunchDescription([
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"robot_description": robot_description}]
            ),
        
        Node(package="joint_state_publisher_gui",
             executable="joint_state_publisher_gui",
             name="joint_state_publisher_gui"
            ),

        Node(package="rviz2",
              executable="rviz2",
              name="rviz2",
              arguments=["-d", rviz_config]
            )
    ])



