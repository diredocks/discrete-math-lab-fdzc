import relationship

def test():
    rel = relationship.Relationship()
    rel.follow("A", ["B"])
    rel.follow("B", ["E", "I"])
    rel.follow("C", ["D", "H"])
    rel.follow("D", ["C"])
    rel.follow("E", [])
    rel.follow("F", [])
    rel.follow("G", ["E"])
    rel.follow("H", [])
    rel.follow("I", [])
    rel.follow("J", ["A"])
    print(rel.recommend("A"))
    print(rel.recommend("B"))
    print(rel.recommend("C"))


if __name__ == "__main__":
    test()
