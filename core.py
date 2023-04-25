from contextlib import contextmanager
import json

class Core:
    def __init__(self):
        pass

    @contextmanager
    def _open_config(self, filepath):
        """
            A context manager that opens a JSON configuration file at the specified filepath, loads
            its contents into a Python dictionary, and yields the dictionary to the calling code. If
            an error occurs during the process, the error is caught and printed to the console. The
            file is always closed after the with block completes.

            :param filepath: The filepath of the JSON configuration file to open.
            :type filepath: str

            :return: A dictionary containing the contents of the JSON configuration file.
            :rtype: dict
            """
        try:
            with open(filepath, 'r') as file:
                yield json.load(file)
                # return data
        except Exception as e:
            print(f"Error: {e}")
        finally:
            file.close()