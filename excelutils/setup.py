from setuptools import find_packages, setup

setup(name='excel-sbol-utils',
      version='1.0.0-alpha-9',
      url='https://github.com/SynBioDex/Excel-utilities/',
      license='BSD 3-clause',
      maintainer='Jet Mante',
      maintainer_email='jet.mante@colorado.edu',
      include_package_data=True,
      description='help convert excel resources into sbol',
      packages=find_packages(include=['excel_sbol_utils']),
      long_description=open('README.md').read(),
      install_requires=['sbol3>=1.0.1'],
      zip_safe=False)
