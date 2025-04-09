import asyncio
from unittest.mock import Mock, call, AsyncMock
from websockets.frames import Frame, Opcode
from sanic.server.websockets.frame import WebsocketFrameAssembler

async def test_ws_frame_put_message_into_queue():
    # Create the assembler
    assembler = WebsocketFrameAssembler(Mock())
    assembler.chunks_queue = AsyncMock(spec=asyncio.Queue)
    assembler.message_fetched = AsyncMock()
    assembler.message_fetched.is_set = Mock(return_value=False)
    
    # Call the put method
    await assembler.put(Frame(Opcode.TEXT, b"foo"))
    
    # Check the calls
    print("Checking calls on AsyncMock...")
    print(f"Actual calls: {assembler.chunks_queue.put.mock_calls}")
    
    # Use has_calls method
    try:
        assembler.chunks_queue.put.has_calls(
            call(b"foo"),
            call(None),
        )
        print("Success! has_calls method worked.")
    except Exception as e:
        print(f"Error with has_calls: {e}")

async def main():
    await test_ws_frame_put_message_into_queue()

if __name__ == "__main__":
    asyncio.run(main())