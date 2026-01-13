import sys
sys.dont_write_bytecode = True

import asyncio
import httpx
import socketio

BASE_URL = "http://localhost:8000"


async def test_rest():
    print("\n=== Testing REST API ===\n")
    async with httpx.AsyncClient(follow_redirects=True) as client:
        print("POST /api/orders - Create order")
        res = await client.post(f"{BASE_URL}/api/orders", json={"item": "pizza", "quantity": 2})
        print(f"  Status: {res.status_code}")
        order = res.json()
        print(f"  Response: {order}")
        order_id = order["id"]

        print("\nGET /api/orders - List orders")
        res = await client.get(f"{BASE_URL}/api/orders")
        print(f"  Status: {res.status_code}")
        print(f"  Response: {res.json()}")

        print(f"\nGET /api/orders/{order_id} - Get order")
        res = await client.get(f"{BASE_URL}/api/orders/{order_id}")
        print(f"  Status: {res.status_code}")
        print(f"  Response: {res.json()}")

        print(f"\nPUT /api/orders/{order_id} - Update order")
        res = await client.put(f"{BASE_URL}/api/orders/{order_id}", json={"status": "completed"})
        print(f"  Status: {res.status_code}")
        print(f"  Response: {res.json()}")

        print(f"\nDELETE /api/orders/{order_id} - Delete order")
        res = await client.delete(f"{BASE_URL}/api/orders/{order_id}")
        print(f"  Status: {res.status_code}")
        print(f"  Response: {res.json()}")


async def test_socketio():
    print("\n=== Testing Socket.IO ===\n")
    sio = socketio.AsyncClient()
    results = {}

    @sio.on("order.created")
    async def on_order_created(data):
        results["created"] = data

    @sio.on("order.list")
    async def on_order_list(data):
        results["list"] = data

    @sio.on("order.data")
    async def on_order_data(data):
        results["data"] = data

    @sio.on("order.updated")
    async def on_order_updated(data):
        results["updated"] = data

    @sio.on("order.deleted")
    async def on_order_deleted(data):
        results["deleted"] = data

    @sio.on("order.error")
    async def on_order_error(data):
        results["error"] = data

    await sio.connect(BASE_URL, socketio_path='/ws')

    print("order.create - Create order")
    await sio.emit("order.create", {"item": "burger", "quantity": 3})
    await asyncio.sleep(0.1)
    print(f"  Response: {results.get('created')}")
    order_id = results["created"]["id"]

    print("\norder.list - List orders")
    await sio.emit("order.list", {})
    await asyncio.sleep(0.1)
    print(f"  Response: {results.get('list')}")

    print("\norder.get - Get order")
    await sio.emit("order.get", {"id": order_id})
    await asyncio.sleep(0.1)
    print(f"  Response: {results.get('data')}")

    print("\norder.update - Update order")
    await sio.emit("order.update", {"id": order_id, "status": "completed"})
    await asyncio.sleep(0.1)
    print(f"  Response: {results.get('updated')}")

    print("\norder.delete - Delete order")
    await sio.emit("order.delete", {"id": order_id})
    await asyncio.sleep(0.1)
    print(f"  Response: {results.get('deleted')}")

    await sio.disconnect()


async def main():
    print("Make sure server is running: python run.py")
    try:
        await test_rest()
        await test_socketio()
        print("\n=== All tests passed ===")
    except Exception as e:
        print(f"\nError: {e}")
        print("Is the server running?")


if __name__ == "__main__":
    asyncio.run(main())
