from setuptools import setup, find_packages

setup(name='gym_rubik',
      version='0.0.1',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['gym', 'matplotlib', 'numpy']  # And any other dependencies rubik needs
)
