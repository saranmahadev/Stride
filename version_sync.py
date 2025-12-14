#!/usr/bin/env python3
"""
Stride Version Synchronization Utility

Centralized version management - updates version across all project files.
Usage: python version_sync.py <version>
Example: python version_sync.py 1.2.0
"""

import re
import sys
from pathlib import Path
from typing import Tuple, List


class VersionSync:
    """Manages version synchronization across all project files."""
    
    def __init__(self, root_path: Path = None):
        self.root = root_path or Path(__file__).parent
        self.version_pattern = r'\d+\.\d+\.\d+(?:-[a-zA-Z0-9]+)?'
        self.changes_made: List[str] = []
        self.errors: List[str] = []
    
    def validate_version(self, version: str) -> bool:
        """Validate version format (semver)."""
        pattern = r'^\d+\.\d+\.\d+(?:-[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*)?$'
        if not re.match(pattern, version):
            self.errors.append(f"Invalid version format: {version}")
            self.errors.append("Expected format: X.Y.Z or X.Y.Z-suffix (e.g., 1.2.3 or 1.2.3-beta.1)")
            return False
        return True
    
    def update_pyproject_toml(self, version: str) -> bool:
        """Update version in pyproject.toml."""
        file_path = self.root / "pyproject.toml"
        try:
            content = file_path.read_text(encoding='utf-8')
            original = content
            
            # Update ONLY the version in [project] section, not python_version in [tool.mypy]
            content = re.sub(
                r'(\[project\][\s\S]*?version\s*=\s*)"[^"]+"',
                rf'\1"{version}"',
                content,
                count=1
            )
            
            if content != original:
                file_path.write_text(content, encoding='utf-8')
                self.changes_made.append(f"✅ pyproject.toml → version = \"{version}\"")
                return True
            else:
                self.changes_made.append(f"ℹ️  pyproject.toml already at version {version}")
                return True
        except Exception as e:
            self.errors.append(f"❌ Failed to update pyproject.toml: {e}")
            return False
    
    def update_stride_init(self, version: str) -> bool:
        """Update __version__ in stride/__init__.py."""
        file_path = self.root / "stride" / "__init__.py"
        try:
            content = file_path.read_text(encoding='utf-8')
            original = content
            
            # Update __version__ = "X.Y.Z"
            content = re.sub(
                r'(__version__\s*=\s*)"[^"]+"',
                rf'\1"{version}"',
                content
            )
            
            if content != original:
                file_path.write_text(content, encoding='utf-8')
                self.changes_made.append(f"✅ stride/__init__.py → __version__ = \"{version}\"")
                return True
            else:
                self.changes_made.append(f"ℹ️  stride/__init__.py already at version {version}")
                return True
        except Exception as e:
            self.errors.append(f"❌ Failed to update stride/__init__.py: {e}")
            return False
    
    def update_readme_badge(self, version: str) -> bool:
        """Update version badge in README.md."""
        file_path = self.root / "README.md"
        try:
            content = file_path.read_text(encoding='utf-8')
            original = content
            
            # Update PyPI version badge - handles both stable and pre-release versions
            content = re.sub(
                r'(https://img\.shields\.io/badge/pypi-v)[0-9.]+(?:-[a-zA-Z0-9.]+)?(-blue\.svg)',
                rf'\g<1>{version}\2',
                content
            )
            
            if content != original:
                file_path.write_text(content, encoding='utf-8')
                self.changes_made.append(f"✅ README.md → badge updated to v{version}")
                return True
            else:
                self.changes_made.append(f"ℹ️  README.md badge already at version {version}")
                return True
        except Exception as e:
            self.errors.append(f"❌ Failed to update README.md: {e}")
            return False
    
    def check_changelog(self, version: str) -> bool:
        """Check if version exists in CHANGELOG.md."""
        file_path = self.root / "CHANGELOG.md"
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Check for [X.Y.Z] header
            if re.search(rf'\[{re.escape(version)}\]', content):
                self.changes_made.append(f"✅ CHANGELOG.md has entry for version {version}")
                return True
            else:
                self.errors.append(f"⚠️  CHANGELOG.md missing entry for version {version}")
                self.errors.append(f"   Add changelog entry manually before release")
                return False
        except Exception as e:
            self.errors.append(f"❌ Failed to check CHANGELOG.md: {e}")
            return False
    
    def sync_version(self, version: str) -> Tuple[bool, int, int]:
        """
        Synchronize version across all files.
        
        Returns:
            Tuple of (success, changes_count, errors_count)
        """
        if not self.validate_version(version):
            return False, 0, len(self.errors)
        
        print(f"\n🔄 Syncing version to: {version}\n")
        
        # Update all files
        self.update_pyproject_toml(version)
        self.update_stride_init(version)
        self.update_readme_badge(version)
        self.check_changelog(version)
        
        # Print results
        print("\n📊 Results:")
        print("=" * 60)
        for change in self.changes_made:
            print(change)
        
        if self.errors:
            print("\n⚠️  Issues:")
            for error in self.errors:
                print(error)
        
        changes_count = len([c for c in self.changes_made if c.startswith("✅")])
        errors_count = len([e for e in self.errors if e.startswith("❌")])
        warnings_count = len([e for e in self.errors if e.startswith("⚠️")])
        
        print("\n" + "=" * 60)
        print(f"Changes: {changes_count} | Warnings: {warnings_count} | Errors: {errors_count}")
        
        success = errors_count == 0
        return success, changes_count, errors_count


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python version_sync.py <version>")
        print("Example: python version_sync.py 1.2.0")
        print("         python version_sync.py 1.2.0-beta.1")
        sys.exit(1)
    
    version = sys.argv[1]
    syncer = VersionSync()
    success, changes, errors = syncer.sync_version(version)
    
    if success:
        print(f"\n✅ Version sync complete!")
        print(f"\n📝 Next steps:")
        print(f"   1. Review changes: git diff")
        print(f"   2. Update CHANGELOG.md if needed")
        print(f"   3. Commit: git add . && git commit -m 'Bump version to {version}'")
        print(f"   4. Tag: git tag v{version}")
        print(f"   5. Push: git push origin main --tags")
        sys.exit(0)
    else:
        print(f"\n❌ Version sync failed with {errors} error(s)")
        print("   Fix the errors above and try again")
        sys.exit(1)


if __name__ == "__main__":
    main()
