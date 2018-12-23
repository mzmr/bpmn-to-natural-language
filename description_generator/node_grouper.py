from description_generator.node_group_el_status import NodeGroupElStatus
from description_generator.pojo.node_group_el import NodeGroupEl


class NodeGrouper:

    def __init__(self, node_flow: list):
        self.node_flow = node_flow

    def group_nodes(self) -> list:
        return self.__create_node_groups()

    def __create_node_groups(self) -> list:
        node_groups = list()

        for idx, nf in enumerate(self.node_flow):
            self.__insert_node_into_groups(idx, nf, node_groups)

        while self.__consolidate_groups(node_groups):
            pass

        return node_groups

    def __insert_node_into_groups(self, node_idx: int, node: tuple, node_groups: list) -> None:
        successors = node[1]
        status = self.__get_group_element_status(node)
        new_group_el = NodeGroupEl(node_idx, successors, status)

        for ng in node_groups:
            for ng_el_idx, ng_el in enumerate(ng):
                if node_idx not in ng_el.successors_ids:
                    continue

                if ng_el.status == NodeGroupElStatus.normal:
                    ng.append(new_group_el)
                else:
                    node_groups.append([new_group_el])

                return

        node_groups.append([new_group_el])

    @staticmethod
    def __consolidate_groups(node_groups: list) -> bool:
        group_to_extend = None
        next_node_idx = None

        for ng in node_groups:
            last = ng[-1]

            if last.status == NodeGroupElStatus.normal:
                group_to_extend = ng
                next_node_idx = last.successors_ids[0]
                break

        if group_to_extend is None:
            return False

        ng_to_remove = None

        for ng_idx, ng in enumerate(node_groups):
            first = ng[0]

            if first.node_idx == next_node_idx:
                group_to_extend.extend(ng)
                ng_to_remove = ng_idx
                break

        if ng_to_remove is None:
            raise Exception()

        del node_groups[ng_to_remove]
        return True

    def __get_group_element_status(self, node: tuple) -> NodeGroupElStatus:
        successors = node[1]
        succ_number = len(successors)

        if succ_number == 0:
            return NodeGroupElStatus.end

        if succ_number > 1:
            return NodeGroupElStatus.splitting

        pred_number = len(self.node_flow[successors[0]][0].predecessors)

        if pred_number > 1:
            return NodeGroupElStatus.joining
        else:
            return NodeGroupElStatus.normal
