# Versioning Strategy

The versioning strategy follows **Semantic Versioning (SemVer)** to maintain consistency across Docker images, Helm charts, and Git tags. This approach ensures that all components are aligned and provides a clear understanding of changes with each release.

### Version Format: `MAJOR.MINOR.PATCH`

- **MAJOR (`X.0.0`):** Incremented for breaking changes or significant updates in either the Docker image or Helm chart that are not backward compatible.
- **MINOR (`0.Y.0`):** Incremented for new features or enhancements that are backward compatible in either the Docker image, Helm chart, or both.
- **PATCH (`0.0.Z`):** Incremented for bug fixes, security patches, or minor updates that are backward compatible in either the Docker image, Helm chart, or both.

### Version Alignment Across Components

- **Docker Images:** Tagged with the version format (e.g., `v1.2.0`) and pushed to the container registry. Changes in Docker images (e.g., bug fixes, new features, or breaking changes) dictate whether the **MAJOR**, **MINOR**, or **PATCH** version is incremented.

- **Helm Charts:** Updated to match the Docker image version. Changes in Helm charts (e.g., new configuration options or breaking changes) will also drive version increments.

- **Git Tags:** Every release is tagged in the Git repository using the same version format (e.g., `v1.2.0`) to track changes in the source code that align with Docker and Helm updates.

### Version Calculation Script

To automate the version calculation and tagging process, we use a script that performs the following steps:

#### Script Overview

The script calculates the next version number based on the latest Git tag and detected changes in the repository. It then updates the Helm chart, builds and tags the Docker image, and creates a new Git tag.

#### Script Breakdown

1. **Retrieve the Latest Git Tag:**
   - Uses `git describe --tags --abbrev=0` to get the latest tag. If no tag is found, initializes the version to `1.0.0`.

2. **Extract the Base Version:**
   - Removes any suffix (e.g., `-develop`, `-branchName`) from the tag to get the base version (`MAJOR.MINOR.PATCH`).

3. **Determine Changes:**
   - Checks for changes in critical files (`Dockerfile`, Helm charts) to decide whether to increment the **MAJOR**, **MINOR**, or **PATCH** version.

4. **Calculate the New Version:**
   - Updates the version number based on the type of changes detected.

5. **Update and Tag:**
   - Updates the `Chart.yaml` file with the new version.
   - Creates and pushes a new Git tag with the new version and any suffix.

#### Example Script

```bash
#!/bin/bash

# Get the latest Git tag
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)

# If no tag is found, initialize to 1.0.0
if [ -z "$LATEST_TAG" ]; then
    LATEST_TAG="1.0.0"
fi

# Extract base version number (without suffix)
BASE_VERSION=$(echo "$LATEST_TAG" | sed -E 's/([0-9]+\.[0-9]+\.[0-9]+).*/\1/')

# Extract current MAJOR, MINOR, and PATCH versions
MAJOR=$(echo "$BASE_VERSION" | cut -d. -f1)
MINOR=$(echo "$BASE_VERSION" | cut -d. -f2)
PATCH=$(echo "$BASE_VERSION" | cut -d. -f3)

# Fetch the list of changed files
CHANGED_FILES=$(git diff --name-only HEAD HEAD~1)

# Initialize version increments
MAJOR_INCREMENT=0
MINOR_INCREMENT=0
PATCH_INCREMENT=0

# Function to determine the type of change
determine_change_type() {
    if [[ "$CHANGED_FILES" == *"Dockerfile"* ]]; then
        # Assume MAJOR increment for breaking changes in Dockerfile
        MAJOR_INCREMENT=1
    elif [[ "$CHANGED_FILES" == *"charts/"* || "$CHANGED_FILES" == *"values.yaml"* ]]; then
        # Assume MINOR increment for changes in Helm charts
        MINOR_INCREMENT=1
    elif [[ "$CHANGED_FILES" == *".*" ]]; then
        # Assume PATCH increment for any other changes
        PATCH_INCREMENT=1
    fi
}

# Determine the type of changes and set increments
determine_change_type

# Calculate the new version based on the changes
if [[ $MAJOR_INCREMENT -eq 1 ]]; then
    MAJOR=$((MAJOR + 1))
    MINOR=0
    PATCH=0
elif [[ $MINOR_INCREMENT -eq 1 ]]; then
    MINOR=$((MINOR + 1))
    PATCH=0
elif [[ $PATCH_INCREMENT -eq 1 ]]; then
    PATCH=$((PATCH + 1))
fi

# Create the new version
NEW_VERSION="$MAJOR.$MINOR.$PATCH"

# Check if the latest tag contains a suffix
SUFFIX=$(echo "$LATEST_TAG" | sed -E 's/^[0-9]+\.[0-9]+\.[0-9]+(-.*)?/\1/')

# If no suffix is found, use the branch name as suffix
if [ -z "$SUFFIX" ]; then
    BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)
    SUFFIX="-${BRANCH_NAME}"
fi

# Create the new tag with the version and suffix
NEW_TAG="v$NEW_VERSION$SUFFIX"

# Update Chart.yaml with the new version
sed -i "s/^version: .*/version: $NEW_VERSION/" Chart.yaml

# Build and tag Docker image with new version
# Assuming Dockerfile is in the root directory
DOCKER_REPO="<your-acr-name>.azurecr.io/my-app"
docker build -t "$DOCKER_REPO:$NEW_VERSION" .
docker push "$DOCKER_REPO:$NEW_VERSION"

# Create a new Git tag for the version
git tag -a "$NEW_TAG" -m "Release version $NEW_TAG"
git push origin "$NEW_TAG"

echo "Updated to version $NEW_TAG. Added tag to GIT"
echo "Next step is to build the container with tag 'latest', a tag with the new version. Package and push the helm package to a repo."

```
<br>

> In the determine_change_type() function you can also add a condition when changes in application code are detected. In this example the app code and versioning is out of scope. 

### CI/CD Automation

The CI/CD pipeline automates the process of building and tagging Docker images, updating Helm chart versions, and applying Git tags. This ensures that every release is consistent, traceable, and ready for deployment.

This strategy, provides maintain clear communication about the state of our application and simplify the process of deploying and managing updates.

---
<br>

[Niels Weistra] @ [ITlusions]

   [ITlusions]: <https://github.com/ITlusions>
   [Niels Weistra]: <mailto:n.weistra@itlusions.com>
   [Azure Devops]: <https://dev.azure.com/ITlusions/ITL.FastAPI.Demo/>