from setuptools import find_packages, setup

setup(name='excelutils',
      version='1.0.0-alpha-9',
      url='https://github.com/SynBioDex/Excel-utilities/',
      license='BSD 3-clause',
      maintainer='Jet Mante',
      maintainer_email='jet.mante@colorado.edu',
      include_package_data=True,
      description='convert excel resources into sbol',
      packages=find_packages(include=['excelutils']),
      long_description=open('README.md').read(),
      install_requires=[],
      zip_safe=False)