from setuptools import setup, find_packages

setup(
    name="auto_sync",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pyyaml>=5.1",
        "watchdog>=2.1.0",
    ],
    entry_points={
        "console_scripts": [
            "auto_sync=main:main",
        ],
    },
    python_requires=">=3.6",
    author="User",
    description="A tool to automatically synchronize directories using rsync",
)
