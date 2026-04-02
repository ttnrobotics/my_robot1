The best learning path is:

1. make a **ROS 2 description package**
2. put an **existing robot URDF/xacro** inside
3. check it in **RViz**
4. run it in **Gazebo**
5. then replace parts step by step to make your **custom robot**

That matches the ROS 2 URDF workflow and Gazebo integration docs for Humble. The ROS 2 docs group URDF, xacro, robot_state_publisher, and Gazebo tutorials together, and Gazebo’s ROS integration for Humble is through `ros_gz` / Gazebo Sim rather than the old Classic workflow. 

---

# 1. The idea you should keep in mind

Think of the robot workflow like this:

**robot description package**
→ contains `urdf/`, `meshes/`, `rviz/`, `launch/`

Then:

* **RViz** uses the URDF to visualize links, joints, TF, and robot shape
* **robot_state_publisher** reads the URDF and publishes TF
* **joint_state_publisher** or **joint_state_publisher_gui** lets you move joints for testing
* **Gazebo** uses the URDF plus physical tags and plugins to simulate the robot

So:

* RViz = “Does my robot description look correct?”
* Gazebo = “Does my robot simulate correctly?”

That is the core separation described in the ROS 2 URDF and Gazebo tutorials.

---

# 2. Recommended package structure

Make one package like this:

```bash
my_robot1/
├── package.xml
├── CMakeLists.txt
├── launch/
│   ├── display.launch.py
│   └── gazebo.launch.py
├── rviz/
│   └── view.rviz
├── urdf/
│   ├── my_robot.urdf
│   └── my_robot.urdf.xacro
├── meshes/
│   ├── visual/
│   └── collision/
└── worlds/
    └── empty.sdf
```

For learning, this package is enough at first.

Use:

* `urdf/` for robot description
* `meshes/` for STL/DAE files
* `launch/` for RViz and Gazebo launch files
* `rviz/` for saved RViz config

---

# 3. Create the package

Inside your workspace:

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake my_robot1
```

Then go inside:

```bash
cd ~/ros2_ws/src/my_robot1
mkdir launch urdf meshes rviz worlds
mkdir -p meshes/visual meshes/collision
```

---

# 4. Put an existing robot in first


# 5. Minimal URDF test first

Before trying a full Panda, first make sure your package and launch flow work.

Create:

`~/franka_ws/src/my_robot1/urdf/test_box.urdf`

```xml
<!-- This is the URDF definition for a simple 2-DOF robotic arm -->
<robot name="two_dof_arm">
  <!-- Links are the rigid parts of the robot. -->
  <!-- 1. The Base Link (The foundation) -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder length="0.05" radius="0.1"/>
      </geometry>
      <origin xyz="0 0 0.025" rpy="0 0 0"/>
      <material name="grey">
        <color rgba="0.5 0.5 0.5 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.05" radius="0.1"/>
      </geometry>
      <origin xyz="0 0 0.025" rpy="0 0 0"/>
    </collision>
  </link>

  <!-- 2. The First Arm Link (The "upper arm") -->
  <link name="link1">
    <visual>
      <geometry>
        <box size="0.5 0.1 0.1"/>
      </geometry>
      <origin xyz="0.25 0 0" rpy="0 0 0"/>
      <material name="orange">
        <color rgba="1.0 0.4 0.0 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.1 0.1"/>
      </geometry>
      <origin xyz="0.25 0 0" rpy="0 0 0"/>
    </collision>
     <inertial>
        <mass value="1.0"/>
        <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <!-- 3. The Second Arm Link (The "forearm") -->
  <link name="link2">
    <visual>
      <geometry>
        <box size="0.4 0.08 0.08"/>
      </geometry>
      <origin xyz="0.2 0 0" rpy="0 0 0"/>
      <material name="blue">
        <color rgba="0.1 0.1 1.0 1.0"/>
      </material>
    </visual>
    <collision>
       <geometry>
        <box size="0.4 0.08 0.08"/>
      </geometry>
      <origin xyz="0.2 0 0" rpy="0 0 0"/>
    </collision>
     <inertial>
        <mass value="0.8"/>
        <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>
  <!-- Joints connect the links and define how they can move. -->

  <!-- 1. The First Joint (Connects base_link to link1) -->
  <joint name="joint1" type="revolute">
    <parent link="base_link"/>
    <child link="link1"/>
    <origin xyz="0 0 0.05" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-3.14" upper="3.14" effort="10" velocity="1.0"/>
  </joint>

  <!-- 2. The Second Joint (Connects link1 to link2) -->
  <joint name="joint2" type="revolute">
    <parent link="link1"/>
    <child link="link2"/>
    <origin xyz="0.5 0 0" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-3.14" upper="3.14" effort="10" velocity="1.0"/>
  </joint>

</robot>
```

This lets you verify the pipeline before debugging a large existing robot.

---

# 6. Add install rules in CMakeLists.txt

Edit `CMakeLists.txt` and add:

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot1)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY launch urdf meshes rviz worlds
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
```

This is important because ROS launch files and package URIs depend on installed package resources being in the share directory.

---

# 7. Edit package.xml

A simple version:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>my_robot1</name>
  <version>0.0.0</version>
  <description>TODO: Package description</description>
  <maintainer email="jungeun@todo.todo">jungeun</maintainer>
  <license>TODO: License declaration</license>

  <buildtool_depend>ament_cmake</buildtool_depend>

  <exec_depend>robot_state_publisher</exec_depend>
  <exec_depend>joint_state_publisher</exec_depend>
  <exec_depend>joint_state_publisher_gui</exec_depend>
  <exec_depend>rviz2</exec_depend>
  <exec_depend>xacro</exec_depend>

  <exec_depend>ros_gz_sim</exec_depend>

  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_lint_common</test_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>

```


---

# 8. Create the RViz file
Create:

`rviz/display.rviz`

```xml
---
```

---

# 9. Create the RViz launch file

Create:

`launch/display.launch.py`

```python
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    package_name = 'my_robot1'

    package_share = get_package_share_directory(package_name)

    urdf_file = os.path.join(package_share, 'urdf', 'panda_collision.urdf')
    rviz_file = os.path.join(package_share, 'rviz', 'display.rviz')

    with open(urdf_file, 'r') as infp:
        robot_description = infp.read()

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description}],
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen',
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_file],
        ),
    ])
```

For a plain `.urdf`, `cat` is okay. For `.xacro`, use `xacro` instead:

```python
robot_description = Command(["xacro ", urdf_file])
```

The ROS URDF tutorials use `robot_state_publisher` with a generated `robot_description` string, and xacro is the standard way to preprocess more complex robot descriptions.

---

# 10. Build and test in RViz

```bash
cd ~/franka_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select my_robot1
source install/setup.bash
ros2 launch my_robot1 display.launch.py
```

In RViz:

* set **Fixed Frame** to `base_link`
* add **RobotModel** if it is not already shown

If the robot appears, your package structure is correct.

Then change `test_box.urdf` to `panda.urdf` in the `lauch file` and rebuild and test it again.

---

# 11. Move to Gazebo after RViz works

Do not go to Gazebo before RViz works.

Gazebo adds more requirements:

* correct inertial tags
* collision tags
* sometimes plugins
* joint interfaces if you want actuation
* possible ros_gz bridge if you want ROS topics bridged

ROS 2 Humble Gazebo docs describe the Gazebo Sim / `ros_gz_sim` workflow, and `ros_gz_sim create` can spawn a URDF from file or parameter. 

---

# 13. Simplest Gazebo test

## 1. Install the Gazebo ROS packages

Run:
```bash
sudo apt update
sudo apt install ros-humble-ros-gz-sim ros-humble-ros-gz-bridge
```
That is the standard Humble Gazebo integration path.

## 2. First test: launch empty Gazebo
```bash
source /opt/ros/humble/setup.bash
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:=empty.sdf
```

If Gazebo opens, the base simulator path is working. gz_sim.launch.py is the official launch entrypoint for Gazebo Sim from ROS 2.


Open another terminal:

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run ros_gz_sim create -name test_box -file ~/franka_ws/src/my_robot1/urdf/test_box.urdf
```

That matches the `ros_gz_sim create` usage described in the package docs. (

If it appears, your URDF can at least be spawned.

---

# 14. Better Gazebo launch from your package

Create:

`launch/gazebo.launch.py`

```python
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_share = FindPackageShare("my_robot1")
    urdf_file = PathJoinSubstitution([pkg_share, "urdf", "test_box.urdf"])

    gazebo = ExecuteProcess(
        cmd=["ros2", "launch", "ros_gz_sim", "gz_sim.launch.py"],
        output="screen"
    )

    spawn = ExecuteProcess(
        cmd=["ros2", "run", "ros_gz_sim", "create",
             "-name", "test_box",
             "-file", urdf_file],
        output="screen"
    )

    return LaunchDescription([
        gazebo,
        spawn
    ])
```

Then:

```bash
ros2 launch my_robot1 gazebo.launch.py
```

---

# 15. Why some robots work in RViz but fail in Gazebo

Very common.

Because RViz mainly needs:

* visual geometry
* TF
* joint tree

Gazebo also needs:

* valid mass and inertia
* collision geometry
* stable joint setup
* sometimes damping/friction
* simulation-compatible tags/plugins

If inertial or collision data is missing or bad, Gazebo may spawn badly, fall apart, explode, or not move.

So the normal learning sequence is:

**URDF visual correctness in RViz first**
→ **physics correctness in Gazebo second**

---

# 16. Existing robot vs custom robot

Here is the best way to understand both.

## Existing robot

Use this to learn the workflow.

You take a known model, for example Panda:

* copy description
* copy meshes
* fix package paths
* display in RViz
* spawn in Gazebo

This teaches:

* package layout
* URDF/xacro structure
* launch files
* mesh path handling
* joint tree understanding

## Custom robot

Use this to learn robot modeling.

You start from:

* `base_link`
* add one link
* add one joint
* add collision
* add inertial
* test in RViz
* test in Gazebo
* repeat

This teaches:

* how to design your own kinematic tree
* how origin/joint axis work
* how inertia and collision matter

---

# 17. Best learning strategy for custom robots

Do not start custom robot from a complicated humanoid or manipulator.

Start with this sequence:

## Stage 1

One box link only

## Stage 2

Two links + one revolute joint

## Stage 3

Three-link arm

## Stage 4

Add meshes

## Stage 5

Add xacro macros

## Stage 6

Add transmissions / ros2_control only when basic simulation works

That is the fastest path to real understanding.

---

# 18. Xacro principle you should remember

Use plain URDF first to understand structure.

Then use xacro when you want:

* repeated links/joints
* reusable macros
* parameters like length/mass/color
* cleaner big robot descriptions

ROS docs explicitly present xacro as the way to make URDF easier to maintain and reuse. ([ROS Documentation][5])

Example:

```xml
<xacro:property name="link_length" value="0.5"/>
```

and later:

```xml
<box size="${link_length} 0.05 0.05"/>
```

So:

* URDF = final robot description
* xacro = templating system that generates URDF

---

# 19. What I recommend you do right now

Follow this exact order:

## Step A

Create `my_robot1`

## Step B

Make `test_box.urdf`

## Step C

Launch it in RViz

## Step D

Spawn it in Gazebo

## Step E

Replace it with your Panda / Franka model

## Step F

After that, make one tiny custom robot from scratch

That way you learn both:

* how to use an existing robot
* how to make your own robot

---

# 20. The key commands collected in one place

```bash
cd ~/franka_ws/src
ros2 pkg create --build-type ament_cmake my_robot1

cd ~/franka_ws/src/my_robot1
mkdir launch urdf meshes rviz worlds
mkdir -p meshes/visual meshes/collision
```

Build:

```bash
cd ~/franka_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select my_robot1
source install/setup.bash
```

RViz test:

```bash
ros2 launch my_robot1 display.launch.py
```

Check URDF:

```bash
check_urdf ~/franka_ws/src/my_robot1/urdf/test_box.urdf
```

If xacro:

```bash
xacro ~/franka_ws/src/my_robot1/urdf/my_robot.urdf.xacro > /tmp/out.urdf
check_urdf /tmp/out.urdf
```

Gazebo:

```bash
ros2 launch ros_gz_sim gz_sim.launch.py
```

Spawn robot:

```bash
ros2 run ros_gz_sim create -name test_box -file ~/franka_ws/src/my_robot1/urdf/test_box.urdf
```

---

# 21. Most common beginner mistakes

1. wrong `package://` path
2. meshes not copied into your package
3. forgot `install(DIRECTORY ...)` in `CMakeLists.txt`
4. forgot to rebuild and `source install/setup.bash`
5. using xacro but launching as plain URDF
6. no inertial/collision for Gazebo
7. bad joint origins or axes
8. fixed frame in RViz not set to `base_link`

---

# 22. My practical advice for you

Since you are learning and also using Franka-related files, the best move is:

* first make a **clean new package** called `my_robot1`
* first verify a **very small URDF**
* then copy your Panda/Franka robot into that package
* then test the same package in RViz and Gazebo

This prevents confusion from large existing codebases.

---

I can write the exact full files for you next:

* `CMakeLists.txt`
* `package.xml`
* `display.launch.py`
* `gazebo.launch.py`
* `test_box.urdf`

ready to copy into your `my_robot1` package.
