from launch import LaunchDescription
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import FindExecutable

def generate_launch_description():
    xacro_file = PathJoinSubstitution(
        [FindPackageShare("my_robot1"),
         "urdf", "2dof_arm.urdf.xacro"])
    
    robot_description = ParameterValue(
        Command([FindExecutable(name="xacro"), " ", xacro_file]),
        value_type=str
    )

    rviz_config = PathJoinSubstitution(
        [FindPackageShare("my_robot1"),
         "rviz", "view_1dof_arm.rviz"]
    )

    return LaunchDescription([
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            output="screen",
            parameters=[{"robot_description": robot_description}]
            ),
        Node(package="joint_state_publisher_gui",
             executable="joint_state_publisher_gui",
             name="joint_state_publisher_gui",
             output="screen"
            ),
        Node(package="rviz2",
              executable="rviz2",
              name="rviz2",
              output="screen",
              arguments=["-d", rviz_config]
            )
    ])