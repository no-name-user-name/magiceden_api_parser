from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["requests>=2.28.1", "undetected_chromedriver>=3.1.5.post4"]

setup(
    name='magiceden_api_parser',
    version='0.26',
    license='GPL2',
    author='no-name-user-name',
    url='https://github.com/no-name-user-name/magiceden_api_parser',
    description='MagicEden API Parser',
    packages=find_packages(),
    install_requires=requirements,
    author_email='dimazver61@gmail.com',
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
