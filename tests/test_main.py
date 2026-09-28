import pytest
from main import validate_tool_args, execute_tool,parse_user_input, run_tool

def test_validate_tool_args_help():
    """Test that '--help' is accepted as a valid argument regardless of tool support."""
    tool = {"name": "Primarch Scraper", "args_supported": True, "args_help": ["--no-headless"]}
    assert validate_tool_args(tool, ["--help"]) is True
    assert validate_tool_args(tool, ["--no-headless"]) is False

def test_validate_tool_args_no_args_support():
    """Test that only '--help' is accepted when args are not supported."""
    tool = {"name": "Port Scanner", "args_supported": False}
    assert validate_tool_args(tool, ["--help"]) is True
    assert validate_tool_args(tool, ["--some-arg"]) is False    

def test_parse_user_input(monkeypatch):
    """Test parsing of user input with an argument string."""
    monkeypatch.setattr("builtins.input", lambda _: "5 --send-email")
    choice, args = parse_user_input()
    assert choice == "5"
    assert args == ["--send-email"]

def test_run_tool_exit():
    """Test that selecting the 'exit' option raises SystemExit."""
    feature_menu = {"10": {"script": "exit", "name": "Exit", "args_supported": False}}
    with pytest.raises(SystemExit):
        run_tool("10", [], feature_menu)

def test_run_tool_invalid_choice():
    """Test that an invalid tool choice returns False."""
    feature_menu = {"1": {"script": "test.py", "name": "Test", "args_supported": False}}
    assert run_tool("999", [], feature_menu) is False

def test_execute_tool_type_error():
    """Test that execute_tool raises KeyError if required keys are missing."""
    with pytest.raises(KeyError):
        execute_tool({}, [], True) 

