from functools import partial
import sys

from globals import *
import threading

import websockets
import asyncio
import time
from datetime import datetime

import json

import logging

logger = logging.getLogger(__name__)

from init_logger import init_logger
init_logger(18)

import nest_asyncio

nest_asyncio.apply()






class IDChip:
    def __init__(self, id, ip4, port, name) -> None:
        assert id is not None
        assert ip4 is not None
        assert port is not None

        self.__id = id
        self.__ip4 = ip4
        self.__port = port

        if name is not None:
            self.__name = name
        else:
            self.__name = f"{id}_{ip4}_{port}"

    @property
    def id(self):
        return self.__id

    @property
    def ip4(self):
        return self.__ip4

    @property
    def port(self):
        return self.__port

    @property
    def name(self):
        return self.__name





id_chip_1 = IDChip("1", "10.0.1.111", "4421", "ID1")
id_chip_2 = IDChip("2", "10.0.1.112", "4422", "ID2")


class NetworkSocket:
    def __init__(self, id_chip) -> None:
        self.id_chip = id_chip
        self.isReady = False
        self.stop = False
        self.__latency = int(10)

        self.server_thread = threading.Thread(target=self.__thread_start_server)
        self.server_thread.start()

    @property
    def id(self):
        return self.id_chip.id

    @property
    def ip4(self):
        return self.id_chip.ip4

    @property
    def port(self):
        return self.id_chip.port

    @property
    def name(self):
        return f"{self.id_chip.name}s_NetworkSocket"

    @property
    def latency(self):
        return self.__latency

    def __thread_start_server(self):
        logger.info_spn(f"Server-thread for {self.id} started")
        asyncio.run(self.__start_server(self.ip4, self.port))

    def __start_server(self, ip4, port):
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        start_server = websockets.serve(self.__receive, ip4, port, loop=event_loop)
        logger.info_spn(
            f"Websockets server for {self.id} listening to {self.ip4}:{self.port}"
        )
        event_loop.run_until_complete(start_server)
        self.isReady = True
        event_loop.run_forever()

    async def __receive(self, websocket, path):
        async for message in websocket:
            # message_json_str = await websocket.recv()
            # message = json.loads(message_json_str)
            message = json.loads(message)
            # if not (self.id is Values.MANAGER_ID):
            # time.sleep(self.latency / 1000)
            source = message.get(Keys.MESSAGE_SOURCE)

            #if source is not None:
            #    source_ip4 = source.get(Keys.MESSAGE_SOURCE_IP4)
            #    source_port = source.get(Keys.MESSAGE_SOURCE_PORT)

            data = message.get(Keys.MESSAGE_DATA)
            if data is not None:
                data_id = data.get(Keys.MESSAGE_DATA_ID)
                data_value = data.get(Keys.MESSAGE_DATA_VALUE)

            #logger.info_spn(
            #    f"{datetime.now()}: receiving at {self.id_chip.ip4}:{self.id_chip.port} from {source_ip4}:{source_port} message {data_id}:{data_value}"
            #)
            self.pong(data_id, data_value)

        # message_json_str = await websocket.recv()
        # message = json.loads(message_json_str)
        # if not (self.id is Values.MANAGER_ID):
        #    time.sleep(self.latency / 1000)
        # self.member.evaluate_message(message)
        # await websocket.send(message_json_str)  ###

    def send(self, target_id_chip, data_id, value):
        while not self.isReady:
            time.sleep(0.001)
        # asyncio.new_event_loop().run_until_complete(
        #    self.__send(target_id_chip, data_id, value)
        # )
        # if self.id is Values.MANAGER_ID:
        #    asyncio.get_event_loop().call_soon(partial(print, "Manager send", flush=True))

        asyncio.get_event_loop().run_until_complete(
            self.__send(target_id_chip, data_id, value)
        )

    async def __send(self, target_id_chip, data_id, data_value):

        target_ip4 = target_id_chip.ip4
        target_port = target_id_chip.port
        uri = f"ws://{target_ip4}:{target_port}"
        async with websockets.connect(uri) as websocket:
            ##start_time = time.time()
            #source = {}
            #source["ip4"] = self.ip4
            #source["port"] = self.port

            data = {}
            data["id"] = data_id
            data["value"] = data_value

            message = {}
            #message["source"] = source
            message["data"] = data

            message_json_str = json.dumps(message)
            #logger.info_spn(
            #    f"{datetime.now()}: sending from {self.ip4}:{self.port} to {target_ip4}:{target_port} message {data_id}:{data_value}"
            #)

            #if target_id_chip.id is Values.MANAGER_ID:
            #    time.sleep(self.latency / 1000)
            #if not ((target_id_chip.id is Values.MANAGER_ID) or (self.id is Values.MANAGER_ID)):
            #    time.sleep(self.latency / 1000)

            await websocket.send(message_json_str)
            # await websocket.recv()  ####
            ##end_time = time.time()
            ##self.member.table_time += end_time - start_time
    
    def pong(self, data_id, data_value):
        data_value = int(data_value)+1
        if(self.id == "1"):
            logger.info_spn(f"ping {data_value}")
        if(data_value == 1000001):
            self.end_time = time.time()
            logger.info_spn(f"Start_time = {self.start_time}")
            logger.info_spn(f"End_time = {self.end_time}")
            time_needed = self.end_time - self.start_time
            logger.info_spn(f"Time per pong = {time_needed/1000001}")
            return
        data_value = str(data_value)
        if self.id == "1":
            self.send(id_chip_2, data_id, data_value)
        elif self.id == "2":
            self.send(id_chip_1, data_id, data_value)
        
        

    def init_ping(self, target_id_chip):
        self.start_time = time.time()
        self.send(target_id_chip, "ping", "1")



import sys
import os


from init_logger import init_logger

logger_level = int(os.getenv("LOGGER_LEVEL"))
id = os.getenv("ID")

id_chip_1 = IDChip("1", "10.0.1.111", "4421", "ID1")
id_chip_2 = IDChip("2", "10.0.1.112", "4422", "ID2")

if id == "1":
    socket_1 = NetworkSocket(id_chip_1)
    socket_1.init_ping(id_chip_2)

if id == "2": 
    socket_2 = NetworkSocket(id_chip_2)


