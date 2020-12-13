import pytest
import j2f5


def test_alter_context():
    """alter_context returns dict and sets global _context"""
    test_ctx = {"context": "test"}
    assert isinstance(j2f5.alter_context(test_ctx), dict)
    assert j2f5._context == test_ctx
