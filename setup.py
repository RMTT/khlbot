import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="khlbot",
    version="0.22",
    author="RMT",
    author_email="d.rong@outlook.com",
    description="Robot framework for KaiHeiLa",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RMTT/khlbot",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'websockets'],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
