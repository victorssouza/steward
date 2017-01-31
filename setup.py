from setuptools import setup

with open('requirements.txt') as f:
	requirements = f.read().splitlines()

setup(name='steward',
      version='0.0.4',
      description='Voice Assistant',
      url='http://github.com/victorssouza/steward',
      author='Victor Santos',
      author_email='vsantos.py@gmail.com',
      license='MIT',
      packages=[''],
 	  install_requires=requirements,
      zip_safe=False)