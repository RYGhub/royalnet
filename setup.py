import setuptools
import rpgpack.version

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    install_requires = f.readlines()

setuptools.setup(
    name="rpgpack",
    version=rpgpack.version.semantic,
    author="Stefano Pigozzi",
    author_email="ste.pigozzi@gmail.com",
    description="A Royalnet pack to play D&D by-chat",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Steffo99/rpgpack",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
)
