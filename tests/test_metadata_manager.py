"""
Tests for MetadataManager.
"""
import pytest
from pathlib import Path
import yaml

from stride.core.metadata_manager import MetadataManager, MetadataValidationError


class TestMetadataManager:
    """Tests for MetadataManager class."""
    
    def test_parse_frontmatter_valid(self):
        """Test parsing valid YAML frontmatter."""
        content = """---
id: SPRINT-TEST
title: Test Sprint
status: proposed
created: 2025-11-17T10:00:00Z
---

# Body content here
This is the body."""
        
        metadata, body = MetadataManager.parse_frontmatter(content)
        
        assert metadata["id"] == "SPRINT-TEST"
        assert metadata["title"] == "Test Sprint"
        assert metadata["status"] == "proposed"
        assert "Body content here" in body
    
    def test_parse_frontmatter_no_frontmatter(self):
        """Test parsing content without frontmatter."""
        content = "Just body content"
        
        metadata, body = MetadataManager.parse_frontmatter(content)
        
        assert metadata == {}
        assert body == content
    
    def test_parse_frontmatter_invalid_format(self):
        """Test parsing invalid frontmatter format."""
        content = """---
id: SPRINT-TEST
Missing closing delimiter"""
        
        with pytest.raises(ValueError, match="Invalid frontmatter format"):
            MetadataManager.parse_frontmatter(content)
    
    def test_parse_frontmatter_invalid_yaml(self):
        """Test parsing malformed YAML."""
        content = """---
id: SPRINT-TEST
title: [unclosed bracket
---

Body"""
        
        with pytest.raises(yaml.YAMLError):
            MetadataManager.parse_frontmatter(content)
    
    def test_serialize_frontmatter(self):
        """Test serializing metadata and body to markdown."""
        metadata = {
            "id": "SPRINT-TEST",
            "title": "Test Sprint",
            "status": "proposed"
        }
        body = "# Test\n\nBody content"
        
        result = MetadataManager.serialize_frontmatter(metadata, body)
        
        assert result.startswith("---\n")
        assert "SPRINT-TEST" in result
        assert "Test Sprint" in result
        assert "Body content" in result
    
    def test_parse_file(self, tmp_path):
        """Test parsing frontmatter from file."""
        test_file = tmp_path / "test.md"
        content = """---
id: SPRINT-FILE
title: File Test
status: active
created: 2025-11-17T10:00:00Z
---

# Content
Test content"""
        test_file.write_text(content)
        
        metadata, body = MetadataManager.parse_file(test_file)
        
        assert metadata["id"] == "SPRINT-FILE"
        assert metadata["title"] == "File Test"
        assert "Test content" in body
    
    def test_parse_file_not_found(self, tmp_path):
        """Test parsing non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            MetadataManager.parse_file(tmp_path / "nonexistent.md")
    
    def test_write_file(self, tmp_path):
        """Test writing frontmatter to file."""
        test_file = tmp_path / "output.md"
        metadata = {
            "id": "SPRINT-WRITE",
            "title": "Write Test",
            "status": "proposed",
            "created": "2025-11-17T10:00:00Z"
        }
        body = "# Test\n\nBody content"
        
        MetadataManager.write_file(test_file, metadata, body)
        
        assert test_file.exists()
        content = test_file.read_text()
        assert "SPRINT-WRITE" in content
        assert "Write Test" in content
        assert "Body content" in content
    
    def test_update_frontmatter_merge(self, tmp_path):
        """Test updating frontmatter with merge."""
        test_file = tmp_path / "update.md"
        initial_content = """---
id: SPRINT-UPDATE
title: Original Title
status: proposed
created: 2025-11-17T10:00:00Z
---

# Content
Body"""
        test_file.write_text(initial_content)
        
        updates = {"title": "Updated Title", "status": "active"}
        metadata = MetadataManager.update_frontmatter(test_file, updates, merge=True)
        
        assert metadata["title"] == "Updated Title"
        assert metadata["status"] == "active"
        assert metadata["id"] == "SPRINT-UPDATE"  # Original field preserved
    
    def test_update_frontmatter_replace(self, tmp_path):
        """Test updating frontmatter with replace."""
        test_file = tmp_path / "replace.md"
        initial_content = """---
id: SPRINT-REPLACE
title: Original Title
status: proposed
created: 2025-11-17T10:00:00Z
extra: field
---

Body"""
        test_file.write_text(initial_content)
        
        new_metadata = {
            "id": "SPRINT-NEW",
            "title": "New Title",
            "status": "active",
            "created": "2025-11-17T11:00:00Z"
        }
        metadata = MetadataManager.update_frontmatter(test_file, new_metadata, merge=False)
        
        assert metadata["id"] == "SPRINT-NEW"
        assert metadata["title"] == "New Title"
        assert "extra" not in metadata  # Old field removed
    
    def test_validate_metadata_valid(self):
        """Test validating valid metadata."""
        metadata = {
            "id": "SPRINT-VALID",
            "title": "Valid Sprint",
            "status": "active",
            "created": "2025-11-17T10:00:00Z"
        }
        
        assert MetadataManager.validate_metadata(metadata) is True
    
    def test_validate_metadata_missing_required_field(self):
        """Test validation fails for missing required field."""
        metadata = {
            "id": "SPRINT-TEST",
            "title": "Test",
            # Missing 'status' and 'created'
        }
        
        with pytest.raises(MetadataValidationError, match="Missing required fields"):
            MetadataManager.validate_metadata(metadata)
    
    def test_validate_metadata_invalid_id_format(self):
        """Test validation fails for invalid ID format."""
        metadata = {
            "id": "INVALID-ID",
            "title": "Test",
            "status": "active",
            "created": "2025-11-17T10:00:00Z"
        }
        
        with pytest.raises(MetadataValidationError, match="Invalid sprint ID format"):
            MetadataManager.validate_metadata(metadata)
    
    def test_validate_metadata_invalid_status(self):
        """Test validation fails for invalid status."""
        metadata = {
            "id": "SPRINT-TEST",
            "title": "Test",
            "status": "invalid_status",
            "created": "2025-11-17T10:00:00Z"
        }
        
        with pytest.raises(MetadataValidationError, match="Invalid status"):
            MetadataManager.validate_metadata(metadata)
    
    def test_validate_metadata_empty_title_strict(self):
        """Test strict validation fails for empty title."""
        metadata = {
            "id": "SPRINT-TEST",
            "title": "   ",  # Empty/whitespace only
            "status": "active",
            "created": "2025-11-17T10:00:00Z"
        }
        
        with pytest.raises(MetadataValidationError, match="Title cannot be empty"):
            MetadataManager.validate_metadata(metadata, strict=True)
    
    def test_validate_metadata_non_strict(self):
        """Test non-strict validation is more lenient."""
        metadata = {
            "id": "SPRINT-TEST",
            "title": "   ",  # Would fail strict validation
            "status": "active",
            "created": "2025-11-17T10:00:00Z"
        }
        
        # Should pass with strict=False
        assert MetadataManager.validate_metadata(metadata, strict=False) is True
    
    def test_create_metadata(self):
        """Test creating new metadata."""
        metadata = MetadataManager.create_metadata(
            sprint_id="SPRINT-CREATE",
            title="Create Test",
            status="proposed",
            author="test@example.com",
            priority="high"
        )
        
        assert metadata["id"] == "SPRINT-CREATE"
        assert metadata["title"] == "Create Test"
        assert metadata["status"] == "proposed"
        assert metadata["author"] == "test@example.com"
        assert metadata["priority"] == "high"
        assert "created" in metadata
        assert "updated" in metadata
    
    def test_merge_metadata(self):
        """Test merging metadata dictionaries."""
        base = {
            "id": "SPRINT-BASE",
            "title": "Base Title",
            "status": "proposed",
            "created": "2025-11-17T10:00:00Z"
        }
        updates = {
            "title": "Updated Title",
            "priority": "high"
        }
        
        merged = MetadataManager.merge_metadata(base, updates)
        
        assert merged["id"] == "SPRINT-BASE"  # Preserved
        assert merged["title"] == "Updated Title"  # Updated
        assert merged["priority"] == "high"  # Added
        assert "updated" in merged  # Auto-added timestamp
    
    def test_extract_field(self, tmp_path):
        """Test extracting specific field from file."""
        test_file = tmp_path / "extract.md"
        content = """---
id: SPRINT-EXTRACT
title: Extract Test
status: active
created: 2025-11-17T10:00:00Z
---

Body"""
        test_file.write_text(content)
        
        title = MetadataManager.extract_field(test_file, "title")
        status = MetadataManager.extract_field(test_file, "status")
        nonexistent = MetadataManager.extract_field(test_file, "nonexistent")
        
        assert title == "Extract Test"
        assert status == "active"
        assert nonexistent is None
    
    def test_extract_field_file_error(self, tmp_path):
        """Test extracting field from non-existent file returns None."""
        result = MetadataManager.extract_field(tmp_path / "nonexistent.md", "id")
        assert result is None
    
    def test_validate_file(self, tmp_path):
        """Test validating frontmatter in a file."""
        test_file = tmp_path / "validate.md"
        content = """---
id: SPRINT-VALIDATE
title: Validate Test
status: active
created: 2025-11-17T10:00:00Z
---

Body"""
        test_file.write_text(content)
        
        assert MetadataManager.validate_file(test_file) is True
    
    def test_validate_file_invalid(self, tmp_path):
        """Test validating file with invalid frontmatter."""
        test_file = tmp_path / "invalid.md"
        content = """---
id: INVALID
title: Test
status: active
created: 2025-11-17T10:00:00Z
---

Body"""
        test_file.write_text(content)
        
        with pytest.raises(MetadataValidationError):
            MetadataManager.validate_file(test_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
