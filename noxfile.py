"""Development automation."""

import glob

import nox


@nox.session(reuse_venv=True)
def lint(session):
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)


@nox.session(python=["3.7", "3.8", "3.9"])
def test(session):
    session.install(".[test]")

    default_args = ["--cov-report", "term", "--cov", "release_helper"]
    args = session.posargs or default_args

    session.run("pytest", *args)


@nox.session
def docs(session):
    session.install(".[doc]")
    session.run("sphinx-build", "-b", "html", "docs/", "build/docs")


@nox.session
def release(session):
    package_name = "release_helper"
    version_file = f"src/{package_name}/__init__.py"
    allowed_upstreams = ["git@github.com:pradyunsg/release-helper.git"]

    release_version, next_version = session.posargs  # expect exactly 2 arguments!

    session.install("build", "twine")
    session.install(".")

    # Sanity Checks
    session.run("release-helper", "version-check-validity", release_version)
    session.run("release-helper", "version-check-validity", next_version)
    session.run("release-helper", "directory-check-empty", "dest")

    session.run("release-helper", "git-check-branch", "master")
    session.run("release-helper", "git-check-clean")
    session.run("release-helper", "git-check-tag", release_version, "--does-not-exist")
    session.run("release-helper", "git-check-remote", "origin", *allowed_upstreams)

    # Prepare release commit
    session.run("release-helper", "version-bump", version_file, release_version)
    session.run("git", "add", version_file, external=True)

    session.run(
        "git", "commit", "-m", f"Prepare release: {release_version}", external=True
    )

    # Build the package
    session.run("python", "-m", "build")
    session.run("twine", "check", *glob.glob("dist/*"))

    # Tag the commit
    session.run(
        # fmt: off
        "git", "tag", release_version, "-m", f"Release {release_version}", "-s",
        external=True,
        # fmt: on
    )

    # Prepare back-to-development commit
    session.run("release-helper", "version-bump", version_file, next_version)
    session.run("git", "add", version_file, external=True)
    session.run("git", "commit", "-m", "Back to development", external=True)

    # Push the commits and tag.
    session.run("git", "push", "origin", "main", release_version, external=True)

    # Upload the distributions.
    session.run("twine", "upload", *glob.glob("dist/*"))
