from network.exercise.io.save_spn_weights_to_file import (
    add_exercise_save_spn_weights_to_file,
)
from spn.algorithms.layerwise.layers import Sum
from network.exercise.exercise_class import Exercise
from globals import IDs, Keys

from spn.structure.Base import get_nodes_by_type, get_topological_order_layers

from functools import partial


def add_exercise_load_spn_from_file(manager):
    manager.exercises.append(
        Exercise(
            IDs.LOAD_SPN_FROM_FILE,
            on_completion=partial(on_completion_load_spn_from_file, manager),
        )
    )


def on_completion_load_spn_from_file(manager, exercise):
    manager.default_on_completion(exercise)
    # from spn.io.Graphics import plot_spn
    # plot_spn(manager.spn, "plots/paper_spn_2.png")
    # add_exercise_save_spn_weights_to_file(manager)
    from spn.algorithms.Statistics import get_structure_stats

    print(get_structure_stats(manager.spn))


def load_spn_from_file(member, message_value=None):
    spn_file_path = member.config[f"ID_{member.id}"].get(Keys.CONFIG_SPN_FILE_PATH)
    assert (
        spn_file_path is not None
    ), f'No "{Keys.CONFIG_SPN_FILE_PATH}" given in the config file'
    f = open(spn_file_path, "r")
    spn_str = f.read()
    member.spn = member.str_to_spn(spn_str)

    member.layers = get_topological_order_layers(member.spn)

    member.network_socket.send(
        member.manager_id_chip, IDs.LOAD_SPN_FROM_FILE, member.id
    )
