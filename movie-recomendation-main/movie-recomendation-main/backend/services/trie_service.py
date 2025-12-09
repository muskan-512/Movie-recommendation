from app import db
from models.movie import Movie
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.titles=[]
class Trie:
    def __init__(self):
        self.root=TrieNode()
    def insert(self,title):
        node=self.root
        for char in title.lower():
            if char not in node.children:
                node.children[char]=TrieNode()
            node=node.children[char]
            if len(node.titles) < 10 and title not in node.titles:
                node.titles.append(title)

        node.is_end=True
    def autocomplete(self,prefix):
        node=self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node=node.children[char]
        return node.titles

def build_trie():
    trie=Trie()
    movie=Movie.query.with_entities(Movie.title).all()
    for i in movie:
        title=i[0]
        trie.insert(title)
    return trie
 