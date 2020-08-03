from setuptools import setup

setup(
    name="auth_server",
    version="1.0.0",
    description="dashboard",
    url="https://github.com/liverpool1026/auth_server",
    author="Kevin Hwa",
    author_email="",
    packages=["auth_server"],
    include_package_data=True,
    install_requires=["boto3", "pyotp", "passlib"],
)
