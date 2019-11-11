import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    install_requires = f.readlines()

setuptools.setup(
    name="keipack",
    version="0.1",
    author="Stefano Pigozzi",
    author_email="ste.pigozzi@gmail.com",
    description="A mysterious AI assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Steffo99/keipack",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
)
