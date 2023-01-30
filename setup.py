from setuptools import setup

setup(
	  name='Autogasuptake', 
	  version='1.1.1',  
	  description='::A tool to automatically treat the data and plot the gas uptake curve::',
	  long_description= 'After major revisions...', 
	  author='wjgoarxiv',
	  author_email='woo_go@yahoo.com',
	  url='https://pypi.org/project/autogasuptake/',
	  license='MIT',
	  py_modules=['autogasuptake'],
	  python_requires='>=3.8', #python version required
	  install_requires = [
    'pandas',
	  'matplotlib',
	  'numpy',
    'scipy', 
	  'scikit-learn',
	  'scipy',
	  'pandas',
	  'seaborn',
	  'argparse',
    'pyfiglet',
    'tabulate',
	  ],
	  packages=['Autogasuptake'],
		entry_points={
			'console_scripts': [
				'autogasuptake = Autogasuptake.__main__:main'
			]
		}
	)