import ast

def extract_requirements_from_file(file_path):
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read(), filename=file_path)

    requirements = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                requirements.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module
            if module is not None:
                requirements.add(module)

    return requirements

# Example usage:
file_path = "C:/Users/luca.pizzetti/Dropbox/01 LUCA/04_PROGRAMMAZIONE/_GitHub/Public/Streamlit/streamlit_app.py" # Replace with the path to your Python file
requirements = extract_requirements_from_file(file_path)
print("Requirements connected to", file_path + ":")
print(requirements)
