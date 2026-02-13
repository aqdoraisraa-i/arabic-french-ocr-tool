"""Setup script for Arabic-French OCR Tool."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="arabic-french-ocr-tool",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="OCR application for Arabic and French text extraction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aqdoraisraa-i/arabic-french-ocr-tool",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "arabic-french-ocr=src.main:main",
        ],
    },
)
