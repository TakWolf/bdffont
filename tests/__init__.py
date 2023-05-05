import os
import shutil

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
assets_dir = os.path.join(project_root_dir, 'assets')
outputs_dir = os.path.join(project_root_dir, 'build', 'tests')

if os.path.exists(outputs_dir):
    shutil.rmtree(outputs_dir)
os.makedirs(outputs_dir)
