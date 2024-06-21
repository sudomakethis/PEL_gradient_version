import pickle

seg1 = [(0,0),(0,5)]
seg2 = [(1,1),(2,2)]
segments = [seg1,seg2]

print(type(segments[0]))
print(segments)

# file = open("segments.txt", "w")

# for segment in segments:
#     file.write("%s" %segment+"\n")

pickle.dump(segments, open('segments.dump', 'wb'))

