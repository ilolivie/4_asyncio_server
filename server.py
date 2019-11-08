import asyncio


async def handle_echo(reader, writer):
    data = await reader.read(100)
    msg = data.decode()
    addr = writer.get_extra_info('peername')
    print(f'Получил {msg} от {addr}')
    
    writer.write(data)
    await writer.drain()

    writer.close()


try:
    port= input("Введите номер порта: ")
    if port == '':
        port = 9090
        port = int(port)
    if type(port) == int and 0 <= port <= 65535:
        pass
    else:
        port = 9090
except ValueError:
    port = 9090
    print("Введен некорректный порт. По умолчанию - 9090.")


loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', port, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
