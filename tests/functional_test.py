import subprocess
import yaml


def test_functional():
    input_yaml = "source_files/project.yaml"
    input_docker = "source_files/Dockerfile"

    result = subprocess.run(
        [
            "python3",
            "solution.py",
            "--yaml-file",
            input_yaml,
            "--docker-file",
            input_docker,
        ],
        capture_output=True,
        text=True,
    )

    with open("source_files/project.yaml", "r") as file:
        yaml_content = yaml.safe_load(file)
        name = yaml_content.get("name", "")
        startup_command = yaml_content.get("startup_command", "")

    with open("output_files/Dockerfile", "r") as file:
        docker_content = file.read()

    assert result.returncode == 0, f"Error: {result.stderr}"
    assert name is not None
    assert startup_command is not None
    assert name in docker_content
    assert ",".join([f'"{arg}"' for arg in startup_command.split()]) in docker_content
