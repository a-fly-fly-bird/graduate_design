from setuptools import setup, find_packages


def _get_requirements(path):
    with open(path) as f:
        data = f.readlines()
    return data


setup(
    name="gaze",
    version="0.2.1",
    python_requires='>=3.6',
    packages=find_packages(exclude=('tests',)),
    install_requires=_get_requirements('requirements.txt'),
    # This tells setuptools to install any data files it finds in your packages.
    include_package_data=True,
    # https://stackoverflow.com/a/14159430/19547229
    # package_data={
    #     # If any package contains *.txt or *.rst files, include them:
    #     '': ['*.txt', '*.rst'],
    #     # And include any *.msg files found in the 'hello' package, too:
    #     'gaze': ['assets/*', 'data/*'],
    # },
    # 在 /usr/local/bin下 生成命令
    entry_points={
        'console_scripts': [
            'gaze = gaze.main:main',
        ],
    },

    # metadata to display on PyPI
    author="Lucas Tan",
    author_email="lucas.y.tan@outlook.com",
    description="Demo Package",
    keywords="gaze estimation",
    url="https://github.com/a-fly-fly-bird/graduate_design",  # project home page, if any
    project_urls={
        "Bug Tracker": "https://github.com/a-fly-fly-bird/graduate_design",
        "Documentation": "https://github.com/a-fly-fly-bird/graduate_design",
        "Source Code": "https://github.com/a-fly-fly-bird/graduate_design",
    },
    classifiers=[
        'License :: OSI Approved :: Python Software Foundation License'
    ]
)
