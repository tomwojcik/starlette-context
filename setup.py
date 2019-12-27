from distutils.core import setup

setup(
  name='starlette_context',
  packages=['starlette_context'],
  version='0.1',
  license='MIT',
  description='Middleware for Starlette (and FastAPI) '
                'that allows you to store and access context data, '
                'like correlation id or metadata.',
  author='Tomasz Wojcik',
  url='https://github.com/tomwojcik',
  download_url='https://github.com/tomwojcik/starlette-context/archive/0.1.tar.gz',
  keywords=['starlette', 'fastapi'],
  install_requires=[
          'starlette',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
