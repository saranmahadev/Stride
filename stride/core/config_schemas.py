"""
Configuration schemas for validation.

Defines the structure and validation rules for user and project configurations.
"""

# User configuration schema
USER_CONFIG_SCHEMA = {
    "user": {
        "name": {
            "type": "string",
            "required": False
        },
        "email": {
            "type": "string",
            "required": False,
            "pattern": "email"
        }
    },
    "defaults": {
        "priority": {
            "type": "string",
            "enum": ["low", "medium", "high", "critical"],
            "required": False
        },
        "tags": {
            "type": "array",
            "items": "string",
            "required": False
        },
        "format": {
            "type": "string",
            "enum": ["table", "list", "json"],
            "required": False
        }
    },
    "editor": {
        "preferred": {
            "type": "string",
            "required": False
        }
    },
    "templates": {
        "custom_path": {
            "type": "string",
            "required": False
        }
    }
}

# Project configuration schema
PROJECT_CONFIG_SCHEMA = {
    "project": {
        "name": {
            "type": "string",
            "required": True
        },
        "version": {
            "type": "string",
            "required": False
        },
        "agents": {
            "type": "array",
            "items": "string",
            "required": False
        }
    },
    "validation": {
        "strict": {
            "type": "boolean",
            "required": False
        },
        "require_tests": {
            "type": "boolean",
            "required": False
        },
        "require_docs": {
            "type": "boolean",
            "required": False
        }
    },
    "sprint": {
        "default_priority": {
            "type": "string",
            "enum": ["low", "medium", "high", "critical"],
            "required": False
        },
        "auto_archive_after_days": {
            "type": "integer",
            "min": 1,
            "max": 365,
            "required": False
        }
    },
    "templates": {
        "path": {
            "type": "string",
            "required": False
        }
    },
    "paths": {
        "sprints": {
            "type": "string",
            "required": False
        },
        "specs": {
            "type": "string",
            "required": False
        }
    }
}
