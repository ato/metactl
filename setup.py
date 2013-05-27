from setuptools import setup, find_packages
name='metactl'
setup(
    name=name,
    version='0.1.0',
    url='http://www.python.org/pypi/'+name,
    author='Alex Osborne',
    author_email='ato@meshy.org',
    package_dir = {'': 'src'},
    packages=find_packages('src'),
    include_package_data = True,
    install_requires=['setuptools', 'configparser', 'argparse'],
    zip_safe = False,
    entry_points={
        'console_scripts': ['metactl = metactl.main:run'],
        },
    )
