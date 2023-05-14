from antlr4 import InputStream, CommonTokenStream
from antlr4 import ParseTreeWalker, ParserRuleContext
from antlr4.error.Errors import ParseCancellationException
from antlr4.tree.Tree import TerminalNodeImpl
from pydot import Dot, Edge, Node

from project.language.GraphLangLexer import GraphLangLexer
from project.language.GraphLangListener import GraphLangListener
from project.language.GraphLangParser import GraphLangParser


class DotVisitor(GraphLangListener):
    def __init__(self, dot: Dot, rules):
        self.dot = dot
        self.nodes_count = 0
        self.nodes = {}
        self.rules = rules
        super(DotVisitor, self).__init__()

    def enterEveryRule(self, context: ParserRuleContext):
        if context not in self.nodes:
            self.nodes_count += 1
            self.nodes[context] = self.nodes_count
        if context.parentCtx:
            self.dot.add_edge(Edge(self.nodes[context.parentCtx], self.nodes[context]))
        text = self.rules[context.getRuleIndex()]
        self.dot.add_node(Node(self.nodes[context], label=text))

    def visitTerminal(self, node: TerminalNodeImpl):
        self.nodes_count += 1
        self.dot.add_edge(Edge(self.nodes[node.parentCtx], self.nodes_count))
        self.dot.add_node(Node(self.nodes_count, label=f"TERM: {node.getText()}"))


def parse_lang(text: str) -> GraphLangParser:
    input_stream = InputStream(text)
    lexer = GraphLangLexer(input_stream)
    lexer.removeErrorListeners()
    stream = CommonTokenStream(lexer)
    parser = GraphLangParser(stream)

    return parser


def is_text_correct_in_language(text: str) -> bool:
    parser = parse_lang(text)
    parser.removeErrorListeners()
    _ = parser.program()
    return parser.getNumberOfSyntaxErrors() == 0


def generate_dot_lang(text: str) -> Dot:
    if not is_text_correct_in_language(text):
        raise ParseCancellationException("Invalid text for current language")
    parser = parse_lang(text)
    program = parser.program()
    dot = Dot("tree", graph_type="digraph")
    walker = ParseTreeWalker()
    walker.walk(DotVisitor(dot, GraphLangParser.ruleNames), program)
    return dot


def generate_dot_to_file(text: str, path: str):
    dot = generate_dot_lang(text)
    dot.write(str(path))


def generate_dot_to_str(text: str) -> str:
    dot = generate_dot_lang(text)
    return dot.to_string()
