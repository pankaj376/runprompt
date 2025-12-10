def add_numbers(a: int, b: int):
    """Adds two numbers together and returns the result.
    
    This is a simple arithmetic tool that takes two integers
    and returns their sum.
    """
    return a + b


def greet(name: str):
    """Greets a person by name.
    
    Returns a friendly greeting message for the specified person.
    """
    return "Hello, %s!" % name

greet.safe = True


def no_docstring_func():
    # This function has no docstring so it won't be loaded as a tool
    return "ignored"
