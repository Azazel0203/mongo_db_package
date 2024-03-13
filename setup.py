from setuptools import setup, find_packages
from typing import List
from pathlib import Path

HYPEN_E_DOT = '-e .'


# # function to get the requiremtns
# def get_requirements(file_path:str) -> List[str]:
#     requirements = []
#     with open(file_path, 'r') as f:
#         requirements = f.readlines()
#         requirements = [req.replace("\n", "") for req in requirements]
#         if HYPEN_E_DOT in requirements:
#             requirements.remove(HYPEN_E_DOT)
#     requirements.remove('')
#     return requirements


# funtion to ge the long description....same as the readme.md file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()     
   

__version__ = "0.0.3"
REPO_NAME = "mongo_db_package"
PKG_NAME= "mongo_only"
AUTHOR_USER_NAME = "Azazel0203"
AUTHOR_EMAIL = "aadarshkr.singh.cd.ece21@itbhu.ac.in"

setup(
    name=PKG_NAME, # name of the package that we see in the repo
    version=__version__, # provide the version
    author=AUTHOR_USER_NAME, # my name
    author_email=AUTHOR_EMAIL, # my email
    description="A python package for connecting with database.", # description
    long_description=long_description, # 
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}", # will be the github url of the repo
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"}, # location of my actual package
    packages=find_packages(where="src"), # find_packages
    install_requires=["pymongo","pymongo[srv]","dnspython","pandas","numpy","ensure"],
)