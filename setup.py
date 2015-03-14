from setuptools import setup, find_packages  # Always prefer setuptools over distutils

long_description = """This program accepts any text and searchs inside every IP address. With
each of those IP addresses, geolocate queries Maxmind GeoIP database (http://www.maxmind.com)_
to look for the city and country where IP address or URL is located.

Geolocate is designed to be used in console with pipes and redirections along
with applications like traceroute, etc. Geolocate's output is the same text
than input but IP addresses are going to have appended its country and city and long-lat
coordinates (depending on verbosity level).

More info in: https://bitbucket.org/dante_signal31/geolocate
"""

setup(name="geolocate",
      version="1.0.0",
      description="This script scans given text to find urls and IP addresses. "
                  "The output is the same text but every url and IP address "
                  "is going to have its geolocation data appended.",
      long_description=long_description,
      author="Dante Signal31",
      author_email="dante.signal31@gmail.com",
      license="GPLv3",
      url="https://bitbucket.org/dante_signal31/geolocate",
      download_url="https://bitbucket.org/dante_signal31/geolocate/downloads",
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Information Technology',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: System Administrators',
                   'Intended Audience :: Telecommunications Industry',
                   'Intended Audience :: Other Audience',
                   'Topic :: System :: Networking',
                   'Topic :: Security',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.4'],
      keywords="geolocation ip addresses",
      install_requires=["geoip2>=2.1.0", "maxminddb>=1.1.1", "requests>=2.5.0"],
      zip_safe=False,
      # TODO: This exclude is not working, tests package is still included in
      # packages. It's a bug in pip:
      #     https://bitbucket.org/pypa/wheel/issue/99/cannot-exclude-directory
      # Until it is fixed, the workaround is to create a MANIFEST.in file where
      # you prune your undesired files and compile package in two steps:
      #     python setup.py sdist
      #     pip wheel --no-index --no-deps --wheel-dir dist dist/*.tar.gz
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*",
                                      "tests", "*tests*"]),
      entry_points={'console_scripts': ['geolocate=geolocate.glocate:main', ],
                    },
      package_data={"geolocate": ["etc/geolocate.conf",
                                  "local_database/empty.txt"], }
      )
