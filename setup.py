from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="commpay",
    version="0.1.0",
    author="Edoardo Ribichesu",
    description="Document builder for generating PDF commercial documents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eribichesu/commpay",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "reportlab>=4.0.0",
        "Pillow>=10.0.0",
        "PyPDF2>=3.0.0",
        "python-dateutil>=2.8.0",
        "pydantic>=2.0.0",
    ],
)
