from setuptools import setup, find_packages

setup(
    name="forge",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "openai",
        "rich",
        "prompt_toolkit",
        "ddgs",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "forge=forge.main:main",
        ],
    },
    author="Milan",
    author_email="milan@example.com",
    description="Autonomous AI Coding Agent",
    long_description=open("README.md").read() if open("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/milan/forge",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
