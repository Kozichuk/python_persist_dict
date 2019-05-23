import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="persistence-dict",
    version="0.0.1a0",
    author="Yaroslav Kozichuk",
    description="Dictionary which saving values to filesystem",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kozichuk/python_persist_dict",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
