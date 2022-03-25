import random
from datetime import datetime
import sqlite3
import cv2
import websockets
import asyncio
import pyautogui
from os import path


con = sqlite3.connect('coords_image.db')
cursor = con.cursor()


def get_mouse_position() -> tuple:
    """
    Returns the real mouse position
    :return:
    """
    coords = pyautogui.position()
    return coords[0], coords[1]


def capture_image(path: str, camera_port: int = 0):
    """
    Captures an image using webcam and saves it to path
    :param path:
    :param camera_port:
    :return:
    """
    camera = cv2.VideoCapture(camera_port)
    _, camera_capture = camera.read()
    cv2.imwrite(path, camera_capture)

    _, buffer = cv2.imencode(".png", camera_capture)
    return buffer


async def feed_coords(websocket):
    """
    Sends the coords to the web sock
    :param websocket:
    """
    while True:
        coords = get_mouse_position()
        await websocket.send(str(coords))
        await asyncio.sleep(0.01)


def insert_data(coords: str, image: bytes):
    """
    Inserts coordinate and image to the database
    :param coords:
    :param image:
    """
    cursor.execute("INSERT INTO CoordsImages VALUES (?,?)", (coords, image))
    con.commit()
    con.close()


def on_click_handle(incoming_coords: str):
    """
    Handles on click event coming from the browser\
    :param incoming_coords:
    """
    image = capture_image(path.join(__file__, f'images/{datetime.now().isoformat()}.png'))
    insert_data(incoming_coords, image)


async def read_clicks(websocket):
    """
    Reads messages from the web socket
    :param websocket:
    """
    while True:
        data = await websocket.recv()
        on_click_handle(data)
        await asyncio.sleep(0.01)


async def setup_web_socket(websocket):
    """
    Setups both operations (read, write) to work in parallel
    :param websocket:
    """
    loop = asyncio.get_event_loop()
    f1 = loop.create_task(feed_coords(websocket))
    f2 = loop.create_task(read_clicks(websocket))
    await asyncio.wait([f1, f2])

def setup_db():
    """
    Sets up the database in case it does not exists
    """
    cursor.execute("CREATE TABLE IF NOT EXISTS CoordsImages (coords TEXT PRIMARY KEY, image BLOB NOT NULL)")
    con.commit()


def main():
    """
    Starts up the websockets
    """
    setup_db()
    start_server = websockets.serve(setup_web_socket, "localhost", 8000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    main()
