from provcore import __version__


def test_backend_package_imports() -> None:
    assert __version__ == "0.1.0"
