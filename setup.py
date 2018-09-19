import io, os, sys
from shutil import rmtree
from setuptools import find_packages, setup, Command

here = os.path.abspath(os.path.dirname(__file__))


class Commands(Command):
    desc = 'Used to build the package'
    options = []

    def init_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            print('[X] could not run setup, OSError caught!')
            pass

        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))
        os.system('twine upload dist/*')
        remove = ['dist', 'build', '__pycache__']
        print('[+] Found OS with Version: {0}'.format(os.sys.version))
        for folder in remove:
            try:
                rmtree(os.path.join(here, folder))
            except Exception:
                pass
        sys.exit(1)

    setup(name='Hypthon', include_package_data=True, keywords=['Hypixel API, Hypthon'], version='1.0-BETA', description='Hypixel API in Python',
          url='https://github.com/eros/Hypthon', author='RapidTheNerd', install_requirements='requirements.txt', python_requires='>=3.6'
          ,
          classifiers=[
              'Development Status :: 1.0 - Beta',
              'Natural Language :: English',
              'Operating System :: OS Independent',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.6',
              'Programming Language :: Python :: 3.7',
              'Topic :: Software Development :: Libraries :: Python Modules',
              'Topic :: Utilities',
          ],)


cmdclass ={
    'cmd': Commands,
    },
