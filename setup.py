"""
PhonoCrypt - Phonetic Encryption Engine
Setup configuration
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="phonocrypt",
    version="0.1.0",
    author="PhonoCrypt Team",
    description="A novel encryption engine leveraging phonetic script consistency",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/phonocrypt",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Security :: Cryptography",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "phonemizer>=3.2.1",
        "epitran>=1.24",
        "pandas>=2.2.0",
        "numpy>=1.26.4",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
            "black>=24.1.1",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "phonocrypt=cli.main:main",
        ],
    },
)
