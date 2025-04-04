import asyncio
import unittest
from unittest.mock import Mock, AsyncMock, call
from websockets.frames import Frame, Opcode

from sanic.server.websockets.frame import WebsocketFrameAssembler

class TestWebsocketFrameAssembler(unittest.TestCase):
    async def test_ws_frame_put_message_into_queue(self):
        # Create a WebsocketFrameAssembler instance
        assembler = WebsocketFrameAssembler(Mock())
        
        # Mock the chunks_queue
        assembler.chunks_queue = AsyncMock(spec=asyncio.Queue)
        
        # Mock the message_fetched
        assembler.message_fetched = AsyncMock()
        assembler.message_fetched.is_set = Mock(return_value=False)
        
        # Call put with a frame
        await assembler.put(Frame(Opcode.TEXT, b"foo"))
        
        # Print the calls that were made
        print("Calls made to chunks_queue.put:", assembler.chunks_queue.put.mock_calls)
        
        # Try to verify the calls
        try:
            # This is what the test is doing
            assembler.chunks_queue.put.has_calls(
                call(b"foo"),
                call(None),
            )
            print("Test passed with has_calls")
        except Exception as e:
            print(f"Error: {e}")
            raise

async def run_test():
    test = TestWebsocketFrameAssembler()
    await test.test_ws_frame_put_message_into_queue()

if __name__ == "__main__":
    asyncio.run(run_test())