import asyncio

async def talk_to_server(name, host, port, message):
    reader, writer = await asyncio.open_connection(host, port)
    writer.write(message.encode() + b'\n')
    await writer.drain()
    response = await reader.readline()
    writer.close()
    await writer.wait_closed()
    return (name, response.decode().strip())

async def main():
    results = await asyncio.gather(
        talk_to_server("ServerA", '127.0.0.1', 8888, "Hello A"),
        talk_to_server("ServerB", '127.0.0.1', 8889, "Hello B"),
        talk_to_server("ServerC", '127.0.0.1', 8890, "Hello C"),
    )

    # You can now process all results
    for name, response in results:
        print(f"[{name}] Response: {response}")

asyncio.run(main())