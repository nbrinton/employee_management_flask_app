from setuptools import setup

setup(
    name='employee_app',
    packages=['employee_app'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
#    setup_requires=[
#        'pytest-runner',
#    ],
    tests_require=[
        'pytest',
    ],
)
