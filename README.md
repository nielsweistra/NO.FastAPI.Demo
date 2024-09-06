# FastAPI-Demo
[![Docker Image CI Github Actions](https://github.com/ITlusions/ITL.FastApi.Demo/actions/workflows/docker-image.yml/badge.svg)](https://github.com/ITlusions/ITL.FastApi.Demo/actions/workflows/docker-image.yml)
[![Build Status - Azure Pipelines](https://dev.azure.com/ITlusions/ITL.FastAPI.Demo/_apis/build/status%2FITL.FastAPI.Demo.Build?branchName=main)](https://dev.azure.com/ITlusions/ITL.FastAPI.Demo/_build/latest?definitionId=35&branchName=main)

## Table of Contents

- [Project Structure](#project-structure)
- [Monorepo Concept](#monorepo-concept)
- [Tech](#tech)
- [Documentation](#documentation)

## Project Structure

This project is designed for a FastAPI application with integrated CI/CD pipelines, Docker, Helm charts, and Tekton pipelines. Below is a breakdown of the project's structure and key components:

### Project Structure Overview

- **Root Directory**
  - **`.gitignore`**: Specifies which files and directories Git should ignore.
  - **`azure-pipelines.yml`**: Configuration file for Azure Pipelines.
  - **`Dockerfile`**: Defines the Docker image for the application.
  - **`README.md`**: Project overview and documentation.
  - **`requirements.txt`**: Lists Python dependencies.

- **`.github`**
  - **`dependabot.yml`**: Configuration file for GitHub Dependabot, which helps keep dependencies updated.
  - **`workflows`**
    - **`docker-image.yml`**: GitHub Actions workflow for building and managing Docker images.

- **`.pytest_cache`**
  - Contains cache files for pytest, which are used to store test results and speed up test runs.

- **`.tekton`**
  - **`chart`**: Helm chart directory containing Tekton pipelines and tasks.
    - **`tekton-pipelines`**: Tekton pipelines Helm chart with YAML files for pipelines and tasks.
  - **`pipelines`**: Tekton pipeline definitions.
  - **`tasks`**: Tekton task definitions for Docker image building, linting, security scanning, and Python setup.
  - **`workspace`**: Persistent volume claim YAML for Tekton pipelines.

- **`.vscode`**
  - **`launch.json`**: VSCode configuration for debugging.

- **`app`**
  - **`main.py`**: Entry point of the FastAPI application.
  - **`base`**: Contains core application components like logging and settings.
    - **`logging`**: Logging configuration and utility files.
    - **`settings`**: Configuration files and documentation for settings.
  - **`models`**: Python modules defining data models.
  - **`routers`**: FastAPI routers for different endpoints.
  - **`tests`**: Unit tests for the application.

- **`charts`**
  - **`itl.fastapi.demo`**: Helm chart for deploying the FastAPI application.
    - **`charts`**: Sub-charts (if any) used in the main chart.
    - **`templates`**: Kubernetes manifests for deployment, service, ingress, etc.

- **`docs`**
  - **`tutorial-findindfixingsqlinject.md`**: Documentation related to finding and fixing SQL injections.
  - **`versioning.md`**: Documentation detailing the versioning strategy and related scripts.

## Monorepo Concept

This project uses a **monorepo** approach, meaning that it houses multiple related projects and components within a single repository. This approach offers several benefits:

- **Unified Versioning**: All related components, such as the FastAPI application, Docker configurations, Helm charts, and Tekton pipelines, are versioned together. This ensures consistency across different parts of the system.
- **Simplified CI/CD**: By having all the configurations and scripts in one place, managing and automating the build, test, and deployment processes is streamlined. The CI/CD pipelines can easily integrate with all components without requiring complex inter-repo dependencies.
- **Easier Refactoring**: Changes that span multiple components can be made and tested in a single commit, ensuring that everything remains in sync and reducing the risk of integration issues.
- **Centralized Documentation**: All documentation related to the project's structure, versioning, and configuration is consolidated in one place, making it easier to maintain and update.

## Tech

- Pipelines
- PyTests
- DevSecOps
- Just checking FastAPI

## Documentation

- [Versioning Strategy](./docs/versioning.md): Details the versioning strategy for Docker images, Helm charts, and Git tags.
- [Version Calculation Script](./docs/versioning.md#version-calculation-script): Describes the script used for automatic versioning and tagging based on repository changes.
- [CI/CD Automation](./docs/versioning.md#cicd-automation): Overview of the CI/CD pipeline and its role in maintaining consistent releases.

> This is a demo, feel free to use and contribute!

This project is also hosted on [Azure DevOps].

[Niels Weistra] @ [ITlusions]

   [ITlusions]: <https://github.com/ITlusions>
   [Niels Weistra]: <mailto:n.weistra@itlusions.com>
   [Azure DevOps]: <https://dev.azure.com/ITlusions/ITL.FastAPI.Demo/>
