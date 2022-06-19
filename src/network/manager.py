import math
from random import randint
from network.exercise.conversion.pq2sq import add_exercise_pq2sq
from network.exercise.conversion.si2sq import add_exercise_si2sq
from network.exercise.conversion.sq2pq import add_exercise_sq2pq
from network.exercise.conversion.sq2si import add_exercise_sq2si
from network.exercise.math.addition import add_exercise_addition
from network.exercise.math.approx_inverse import add_exercise_approx_inverse
from network.exercise.math.division import (
    add_exercise_division,
    add_exercise_division_with_d_multiplyer,
)
from network.exercise.math.multiplication_with_clear_value import (
    add_exercise_multiplication_with_clear_value,
)
from network.exercise.math.multiplication import add_exercise_multiplication
from network.exercise.math.trunc import add_exercise_trunc
from spn.io.Graphics import plot_spn
from network.exercise.reveal import reveal_weights

from numpy.core.arrayprint import _none_or_positive_arg
from globals import DataIDs, IDs, Keys, Values


from network.member import Member
from network.exercise.exercise_class import Exercise

import logging
import numpy as np

import nest_asyncio
from datetime import datetime

from spn.structure.Base import get_nodes_by_type
from spn.structure.Base import get_topological_order
from spn.structure.Base import Sum, Product, Leaf

nest_asyncio.apply()

logger = logging.getLogger(__name__)

from network.exercise import *
import time


class Manager(Member):
    def __init__(self, configuration_filepath):
        super().__init__(configuration_filepath, Values.MANAGER_ID)
        self.exercise_measuring = {}
        self.last_start = time.time()
        self.table_time = 0

        self.amount_members = len(self.id_chips_for_id.keys())
        self.logger = logging.getLogger(__name__)
        Exercise.amount_members = self.amount_members
        Exercise.on_completion = self.default_on_completion
        Exercise.on_start = self.default_on_start
        self.member_online_ids = []
        self.insert_edge_usage_done_ids = []
        self.current_exercise_index = 0
        self.exercises = []

        add_exercise_member_online(self)

        ## Loading from files the structure of the spn and private data to train with
        add_exercise_load_private_data_from_file(self)
        add_exercise_load_spn_from_file(self)

        from network.exercise.io.load_spn_from_file import load_spn_from_file

        load_spn_from_file(self)

        add_exercise_load_private_data_for_private_evaluation_from_file(self)

        add_exercise_jrsz(self, DataIDs.JRSZ_FOR_NUMERATOR)
        add_exercise_jrsz(self, DataIDs.JRSZ_FOR_DENOMINATOR)

        self.data[DataIDs.DIVISION_MULTIPLYER] = self.d_multiplyer
        add_exercise_manager_inser_in_share(self, DataIDs.DIVISION_MULTIPLYER)

        self.data[DataIDs.APPINVERSE_OF_TWO_POW_N_PLUS_1] = pow(
            2, self.truncate_n + 1
        )  # "approx_inverse_2^(n+1)"
        add_exercise_manager_inser_in_share(
            self, DataIDs.APPINVERSE_OF_TWO_POW_N_PLUS_1
        )

        self.data[DataIDs.APPINVERSE_OF_TWO_POW_T_MINUS_1] = pow(2, self.truncate_t - 1)
        add_exercise_manager_inser_in_share(
            self, DataIDs.APPINVERSE_OF_TWO_POW_T_MINUS_1
        )

        add_exercise_approx_inverse(
            self, DataIDs.DIVISION_MULTIPLYER, DataIDs.DIVISION_MULTIPLYER_APPINVERSE
        )

        

        ## Load weight of the SPN from file if stated in config
        if self.config[Keys.CONFIG_GENERAL_SECTION].get(
            Keys.CONFIG_GENERAL_LOAD_SPN_WEIGHTS
        ) in ["True", "true"]:
            print(
                f"Will load spn weights cause of {self.config[Keys.CONFIG_GENERAL_SECTION].get(Keys.CONFIG_GENERAL_LOAD_SPN_WEIGHTS)} evaluates to true"
            )
            add_exercise_load_spn_weights_from_file(self)
            # for sum_node in get_nodes_by_type(self.spn, Sum):
            #    for child_node in sum_node.children:
            #        data_id = f"({sum_node.id}, {child_node.id})"
            #        add_exercise_multiplication_with_clear_value(self, data_id, 10)
        else:
            add_exercise_insert_edge_usage(self)
            add_exercise_compute_weight_of_sum_nodes(self)
            add_exercise_compute_weights(self)

        ## Private Evaluations for clients stated in config
        for member_id_chip in self.id_chips_for_id.values():
            if self.config[f"ID_{member_id_chip.id}"].get(
                Keys.CONFIG_PRIVATE_EVALUATION
            ) in ["True", "true"]:
                amount_of_evaluations = int(
                    self.config[f"ID_{member_id_chip.id}"].get(
                        Keys.CONFIG_PRIVATE_EVALUATION_AMOUNT_LINES_TO_EVALUATE
                    )
                )
                for index in range(amount_of_evaluations):
                    add_exercise_evaluation_for_member(self, member_id_chip.id, index)

        ## Save SPN weights if requested in config
        if self.config[Keys.CONFIG_GENERAL_SECTION].get(
            Keys.CONFIG_GENERAL_SAVE_SPN_WEIGHTS
        ) in ["True", "true"]:
            add_exercise_save_spn_weights_to_file(self)

        ##add_exercise_reveal_weights(self)
        add_exercise_dummy(self, "fine")

    @property
    def current_exercise(self):
        return self.exercises[self.current_exercise_index]

    @property
    def amount_exercises(self):
        return len(self.exercises)

    def default_on_completion(self, exercise):
        percentage = (self.current_exercise_index + 1) / self.amount_exercises * 100
        logger.info_spn(
            f'{datetime.now()}: Exercise "{exercise.id}" is finished from all {len(exercise.completed_member_ids)} members ({self.current_exercise_index+1}/{self.amount_exercises}, {percentage:.2f}%)'
        )

    def default_on_start(self, exercise):
        logger.info_spn(
            f'{datetime.now()}: Exercise "{exercise.id}" is send to all members'
        )
        self.send_to_all(exercise.id, exercise.value)

    def on_ready(self):
        logger.info_spn("Manager ready")

    def send_to_all(self, data_id, data_value):
        # start_time = time.time()
        for id_chip in self.id_chips_for_id.values():
            self.network_socket.send(id_chip, data_id, data_value)
        # end_time = time.time()
        # self.table_time += end_time - start_time

    def evaluate_message(self, message):
        #logger.info_spn(f"message: {message} und d: {d}")
        source = message.get(Keys.MESSAGE_SOURCE)

        if source is not None:
            source_ip4 = source.get(Keys.MESSAGE_SOURCE_IP4)
            source_port = source.get(Keys.MESSAGE_SOURCE_PORT)

        data = message.get(Keys.MESSAGE_DATA)
        if data is not None:
            data_id = data.get(Keys.MESSAGE_DATA_ID)
            data_value = data.get(Keys.MESSAGE_DATA_VALUE)

        logger.debug_spn_communication(
            f"{datetime.now()}: receiving at {self.id_chip.ip4}:{self.id_chip.port} from {source_ip4}:{source_port} message {data_id}:{data_value}"
        )

        if data_id == self.current_exercise.id:
            self.current_exercise.add_id_of_completed_member(data_value)
            if (
                self.current_exercise.is_finished
                and self.current_exercise_index + 1 < self.amount_exercises
            ):
                #### performance measuring ####

                end_time = time.time()
                needed_time = end_time - self.last_start
                measure_stored = self.exercise_measuring.get(self.current_exercise.id)
                if measure_stored is None:
                    amount = 0
                    time_stored = 0
                else:
                    amount, time_stored = measure_stored
                    # amount =  measure_stored[0]
                    # time_stored = measure_stored[1]
                self.exercise_measuring[self.current_exercise.id] = (
                    amount + 1,
                    time_stored + needed_time,
                )
                self.last_start = time.time()
                #### ####

                self.current_exercise_index += 1
                self.current_exercise.start()

        else:
            self.data[data_id] = data_value
