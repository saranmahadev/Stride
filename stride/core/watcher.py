"""
File system watcher for monitoring sprint changes in real-time.

This module provides file system monitoring capabilities for the watch command,
tracking changes to sprint files and emitting events for live display.
"""

import time
from pathlib import Path
from typing import Callable, Optional, Set, TYPE_CHECKING
from datetime import datetime
from threading import Event as ThreadEvent

from watchdog.observers import Observer

if TYPE_CHECKING:
    from watchdog.observers import Observer as ObserverType
from watchdog.events import (
    FileSystemEventHandler,
    FileSystemEvent,
    FileModifiedEvent,
    FileCreatedEvent,
    FileDeletedEvent,
    FileMovedEvent,
)


class SprintEvent:
    """Represents a file system event within a sprint."""
    
    def __init__(
        self,
        event_type: str,
        file_path: Path,
        timestamp: Optional[datetime] = None,
        src_path: Optional[Path] = None,
        dest_path: Optional[Path] = None,
    ):
        self.event_type = event_type  # 'modified', 'created', 'deleted', 'moved'
        self.file_path = file_path
        self.timestamp = timestamp or datetime.now()
        self.src_path = src_path
        self.dest_path = dest_path
    
    @property
    def file_name(self) -> str:
        """Get the filename from the path."""
        return self.file_path.name
    
    @property
    def relative_path(self) -> str:
        """Get relative path string."""
        return str(self.file_path)
    
    def __repr__(self) -> str:
        return f"SprintEvent({self.event_type}, {self.file_name}, {self.timestamp})"


class SprintFileHandler(FileSystemEventHandler):
    """
    Handler for file system events within a sprint folder.
    
    Filters events to only track sprint-relevant files and calls
    callback function for each event.
    """
    
    # Files to monitor (sprint documents)
    TRACKED_FILES = {
        'proposal.md',
        'plan.md',
        'design.md',
        'implementation.md',
        'retrospective.md',
        'notes.md',
    }
    
    # Directories to ignore
    IGNORED_DIRS = {
        '__pycache__',
        '.git',
        '.pytest_cache',
        'node_modules',
        'venv',
        '.venv',
    }
    
    def __init__(
        self,
        sprint_path: Path,
        callback: Callable[[SprintEvent], None],
    ):
        """
        Initialize the handler.
        
        Args:
            sprint_path: Path to the sprint folder to monitor
            callback: Function to call when events occur
        """
        super().__init__()
        self.sprint_path = sprint_path
        self.callback = callback
        self._last_events: dict[str, float] = {}  # Debounce duplicate events
        self._debounce_seconds = 0.5
    
    def _should_process(self, path: str) -> bool:
        """
        Check if file should be processed.
        
        Args:
            path: File path to check
            
        Returns:
            True if file should be tracked, False otherwise
        """
        file_path = Path(path)
        
        # Check if path is within sprint folder
        try:
            file_path.relative_to(self.sprint_path)
        except ValueError:
            return False
        
        # Ignore directories
        if file_path.is_dir():
            return False
        
        # Check if any parent is in ignored directories
        for parent in file_path.parents:
            if parent.name in self.IGNORED_DIRS:
                return False
        
        # Check if filename is tracked
        if file_path.name not in self.TRACKED_FILES:
            return False
        
        # Debounce duplicate events
        event_key = str(file_path)
        current_time = time.time()
        last_time = self._last_events.get(event_key, 0)
        
        if current_time - last_time < self._debounce_seconds:
            return False
        
        self._last_events[event_key] = current_time
        return True
    
    def _create_event(
        self,
        event_type: str,
        path: str,
        src_path: Optional[str] = None,
        dest_path: Optional[str] = None,
    ) -> SprintEvent:
        """Create a SprintEvent from file system event data."""
        file_path = Path(path)
        
        return SprintEvent(
            event_type=event_type,
            file_path=file_path,
            timestamp=datetime.now(),
            src_path=Path(src_path) if src_path else None,
            dest_path=Path(dest_path) if dest_path else None,
        )
    
    def on_modified(self, event: FileModifiedEvent) -> None:
        """Handle file modification events."""
        if not event.is_directory and self._should_process(event.src_path):
            sprint_event = self._create_event('modified', event.src_path)
            self.callback(sprint_event)
    
    def on_created(self, event: FileCreatedEvent) -> None:
        """Handle file creation events."""
        if not event.is_directory and self._should_process(event.src_path):
            sprint_event = self._create_event('created', event.src_path)
            self.callback(sprint_event)
    
    def on_deleted(self, event: FileDeletedEvent) -> None:
        """Handle file deletion events."""
        if not event.is_directory and self._should_process(event.src_path):
            sprint_event = self._create_event('deleted', event.src_path)
            self.callback(sprint_event)
    
    def on_moved(self, event: FileMovedEvent) -> None:
        """Handle file move/rename events."""
        if not event.is_directory and self._should_process(event.dest_path):
            sprint_event = self._create_event(
                'moved',
                event.dest_path,
                src_path=event.src_path,
                dest_path=event.dest_path,
            )
            self.callback(sprint_event)


class SprintWatcher:
    """
    Watches a sprint folder for file system changes.
    
    Monitors sprint documents and emits events for live display.
    """
    
    def __init__(
        self,
        sprint_path: Path,
        callback: Callable[[SprintEvent], None],
    ):
        """
        Initialize the watcher.
        
        Args:
            sprint_path: Path to sprint folder to watch
            callback: Function to call when events occur
        """
        self.sprint_path = sprint_path
        self.callback = callback
        
        self._observer = None
        self._handler = None
        self._stop_event = ThreadEvent()
        self._is_running = False
    
    def start(self) -> None:
        """Start watching the sprint folder."""
        if self._is_running:
            return
        
        # Create handler and observer
        self._handler = SprintFileHandler(self.sprint_path, self.callback)
        self._observer = Observer()
        
        # Schedule watching the sprint folder
        self._observer.schedule(
            self._handler,
            str(self.sprint_path),
            recursive=True,
        )
        
        # Start observer
        self._observer.start()
        self._is_running = True
    
    def stop(self) -> None:
        """Stop watching the sprint folder."""
        if not self._is_running:
            return
        
        if self._observer:
            self._observer.stop()
            self._observer.join(timeout=2.0)
        
        self._is_running = False
        self._stop_event.set()
    
    def wait(self, timeout: Optional[float] = None) -> bool:
        """
        Wait for stop signal.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if stopped, False if timeout
        """
        return self._stop_event.wait(timeout=timeout)
    
    @property
    def is_running(self) -> bool:
        """Check if watcher is currently running."""
        return self._is_running
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
        return False
