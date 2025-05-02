# FinMath Dev Container - GHCR Authentication

This document explains how to set up proper authentication for using GitHub Container Registry (ghcr.io) with this development container and how it works in different environments (local, fork, GitHub Codespaces).

## Authentication Setup for GitHub Container Registry

The development container can pull cached images from GitHub Container Registry to speed up build times. To enable this feature, you need to authenticate with GHCR by setting up a GitHub token.

### 1. Generate a GitHub Personal Access Token (PAT)

1. Go to your GitHub account settings: https://github.com/settings/tokens
2. Click "Generate new token" (classic)
3. Give it a descriptive name like "FinMath Dev Container"
4. Set an expiration date
5. Select at least the following scopes:
   - `read:packages` (to read packages from GitHub package registry)
   - `write:packages` (if you want to publish packages)
6. Click "Generate token"
7. **Important**: Copy the token immediately as you won't be able to see it again

### 2. Configure the GitHub Token as an Environment Variable

#### Option A: VS Code Environment Variables

1. Open VS Code settings (File > Preferences > Settings)
2. Search for "dev container env"
3. Under "Dev > Containers: Environment Variables", add the following:
   ```json
   {
     "GITHUB_TOKEN": "your-github-token-here", 
     "USER_NAME": "your-github-username",
     "REPO_NAME": "finmath"
   }
   ```

#### Option B: Environment File

1. Create a `.env` file in your project root (make sure it's in `.gitignore`)
2. Add the following variables:
   ```
   GITHUB_TOKEN=your-github-token-here
   USER_NAME=your-github-username
   REPO_NAME=finmath
   ```
3. VSCode will automatically load these variables when opening the dev container

### 3. Understanding the Authentication Process

- The `.github/workflows/notebook-tests.yml` file uses GitHub Actions' built-in authentication with GHCR
- For local development, the `devcontainer.json` passes your GitHub token to the Docker build process
- The Dockerfile uses this token to authenticate with GHCR and pull cached layers

With this setup, you'll be able to take advantage of cached image layers from GHCR to significantly speed up your container builds.

## Behavior in Different Environments

### GitHub Codespaces

When using GitHub Codespaces:

1. **Authentication**: Codespaces automatically provides the `CODESPACES_GITHUB_TOKEN` environment variable, which is used by our configuration.
2. **Cache Access**: The container will automatically authenticate with GHCR to access cached layers.
3. **No Manual Setup**: You don't need to configure any authentication tokens manually.
4. **Performance**: Builds will be faster as they use cached layers.

### Forked Repositories

When you fork this repository:

1. **First Build**: The first build will not have access to the original repository's cache layers unless you have explicit permissions.
2. **GitHub Actions**: The workflow will still run but may take longer initially as it builds from scratch.
3. **Local Development**: 
   - If you have a GitHub token with access to your fork's registry, add it as described above.
   - If you don't have a token, the container will still build successfully but without using cache.
4. **Cache Creation**: Your fork will create its own set of cached layers for future builds.

### No Authentication Fallback

The container is designed to work even without authentication:

1. **No Token**: If no GitHub token is provided, Docker will build the container without using cached layers.
2. **Complete Build**: All dependencies will still be installed correctly, just without the speed benefit of layer caching.
3. **Functionality**: All features of the container will work normally.

This flexible design ensures that anyone can use this development container in any environment without complications.
