from setuptools import find_packages, setup

setup(
    name='pybeacon',
    version='0.2.0',
    description='A library for retrieving credentials to interact with the Beacon frontend and API',
    author='Brendan Leo',
    license='MIT',
    packages=find_packages(include=['pybeacon']),
    install_requires=[
        'requests-html',
    ],
)
