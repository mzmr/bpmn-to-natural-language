from description_generator.sentence.sentence_generator import SentenceGenerator


class BPMNDescription:

    def __init__(self, node_flow: list):
        self.node_flow = node_flow
        self.sentences = list()
        self.inflector = SentenceGenerator()

    def generate(self):
        for node in self.node_flow:
            successors = [self.node_flow[i] for i in node[1]]

            if node[0] is None:  # first tuple in a list should look like (None, [start_node1, start_node2...])
                start_nodes = [s[0] for s in successors]
                start_sentence = self.inflector.generate_start_sentence(start_nodes)
                self.sentences.append(start_sentence)

        return self.sentences
