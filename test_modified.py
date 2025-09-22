import asyncio
from unittest.mock import AsyncMock, Mock, call
from websockets.frames import Frame, Opcode

from sanic.server.websockets.frame import WebsocketFrameAssembler

async def test_modified():
    # Create a WebsocketFrameAssembler instance
    assembler = WebsocketFrameAssembler(Mock())
    
    # Mock the chunks_queue with AsyncMock but without spec
    assembler.chunks_queue = AsyncMock()  # No spec here
    assembler.message_fetched = AsyncMock()
    assembler.message_fetched.is_set = Mock(return_value=False)
    
    # Call the put method with a frame
    await assembler.put(Frame(Opcode.TEXT, b"foo"))
    
    # Try to use assert_has_calls on the AsyncMock
    try:
        assembler.chunks_queue.put.assert_has_calls(
            [call(b"foo"), call(None)]
        )
        print("Test passed with assert_has_calls!")
    except AttributeError as e:
        print(f"assert_has_calls failed with error: {e}")
    except AssertionError as e:
        print(f"assert_has_calls failed with assertion error: {e}")
        
    # Print the call args
    print(f"Call args: {assembler.chunks_queue.put.call_args_list}")

if __name__ == "__main__":
    asyncio.run(test_modified())