"""
Tests for stride CLI authentication commands (login, logout, whoami).

Tests the user authentication system including interactive and non-interactive modes,
validation, error handling, and integration with ConfigManager.
"""
import pytest
from click.testing import CliRunner
from stride.cli.main import cli
from stride.core.config_manager import ConfigManager
from pathlib import Path
import tempfile
import os


@pytest.fixture
def runner():
    """Provide a CLI test runner."""
    return CliRunner()


@pytest.fixture
def isolated_config(runner):
    """Create an isolated config environment for testing."""
    with runner.isolated_filesystem():
        # Create a temporary home directory for config
        temp_home = Path.cwd() / "temp_home"
        temp_home.mkdir()
        
        # Set HOME environment variable to temp directory
        old_home = os.environ.get("HOME")
        old_userprofile = os.environ.get("USERPROFILE")
        
        os.environ["HOME"] = str(temp_home)
        os.environ["USERPROFILE"] = str(temp_home)
        
        yield temp_home
        
        # Restore original HOME
        if old_home:
            os.environ["HOME"] = old_home
        else:
            os.environ.pop("HOME", None)
        
        if old_userprofile:
            os.environ["USERPROFILE"] = old_userprofile
        else:
            os.environ.pop("USERPROFILE", None)


class TestLoginCommand:
    """Test stride login command."""
    
    def test_login_non_interactive_both_flags(self, runner, isolated_config):
        """Test login with both name and email flags."""
        result = runner.invoke(cli, [
            "login",
            "--name", "Test User",
            "--email", "test@example.com"
        ])
        
        assert result.exit_code == 0
        assert "Logged in as Test User" in result.output
        assert "test@example.com" in result.output
    
    def test_login_non_interactive_email_only(self, runner, isolated_config):
        """Test login with only email flag."""
        result = runner.invoke(cli, [
            "login",
            "--email", "test@example.com"
        ])
        
        assert result.exit_code == 0
        assert "test@example.com" in result.output
    
    def test_login_invalid_email_no_at(self, runner, isolated_config):
        """Test login with invalid email (no @ symbol)."""
        result = runner.invoke(cli, [
            "login",
            "--name", "Test User",
            "--email", "invalid-email"
        ])
        
        assert result.exit_code == 1
        assert "must contain '@'" in result.output
    
    def test_login_invalid_email_no_domain(self, runner, isolated_config):
        """Test login with invalid email (no domain)."""
        result = runner.invoke(cli, [
            "login",
            "--name", "Test User",
            "--email", "test@"
        ])
        
        assert result.exit_code == 1
        assert "must have a domain after '@'" in result.output
    
    def test_login_invalid_email_no_tld(self, runner, isolated_config):
        """Test login with invalid email (no TLD)."""
        result = runner.invoke(cli, [
            "login",
            "--name", "Test User",
            "--email", "test@domain"
        ])
        
        assert result.exit_code == 1
        assert "domain must contain a '.'" in result.output
    
    def test_login_invalid_name_too_short(self, runner, isolated_config):
        """Test login with name that's too short."""
        result = runner.invoke(cli, [
            "login",
            "--name", "A",
            "--email", "test@example.com"
        ])
        
        assert result.exit_code == 1
        assert "at least 2 characters" in result.output
    
    def test_login_invalid_name_too_long(self, runner, isolated_config):
        """Test login with name that's too long."""
        long_name = "A" * 101
        result = runner.invoke(cli, [
            "login",
            "--name", long_name,
            "--email", "test@example.com"
        ])
        
        assert result.exit_code == 1
        assert "100 characters" in result.output
    
    def test_login_update_existing_user(self, runner, isolated_config):
        """Test updating an existing logged-in user."""
        # First login
        result1 = runner.invoke(cli, [
            "login",
            "--name", "First User",
            "--email", "first@example.com"
        ])
        assert result1.exit_code == 0
        
        # Update login
        result2 = runner.invoke(cli, [
            "login",
            "--name", "Updated User",
            "--email", "updated@example.com"
        ])
        assert result2.exit_code == 0
        assert "Updated User" in result2.output
        assert "updated@example.com" in result2.output
    
    def test_login_interactive_mode(self, runner, isolated_config):
        """Test interactive login with prompts."""
        result = runner.invoke(cli, ["login"], input="John Doe\njohn@example.com\n")
        
        assert result.exit_code == 0
        assert "Setup User Identity" in result.output or "Name:" in result.output
        assert "john@example.com" in result.output
    
    def test_login_quiet_mode(self, runner, isolated_config):
        """Test login in quiet mode."""
        result = runner.invoke(cli, [
            "--quiet",
            "login",
            "--name", "Test User",
            "--email", "test@example.com"
        ])
        
        assert result.exit_code == 0
        # Should have minimal output in quiet mode
        assert "Test User" not in result.output or result.output.strip() == ""
    
    def test_login_special_characters_in_name(self, runner, isolated_config):
        """Test login with special characters in name."""
        result = runner.invoke(cli, [
            "login",
            "--name", "John O'Brien-Smith",
            "--email", "john@example.com"
        ])
        
        assert result.exit_code == 0
        assert "John O'Brien-Smith" in result.output


class TestLogoutCommand:
    """Test stride logout command."""
    
    def test_logout_not_logged_in(self, runner, isolated_config):
        """Test logout when no user is logged in."""
        result = runner.invoke(cli, ["logout", "--force"])
        
        assert result.exit_code == 1
        assert "Not logged in" in result.output
    
    def test_logout_with_force_flag(self, runner, isolated_config):
        """Test logout with force flag (skip confirmation)."""
        # First login
        runner.invoke(cli, [
            "login",
            "--name", "Test User",
            "--email", "test@example.com"
        ])
        
        # Logout with force
        result = runner.invoke(cli, ["logout", "--force"])
        
        assert result.exit_code == 0
        assert "Logged out successfully" in result.output
    
    def test_logout_with_confirmation_yes(self, runner, isolated_config):
        """Test logout with confirmation (user confirms)."""
        # First login
        runner.invoke(cli, [
            "login",
            "--name", "Test User",
            "--email", "test@example.com"
        ])
        
        # Logout with confirmation (answer yes)
        result = runner.invoke(cli, ["logout"], input="y\n")
        
        assert result.exit_code == 0
        assert "Logged out successfully" in result.output
    
    def test_logout_with_confirmation_no(self, runner, isolated_config):
        """Test logout with confirmation (user cancels)."""
        # First login
        runner.invoke(cli, [
            "login",
            "--name", "Test User",
            "--email", "test@example.com"
        ])
        
        # Logout with confirmation (answer no)
        result = runner.invoke(cli, ["logout"], input="n\n")
        
        assert result.exit_code == 0
        assert "Cancelled" in result.output
        
        # Verify still logged in
        result = runner.invoke(cli, ["whoami"])
        assert result.exit_code == 0
        assert "Test User" in result.output
    
    def test_logout_clears_credentials(self, runner, isolated_config):
        """Test that logout properly clears credentials."""
        # First login
        runner.invoke(cli, [
            "login",
            "--name", "Test User",
            "--email", "test@example.com"
        ])
        
        # Logout
        runner.invoke(cli, ["logout", "--force"])
        
        # Verify not logged in
        result = runner.invoke(cli, ["whoami"])
        assert result.exit_code == 1
        assert "Not logged in" in result.output
    
    def test_logout_quiet_mode(self, runner, isolated_config):
        """Test logout in quiet mode."""
        # First login
        runner.invoke(cli, [
            "login",
            "--name", "Test User",
            "--email", "test@example.com"
        ])
        
        # Logout in quiet mode with force
        result = runner.invoke(cli, ["--quiet", "logout", "--force"])
        
        assert result.exit_code == 0


class TestWhoamiCommand:
    """Test stride whoami command."""
    
    def test_whoami_not_logged_in(self, runner, isolated_config):
        """Test whoami when no user is logged in."""
        result = runner.invoke(cli, ["whoami"])
        
        assert result.exit_code == 1
        assert "Not logged in" in result.output
        assert "stride login" in result.output
    
    def test_whoami_logged_in(self, runner, isolated_config):
        """Test whoami with logged-in user."""
        # First login
        runner.invoke(cli, [
            "login",
            "--name", "Test User",
            "--email", "test@example.com"
        ])
        
        # Check whoami
        result = runner.invoke(cli, ["whoami"])
        
        assert result.exit_code == 0
        assert "Test User" in result.output
        assert "test@example.com" in result.output
        assert "Logged in" in result.output
    
    def test_whoami_quiet_mode_logged_in(self, runner, isolated_config):
        """Test whoami in quiet mode when logged in."""
        # First login
        runner.invoke(cli, [
            "login",
            "--name", "Test User",
            "--email", "test@example.com"
        ])
        
        # Check whoami in quiet mode
        result = runner.invoke(cli, ["--quiet", "whoami"])
        
        assert result.exit_code == 0
        assert "test@example.com" in result.output
    
    def test_whoami_quiet_mode_not_logged_in(self, runner, isolated_config):
        """Test whoami in quiet mode when not logged in."""
        result = runner.invoke(cli, ["--quiet", "whoami"])
        
        assert result.exit_code == 1
        assert "Not logged in" in result.output
    
    def test_whoami_shows_config_path(self, runner, isolated_config):
        """Test that whoami shows config file path."""
        # First login
        runner.invoke(cli, [
            "login",
            "--name", "Test User",
            "--email", "test@example.com"
        ])
        
        # Check whoami
        result = runner.invoke(cli, ["whoami"])
        
        assert result.exit_code == 0
        assert "Config:" in result.output or "config" in result.output.lower()


class TestAuthenticationFlow:
    """Test complete authentication workflows."""
    
    def test_login_logout_login_flow(self, runner, isolated_config):
        """Test complete login -> logout -> login flow."""
        # First login
        result1 = runner.invoke(cli, [
            "login",
            "--name", "First User",
            "--email", "first@example.com"
        ])
        assert result1.exit_code == 0
        
        # Verify logged in
        result2 = runner.invoke(cli, ["whoami"])
        assert result2.exit_code == 0
        assert "First User" in result2.output
        
        # Logout
        result3 = runner.invoke(cli, ["logout", "--force"])
        assert result3.exit_code == 0
        
        # Verify logged out
        result4 = runner.invoke(cli, ["whoami"])
        assert result4.exit_code == 1
        
        # Login again with different user
        result5 = runner.invoke(cli, [
            "login",
            "--name", "Second User",
            "--email", "second@example.com"
        ])
        assert result5.exit_code == 0
        
        # Verify new user
        result6 = runner.invoke(cli, ["whoami"])
        assert result6.exit_code == 0
        assert "Second User" in result6.output
        assert "second@example.com" in result6.output
    
    def test_multiple_login_updates(self, runner, isolated_config):
        """Test multiple login updates without logout."""
        users = [
            ("User One", "one@example.com"),
            ("User Two", "two@example.com"),
            ("User Three", "three@example.com"),
        ]
        
        for name, email in users:
            result = runner.invoke(cli, [
                "login",
                "--name", name,
                "--email", email
            ])
            assert result.exit_code == 0
            
            # Verify current user
            result = runner.invoke(cli, ["whoami"])
            assert name in result.output
            assert email in result.output
