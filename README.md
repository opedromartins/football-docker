# Dockerized Google Research Football with Ray and Baselines

This Dockerfile provides a containerized environment for running examples and training scenarios with Google Research Football using both Ray and Baselines libraries.

## Usage

### Building the Docker Image

```bash
docker build -t gfootball_python37 .
```

### Running the Docker Container

```bash
./run.sh <docker image> [--rm] [--nvidia]
```

- `<docker image>`: The name or ID of the Docker image.
- `--rm`: Remove the container after it exits (optional).
- `--nvidia`: Use NVIDIA GPU for acceleration (optional).

Example:

```bash
./run.sh gfootball_python37 --rm --nvidia
```

### Examples with Baselines

To run examples with Baselines, use the following command within the container:

```bash
python -m gfootball.examples.run_ppo2 --dump_full_episodes=True --render=True
```

### Examples with Ray

To run examples with Ray, use the following command within the container:

```bash
python -m gfootball.examples.run_multiagent_rllib
```

## Dockerfile Details

The Dockerfile sets up a Python 3.7 environment with necessary dependencies and installs Google Research Football, TensorFlow, Ray, and Baselines. It utilizes Conda for managing Python packages.

## Notes

- Ensure you have Docker installed and running on your system.
- Adjust the Dockerfile or shell scripts based on your specific requirements.
- NVIDIA GPU acceleration requires compatible hardware and appropriate Docker setup.

Feel free to explore and customize the provided Dockerfile and scripts to suit your needs.