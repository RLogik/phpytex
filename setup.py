import os;
import re;
from pyinstaller_setuptools import setup;

CURRENTDIRECTORY = os.path.dirname(os.path.realpath(__file__));

def get_version() -> str:
    global CURRENTDIRECTORY;
    version = None;
    try:
        with open(os.path.join(CURRENTDIRECTORY, 'dist', 'VERSION')) as fp:
            for line in fp.readlines():
                line = re.sub(r'^[\s\n\r]+|[\s\n\r]+$', r'', line);
                if not re.match(r'^\d+\.\d+\.\d+$', line):
                    continue;
                version = line;
                break;
    except:
        pass;
    if version is None:
        raise ValueError('VERSION file missing in the distribution folder or the value is invalid!');
    return version;

setup(
    name='phpytex',
    version=get_version(),
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
