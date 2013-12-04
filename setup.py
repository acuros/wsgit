import os.path
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from wsgit import VERSION


def readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
        return f.read()


setup(name='WSGIT',
      packages=['wsgit'],
      version=VERSION,
      description='WSGI Server on TCP',
      long_description=readme(),
      license='MIT License',
      author='Seungyeon Kim(Acuros)',
      author_email='acuroskr' '@' 'gmail.com',
      tests_require=[
          'pyOpenSSL',
      ],
      test_suite='tests',
      install_requires=[
          'bson>=0.3.3',
      ],
      entry_points={
          'console_scripts': [
              'wsgit=wsgit.server:run'
          ]
      },
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Internet :: WWW/HTTP :: WSGI',
          'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
      ])
