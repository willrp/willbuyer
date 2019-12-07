import sys
import click
import pytest


@click.group()
def cli():
    pass


@cli.command()
def test():
    """Run tests"""
    print("RUN TESTS")
    sys.exit(pytest.main(["backend/tests/", "-v", "--tb", "short", "-m", "dev", "--disable-warnings"]))


@cli.command()
def test_cov():
    """Run tests with coverage"""
    print("RUN TESTS WITH COVERAGE")
    sys.exit(pytest.main(["backend/tests/", "-v", "--tb", "short", "--cov-report", "term:skip-covered", "--cov=backend", "--disable-warnings"]))


@cli.command()
def test_cov_html():
    """Run tests"""
    print("RUN TESTS WITH COVERAGE ON HTML INTERFACE")
    sys.exit(pytest.main(["backend/tests/", "-v", "--tb", "short", "--cov-report", "html:cov_html", "--cov=backend"]))


if __name__ == "__main__":
    cli()
