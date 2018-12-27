from typing import NamedTuple

from description_generator.node_group_el_status import NodeGroupElStatus


class NodeGroupEl(NamedTuple):
    node_idx: int
    successors_ids: list
    status: NodeGroupElStatus
