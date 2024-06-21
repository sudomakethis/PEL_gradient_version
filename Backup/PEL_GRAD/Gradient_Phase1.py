
# ------------------------- FILLING GAPS -------------------------

class Phase1:
    def __init__(self) -> None:
        #senso orario
        self.values = [
                {
                    "from_edge": (-1,0),
                    "not_edges":[(1,0),(1,-1),(1,1)],
                    "edges":[(2,0),(2,-1),(2,-2),(1,-2),(2,1),(2,2),(1,2)]
                },{
                    "from_edge": (1,0),
                    "not_edges":[(-1,0),(-1,-1),(-1,1)],
                    "edges":[(-2,0),(-2,-1),(-2,-2),(-1,-2),(-2,1),(-2,2),(-1,2)]
                },{
                    "from_edge": (0,-1),
                    "not_edges":[(0,-1),(1,-1),(-1,-1)],
                    "edges":[(0,2),(1,2),(2,2),(2,1),(-1,2),(-2,2),(-2,1)]
                },{
                    "from_edge": (0,1),
                    "not_edges":[(0,-1),(1,-1),(-1,-1)],
                    "edges":[(0,-2),(1,-2),(2,-2),(2,-1),(-1,-2),(-2,-2),(-2,-1)]
                },{
                    "from_edge": (-1,-1),
                    "not_edges":[(1,1),(0,1),(1,0)],
                    "edges":[(2,2),(2,1),(1,2),(0,2),(2,0)]
                },{
                    "from_edge": (1,1),
                    "not_edges":[(-1,-1),(-1,0),(0,-1)],
                    "edges":[(-2,-2),(-2,-1),(-1,-2),(-2,0),(0,-2)]
                },{
                    "from_edge": (1,-1),
                    "not_edges":[(-1,1),(0,1),(-1,0)],
                    "edges":[(-2,2),(-2,1),(-1,2),(0,2),(-2,0)]
                },{
                    "from_edge": (-1,1),
                    "not_edges":[(1,-1),(1,0),(0,-1)],
                    "edges":[(2,-2),(1,-2),(2,-1),(2,0),(0,-2)]
                }
            ]

    def are_not_edges(self, edges, coord_center, coords):
        co=0
        for coord in coords:
            if edges[coord_center[0] + coord[0], coord_center[1] + coord[1]] == 0:
                co+=1
        return co==len(coords)
    
    def fill_val(self, edges, coord_center, di, deltas_to_apply):
        for t_delta in di:
            x = coord_center[0] + t_delta[0]
            y = coord_center[1] + t_delta[1]
            #if this pixel is an edge, 
            if edges[x,y] != 0:
                #set previous pixel  and interrupt the cycle
                t_x = coord_center[0] + deltas_to_apply[0]
                t_y = coord_center[1] + deltas_to_apply[1]
                edges[t_x,t_y] = 255
                return (edges, True)
        return (edges, False)

    def fill_values(self, edges, coord_center, d1,d2,d3, deltas_to_apply):
        (edg, ok) = self.fill_val(edges,coord_center,d1,deltas_to_apply[0])
        if ok:
            return edg
        (edg, ok) = self.fill_val(edges,coord_center,d2,deltas_to_apply[1])
        if ok:
            return edg
        (edg, ok) = self.fill_val(edges,coord_center,d3,deltas_to_apply[2])
        if ok:
            return edg
        return edges

    def fill_neighbors(self, edges, coord_center, deltas, deltas_to_apply):
        if len(deltas)==7:
            #ci troviamo nei casi a, b + opposti
            return self.fill_values(edges,coord_center, [deltas[0]],deltas[1:4],deltas[4:7], deltas_to_apply)
        elif len(deltas) == 5:
            #ci troviamo nei casi c, d + opposti
            return self.fill_values(edges,coord_center, deltas[0:3],[deltas[3]],[deltas[4]], deltas_to_apply)
        #else do nothing
        return edges
         
    #PHASE 1: FILL GAPS
    def PEL_1_FillGaps(self, edges, Theta):
        for i in range(2, edges.shape[0]-2):
            for j in range(2, edges.shape[1]-2):
                curr_theta = Theta[i,j]
                if curr_theta == 0:
                    values_to_check = self.values[0:2]
                elif curr_theta == 45:
                    values_to_check = self.values[4:6]
                elif curr_theta == 90:
                    values_to_check = self.values[2:4]
                elif curr_theta == 135:
                    values_to_check = self.values[6:8]

                for elem in values_to_check:
                    t_indexes = elem["not_edges"]
                    from_edge = elem["from_edge"]
                    if edges[i+from_edge[0],j+from_edge[1]] != 0 and edges[i,j] != 0 and self.are_not_edges(edges,(i,j), t_indexes):
                        edges = self.fill_neighbors(edges, (i,j), elem["edges"], t_indexes)
        return edges
