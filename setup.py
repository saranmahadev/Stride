"""
Stride - Sprint-Powered, Spec-Driven Development for AI Agents
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read the long description from README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="stride-ai",
    version="0.1.0",
    author="Stride Development Team",
    author_email="dev@stride.dev",
    description="Sprint-powered, spec-driven development engine for AI agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saranmahadev/Stride",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    package_data={
        "stride": [
            "templates/*.j2",
            "config/*.yaml",
        ],
    },
    python_requires=">=3.11",
    install_requires=[
        "click>=8.1.7",
        "PyYAML>=6.0.1",
        "Jinja2>=3.1.2",
        "python-dateutil>=2.8.2",
        "colorama>=0.4.6",
        "rich>=13.7.0",
        "watchdog>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "flake8>=6.1.0",
            "mypy>=1.7.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "stride=stride.cli.main:cli",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="ai agents development sprint agile spec-driven",
)
