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
    description='(PH(p)y)TeX and (PH(p)y)create',
    long_description='README.md',
    long_description_content_type='text/markdown',
    url='https://github.com/RLogik/',
    author='RLogik',
    author_email='author@email.com',
    license='PYTHON',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    packages=[
        'src',
        'src/core',
        'src/info',
        'src/values',
        'src/types',
        'src/programmes',
        'src/programmes/create',
        'src/programmes/examples',
        'src/programmes/transpile',
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
        # 'oas==0.1.13', # installs package 'pyyaml', 'yaml', usw.
        'pyyaml==5.3.1', # installs package 'yaml'
        'typing>=3.7.4.3',
        # 'logging>=0.4.9.6', # no longer use this.
        'gitignore_parser==0.0.6',
    ],
    entry_points={
        'console_scripts': ['phpytex=src.__main__:main'], # note only one entry point allowed!
    },
);
