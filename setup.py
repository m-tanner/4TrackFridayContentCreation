from setuptools import setup, find_packages

install_requirements = [
    "boto3",
    "botocore~=1.14",
    "six~=1.12",
    "google-cloud-storage",
    "beautifulsoup4",
]

test_requirements = [
    "pytest",
    "pytest-cov",
    "black",
    "flake8",
    "pylint",
]

setup(
    name="FourTrackFriday",
    version="0.1",
    packages=find_packages(),
    url="fourtrackfriday.com",
    license="",
    author="Michael Tanner",
    author_email="tanner.mbt@gmail.com",
    description="Code for Four Track Friday Content Creation",
    install_requires=install_requirements,
    extras_require={"tests": [test_requirements]},
    entry_points={"console_scripts": ["ftf_content=src.app.main:main"]},
)
