import pickle

retrieved_segments = pickle.load(open('segments.dump', 'rb'))

print(type(retrieved_segments))
print(type(retrieved_segments[0]))
print(type((retrieved_segments[0][0])))
print(type((retrieved_segments[0][0][0])))