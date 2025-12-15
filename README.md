## GPU Version

Must be run on an NVIDIA Volta GPU or higher and compute cpcability 7.0+. (Some examples used during testing were RTX A5000, RTX 4090, A100, and H100 provisioned through Vast.ai)

### Environment setup
Ru the setup script using the following command. This will install all correct package versions required to run the RAPIDSAI libraries:
```python
./setup.sh
```

### Running a test script

An example running the backendScript.py file located in the backend directory. This enables the cuml.accel and cudf.pandas modules for the RAPIDSAI zero code change acceleration:

```
python3.12 -m cudf.pandas -m cuml.accel backend/backendScript.py
```

### Monitoring GPU Usage

To moitor GPU utilization duing execution, we can use the nvidia-smi CLI tool:

```
watch nvidia-smi
```

This gives an overview of the resource utilization:
