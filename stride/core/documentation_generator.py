"""
Logic for generating project documentation from completed sprints.
"""

from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime
from ..models import Sprint
from ..constants import (
    SprintStatus,
    STRIDE_DIR,
    SPRINTS_DIR,
    FILE_PROPOSAL,
    FILE_PLAN,
    FILE_DESIGN,
    FILE_IMPLEMENTATION,
    FILE_RETROSPECTIVE,
    PROJECT_FILE,
)
from .sprint_manager import SprintManager


class DocumentationGenerator:
    """Generator for project documentation from sprint data."""

    def __init__(self, base_path: Path = Path.cwd()):
        self.base_path = base_path
        self.docs_dir = base_path / "docs"
        self.stride_dir = base_path / STRIDE_DIR
        self.project_file = self.stride_dir / PROJECT_FILE
        self.sprint_manager = SprintManager(base_path)

    def validate_project(self) -> bool:
        """
        Validate that project.md exists.

        Returns:
            True if project is valid, False otherwise
        """
        return self.project_file.exists()

    def get_completed_sprints(self) -> List[Sprint]:
        """
        Get all completed sprints (those with retrospective.md).

        Returns:
            List of completed Sprint objects with full details
        """
        all_sprints = self.sprint_manager.list_sprints()
        completed = [
            self.sprint_manager.get_sprint_details(sprint.id)
            for sprint in all_sprints
            if sprint.status == SprintStatus.COMPLETED
        ]
        return [s for s in completed if s is not None]

    def read_sprint_files(self, sprint: Sprint) -> Dict[str, str]:
        """
        Read all sprint files and return their contents.

        Args:
            sprint: Sprint object

        Returns:
            Dictionary mapping file names to their contents
        """
        sprint_path = Path(sprint.path)
        files = {}

        file_names = [
            FILE_PROPOSAL,
            FILE_PLAN,
            FILE_DESIGN,
            FILE_IMPLEMENTATION,
            FILE_RETROSPECTIVE,
        ]

        for file_name in file_names:
            file_path = sprint_path / file_name
            if file_path.exists():
                try:
                    files[file_name] = file_path.read_text(encoding="utf-8")
                except Exception:
                    files[file_name] = ""

        return files

    def extract_features_from_sprints(self, sprints: List[Sprint]) -> List[Dict[str, str]]:
        """
        Extract feature information from completed sprints.

        Args:
            sprints: List of completed Sprint objects

        Returns:
            List of feature dictionaries with name, description, and implementation notes
        """
        features = []

        for sprint in sprints:
            files = self.read_sprint_files(sprint)

            # Extract feature name from proposal
            feature_name = sprint.title
            description = ""
            implementation_notes = ""

            # Parse proposal for description
            if FILE_PROPOSAL in files:
                proposal = files[FILE_PROPOSAL]
                # Extract description section if present
                lines = proposal.split("\n")
                in_desc = False
                desc_lines = []

                for line in lines:
                    if line.strip().startswith("## Description"):
                        in_desc = True
                        continue
                    elif line.strip().startswith("##") and in_desc:
                        break
                    elif in_desc and line.strip():
                        desc_lines.append(line.strip())

                description = " ".join(desc_lines)

            # Extract implementation summary from retrospective
            if FILE_RETROSPECTIVE in files:
                retro = files[FILE_RETROSPECTIVE]
                lines = retro.split("\n")
                in_summary = False
                summary_lines = []

                for line in lines:
                    if "## Summary" in line or "## What We Built" in line:
                        in_summary = True
                        continue
                    elif line.strip().startswith("##") and in_summary:
                        break
                    elif in_summary and line.strip():
                        summary_lines.append(line.strip())

                implementation_notes = " ".join(summary_lines)

            features.append(
                {
                    "name": feature_name,
                    "description": description,
                    "implementation": implementation_notes,
                    "sprint_id": sprint.id,
                }
            )

        return features

    def generate_index(self, project_name: str, features: List[Dict[str, str]]) -> str:
        """
        Generate index.md content.

        Args:
            project_name: Name of the project
            features: List of feature dictionaries

        Returns:
            Markdown content for index.md
        """
        content = f"# {project_name}\n\n"
        content += "## Overview\n\n"
        content += (
            f"This is the documentation for **{project_name}**, "
            "built using the Stride framework for sprint-powered development.\n\n"
        )

        content += "## Features\n\n"
        if features:
            for feature in features:
                content += f"- **{feature['name']}**"
                if feature["description"]:
                    content += f": {feature['description'][:100]}"
                    if len(feature["description"]) > 100:
                        content += "..."
                content += "\n"
        else:
            content += "*No completed features yet.*\n"

        content += "\n## Project Structure\n\n"
        content += "This documentation is organized as follows:\n\n"
        content += "- **Features**: Detailed documentation of implemented features\n"
        content += "- **Getting Started**: Guide to setting up and using the project\n\n"

        return content

    def generate_features_docs(self, features: List[Dict[str, str]]) -> str:
        """
        Generate features.md content.

        Args:
            features: List of feature dictionaries

        Returns:
            Markdown content for features.md
        """
        content = "# Features\n\n"
        content += "This page documents all implemented features in the project.\n\n"

        if not features:
            content += "*No features have been completed yet.*\n"
            return content

        for i, feature in enumerate(features, 1):
            content += f"## {i}. {feature['name']}\n\n"

            if feature["description"]:
                content += f"**Description**: {feature['description']}\n\n"

            if feature["implementation"]:
                content += f"**Implementation**: {feature['implementation']}\n\n"

            content += "---\n\n"

        return content

    def generate_getting_started(self, project_name: str) -> str:
        """
        Generate getting-started.md content.

        Args:
            project_name: Name of the project

        Returns:
            Markdown content for getting-started.md
        """
        content = "# Getting Started\n\n"
        content += f"Welcome to **{project_name}**!\n\n"
        content += "## Prerequisites\n\n"
        content += "List your prerequisites here:\n\n"
        content += "- Requirement 1\n"
        content += "- Requirement 2\n"
        content += "- Requirement 3\n\n"

        content += "## Installation\n\n"
        content += "```bash\n"
        content += "# Add installation steps here\n"
        content += "```\n\n"

        content += "## Configuration\n\n"
        content += "Describe configuration steps here.\n\n"

        content += "## Usage\n\n"
        content += "Provide usage examples here.\n\n"

        return content

    def create_mkdocs_config(self, project_name: str) -> str:
        """
        Generate mkdocs.yml configuration.

        Args:
            project_name: Name of the project

        Returns:
            YAML content for mkdocs.yml
        """
        config = f"""site_name: {project_name} Documentation
site_description: Documentation for {project_name}
site_author: Stride Framework

theme:
  name: material
  palette:
    primary: indigo
    accent: indigo
  features:
    - navigation.instant
    - navigation.sections
    - navigation.expand
    - toc.integrate

nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - Features: features.md

markdown_extensions:
  - admonition
  - codehilite
  - toc:
      permalink: true

extra:
  generator: Stride Framework
"""
        return config

    def generate_documentation(self) -> bool:
        """
        Generate complete project documentation.

        Returns:
            True if successful, False otherwise
        """
        # Validate project
        if not self.validate_project():
            return False

        # Get completed sprints
        completed_sprints = self.get_completed_sprints()

        # Extract project name
        project_name = "Project"
        if self.project_file.exists():
            try:
                content = self.project_file.read_text(encoding="utf-8")
                lines = content.split("\n")
                for line in lines:
                    if line.startswith("# "):
                        project_name = line[2:].strip()
                        break
            except Exception:
                pass

        # Extract features
        features = self.extract_features_from_sprints(completed_sprints)

        # Create docs directory
        self.docs_dir.mkdir(exist_ok=True)

        # Generate documentation files
        try:
            # index.md
            index_content = self.generate_index(project_name, features)
            (self.docs_dir / "index.md").write_text(index_content, encoding="utf-8")

            # features.md
            features_content = self.generate_features_docs(features)
            (self.docs_dir / "features.md").write_text(features_content, encoding="utf-8")

            # getting-started.md
            getting_started = self.generate_getting_started(project_name)
            (self.docs_dir / "getting-started.md").write_text(
                getting_started, encoding="utf-8"
            )

            # mkdocs.yml
            mkdocs_config = self.create_mkdocs_config(project_name)
            (self.docs_dir / "mkdocs.yml").write_text(mkdocs_config, encoding="utf-8")

            return True
        except Exception:
            return False

    def has_mkdocs_config(self) -> bool:
        """
        Check if mkdocs.yml exists in docs directory.

        Returns:
            True if mkdocs.yml exists, False otherwise
        """
        return (self.docs_dir / "mkdocs.yml").exists()

    def create_basic_mkdocs_config(self, project_name: str = "Project") -> bool:
        """
        Create a basic mkdocs.yml configuration.

        Args:
            project_name: Name of the project

        Returns:
            True if successful, False otherwise
        """
        try:
            self.docs_dir.mkdir(exist_ok=True)
            config = self.create_mkdocs_config(project_name)
            (self.docs_dir / "mkdocs.yml").write_text(config, encoding="utf-8")

            # Create basic index.md if it doesn't exist
            if not (self.docs_dir / "index.md").exists():
                index = f"# {project_name}\n\nWelcome to the documentation.\n"
                (self.docs_dir / "index.md").write_text(index, encoding="utf-8")

            return True
        except Exception:
            return False
