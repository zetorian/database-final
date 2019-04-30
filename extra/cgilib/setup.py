from setuptools import setup, find_packages

install_requires= [
    'cookies>=1.0'
    'pymacaroons>=0.10'
] 

setup(
    name="cgilib",
    version="0.1",
    packages=find_packages(),
    author="Ben Metzger",
    description="Library for easy cookie based login through python",
    #url="http://github.com/UND-UCAS/crypt-swarm",
    install_requires=install_requires,

    #entry_points={
    #    'console_scripts': [
    #        'cswarmd=cswarmd.__main__:main',
    #    ],
    #}
)
