from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='utilities',
    version='0.1',
    description='Code I always need.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Björn Schrammel',
    author_email='your-email@example.com',
    url='https://github.com/i3iorn/utilities.git',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
