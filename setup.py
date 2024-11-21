import os

from setuptools import setup

REQ_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "requirements"
)


def read(fname: str) -> str:
    """Read path for analyze requirements.

    Args:
        fname (object): requirement path
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_requirements(req_file: str) -> tuple:
    """Read requirements file and return packages and git repos separately.

    Args:
        req_file (str) : list of requirements
    """
    requirements = []
    dependency_links = []
    lines = read(req_file).split("\n")
    for line in lines:
        if line.startswith("git+"):
            dependency_links.append(line)
        else:
            requirements.append(line)
    return requirements, dependency_links


core_reqs, core_dependency_links = get_requirements(
    os.path.join(REQ_DIR, "requirements.txt")
)
dev_reqs = read(os.path.join(REQ_DIR, "requirements_dev.txt")).split("\n")

# Metadata goes in setup.cfg
setup(
    version="0.1.0.dev",
    install_requires=core_reqs,
    extras_require={"dev": dev_reqs},
    dependency_links=core_dependency_links,
)
