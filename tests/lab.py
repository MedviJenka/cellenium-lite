import os
import inspect
import importlib.util
import openpyxl


def load_module_from_file(filepath):
    """Dynamically load a module from a file path."""
    module_name = os.path.splitext(os.path.basename(filepath))[0]
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_test_functions_to_xlsx(directory, xlsx_filename):
    # Create a new Excel workbook and sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Test Functions"

    # Write the header row
    sheet.append(["File Name", "Test Function Name"])
    print(os.listdir(directory))
    # Loop through Python files in the specified directory
    for filename in os.listdir(directory):

        if filename.endswith(".py"):
            filepath = os.path.join(directory, filename)
            module = load_module_from_file(filepath)

            # Get all functions from the module
            functions = inspect.getmembers(module, inspect.isfunction)

            # Filter only the test functions (assuming they start with "test_")
            test_functions = [name for name, func in functions if name.startswith('test_')]

            # Write each test function name into the Excel file
            for test_func in test_functions:
                sheet.append([filename, test_func, functions, module])

    # Save the Excel workbook
    workbook.save(xlsx_filename)
    print(f"Test function names have been written to {xlsx_filename}")


if __name__ == "__main__":
    directory_path = r'C:\Users\medvi\OneDrive\Desktop\cellenium-lite\tests'  # Replace with the path to your directory
    write_test_functions_to_xlsx(directory_path, 'tests_count.xlsx')
