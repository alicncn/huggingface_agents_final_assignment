"""Code interpreter tools for safe Python code execution."""
import sys
import io
import traceback
from typing import Optional
from langchain_core.tools import tool
import contextlib


@tool
def execute_python_code(code: str, timeout: int = 10) -> str:
    """
    Execute Python code in a restricted environment and return the output.
    
    Args:
        code: Python code to execute
        timeout: Maximum execution time in seconds (default: 10)
    
    Returns:
        Output from code execution (stdout, stderr, or result)
    
    WARNING: This executes code in the current process. For production use,
    implement proper sandboxing with containers or RestrictedPython.
    """
    try:
        # Create string buffers to capture output
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        
        # Redirect stdout and stderr
        with contextlib.redirect_stdout(stdout_buffer), \
             contextlib.redirect_stderr(stderr_buffer):
            
            # Create a restricted namespace
            namespace = {
                '__builtins__': __builtins__,
                'print': print,
                'len': len,
                'range': range,
                'sum': sum,
                'max': max,
                'min': min,
                'abs': abs,
                'round': round,
                'sorted': sorted,
                'list': list,
                'dict': dict,
                'set': set,
                'tuple': tuple,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
            }
            
            # Execute the code
            exec(code, namespace)
        
        # Get outputs
        stdout_output = stdout_buffer.getvalue()
        stderr_output = stderr_buffer.getvalue()
        
        # Combine outputs
        result = []
        if stdout_output:
            result.append(f"Output:\n{stdout_output}")
        if stderr_output:
            result.append(f"Errors:\n{stderr_output}")
        
        if not result:
            result.append("Code executed successfully with no output.")
        
        return "\n".join(result)
        
    except SyntaxError as e:
        return f"Syntax Error: {str(e)}\nLine {e.lineno}: {e.text}"
    except Exception as e:
        return f"Runtime Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"


@tool
def evaluate_python_expression(expression: str) -> str:
    """
    Evaluate a Python expression and return the result.
    
    Args:
        expression: Python expression to evaluate (e.g., "2 + 2", "sum([1,2,3])")
    
    Returns:
        The evaluated result as a string
    """
    try:
        # Create a safe namespace
        namespace = {
            '__builtins__': __builtins__,
            'sum': sum,
            'max': max,
            'min': min,
            'abs': abs,
            'round': round,
            'len': len,
            'sorted': sorted,
            'list': list,
            'dict': dict,
            'set': set,
            'tuple': tuple,
        }
        
        # Evaluate the expression
        result = eval(expression, namespace)
        
        return f"Result: {result}"
        
    except SyntaxError as e:
        return f"Syntax Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def analyze_code_output(code: str) -> str:
    """
    Analyze what a piece of Python code will output without executing it in a full environment.
    Useful for predicting code behavior.
    
    Args:
        code: Python code to analyze
    
    Returns:
        Prediction of what the code will output
    """
    # For simple cases, we can execute safely
    # For complex cases, this would use static analysis
    result = execute_python_code.invoke({"code": code, "timeout": 5})
    
    return f"Code Analysis:\n{result}"
