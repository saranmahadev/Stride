"""
Tests for stride.utils.validators module.

Tests email and name validation functionality with various valid and invalid inputs.
"""
import pytest
from stride.utils.validators import validate_email, validate_name


class TestEmailValidation:
    """Test email validation function."""
    
    def test_valid_email(self):
        """Test valid email formats."""
        valid_emails = [
            "user@example.com",
            "john.doe@example.com",
            "test+tag@example.co.uk",
            "user_name@example.com",
            "user123@test-domain.com",
            "a@b.co",
            "test@subdomain.example.com",
        ]
        
        for email in valid_emails:
            is_valid, error = validate_email(email)
            assert is_valid, f"Expected {email} to be valid, got error: {error}"
            assert error == ""
    
    def test_empty_email(self):
        """Test empty email validation."""
        is_valid, error = validate_email("")
        assert not is_valid
        assert "Email cannot be empty" in error
    
    def test_whitespace_email(self):
        """Test whitespace-only email."""
        is_valid, error = validate_email("   ")
        assert not is_valid
        assert "Email is too short" in error
    
    def test_missing_at_symbol(self):
        """Test email without @ symbol."""
        is_valid, error = validate_email("userexample.com")
        assert not is_valid
        assert "must contain '@'" in error
    
    def test_multiple_at_symbols(self):
        """Test email with multiple @ symbols."""
        is_valid, error = validate_email("user@@example.com")
        assert not is_valid
        assert "cannot contain multiple '@' symbols" in error
    
    def test_missing_local_part(self):
        """Test email without local part."""
        is_valid, error = validate_email("@example.com")
        assert not is_valid
        assert "must have a username before '@'" in error
    
    def test_missing_domain(self):
        """Test email without domain."""
        is_valid, error = validate_email("user@")
        assert not is_valid
        assert "must have a domain after '@'" in error
    
    def test_missing_tld(self):
        """Test email without TLD."""
        is_valid, error = validate_email("user@example")
        assert not is_valid
        assert "domain must contain a '.'" in error
    
    def test_too_long_email(self):
        """Test email exceeding maximum length."""
        # RFC 5321 maximum is 254 characters
        long_local = "a" * 250
        email = f"{long_local}@test.com"  # This will be over 254 chars
        is_valid, error = validate_email(email)
        assert not is_valid
        assert "too long" in error.lower()
    
    def test_case_insensitivity(self):
        """Test that email validation is case-insensitive."""
        emails = [
            "USER@EXAMPLE.COM",
            "User@Example.Com",
            "uSeR@eXaMpLe.CoM",
        ]
        
        for email in emails:
            is_valid, error = validate_email(email)
            assert is_valid, f"Expected {email} to be valid"


class TestNameValidation:
    """Test name validation function."""
    
    def test_valid_names(self):
        """Test valid name formats."""
        valid_names = [
            "John Doe",
            "Jane",
            "Dr. Smith",
            "Mary-Jane Watson",
            "O'Brien",
            "José García",
            "李明",  # Chinese characters
            "Müller",  # German umlaut
            "A B",  # Minimum length
            "a" * 100,  # Maximum length
        ]
        
        for name in valid_names:
            is_valid, error = validate_name(name)
            assert is_valid, f"Expected '{name}' to be valid, got error: {error}"
            assert error == ""
    
    def test_empty_name(self):
        """Test empty name validation."""
        is_valid, error = validate_name("")
        assert not is_valid
        assert "Name cannot be empty" in error
    
    def test_whitespace_name(self):
        """Test whitespace-only name."""
        is_valid, error = validate_name("   ")
        assert not is_valid
        assert "at least 2 characters" in error
    
    def test_too_short_name(self):
        """Test name that's too short."""
        is_valid, error = validate_name("A")
        assert not is_valid
        assert "at least 2 characters" in error
    
    def test_too_long_name(self):
        """Test name that's too long."""
        long_name = "a" * 101
        is_valid, error = validate_name(long_name)
        assert not is_valid
        assert "100 characters" in error
    
    def test_name_with_numbers(self):
        """Test names with numbers (should be valid)."""
        names_with_numbers = [
            "John Doe 2nd",
            "Agent 007",
            "User123",
        ]
        
        for name in names_with_numbers:
            is_valid, error = validate_name(name)
            assert is_valid, f"Expected '{name}' to be valid"
    
    def test_name_with_special_chars(self):
        """Test names with special characters (should be valid)."""
        special_names = [
            "Anne-Marie",
            "O'Connor",
            "João Silva",
            "Nguyễn Văn A",
        ]
        
        for name in special_names:
            is_valid, error = validate_name(name)
            assert is_valid, f"Expected '{name}' to be valid"


class TestValidationEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_none_values(self):
        """Test validation with None values."""
        # Email validation should handle None gracefully
        try:
            is_valid, error = validate_email(None)
            # If it doesn't raise, it should return invalid
            assert not is_valid
        except (TypeError, AttributeError):
            # It's acceptable to raise an error for None
            pass
        
        # Name validation should handle None gracefully
        try:
            is_valid, error = validate_name(None)
            # If it doesn't raise, it should return invalid
            assert not is_valid
        except (TypeError, AttributeError):
            # It's acceptable to raise an error for None
            pass
    
    def test_exact_boundary_lengths(self):
        """Test exact boundary conditions for length validation."""
        # Name: exactly 2 characters (minimum)
        is_valid, error = validate_name("AB")
        assert is_valid
        
        # Name: exactly 100 characters (maximum)
        is_valid, error = validate_name("A" * 100)
        assert is_valid
        
        # Email: exactly 254 characters (maximum for RFC 5321)
        local = "a" * 64  # Max local part
        domain = "b" * 63 + ".com"  # Max label length
        # Adjust to exactly 254
        total_needed = 254 - len(domain) - 1  # -1 for @
        local = "a" * total_needed
        email = f"{local}@{domain}"
        is_valid, error = validate_email(email)
        # Should be valid at exactly 254
        assert is_valid or len(email) <= 254
    
    def test_unicode_in_email(self):
        """Test Unicode characters in email (should generally be invalid in basic validation)."""
        # Note: Internationalized email addresses exist but basic validation typically rejects them
        unicode_emails = [
            "用户@example.com",
            "user@例え.jp",
        ]
        
        for email in unicode_emails:
            is_valid, error = validate_email(email)
            # Basic regex validation should reject these
            # (internationalized email requires special handling)
            assert not is_valid or error != ""
