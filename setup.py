from setuptools import setup, find_packages

setup(
    name='tesla',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'obspy',
        'numpy',
        'scipy',
        'matplotlib',
        'python-math',
        'shutils',
        'rich',
        'pyyaml',
        'pandas',
        'wheel',
    ],
    entry_points={
        'console_scripts': [
            'Tesla = tesla.main:main',
        ],
    },
    author='Guido Maria Adinolfi',
    author_email='guidomaria.adinolfi@unito.it',
    description='TESLA, a Tool for automatic Earthquake low‐frequency Spectral Level estimAtion',
    keywords='earthquake, seismology, source spectra, focal mechanism',
    url='https://github.com/DrGMA/TESLA',
    project_urls={
        'Source Code': 'https://github.com/DrGMA/tesla',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    license='EUROPEAN UNION PUBLIC LICENCE v. 1.2',
    long_description='A tool for automatic Earthquake low‐frequency Spectral Level estimation.',
    long_description_content_type='text/markdown',
)
