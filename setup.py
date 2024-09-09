# -*- encoding: utf-8 -*-
# Source: https://packaging.python.org/guides/distributing-packages-using-setuptools/

import io
import re

from setuptools import find_packages, setup

dev_requirements = [
    'flake8',
    'pytest',
]
unit_test_requirements = [
    'pytest',
    'pandas'
]
integration_test_requirements = [
    'pytest',
    'pandas'
]
run_requirements = [
    'fastapi==0.103.2',
    'uvicorn==0.30.0',
    'starlette-exporter==0.7.0',
    'pydantic==1.10.9',
    'numpy==1.23.5',
    'loguru==0.6.0',
    'scikit-learn==1.5.1',
    'category_encoders==2.6.3',
    'python-multipart==0.0.9',
    'joblib==1.4.2',
    'boto3==1.35.14',
    'psycopg2==2.9.9'
]

with io.open('./service/__init__.py', encoding='utf8') as version_f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name="service",
    version=version,
    packages=find_packages(exclude='tests'),
    include_package_data=True,
    description="Predict Price arq 3.0",
    zip_safe=False,
    install_requires=run_requirements,
    extras_require={
         'dev': dev_requirements,
         'unit': unit_test_requirements,
         'integration': integration_test_requirements,
    },
    python_requires='>=3.6',
    classifiers=[
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6'
    ],
    keywords=(),
    entry_points={
        'console_scripts': [
            'service = service.__main__:app'
        ],
    },
)
