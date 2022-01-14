from spn.structure.Base import Sum, get_nodes_by_type
from spn.algorithms.Inference import likelihood
from evaluation import Evaluation
from network.exercise.exercise_class import Exercise
from globals import IDs


def add_exercise_insert_edge_usage(manager):
    manager.exercises.append(Exercise(IDs.INSERT_EDGE_USAGE))


def insert_edge_usage(member, message_value=None):
    eval = Evaluation(member.spn)
    # used_edges = eval.evaluate_edges(member.private_data)
    member.used_edges = {}
    for sumNode in get_nodes_by_type(member.spn, ntype=Sum):
        for child in sumNode.children:
            member.used_edges[(sumNode.id, child.id)] = 0

    likelihood(member.spn, member.private_data, member=member, insert_edge_usage=True)

    for data_id, value in member.used_edges.items():
        # print(f"id {member.id} for {data_id} we got value {value}")
        member.insert_in_share(data_id, value)

    member.network_socket.send(member.manager_id_chip, IDs.INSERT_EDGE_USAGE, member.id)
