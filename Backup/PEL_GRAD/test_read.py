import pickle

retrieved_segments = pickle.load(open('segments.dump', 'rb'))

# print(type(retrieved_segments))
# print(type(retrieved_segments[0]))
# print(type((retrieved_segments[0][0])))
# print(type((retrieved_segments[0][0][0])))

values = [
        {
            "from_edge": (-1,0),
            "not_edges":[(1,0),(1,-1),(1,1)],
            "edges":[(2,0),(2,-1),(2,-2),(1,-2),(2,1),(2,2),(1,2)]
        },{
            "from_edge": (1,0),
            "not_edges":[(-1,0),(-1,-1),(-1,1)],
            "edges":[(-2,0),(-2,-1),(-2,-2),(-1,-2),(-2,1),(-2,2),(-1,2)]
        }
    ]

print(type(values))
print(type(values[1]))
print(type(values[0:2]))