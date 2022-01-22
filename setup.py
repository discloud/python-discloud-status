from setuptools import setup, find_packages

with open('README.md', 'r') as fp:
    long_desc = fp.read()


setup(name='discloud',
      version='1.0.0b',
      license='MIT',
      description="DisCloud API async wrapper",
      long_description=long_desc,
      long_description_content_type="text/markdown",
      author='Algueem',
      url='https://github.com/discloud/python-discloud-status',
      keywords=['discloud'],
      packages=find_packages(),
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Programming Language :: Python :: 3.10",
          "License :: OSI Approved :: MIT License",
          "License :: OSI Approved :: Apache Software License",
          "Operating System :: OS Independent"
      ]
      )