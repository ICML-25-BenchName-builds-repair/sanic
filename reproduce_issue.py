import asyncio
from unittest.mock import Mock, AsyncMock, call
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
    
    # Try to verify the calls using has_calls
    try:
        assembler.chunks_queue.put.has_calls(
            call(b"foo"),
            call(None),
        )
        print("Test passed (unexpected)")
    except AttributeError as e:
        print(f"Test failed with error: {e}")
        print("This reproduces the issue in the CI workflow")

if __name__ == "__main__":
    asyncio.run(test_reproduction())