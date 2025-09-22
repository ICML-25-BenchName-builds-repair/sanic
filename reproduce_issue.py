import asyncio
from unittest.mock import AsyncMock, Mock, call
from websockets.frames import Frame, Opcode

from sanic.server.websockets.frame import WebsocketFrameAssembler

async def test_reproduction():
    # Create a WebsocketFrameAssembler instance
    assembler = WebsocketFrameAssembler(Mock())
    
    # Mock the chunks_queue with AsyncMock
    assembler.chunks_queue = AsyncMock(spec=asyncio.Queue)
    assembler.message_fetched = AsyncMock()
    assembler.message_fetched.is_set = Mock(return_value=False)
    
    # Call the put method with a frame
    await assembler.put(Frame(Opcode.TEXT, b"foo"))
    
    # Try to use has_calls on the AsyncMock
    try:
        assembler.chunks_queue.put.has_calls(
            call(b"foo"),
            call(None),
        )
        print("Test passed!")
    except AttributeError as e:
        print(f"Test failed with error: {e}")
        
    # Check if the calls were made using assert_awaited_with
    try:
        assembler.chunks_queue.put.assert_awaited_with(b"foo")
        print("First call assertion passed!")
    except AssertionError as e:
        print(f"First call assertion failed: {e}")
        
    try:
        # Check the call count
        print(f"Call count: {assembler.chunks_queue.put.call_count}")
        # Print the call args
        print(f"Call args: {assembler.chunks_queue.put.call_args_list}")
    except Exception as e:
        print(f"Error getting call info: {e}")

if __name__ == "__main__":
    asyncio.run(test_reproduction())