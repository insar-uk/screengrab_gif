from setuptools import setup

setup(
    name='screengrab_gif',
    version='1.0.0',
    description='A Python program to capture screenshots and convert them into GIFs',
    author='Stewart Agar',
    author_email='s.agar16@imperial.ac.uk',
    packages=['screen_gif'],
    install_requires=['pywin32', 'PyQt5', 'imageio'],
    entry_points={
        'console_scripts': [
            'screengrab_gif = screengrab_gif.main_window:main'
        ]
    },
)
