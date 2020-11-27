from setuptools import find_packages, setup
setup(
    name = 'nswses_identity',
    packages=find_packages(include=['nswses_identity']),
    version='0.1.0',
    description='A library for retrieving credentials to interact with the Beacon frontend and API',
    author='Brendan Leo',
    license='MIT',
)
