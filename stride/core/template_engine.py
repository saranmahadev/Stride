"""
TemplateEngine - Renders Jinja2 templates for sprint documents.

Handles rendering of:
- proposal.md
- plan.md
- implementation.md
- retrospective.md
- design.md
"""
from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)


class TemplateEngine:
    """Renders Jinja2 templates for sprint documents."""
    
    def __init__(self, template_dir: Optional[Path] = None) -> None:
        """
        Initialize the TemplateEngine.
        
        Args:
            template_dir: Directory containing Jinja2 templates.
                         Defaults to stride/templates/
        """
        if template_dir is None:
            # Default to package templates directory
            template_dir = Path(__file__).parent.parent / "templates"
        
        self.template_dir = template_dir
        logger.debug(f"Initializing TemplateEngine with template_dir: {template_dir}")
        
        # Set up Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )
        
        # Add custom filters
        self.env.filters['timestamp'] = self._format_timestamp
        self.env.filters['date'] = self._format_date
        
        logger.info("TemplateEngine initialized successfully")
    
    @staticmethod
    def _format_timestamp(dt: Optional[datetime] = None) -> str:
        """
        Format datetime as ISO 8601 timestamp.
        
        Args:
            dt: Datetime object, defaults to now (UTC)
            
        Returns:
            ISO 8601 formatted timestamp with Z suffix
        """
        if dt is None:
            dt = datetime.now(timezone.utc)
        # Handle both aware and naive datetimes
        iso_str = dt.isoformat()
        if iso_str.endswith("+00:00"):
            return iso_str.replace("+00:00", "Z")
        elif not iso_str.endswith("Z"):
            return iso_str + "Z"
        return iso_str
    
    @staticmethod
    def _format_date(dt: Optional[datetime] = None) -> str:
        """
        Format datetime as date string.
        
        Args:
            dt: Datetime object, defaults to now (UTC)
            
        Returns:
            Formatted date string (YYYY-MM-DD)
        """
        if dt is None:
            dt = datetime.now(timezone.utc)
        return dt.strftime("%Y-%m-%d")
    
    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Render a Jinja2 template with the given context.
        
        Args:
            template_name: Name of the template file
            context: Dictionary of template variables
            
        Returns:
            Rendered template as string
            
        Raises:
            TemplateNotFound: If template doesn't exist
        """
        logger.debug(f"Rendering template: {template_name}")
        
        try:
            template = self.env.get_template(template_name)
            rendered = template.render(**context)
            logger.debug(f"Successfully rendered {template_name}")
            return rendered
        except TemplateNotFound as e:
            logger.error(f"Template not found: {template_name}")
            raise
        except Exception as e:
            logger.error(f"Error rendering template {template_name}: {e}")
            raise
    
    def render_proposal(
        self,
        sprint_id: str,
        title: str,
        description: str,
        author: str,
        created: Optional[datetime] = None,
        **kwargs: Any
    ) -> str:
        """
        Render a proposal.md template.
        
        Args:
            sprint_id: Sprint identifier
            title: Sprint title
            description: Sprint description
            author: Author email
            created: Creation timestamp
            **kwargs: Additional template variables
            
        Returns:
            Rendered proposal markdown
        """
        logger.info(f"Rendering proposal for {sprint_id}")
        
        context = {
            "sprint_id": sprint_id,
            "title": title,
            "description": description,
            "author": author,
            "created": created or datetime.now(),
            "status": kwargs.get("status", "proposed"),
            "priority": kwargs.get("priority", "medium"),
            **kwargs
        }
        
        return self.render_template("proposal.md.j2", context)
    
    def render_plan(
        self,
        sprint_id: str,
        title: str,
        objectives: list[str],
        tasks: list[Dict[str, Any]],
        estimated_hours: int,
        risks: Optional[list[str]] = None,
        dependencies: Optional[list[str]] = None,
        **kwargs: Any
    ) -> str:
        """
        Render a plan.md template.
        
        Args:
            sprint_id: Sprint identifier
            title: Sprint title
            objectives: List of objectives
            tasks: List of task dictionaries
            estimated_hours: Estimated hours for sprint
            risks: Optional list of risks
            dependencies: Optional list of dependencies
            **kwargs: Additional template variables
            
        Returns:
            Rendered plan markdown
        """
        logger.info(f"Rendering plan for {sprint_id}")
        
        context = {
            "sprint_id": sprint_id,
            "title": title,
            "objectives": objectives,
            "tasks": tasks,
            "estimated_hours": estimated_hours,
            "risks": risks or [],
            "dependencies": dependencies or [],
            "created": datetime.now(),
            **kwargs
        }
        
        return self.render_template("plan.md.j2", context)
    
    def render_implementation(
        self,
        sprint_id: str,
        title: str,
        summary: str,
        changes: list[Dict[str, Any]],
        tests_added: Optional[list[str]] = None,
        notes: Optional[list[str]] = None,
        **kwargs: Any
    ) -> str:
        """
        Render an implementation.md template.
        
        Args:
            sprint_id: Sprint identifier
            title: Sprint title
            summary: Implementation summary
            changes: List of changes made
            tests_added: Optional list of tests added
            notes: Optional implementation notes
            **kwargs: Additional template variables
            
        Returns:
            Rendered implementation markdown
        """
        logger.info(f"Rendering implementation for {sprint_id}")
        
        context = {
            "sprint_id": sprint_id,
            "title": title,
            "summary": summary,
            "changes": changes,
            "tests_added": tests_added or [],
            "notes": notes or [],
            "completed": datetime.now(),
            **kwargs
        }
        
        return self.render_template("implementation.md.j2", context)
    
    def render_retrospective(
        self,
        sprint_id: str,
        title: str,
        what_went_well: list[str],
        what_went_wrong: list[str],
        lessons_learned: list[str],
        action_items: Optional[list[str]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> str:
        """
        Render a retrospective.md template.
        
        Args:
            sprint_id: Sprint identifier
            title: Sprint title
            what_went_well: List of successes
            what_went_wrong: List of problems
            lessons_learned: List of lessons
            action_items: Optional list of action items
            metrics: Optional metrics dictionary
            **kwargs: Additional template variables
            
        Returns:
            Rendered retrospective markdown
        """
        logger.info(f"Rendering retrospective for {sprint_id}")
        
        context = {
            "sprint_id": sprint_id,
            "title": title,
            "what_went_well": what_went_well,
            "what_went_wrong": what_went_wrong,
            "lessons_learned": lessons_learned,
            "action_items": action_items or [],
            "metrics": metrics or {},
            "completed": datetime.now(),
            **kwargs
        }
        
        return self.render_template("retrospective.md.j2", context)
    
    def render_design(
        self,
        sprint_id: str,
        title: str,
        overview: str,
        architecture: Optional[str] = None,
        components: Optional[list[Dict[str, str]]] = None,
        data_model: Optional[str] = None,
        api_design: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        """
        Render a design.md template.
        
        Args:
            sprint_id: Sprint identifier
            title: Sprint title
            overview: Design overview
            architecture: Optional architecture description
            components: Optional list of components
            data_model: Optional data model description
            api_design: Optional API design
            **kwargs: Additional template variables
            
        Returns:
            Rendered design markdown
        """
        logger.info(f"Rendering design for {sprint_id}")
        
        context = {
            "sprint_id": sprint_id,
            "title": title,
            "overview": overview,
            "architecture": architecture,
            "components": components or [],
            "data_model": data_model,
            "api_design": api_design,
            "created": datetime.now(),
            **kwargs
        }
        
        return self.render_template("design.md.j2", context)
    
    def render_from_string(self, template_string: str, context: Dict[str, Any]) -> str:
        """
        Render a template from a string instead of a file.
        
        Args:
            template_string: Template content as string
            context: Dictionary of template variables
            
        Returns:
            Rendered template as string
        """
        logger.debug("Rendering template from string")
        
        try:
            template = self.env.from_string(template_string)
            return template.render(**context)
        except Exception as e:
            logger.error(f"Error rendering template from string: {e}")
            raise
