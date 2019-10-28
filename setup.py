import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name='molly-py',
    version='0.1.0',
    description='A multithreaded TCP port scanner.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(
        exclude=['docs', 'tests']
    ),
    url="https://github.com/Zabanaa/molly",
    author="Karim C",
    author_email="karim.cheurfi@gmail.com",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Security'
    ],
    keywords="multithreaded tcp port scanner",
    python_requires='>=3.7',
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'molly=molly.cli:cli'
        ]
    }
)