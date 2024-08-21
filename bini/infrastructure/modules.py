import yaml


def read_yaml(file_path) -> dict:

    """
    Reads a YAML file and returns the content as a dictionary.

    :param file_path: Path to the YAML file.
    :return: Dictionary containing YAML data.

    """

    with open(file_path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError:
            raise FileNotFoundError
