from setuptools import setup

setup(
    name='Kasir CLI',
    version='0.1',
    author='TheManusia',
    description='Kasir CLI dengan MySql',
    url='https://github.com/TheManusia',
    python_requires='>=3.7, <4',
    license='DO WHAT THE FUCK YOU WANT TO PUBLIC',
    install_requires=[
        'mysql-connector==2.2.9',
        'python-dotenv==1.0.0',
    ],
    long_description=open('README.md').read(),
)
