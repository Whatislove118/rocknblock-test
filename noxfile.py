import os

import nox

os.environ["PDM_IGNORE_SAVED_PYTHON"] = "1"

DEBUG = "0"


def install_dependencies(session):
    session.install(
        "pdm",
        "setuptools",
        "wheel",
    )
    session.run(
        "pdm",
        "install",
        "-G",
        ":all",
        "--no-self",
        external=True,
    )


@nox.session(python="3.11")
def lint(session: nox.Session):
    install_dependencies(session)
    session.run("mypy", "src", "--config-file=.mypy.ini", env={"PYTHONPATH": "src"})
