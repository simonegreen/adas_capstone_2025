#!/bin/bash

apt update
apt install -y software-properties-common
add-apt-repository ppa:deadsnakes/ppa -y
apt update
apt install -y python3.12 python3.12-dev python3.12-venv
python3.12 --version
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12
python3.12 -m pip --version

pip install --extra-index-url=https://pypi.nvidia.com \
"cudf-cu12==25.10.*" "dask-cudf-cu12==25.10.*" "cuml-cu12==25.10.*" \
"cugraph-cu12==25.10.*" "nx-cugraph-cu12==25.10.*" "cuxfilter-cu12==25.10.*" \
"cucim-cu12==25.10.*" "pylibraft-cu12==25.10.*" "raft-dask-cu12==25.10.*" \
"cuvs-cu12==25.10.*" "seaborn==0.13.2" "scikit-learn==1.7.2"


apt install -y build-essential
pip install git+https://github.com/TimotheeMathieu/scikit-learn-extra

# ---- FastAPI backend dependencies ----
pip install fastapi uvicorn python-multipart "pydantic<3"

pip install python-dotenv

pip install openai

python3.12 - <<EOF
import numpy, pandas, sklearn, sklearn_extra, cudf, cuml
print("numpy", numpy.__version__, "| pandas", pandas.__version__, "| sklearn", sklearn.__version__, "| sklearn_extra", sklearn_extra.__version__, "| cudf", cudf.__version__, "| cuml", cuml.__version__)
EOF

apt install -y nvidia-cuda-toolkit
export CUDA_PATH=/usr