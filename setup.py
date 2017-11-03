"""
Converts cookiecutter v1 template to v2 template.
Cookiecutter v2.x is required to subsequently use the converted v2 template.
"""
from setuptools import find_packages, setup

dependencies = ['click']

setup(
    name='cctconvert',
    version='1.0.0',
    url='https://github.com/eruber/cookiecutter-template-convert',
    license='MIT',
    author='E.R. Uber',
    author_email='eruber@gmail.com',
    description='Converts cookiecutter v1 template to v2',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    setup_requires=['pytest-runner', ],
    tests_require=['pytest', 'pytest-cov', 'pytest-mock'],
    entry_points={
        'console_scripts': [
            'cctconvert = cctconvert.cctconvert:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
