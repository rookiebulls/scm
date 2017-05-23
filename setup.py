from setuptools import setup, find_packages


setup(
    name='scm',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
            'Click',
            'requests',
            'pygments',
            'prompt-toolkit',
            'six'
    ],
    entry_points='''
            [console_scripts]
            scm=scm.scm:cli
        ''',
)
