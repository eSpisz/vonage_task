import yaml
import logger
import argparse
import re
from abc import ABC, abstractmethod

class FileLoader(ABC):
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    @abstractmethod
    def load_file(self):
        pass

class YAMLFileLoader(FileLoader):
    """
    YAML file Loader.
    """
    
    def load_file(self):
        """
        Load a YAML file and return its content.
        """
        try:
            with open(self.file_path, 'r') as file:
                data = yaml.safe_load(file)
            return data
        
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
class DockerFileLoader(FileLoader):
    """
    Docker file Loader.
    """

    def load_file(self):
        """
        Load a Docker file and return its content.
        """
        try:
            with open(self.file_path, 'r') as file:
                data = file.read()
            return data
        
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.file_path}")

class DataPrinter(ABC):
    """
    Data Printer.
    """

    def __init__(self, data, logger_obj):
        self.data = data
        self.logger_obj = logger_obj

    @abstractmethod
    def validate_data(self):
        """
        Check if data has the required fields.
        """
        pass

    @abstractmethod
    def print_data(self):
        """
        Print the loaded data.
        """
        pass

class YAMLDataPrinter(DataPrinter):
    """
    YAML Data Printer.
    """

    def validate_data(self):
        self.name = self.data.get('name', '')
        self.startup_command = self.data.get('startup_command', '')

        if not self.name or not self.startup_command:
            self.logger_obj.error("Validation Error: Name and startup_command are required fields.")
            raise ValueError("Name and startup_command are required fields.")

    def print_data(self):
        """
        Print the loaded data.
        """
        self.logger_obj.info(f"Name parameter: {self.name}")
        self.logger_obj.info(f"Startup command: {self.startup_command}")

        return self.name, self.startup_command

class TemplateEngine(ABC):
    """
    Template Engine.
    """

    def __init__(self, loader: FileLoader, name: str, startup_command: str):
        self.name = name
        self.startup_command = startup_command
        self.loader = loader

    @abstractmethod
    def create_template(self):
        """
        Create a template.
        """
        pass

class DockerTemplateEngine(TemplateEngine):
    """
    Docker Template Engine.
    """

    def create_template(self):
        """
        Render the template with the provided parameters.
        """
        template = self.loader.load_file()
        template = re.sub(r'"<startup_command>"', ",".join([f'"{arg}"' for arg in self.startup_command.split()]), template)
        template = re.sub(r'<name>', self.name, template)
        
        with open("./output_files/Dockerfile", 'w') as file:
            file.write(template)
        



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--yaml-file", help="Path to source files", required=True)
    parser.add_argument("--docker-file", help="Path to Docker file", required=True)
    return parser.parse_args()

def main():
    """
    Main function.
    """

    logger_obj = logger.get_logger(__name__)

    args = parse_args()
    yaml_file_path = args.yaml_file
    docker_file_path = args.docker_file
    
    yaml_loader = YAMLFileLoader(yaml_file_path)
    yaml_data = yaml_loader.load_file()

    printer = YAMLDataPrinter(yaml_data, logger_obj)
    printer.validate_data()
    name, startup_command = printer.print_data()

    docker_loader = DockerFileLoader(docker_file_path)
    docker_template_engine = DockerTemplateEngine(docker_loader, name, startup_command)
    docker_template_engine.create_template()


if __name__ == "__main__":
    main()