FROM continuumio/miniconda3:latest

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy environment files
COPY .devcontainer/environment.yml /tmp/environment.yml
COPY requirements.txt /tmp/requirements.txt

# Create conda environment from environment.yml
RUN conda env create -f /tmp/environment.yml && \
    conda clean -afy

# Make the conda environment the default
RUN echo "conda activate finmath" >> ~/.bashrc && \
    echo "PATH=/opt/conda/envs/finmath/bin:$PATH" >> ~/.bashrc

# Add a verification script that will run during container startup
RUN echo '#!/bin/bash\necho "Testing TA-Lib installation..."\nsource /opt/conda/etc/profile.d/conda.sh && conda activate finmath && python -c "import talib; print(\"TA-Lib version:\", talib.get_version())" || echo "TA-Lib import failed"\necho "Environment setup complete!"\n' > /usr/local/bin/verify-environment.sh && \
    chmod +x /usr/local/bin/verify-environment.sh

# Set the default workspace location
WORKDIR /workspaces

# Run verification script during container startup
ENTRYPOINT ["/bin/bash", "-c", "source /opt/conda/etc/profile.d/conda.sh && conda activate finmath && /usr/local/bin/verify-environment.sh && exec \"$@\"", "--"]
CMD ["bash"]
