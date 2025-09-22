"""
Monkey patch for AsyncMock to add has_calls method for Python 3.12 compatibility.

In Python 3.12, the `has_calls` method is not available on AsyncMock objects with a spec.
This module adds the method to AsyncMock for compatibility with existing tests.
"""
import sys
import types
from unittest.mock import AsyncMock, call

if sys.version_info >= (3, 12):
    # Add has_calls method to AsyncMock for Python 3.12 compatibility
    def has_calls(self, calls, any_order=False):
        """
        Check if the mock has been called with the specified calls.
        This is a compatibility method for Python 3.12.
        
        Args:
            calls: A list of call objects to check against the mock's call list.
            any_order: If True, the calls can be in any order. If False, the calls
                must be in the same order as the mock's call list.
                
        Returns:
            True if the mock has been called with the specified calls, False otherwise.
        """
        if not isinstance(calls, list):
            calls = [calls]
            
        try:
            self.assert_has_calls(calls, any_order)
            return True
        except (AssertionError, AttributeError):
            # Check manually if assert_has_calls is not available
            if not hasattr(self, 'assert_has_calls'):
                call_list = self.call_args_list
                if any_order:
                    return all(c in call_list for c in calls)
                else:
                    if len(calls) > len(call_list):
                        return False
                    return all(c == call_list[i] for i, c in enumerate(calls))
            return False
    
    # Add the method to AsyncMock
    if not hasattr(AsyncMock, 'has_calls'):
        AsyncMock.has_calls = has_calls