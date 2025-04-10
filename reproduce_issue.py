import asyncio
from unittest.mock import Mock, call, AsyncMock
from websockets.frames import Frame, Opcode
from sanic.server.websockets.frame import WebsocketFrameAssembler

async def test_ws_frame_put():
    # Create a WebsocketFrameAssembler with a mock protocol
    assembler = WebsocketFrameAssembler(Mock())
    
    # Replace chunks_queue with an AsyncMock
    assembler.chunks_queue = AsyncMock(spec=asyncio.Queue)
    assembler.message_fetched = AsyncMock()
    assembler.message_fetched.is_set = Mock(return_value=False)
    
    # Call put with a frame
    await assembler.put(Frame(Opcode.TEXT, b"foo"))
    
    # Check if put was called with the expected arguments
    print("Calls:", assembler.chunks_queue.put.mock_calls)
    
    # This will fail in Python 3.12
    try:
        assembler.chunks_queue.put.has_calls(
            call(b"foo"),
            call(None),
        )
        print("has_calls succeeded")
    except AttributeError as e:
        print(f"has_calls failed: {e}")
    
    # This should work in Python 3.12
    try:
        # Print the actual data type
        print(f"Type of first call arg: {type(assembler.chunks_queue.put.call_args_list[0][0][0])}")
        print(f"Value of first call arg: {assembler.chunks_queue.put.call_args_list[0][0][0]}")
        
        assembler.chunks_queue.put.assert_has_calls([
            call(b"foo"),  # Should now match the actual calls
            call(None),
        ])
        print("assert_has_calls succeeded")
    except AssertionError as e:
        print(f"assert_has_calls failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_ws_frame_put())