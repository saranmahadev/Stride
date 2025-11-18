"""
Tests for TemplateEngine.
"""
import pytest
from pathlib import Path
from datetime import datetime

from stride.core.template_engine import TemplateEngine


class TestTemplateEngine:
    """Tests for TemplateEngine class."""
    
    @pytest.fixture
    def template_dir(self, tmp_path):
        """Create a temporary template directory with test templates."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        
        # Create a simple test template
        (template_dir / "test.md.j2").write_text("""---
id: {{ sprint_id }}
title: {{ title }}
---

# {{ title }}

Description: {{ description }}
""")
        
        # Create proposal template
        (template_dir / "proposal.md.j2").write_text("""---
id: {{ sprint_id }}
title: {{ title }}
status: {{ status }}
created: {{ created | timestamp }}
author: {{ author }}
---

# Sprint Proposal: {{ title }}

## Description
{{ description }}

## Priority
{{ priority }}
""")
        
        # Create plan template
        (template_dir / "plan.md.j2").write_text("""---
id: {{ sprint_id }}
title: {{ title }}
---

# Sprint Plan: {{ title }}

## Objectives
{% for objective in objectives %}
- {{ objective }}
{% endfor %}

## Tasks
{% for task in tasks %}
### Task {{ loop.index }}: {{ task.name }}
- Estimated: {{ task.hours }}h
- Description: {{ task.description }}
{% endfor %}

## Estimated Hours
{{ estimated_hours }}h total

## Risks
{% for risk in risks %}
- {{ risk }}
{% endfor %}
""")
        
        return template_dir
    
    def test_template_engine_init(self, template_dir):
        """Test TemplateEngine initialization."""
        engine = TemplateEngine(template_dir)
        assert engine.template_dir == template_dir
        assert engine.env is not None
    
    def test_render_template(self, template_dir):
        """Test basic template rendering."""
        engine = TemplateEngine(template_dir)
        
        result = engine.render_template("test.md.j2", {
            "sprint_id": "SPRINT-TEST",
            "title": "Test Sprint",
            "description": "A test sprint"
        })
        
        assert "SPRINT-TEST" in result
        assert "Test Sprint" in result
        assert "A test sprint" in result
    
    def test_render_template_not_found(self, template_dir):
        """Test rendering non-existent template raises error."""
        from jinja2 import TemplateNotFound
        
        engine = TemplateEngine(template_dir)
        
        with pytest.raises(TemplateNotFound):
            engine.render_template("nonexistent.md.j2", {})
    
    def test_render_proposal(self, template_dir):
        """Test rendering proposal template."""
        engine = TemplateEngine(template_dir)
        
        result = engine.render_proposal(
            sprint_id="SPRINT-PROP",
            title="Proposal Test",
            description="Test description",
            author="test@example.com",
            priority="high"
        )
        
        assert "SPRINT-PROP" in result
        assert "Proposal Test" in result
        assert "Test description" in result
        assert "test@example.com" in result
        assert "high" in result
    
    def test_render_plan(self, template_dir):
        """Test rendering plan template."""
        engine = TemplateEngine(template_dir)
        
        tasks = [
            {"name": "Task 1", "hours": 4, "description": "First task"},
            {"name": "Task 2", "hours": 6, "description": "Second task"}
        ]
        
        result = engine.render_plan(
            sprint_id="SPRINT-PLAN",
            title="Plan Test",
            objectives=["Objective 1", "Objective 2"],
            tasks=tasks,
            estimated_hours=10,
            risks=["Risk 1", "Risk 2"]
        )
        
        assert "SPRINT-PLAN" in result
        assert "Plan Test" in result
        assert "Objective 1" in result
        assert "Objective 2" in result
        assert "Task 1" in result
        assert "Task 2" in result
        assert "10h total" in result
        assert "Risk 1" in result
    
    def test_render_from_string(self, template_dir):
        """Test rendering template from string."""
        engine = TemplateEngine(template_dir)
        
        template_string = "Hello {{ name }}!"
        result = engine.render_from_string(template_string, {"name": "World"})
        
        assert result == "Hello World!"
    
    def test_custom_filters(self, template_dir):
        """Test custom Jinja2 filters."""
        engine = TemplateEngine(template_dir)
        
        # Test timestamp filter
        template = "{{ dt | timestamp }}"
        dt = datetime(2025, 11, 17, 10, 30, 0)
        result = engine.render_from_string(template, {"dt": dt})
        assert "2025-11-17" in result
        
        # Test date filter
        template = "{{ dt | date }}"
        result = engine.render_from_string(template, {"dt": dt})
        assert result == "2025-11-17"
    
    def test_render_implementation(self, template_dir):
        """Test rendering implementation template."""
        # Create implementation template
        (template_dir / "implementation.md.j2").write_text("""---
id: {{ sprint_id }}
title: {{ title }}
completed: {{ completed | timestamp }}
---

# Implementation: {{ title }}

## Summary
{{ summary }}

## Changes
{% for change in changes %}
- {{ change.file }}: {{ change.description }}
{% endfor %}
""")
        
        engine = TemplateEngine(template_dir)
        
        changes = [
            {"file": "file1.py", "description": "Added feature"},
            {"file": "file2.py", "description": "Fixed bug"}
        ]
        
        result = engine.render_implementation(
            sprint_id="SPRINT-IMPL",
            title="Implementation Test",
            summary="Implemented the feature",
            changes=changes
        )
        
        assert "SPRINT-IMPL" in result
        assert "Implementation Test" in result
        assert "Implemented the feature" in result
        assert "file1.py" in result
        assert "Added feature" in result
    
    def test_render_retrospective(self, template_dir):
        """Test rendering retrospective template."""
        # Create retrospective template
        (template_dir / "retrospective.md.j2").write_text("""---
id: {{ sprint_id }}
title: {{ title }}
completed: {{ completed | timestamp }}
---

# Retrospective: {{ title }}

## What Went Well
{% for item in what_went_well %}
- {{ item }}
{% endfor %}

## What Went Wrong
{% for item in what_went_wrong %}
- {{ item }}
{% endfor %}

## Lessons Learned
{% for lesson in lessons_learned %}
- {{ lesson }}
{% endfor %}
""")
        
        engine = TemplateEngine(template_dir)
        
        result = engine.render_retrospective(
            sprint_id="SPRINT-RETRO",
            title="Retrospective Test",
            what_went_well=["Good thing 1", "Good thing 2"],
            what_went_wrong=["Bad thing 1"],
            lessons_learned=["Lesson 1", "Lesson 2"]
        )
        
        assert "SPRINT-RETRO" in result
        assert "Retrospective Test" in result
        assert "Good thing 1" in result
        assert "Bad thing 1" in result
        assert "Lesson 1" in result
    
    def test_render_design(self, template_dir):
        """Test rendering design template."""
        # Create design template
        (template_dir / "design.md.j2").write_text("""---
id: {{ sprint_id }}
title: {{ title }}
---

# Design: {{ title }}

## Overview
{{ overview }}

{% if architecture %}
## Architecture
{{ architecture }}
{% endif %}
""")
        
        engine = TemplateEngine(template_dir)
        
        result = engine.render_design(
            sprint_id="SPRINT-DESIGN",
            title="Design Test",
            overview="This is the design overview",
            architecture="Layered architecture"
        )
        
        assert "SPRINT-DESIGN" in result
        assert "Design Test" in result
        assert "This is the design overview" in result
        assert "Layered architecture" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
