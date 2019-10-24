import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    install_requires = f.readlines()

setuptools.setup(
    name="{packname}",
    version="0.1",
    author="{packauthorname}",
    author_email="{packauthoremail}",
    description="{packdescription}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="{packgithublink}",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
)
