import pytest
from src.utils.validator import (
    validate_input,
    validate_port,
    get_ip,
    get_port_range,
    validate_paramiko_input
)


def test_validate_input():
    '''Tests for validate_input'''
    assert validate_input("192.168.1.1") == ("ip", "192.168.1.1")
    assert validate_input("example.com") == ("domain", "example.com")
    assert validate_input("not-valid-@#$") == (None, "not-valid-@#$")

def test_validate_port():
    """Tests for validate_port"""
    assert validate_port("8080") == 8080
    with pytest.raises(ValueError):
        validate_port("abc")

def test_get_ip(monkeypatch):
    """Tests for get_ip with mocked input"""
    monkeypatch.setattr("builtins.input", lambda _: "192.168.1.1")
    assert get_ip() == "192.168.1.1"
    monkeypatch.setattr("builtins.input", lambda _: "2001:0db8:85a3:0000:0000:8a2e:0370:7334")
    assert get_ip() == "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    inputs = iter(["invalid", "192.168.1.1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert get_ip() == "192.168.1.1"

def test_get_port_range(monkeypatch):
    """Tests for get_port_range with mocked input"""
    monkeypatch.setattr("builtins.input", lambda _: "80-100")
    assert get_port_range() == (80, 100)
    monkeypatch.setattr("builtins.input", lambda _: "8080 - 8090")
    assert get_port_range() == (8080, 8090)
    inputs = iter(["invalid", "1000-2000"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert get_port_range() == (1000, 2000)

def test_validate_paramiko_input():
    """ Tests for validate_paramiko_input"""
    assert validate_paramiko_input("192.168.1.1") == "192.168.1.1"
    assert validate_paramiko_input("server.example.com") is True
    assert validate_paramiko_input("invalid@domain") is False