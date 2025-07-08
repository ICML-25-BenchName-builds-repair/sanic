import asyncio
from unittest.mock import AsyncMock, Mock, call
from asyncio import Queue

async def main():
    # Create a mock with spec=Queue
    queue_mock = AsyncMock(spec=Queue)
    
    # Try to use has_calls on the put method
    try:
        queue_mock.put.has_calls(
            call("data"),
            call(None)
        )
        print("has_calls worked!")
    except AttributeError as e:
        print(f"Error: {e}")
    
    # Try to use assert_has_calls on the put method
    try:
        queue_mock.put.assert_has_calls([
            call("data"),
            call(None)
        ])
        print("assert_has_calls worked!")
    except AssertionError as e:
        print(f"Assertion Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())