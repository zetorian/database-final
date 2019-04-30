from setuptools import setup, find_packages

install_requires= [
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
    zip_safe=False

    #entry_points={
    #    'console_scripts': [
    #        'cswarmd=cswarmd.__main__:main',
    #    ],
    #}
)
