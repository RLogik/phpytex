from pyinstaller_setuptools import setup;

setup(
    name='phpytex',
    version='2.0.0',
    description='(Ph(P)y)TeX and (Ph(P)y)create',
    long_description='README.md',
    long_description_content_type='text/markdown',
    url='https://github.com/RLogik/bla',
    author='RLogik',
    author_email='rbitlogik@gmail.com',
    license='PYTHON',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    packages=[
        'src',
        'src/core',
        'src/create',
        'src/transpiler',
    ],
    include_package_data=True,
    requires=[
        're',
        'os',
        'sys',
        'copy',
        'subprocess',
        'traceback',
        'json',
    ],
    install_requires=[
        'setuptools',
        'typing',
        'logging',
        'PyYAML', # installs package 'yaml'
        'gitignore_parser',
    ],
    entry_points={
        'console_scripts': ['phpytex=src.__main__:main'], # note only one entry point allowed!
    },
);
