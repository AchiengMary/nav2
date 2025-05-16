import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/achieng/robotics_projects/pick_n_place/install/panda_sim'
