import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
  long_description = fh.read()

setuptools.setup(
  name="varman",
  version="0.0.6",
  author="zloss",
  author_email="zlos@foxmail.com",
  description="A dict like variable container, listen for variable changes.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/zlolss/VarMan.py.git",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)