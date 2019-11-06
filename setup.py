from setuptools import setup, find_packages


with open('README.md', 'r') as fp:
    long_desc = fp.read()


setup(name='discloud-status',
      version='0.1.0',
      license='MIT',
      description='Esse módulo Python funciona apenas no Linux, e foi criado exclusivamente para atender os usuários da discloudbot.com',
      long_description=long_desc,
      long_description_content_type="text/markdown",
      author='Algueem',
      url='https://github.com/discloud/python-discloud-status',
      keywords=['discloud', 'discloud-status'],
      packages=find_packages(),
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8"
          "License :: OSI Approved :: MIT License",
          "License :: OSI Approved :: Apache Software License",
          "Operating System :: POSIX :: Linux"
      ]
      )
