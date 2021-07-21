
def mock_output(return_value=None):
    return lambda *args, **kwargs: return_value
