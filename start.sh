#!/bin/bash

# Start script for Projects and Blogs API
# For Linux and macOS with Miniconda/Anaconda

echo "=========================================="
echo "  Projects and Blogs API - Startup"
echo "=========================================="
echo ""

# Nombre del environment de conda
CONDA_ENV_NAME="api_project_clean"

# Inicializar conda
eval "$(conda shell.bash hook)"

# Verificar si el environment existe
if ! conda env list | grep -q "^$CONDA_ENV_NAME "; then
    echo "Creating conda environment '$CONDA_ENV_NAME'..."
    conda create -n $CONDA_ENV_NAME python=3.12 -y
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create conda environment"
        exit 1
    fi
fi

# Activar environment
echo "Activating conda environment '$CONDA_ENV_NAME'..."
conda activate $CONDA_ENV_NAME

# Instalar dependencias
if [ -f "requirements.txt" ]; then
    echo "Installing/updating dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
fi

# Verificar archivo .env
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "Warning: .env file not found. Copying from .env.example..."
        cp .env.example .env
        echo "Please edit .env file with your configuration before running again."
        exit 1
    else
        echo "Warning: No .env file found. Using default settings."
    fi
fi

echo ""
echo "=========================================="
echo "  Starting API server..."
echo "=========================================="
echo "API will be available at: http://localhost:8000"
echo "API documentation at: http://localhost:8000/docs"
echo "Press Ctrl+C to stop the server"
echo ""

# Iniciar servidor
uvicorn main:app --host 0.0.0.0 --port 8000 --reload