
import sys, os, types
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '{repo_basename}')))


# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', f'{safe_repo_name}')))
# Auto-mock tkinter for headless environments
try:
    import tkinter as tk
except ImportError:
    import sys, types
    class _WidgetMock:
        def __init__(self, *a, **k): self._text = ""
        def config(self, **kwargs): 
            if "text" in kwargs: self._text = kwargs["text"]
        def cget(self, key): return self._text if key == "text" else None
        def get(self): return self._text
        def grid(self, *a, **k): return []
        def pack(self, *a, **k): return []
        def place(self, *a, **k): return []
        def destroy(self): return None
        def __getattr__(self, item): return lambda *a, **k: None
    tk = types.ModuleType("tkinter")
    for widget in ["Tk","Label","Button","Entry","Frame","Canvas","Text","Scrollbar","Checkbutton",
                "Radiobutton","Spinbox","Menu","Toplevel","Listbox"]:
        setattr(tk, widget, _WidgetMock)
    for const in ["N","S","E","W","NE","NW","SE","SW","CENTER","NS","EW","NSEW"]:
        setattr(tk, const, const)
    sys.modules["tkinter"] = tk

import sys
sys.path.insert(0, r'/home/vvdn/projects/sfit_unitest_19_9_2025/cloned_repos/Calculator')

import tkinter as tk
from unittest.mock import MagicMock

from calculator import Calculator

class _WidgetMock(MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.children = {}

    def __setitem__(self, key, value):
        self.children[key] = value

    def __getitem__(self, key):
        return self.children[key]

    def configure(self, **kwargs):
        pass

    def pack(self, **kwargs):
        pass

    def grid(self, **kwargs):
        pass

    def bind(self, **kwargs):
        pass

    def config(self, **kwargs):
        pass

    def mainloop(self):
        pass

def create_mock_calculator():
    mock_tk = _WidgetMock()
    tk.Tk = MagicMock(return_value=mock_tk)
    mock_calculator = Calculator()
    mock_calculator.window = mock_tk
    mock_calculator.display_frame = _WidgetMock()
    mock_calculator.buttons_frame = _WidgetMock()
    mock_calculator.total_label = _WidgetMock()
    mock_calculator.label = _WidgetMock()
    return mock_calculator

def test_calculator_initialization():
    mock_calculator = create_mock_calculator()
    assert mock_calculator.total_expression == ""
    assert mock_calculator.current_expression == ""
    assert isinstance(mock_calculator.window, _WidgetMock)
    assert isinstance(mock_calculator.display_frame, _WidgetMock)
    assert isinstance(mock_calculator.buttons_frame, _WidgetMock)
    assert isinstance(mock_calculator.total_label, _WidgetMock)
    assert isinstance(mock_calculator.label, _WidgetMock)

def test_add_to_expression():
    mock_calculator = create_mock_calculator()
    mock_calculator.add_to_expression("5")
    assert mock_calculator.current_expression == "5"
    mock_calculator.add_to_expression("+")
    assert mock_calculator.current_expression == "5+"

def test_append_operator():
    mock_calculator = create_mock_calculator()
    mock_calculator.current_expression = "123"
    mock_calculator.append_operator("+")
    assert mock_calculator.total_expression == "123+"
    assert mock_calculator.current_expression == ""

def test_clear():
    mock_calculator = create_mock_calculator()
    mock_calculator.current_expression = "123"
    mock_calculator.total_expression = "456"
    mock_calculator.clear()
    assert mock_calculator.current_expression == ""
    assert mock_calculator.total_expression == ""

def test_square():
    mock_calculator = create_mock_calculator()
    mock_calculator.current_expression = "5"
    mock_calculator.square()
    assert mock_calculator.current_expression == "25"

def test_sqrt():
    mock_calculator = create_mock_calculator()
    mock_calculator.current_expression = "25"
    mock_calculator.sqrt()
    assert mock_calculator.current_expression == "5.0"

def test_evaluate_valid_expression():
    mock_calculator = create_mock_calculator()
    mock_calculator.current_expression = "5"
    mock_calculator.total_expression = "2+3"
    mock_calculator.evaluate()
    assert mock_calculator.current_expression == "5"
    assert mock_calculator.total_expression == ""

def test_evaluate_expression_with_operators():
    mock_calculator = create_mock_calculator()
    mock_calculator.current_expression = "5"
    mock_calculator.append_operator("+")
    mock_calculator.current_expression = "3"
    mock_calculator.evaluate()
    assert mock_calculator.current_expression == "8"
    assert mock_calculator.total_expression == ""

def test_evaluate_error_expression():
    mock_calculator = create_mock_calculator()
    mock_calculator.current_expression = "abc"
    mock_calculator.evaluate()
    assert mock_calculator.current_expression == "Error"
    assert mock_calculator.total_expression == ""

def test_bind_keys_return():
    mock_calculator = create_mock_calculator()
    mock_calculator.window.bind.assert_any_call("<Return>", mock_calculator.evaluate)

def test_bind_keys_digits():
    mock_calculator = create_mock_calculator()
    for digit in mock_calculator.digits:
        mock_calculator.window.bind.assert_any_call(str(digit), mock_calculator.add_to_expression)

def test_bind_keys_operators():
    mock_calculator = create_mock_calculator()
    for operator in mock_calculator.operations:
        mock_calculator.window.bind.assert_any_call(operator, mock_calculator.append_operator)

def test_update_label():
    mock_calculator = create_mock_calculator()
    mock_calculator.current_expression = "1234567890123"
    mock_calculator.update_label()
    mock_calculator.label.config.assert_called_once_with(text="12345678901")

def test_update_total_label():
    mock_calculator = create_mock_calculator()
    mock_calculator.total_expression = "2+3"
    mock_calculator.update_total_label()
    mock_calculator.total_label.config.assert_called_once_with(text="2 + 3 ")

if __name__ == "__main__":
    import pytest, sys
    sys.exit(pytest.main([__file__, "-v"]))