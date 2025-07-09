import asyncio
import os
import secrets

# --- FINAL, OKTETO-OPTIMIZED SCRIPT ---

# --- Configuration ---
LOCAL_PORT = 8888

# --- The Pure Python MTProto Proxy Server Implementation ---
async def handle_client(reader, writer):
    try:
        client_handshake = await reader.readexactly(64)
        # Connect to an official Telegram Data Center (e.g., DC4)
        tg_reader, tg_writer = await asyncio.open_connection("149.154.167.51", 443)
        server_handshake = await tg_reader.readexactly(64)
        writer.write(server_handshake)
        await writer.drain()
        tg_writer.write(client_handshake)
        await tg_writer.drain()

        async def forward(src_reader, dest_writer):
            while not src_reader.at_eof() and not dest_writer.is_closing():
                try:
                    data = await src_reader.read(4096)
                    if not data:
                        break
                    dest_writer.write(data)
                    await dest_writer.drain()
                except (ConnectionResetError, BrokenPipeError):
                    break
            if not dest_writer.is_closing():
                dest_writer.close()
                await dest_writer.wait_closed()
        
        await asyncio.gather(
            forward(reader, tg_writer),
            forward(tg_reader, writer)
        )
    except Exception:
        pass
    finally:
        if not writer.is_closing():
            writer.close()

async def start_proxy_server(host, port, secret):
    print("="*40)
    print("✅ Your Proxy Server is starting on Okteto...")
    print(f"[*] Listening on internal port: {port}")
    print(f"[*] Your secret is: {secret}")
    print("="*40)
    print("\nGo to your Okteto dashboard to find the public URL (Endpoints).")
    print("Combine the public URL from Okteto with your secret to build the final link.")
    
    server = await asyncio.start_server(handle_client, host, port)
    async with server:
        await server.serve_forever()

# --- Main script logic ---
if __name__ == "__main__":
    proxy_secret = secrets.token_hex(16)
    
    try:
        asyncio.run(start_proxy_server('0.0.0.0', LOCAL_PORT, proxy_secret))
    except KeyboardInterrupt:
        print("\n[*] Proxy server stopped.")
