import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="royalherald",
    version="5.0b5",
    author="Stefano Pigozzi",
    author_email="ste.pigozzi@gmail.com",
    description="A websocket communication protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Steffo99/royalherald",
    packages=setuptools.find_packages(),
    install_requires=["websockets>=8.0"],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License"
    ]
)
