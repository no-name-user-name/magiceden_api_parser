from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["requests>=2.28.1", "undetected_chromedriver>=3.1.5.post4"]

setup(
    name='magiceden-api-parser',
    version='0.2',
    license='GPL2',
    author='no-name-user-name',
    url='https://github.com/no-name-user-name',
    description='MagicEden API Parser',
    packages=find_packages(),
    install_requires=requirements,
    author_email='97606234+no-name-user-name@users.noreply.github.com',
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
