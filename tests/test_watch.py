"""
Tests for watch command and file system monitoring.
"""
import pytest
from pathlib import Path
import time
from click.testing import CliRunner

from stride.cli.main import cli
from stride.core.watcher import SprintWatcher, SprintEvent, SprintFileHandler


class TestSprintEvent:
    """Tests for SprintEvent class."""
    
    def test_create_event(self):
        """Test creating a sprint event."""
        event = SprintEvent(
            event_type='modified',
            file_path=Path('proposal.md'),
        )
        
        assert event.event_type == 'modified'
        assert event.file_name == 'proposal.md'
        assert event.timestamp is not None
    
    def test_event_with_move(self):
        """Test event with source and destination paths."""
        event = SprintEvent(
            event_type='moved',
            file_path=Path('new.md'),
            src_path=Path('old.md'),
            dest_path=Path('new.md'),
        )
        
        assert event.event_type == 'moved'
        assert event.src_path == Path('old.md')
        assert event.dest_path == Path('new.md')
    
    def test_event_repr(self):
        """Test event string representation."""
        event = SprintEvent(
            event_type='created',
            file_path=Path('plan.md'),
        )
        
        repr_str = repr(event)
        assert 'SprintEvent' in repr_str
        assert 'created' in repr_str
        assert 'plan.md' in repr_str


class TestSprintFileHandler:
    """Tests for SprintFileHandler class."""
    
    def test_tracked_files(self):
        """Test that correct files are tracked."""
        assert 'proposal.md' in SprintFileHandler.TRACKED_FILES
        assert 'plan.md' in SprintFileHandler.TRACKED_FILES
        assert 'design.md' in SprintFileHandler.TRACKED_FILES
        assert 'implementation.md' in SprintFileHandler.TRACKED_FILES
        assert 'retrospective.md' in SprintFileHandler.TRACKED_FILES
        assert 'notes.md' in SprintFileHandler.TRACKED_FILES
    
    def test_ignored_dirs(self):
        """Test that correct directories are ignored."""
        assert '__pycache__' in SprintFileHandler.IGNORED_DIRS
        assert '.git' in SprintFileHandler.IGNORED_DIRS
        assert 'node_modules' in SprintFileHandler.IGNORED_DIRS
    
    def test_should_process_tracked_file(self, tmp_path):
        """Test that tracked files are processed."""
        sprint_path = tmp_path / "SPRINT-TEST"
        sprint_path.mkdir()
        
        events = []
        handler = SprintFileHandler(sprint_path, lambda e: events.append(e))
        
        file_path = sprint_path / "proposal.md"
        file_path.write_text("test")
        
        assert handler._should_process(str(file_path))
    
    def test_should_not_process_untracked_file(self, tmp_path):
        """Test that untracked files are ignored."""
        sprint_path = tmp_path / "SPRINT-TEST"
        sprint_path.mkdir()
        
        events = []
        handler = SprintFileHandler(sprint_path, lambda e: events.append(e))
        
        file_path = sprint_path / "random.txt"
        file_path.write_text("test")
        
        assert not handler._should_process(str(file_path))
    
    def test_should_not_process_ignored_dir(self, tmp_path):
        """Test that files in ignored directories are skipped."""
        sprint_path = tmp_path / "SPRINT-TEST"
        sprint_path.mkdir()
        
        events = []
        handler = SprintFileHandler(sprint_path, lambda e: events.append(e))
        
        ignored_dir = sprint_path / "__pycache__"
        ignored_dir.mkdir()
        file_path = ignored_dir / "proposal.md"
        file_path.write_text("test")
        
        assert not handler._should_process(str(file_path))
    
    def test_debounce_duplicate_events(self, tmp_path):
        """Test that duplicate events are debounced."""
        sprint_path = tmp_path / "SPRINT-TEST"
        sprint_path.mkdir()
        
        events = []
        handler = SprintFileHandler(sprint_path, lambda e: events.append(e))
        
        file_path = sprint_path / "proposal.md"
        file_path.write_text("test")
        
        # First call should process
        assert handler._should_process(str(file_path))
        
        # Immediate second call should be debounced
        assert not handler._should_process(str(file_path))
        
        # After debounce period, should process again
        time.sleep(0.6)  # Longer than debounce_seconds (0.5)
        assert handler._should_process(str(file_path))


class TestSprintWatcher:
    """Tests for SprintWatcher class."""
    
    def test_watcher_initialization(self, tmp_path):
        """Test watcher initialization."""
        sprint_path = tmp_path / "SPRINT-TEST"
        sprint_path.mkdir()
        
        events = []
        watcher = SprintWatcher(sprint_path, lambda e: events.append(e))
        
        assert watcher.sprint_path == sprint_path
        assert not watcher.is_running
    
    def test_watcher_start_stop(self, tmp_path):
        """Test starting and stopping watcher."""
        sprint_path = tmp_path / "SPRINT-TEST"
        sprint_path.mkdir()
        
        events = []
        watcher = SprintWatcher(sprint_path, lambda e: events.append(e))
        
        watcher.start()
        assert watcher.is_running
        
        watcher.stop()
        assert not watcher.is_running
    
    def test_watcher_context_manager(self, tmp_path):
        """Test watcher as context manager."""
        sprint_path = tmp_path / "SPRINT-TEST"
        sprint_path.mkdir()
        
        events = []
        
        with SprintWatcher(sprint_path, lambda e: events.append(e)) as watcher:
            assert watcher.is_running
        
        assert not watcher.is_running
    
    def test_watcher_detects_file_creation(self, tmp_path):
        """Test that watcher detects file creation."""
        sprint_path = tmp_path / "SPRINT-TEST"
        sprint_path.mkdir()
        
        events = []
        
        with SprintWatcher(sprint_path, lambda e: events.append(e)):
            time.sleep(0.5)  # Give watcher time to start
            
            # Create a tracked file
            file_path = sprint_path / "proposal.md"
            file_path.write_text("# Test Proposal\n")
            
            time.sleep(1.0)  # Give watcher time to detect
        
        # Should have detected the file creation
        assert len(events) > 0
        assert any(e.event_type == 'created' for e in events)
        assert any(e.file_name == 'proposal.md' for e in events)
    
    def test_watcher_detects_file_modification(self, tmp_path):
        """Test that watcher detects file modifications."""
        sprint_path = tmp_path / "SPRINT-TEST"
        sprint_path.mkdir()
        
        # Create file before watching
        file_path = sprint_path / "proposal.md"
        file_path.write_text("# Test Proposal\n")
        
        events = []
        
        with SprintWatcher(sprint_path, lambda e: events.append(e)):
            time.sleep(0.5)  # Give watcher time to start
            
            # Modify the file
            file_path.write_text("# Updated Proposal\n")
            
            time.sleep(1.0)  # Give watcher time to detect
        
        # Should have detected the modification
        assert len(events) > 0
        assert any(e.event_type == 'modified' for e in events)
        assert any(e.file_name == 'proposal.md' for e in events)
    
    def test_watcher_ignores_untracked_files(self, tmp_path):
        """Test that watcher ignores untracked files."""
        sprint_path = tmp_path / "SPRINT-TEST"
        sprint_path.mkdir()
        
        events = []
        
        with SprintWatcher(sprint_path, lambda e: events.append(e)):
            time.sleep(0.5)  # Give watcher time to start
            
            # Create an untracked file
            file_path = sprint_path / "random.txt"
            file_path.write_text("Random content\n")
            
            time.sleep(1.0)  # Give watcher time (if it would detect)
        
        # Should not have detected anything
        assert len(events) == 0


class TestWatchCommand:
    """Tests for watch CLI command."""
    
    def test_watch_command_help(self):
        """Test watch command help text."""
        runner = CliRunner()
        result = runner.invoke(cli, ['watch', '--help'])
        
        assert result.exit_code == 0
        assert 'Watch a sprint for real-time file changes' in result.output
        assert '--interval' in result.output
    
    def test_watch_nonexistent_sprint(self, tmp_path):
        """Test watch command with non-existent sprint."""
        runner = CliRunner()
        
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Initialize project
            runner.invoke(cli, ['init', '--name', 'Test', '--force'])
            
            # Try to watch non-existent sprint
            result = runner.invoke(cli, ['watch', 'SPRINT-NONE'])
            
            assert result.exit_code != 0
            assert 'Sprint not found' in result.output or 'not found' in result.output.lower()
    
    def test_watch_command_requires_sprint_id(self):
        """Test that watch command requires sprint ID."""
        runner = CliRunner()
        result = runner.invoke(cli, ['watch'])
        
        assert result.exit_code != 0
        assert 'Missing argument' in result.output or 'SPRINT_ID' in result.output
    
    def test_watch_interval_option(self, tmp_path):
        """Test watch command with custom interval."""
        runner = CliRunner()
        
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Initialize and create sprint
            runner.invoke(cli, ['init', '--name', 'Test', '--force'])
            create_result = runner.invoke(cli, ['create', '--title', 'Test Sprint'])
            
            # Extract sprint ID from output
            sprint_id = None
            for line in create_result.output.split('\n'):
                if 'SPRINT-' in line:
                    parts = line.split('SPRINT-')
                    if len(parts) > 1:
                        sprint_id = 'SPRINT-' + parts[1].split()[0].strip()
                        break
            
            assert sprint_id is not None
            
            # Watch command should accept interval option (we won't actually run it)
            result = runner.invoke(cli, ['watch', '--help'])
            assert '--interval' in result.output
            assert '-i' in result.output


class TestWatcherEdgeCases:
    """Tests for edge cases in watcher functionality."""
    
    def test_watcher_handles_missing_directory(self):
        """Test watcher with non-existent directory."""
        sprint_path = Path("/nonexistent/path/SPRINT-TEST")
        
        events = []
        watcher = SprintWatcher(sprint_path, lambda e: events.append(e))
        
        # watchdog raises FileNotFoundError on Windows for non-existent paths
        # This is expected behavior - the watch command validates existence first
        with pytest.raises(FileNotFoundError):
            watcher.start()
        
        # Ensure watcher can still be stopped even after failed start
        watcher.stop()
    
    def test_multiple_watchers_same_path(self, tmp_path):
        """Test multiple watchers on same path."""
        sprint_path = tmp_path / "SPRINT-TEST"
        sprint_path.mkdir()
        
        events1 = []
        events2 = []
        
        watcher1 = SprintWatcher(sprint_path, lambda e: events1.append(e))
        watcher2 = SprintWatcher(sprint_path, lambda e: events2.append(e))
        
        watcher1.start()
        watcher2.start()
        
        time.sleep(0.5)
        
        # Create file
        file_path = sprint_path / "proposal.md"
        file_path.write_text("test")
        
        time.sleep(1.0)
        
        watcher1.stop()
        watcher2.stop()
        
        # Both watchers should have detected the event
        assert len(events1) > 0
        assert len(events2) > 0
    
    def test_watcher_double_start(self, tmp_path):
        """Test that double start is handled gracefully."""
        sprint_path = tmp_path / "SPRINT-TEST"
        sprint_path.mkdir()
        
        events = []
        watcher = SprintWatcher(sprint_path, lambda e: events.append(e))
        
        watcher.start()
        watcher.start()  # Second start should be ignored
        
        assert watcher.is_running
        
        watcher.stop()
    
    def test_watcher_double_stop(self, tmp_path):
        """Test that double stop is handled gracefully."""
        sprint_path = tmp_path / "SPRINT-TEST"
        sprint_path.mkdir()
        
        events = []
        watcher = SprintWatcher(sprint_path, lambda e: events.append(e))
        
        watcher.start()
        watcher.stop()
        watcher.stop()  # Second stop should be ignored
        
        assert not watcher.is_running
