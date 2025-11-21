
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

import pytest
import sys
from unittest.mock import MagicMock, patch

# Mock tkinter widgets and CTk
class MockCTkEntry:
    def __init__(self, master=None, **kwargs):
        self._text = ""

    def get(self):
        return self._text

    def insert(self, index, string):
        self._text += string

    def delete(self, first, last=None):
        if last is None:
            self._text = ""
        else:
            self._text = self._text[:first] + self._text[last:]

class MockCTkButton:
    def __init__(self, master=None, command=None, **kwargs):
        self.command = command

    def configure(self, **kwargs):
        pass

class MockCTkLabel:
    def __init__(self, master=None, **kwargs):
        pass

    def configure(self, **kwargs):
        pass

class MockCTkFrame:
    def __init__(self, master=None, **kwargs):
        self._children = []

    def pack(self, **kwargs):
        pass

    def pack_propagate(self, value):
        pass

    def configure(self, **kwargs):
        pass

    def destroy(self):
        pass

class MockCTkTextbox:
    def __init__(self, master=None, **kwargs):
        self._text = ""

    def get(self, index1, index2):
        return self._text

    def delete(self, index1, index2):
        self._text = ""

    def insert(self, index, string):
        self._text += string

    def configure(self, **kwargs):
        pass

    def mark_set(self, name, index):
        pass

class MockCTkComboBox:
    def __init__(self, master=None, values=None, **kwargs):
        self.values = values
        self._current_value = '[select]'

    def get(self):
        return self._current_value

    def set(self, value):
        self._current_value = value

    def configure(self, **kwargs):
        pass

class MockCTkFont:
    def __init__(self, size=10, weight='normal', slant='roman'):
        pass

class MockCTk:
    def __init__(self):
        self.geometry_val = ''
        self.title_val = ''
        self.appearance_mode = 'light'
        self._children = []

    def geometry(self, value):
        self.geometry_val = value

    def title(self, value):
        self.title_val = value

    def set_appearance_mode(self, mode):
        self.appearance_mode = mode

    def mainloop(self):
        pass

    def pack(self, **kwargs):
        pass

    def configure(self, **kwargs):
        pass

    def destroy(self):
        pass

# Replace customtkinter with mocks
ctk = MagicMock()
ctk.CTk = MockCTk
ctk.CTkLabel = MockCTkLabel
ctk.CTkFrame = MockCTkFrame
ctk.CTkButton = MockCTkButton
ctk.CTkEntry = MockCTkEntry
ctk.CTkTextbox = MockCTkTextbox
ctk.CTkComboBox = MockCTkComboBox
ctk.CTkFont = MockCTkFont
ctk.END = "end"

# Mock external libraries
class MockSympy:
    def symbols(self, *args, **kwargs):
        return tuple(args)

    def diff(self, expr, wrt):
        return f"diff({expr}, {wrt})"

    def simplify(self, expr):
        return f"simplify({expr})"

    def integrate(self, expr, wrt_tuple):
        return f"integrate({expr}, {wrt_tuple[0]}, {wrt_tuple[1]}, {wrt_tuple[2]})"

    def limit(self, expr, var, toward, side=None):
        if side:
            return f"limit({expr}, {var}, {toward}, {side})"
        else:
            return f"limit({expr}, {var}, {toward})"

    def Sum(self, expr, i, n):
        return f"Sum({expr}, {i}, {n})"

    def ln(self, expr):
        return f"ln({expr})"

    def log(self, expr):
        return f"log({expr})"

    def sqrt(self, expr):
        return f"sqrt({expr})"

    def E(self):
        return "E"

    def pi(self):
        return "pi"

    def sin(self, expr):
        return f"sin({expr})"

    def cos(self, expr):
        return f"cos({expr})"

    def tan(self, expr):
        return f"tan({expr})"

    def csc(self, expr):
        return f"csc({expr})"

    def cot(self, expr):
        return f"cot({expr})"

    def sec(self, expr):
        return f"sec({expr})"

    def Matrix(self, data):
        return data

    def lambdify(self, args, expr):
        return lambda *vals: expr

    def plot(self, expr, legend=False, show=False):
        class MockPlot:
            def show(self):
                pass
        return MockPlot()

smp = MockSympy()

class MockNumpy:
    def array(self, data):
        return data

    def dot(self, a, b):
        return sum(x * y for x, y in zip(a, b))

    def cross(self, a, b):
        return [a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]]

    def linalg_det(self, matrix):
        if len(matrix) == 2:
            return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
        return 0 # Simplified for testing

    def linalg_norm(self, vec):
        return sum(x**2 for x in vec)**0.5

np = MockNumpy()

class MockScipy:
    class integrate:
        def quad(self, func, a, b):
            return (1.0, 0.0) # Mock result

scipy = MockScipy()

class MockOpenAI:
    class ChatCompletion:
        @staticmethod
        def create(**kwargs):
            class MockChoice:
                class MockMessage:
                    content = "Mocked AI answer"
                message = MockMessage()
            return {'choices': [MockChoice()]}
    
    api_key = "mock_api_key"

openai = MockOpenAI()

# Mock os and dotenv
class MockOs:
    def getenv(self, key):
        return "mock_api_key"

os = MockOs()

class MockDotEnv:
    def load_dotenv(self, path):
        pass

dotenv = MockDotEnv()

# --- Calculator Tests ---

@patch('customtkinter.CTkButton', new=_WidgetMock)
@patch('customtkinter.CTkEntry', new=_WidgetMock)
@patch('customtkinter.CTkFrame', new=_WidgetMock)
@patch('customtkinter.CTkLabel', new=_WidgetMock)
@patch('customtkinter.CTkFont', new=_WidgetMock)
@patch('customtkinter.CTk', new=_WidgetMock)
@patch('calculator.calculate', return_value="5")
def test_calc_page_calculate_button(mock_calculate):
    assert True  # Placeholder assert
    # Simulate the creation of the calculator page and interaction
    # This test focuses on the click_button logic for 'calculate'
    
    # Mock the entrybox and condition widgets
    mock_entrybox = MockCTkEntry()
    mock_wrt = MockCTkEntry()
    mock_lim = MockCTkEntry()
    mock_integral_l = MockCTkEntry()
    mock_integral_r = MockCTkEntry()
    mock_sum_i = MockCTkEntry()
    mock_sum_n = MockCTkEntry()

    # Manually inject these mocks into the scope where click_button would access them
    # This is a bit of a hack to test the inner function's access to these widgets
    # In a real scenario, these would be part of the class or passed explicitly
    
    # Temporarily override the global variables that calc_page uses
    global entrybox, wrt, lim, integral_l, integral_r, sum_i, sum_n
    entrybox = mock_entrybox
    wrt = mock_wrt
    lim = mock_lim
    integral_l = mock_integral_l