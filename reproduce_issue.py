#!/usr/bin/env python3

"""
Reproduction script for the websocket test issue.
This script demonstrates the problem with has_calls vs assert_has_calls.
"""

import asyncio
from asyncio import Queue
from unittest.mock import Mock, call

try:
    from unittest.mock import AsyncMock
except ImportError:
    from tests.asyncmock import AsyncMock

from websockets.frames import DATA_OPCODES, Frame
from sanic.server.websockets.frame import WebsocketFrameAssembler


async def test_broken_version():
    """This reproduces the failing test."""
    print("Testing broken version with has_calls...")
    
    assembler = WebsocketFrameAssembler(Mock())
    assembler.chunks_queue = AsyncMock(spec=Queue)
    assembler.message_fetched = AsyncMock()
    assembler.message_fetched.is_set = Mock(return_value=False)

    await assembler.put(Frame(DATA_OPCODES[0], b"foo"))

    try:
        # This should fail with AttributeError
        assembler.chunks_queue.put.has_calls(
            call(b"foo"),
            call(None),
        )
        print("ERROR: has_calls should have failed!")
    except AttributeError as e:
        print(f"Expected error: {e}")


async def test_fixed_version():
    """This shows the correct way to do the assertion."""
    print("\nTesting fixed version with assert_has_calls...")
    
    for opcode in DATA_OPCODES:
        print(f"  Testing opcode {opcode.name} ({opcode.value})...")
        assembler = WebsocketFrameAssembler(Mock())
        assembler.chunks_queue = AsyncMock(spec=Queue)
        assembler.message_fetched = AsyncMock()
        assembler.message_fetched.is_set = Mock(return_value=False)

        await assembler.put(Frame(opcode, b"foo"))

        try:
            # For TEXT frames, data gets decoded to string; for others, it remains bytes
            expected_data = "foo" if opcode.value == 1 else b"foo"  # TEXT opcode is 1
            assembler.chunks_queue.put.assert_has_calls([
                call(expected_data),
                call(None),
            ])
            print(f"    SUCCESS: {opcode.name} opcode worked correctly!")
        except Exception as e:
            print(f"    ERROR for {opcode.name}: {e}")


async def main():
    await test_broken_version()
    await test_fixed_version()


if __name__ == "__main__":
    asyncio.run(main())