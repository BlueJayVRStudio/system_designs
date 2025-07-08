import argparse
import asyncio

parser = argparse.ArgumentParser()
parser.add_argument('-p', type=int, default=8888)
parser.add_argument('-n', type=str, default="A")
args = parser.parse_args()
print(args.p, args.n)

async def handle_client(reader, writer):
    data = await reader.readline()
    addr = writer.get_extra_info('peername')
    print(f"[ServerA] Received {data.decode().strip()} from {addr}")

    await asyncio.sleep(5)
    writer.write(f"Response from Server {args.n}\n".encode())
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', args.p)
    print(f"[ServerA] Listening on 127.0.0.1:{args.p}")
    async with server:
        await server.serve_forever()

asyncio.run(main())