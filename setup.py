import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CMPE295", # Replace with your own username
    version="0.0.1",
    author="Kun Su",
    author_email="kun.su@sjsu.edu",
    description="https://github.com/KunSu/cmpe295",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KunSu/cmpe295",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)