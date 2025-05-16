from setuptools import setup

package_name = 'panda_sim'

setup(
    name=package_name,
    version='0.0.0',
    packages=[],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/panda_sim']),
        ('share/' + package_name + '/launch', ['launch/panda_sim_moveit.launch.py']),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Achieng Mary',
    maintainer_email='achieng75mary@gmail.com',
    description='Simulates Franka Panda with MoveIt and Gazebo',
    license='Apache License 2.0',
)
