import ast
import matplotlib.pyplot as plt
import networkx as nx


class Visualizer(ast.NodeVisitor):
    def __init__(self):
        super().__init__()

        self.graph = nx.Graph()
        self.labels = dict()
        self.classes = dict()
        self.stack = []

    def find_label(self, node):
        label = node.__class__.__name__

        if isinstance(node, ast.Name):
            label = label = f"{node.__class__.__name__}:\n{node.id}"

        elif isinstance(node, ast.FunctionDef):
            label = f"{node.__class__.__name__}:\n{node.name}"

        elif isinstance(node, ast.arg):
            label = f"{node.__class__.__name__}:\n{node.arg}"

        elif isinstance(node, ast.Constant):
            label = f"{node.__class__.__name__}:\n{node.value}"

        return label

    def generic_visit(self, node):
        parent_name = self.stack[-1] if len(self.stack) > 0 else None
        class_name = str(node)

        class_cnt = self.classes.get(class_name, 0) + 1
        self.classes[class_name] = class_cnt

        node_name = f"{class_name}_{class_cnt}"
        self.labels[node_name] = self.find_label(node)

        self.stack.append(node_name)
        self.graph.add_node(node_name)

        if parent_name is not None:
            self.graph.add_edge(parent_name, node_name)

        ast.NodeVisitor.generic_visit(self, node)

        self.stack.pop()


if __name__ == "__main__":
    func_path = "fib.py"
    out_path = "artifacts/tree.png"

    with open(func_path, "r") as f:
        func = f.read()

    tree = ast.parse(func)
    visualizer = Visualizer()
    visualizer.visit(tree)

    # plot graph and save
    plt.figure(1, figsize=(10, 10))
    nx.draw(visualizer.graph, labels=visualizer.labels, with_labels=True)
    plt.savefig(out_path)
