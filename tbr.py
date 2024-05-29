################################################
# Author: Paventhan Vivekanandan               #
# Course: B659 Final Project                   #
# Title: Deep Generalization based on Types    #
################################################

from neo4j import GraphDatabase
from random import randint


NEO4J_URI = "bolt://localhost:11003"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWD = "neo4j"


## Class to maintain the connect with neo4j graph database
class DB:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    ## creates new node
    def add_node(self, typ, pty, ifpty, styp=None, stypinf=1):
        with self.driver.session() as session:
            res = session.run("CREATE (a:Node {Type : $typ, property : $pty, inferred_property : $ifpty, SuperType: $styp, SuperType_inferred : $stypinf})", 
                     typ=typ, pty=pty, ifpty=ifpty, styp=styp, stypinf=stypinf)

    ## update node properties
    def update_node(self, typ, pty, ifpty):
        with self.driver.session() as session:
            res = session.run("MATCH (a:Node {Type : $typ}) SET a.property=$pty, a.inferred_property=$ifpty ", 
                     typ=typ, pty=pty, ifpty=ifpty)


    ## creates inferred node based on properties            
    def add_node_inferred(self, typ, pty, ifpty, styp=None, stypinf=1):
        with self.driver.session() as session:
            res = session.run("CREATE (a:Node:Inferred {Type : $typ, property : $pty, inferred_property : $ifpty, SuperType: $styp, SuperType_inferred : $stypinf})", 
                     typ=typ, pty=pty, ifpty=ifpty, styp=styp, stypinf=stypinf)

    ## update inferred node properties
    def update_node_inferred(self, typ, pty, ifpty):
        with self.driver.session() as session:
            res = session.run("MATCH (a:Node:Inferred {Type : $typ}) SET a.property=$pty, a.inferred_property=$ifpty ", 
                     typ=typ, pty=pty, ifpty=ifpty)

    def change_node_type(self, typ):
        with self.driver.session() as session:
            res = session.run("MATCH (n {Type : $typ}) REMOVE n:Inferred RETURN n.Type", typ=typ)

    ## creates new edge
    def add_edge(self, typ_A, typ_B, pty, prpty, ifpty):
        with self.driver.session() as session:
            res = session.run("MATCH (a:Node), (b:Node) WHERE a.Type=$typ_A AND b.Type=$typ_B CREATE (a)-[:Edge {property: $pty, primitive_property : $prpty, inferred_property : $ifpty}]->(b)", 
                      typ_A=typ_A, typ_B=typ_B, pty=pty, prpty=prpty, ifpty=ifpty)

    ## creates new edge in type hierarchy
    def add_edge_tyh(self, typ_A, typ_B, pty, prpty, ifpty):
        with self.driver.session() as session:
            res = session.run("MATCH (a:Node), (b:Node) WHERE a.Type=$typ_A AND b.Type=$typ_B CREATE (a)-[:Edge_TyH {property: $pty, primitive_property : $prpty, inferred_property : $ifpty}]->(b)", 
                      typ_A=typ_A, typ_B=typ_B, pty=pty, prpty=prpty, ifpty=ifpty)


    ## creates inferred edges           
    def add_edge_inferred(self, typ_A, typ_B, pty, prpty, ifpty):
        with self.driver.session() as session:
            res = session.run("MATCH (a:Node), (b:Node) WHERE a.Type=$typ_A AND b.Type=$typ_B CREATE (a)-[:Edge_Inf {property: $pty, primitive_property : $prpty, inferred_property : $ifpty}]->(b)", 
                      typ_A=typ_A, typ_B=typ_B, pty=pty, prpty=prpty, ifpty=ifpty)

    ## creates inferred edges in type hierarchy           
    def add_edge_inferred_tyh(self, typ_A, typ_B, pty, prpty, ifpty):
        with self.driver.session() as session:
            res = session.run(("MATCH (a:Node), (b:Node) WHERE a.Type=$typ_A AND b.Type=$typ_B " 
                              "CREATE (a)-[:Edge_Inf_TyH {property: $pty, primitive_property : $prpty, inferred_property : $ifpty}]->(b)"), 
                      typ_A=typ_A, typ_B=typ_B, pty=pty, prpty=prpty, ifpty=ifpty)

    ## updates edge properties
    def update_edge(self, typ_A, typ_B, pty, prpty, ifpty):
        with self.driver.session() as session:
            res = session.run("MATCH (a:Node)-[e:Edge]->(b:Node) WHERE a.Type=$typ_A AND b.Type=$typ_B SET e.property=$pty, e.primitive_property=$prpty, e.inferred_property=$ifpty", 
                      typ_A=typ_A, typ_B=typ_B, pty=pty, prpty=prpty, ifpty=ifpty)

    ## updates edge properties in type hierarchy
    def update_edge_tyh(self, typ_A, typ_B, pty, prpty, ifpty):
        with self.driver.session() as session:
            res = session.run("MATCH (a:Node)-[e:Edge_TyH]->(b:Node) WHERE a.Type=$typ_A AND b.Type=$typ_B SET e.property=$pty, e.primitive_property=$prpty, e.inferred_property=$ifpty", 
                      typ_A=typ_A, typ_B=typ_B, pty=pty, prpty=prpty, ifpty=ifpty)


    ## updates edge type
    def update_edge_type(self, typ_A, typ_B, pty, prpty, ifpty):
        with self.driver.session() as session:
            res = session.run("MATCH (a:Node)-[e:Edge_Inf]->(b:Node) WHERE a.Type=$typ_A AND b.Type=$typ_B DELETE e", 
                      typ_A=typ_A, typ_B=typ_B, pty=pty, prpty=prpty, ifpty=ifpty)
            res = session.run("MATCH (a:Node), (b:Node) WHERE a.Type=$typ_A AND b.Type=$typ_B CREATE (a)-[:Edge {property: $pty, primitive_property : $prpty, inferred_property : $ifpty}]->(b)", 
                      typ_A=typ_A, typ_B=typ_B, pty=pty, prpty=prpty, ifpty=ifpty)

    ## updates edge type in type hierarchy
    def update_edge_type_tyh(self, typ_A, typ_B, pty, prpty, ifpty):
        with self.driver.session() as session:
            res = session.run("MATCH (a:Node)-[e:Edge_Inf_TyH]->(b:Node) WHERE a.Type=$typ_A AND b.Type=$typ_B DELETE e", 
                      typ_A=typ_A, typ_B=typ_B, pty=pty, prpty=prpty, ifpty=ifpty)
            res = session.run("MATCH (a:Node), (b:Node) WHERE a.Type=$typ_A AND b.Type=$typ_B CREATE (a)-[:Edge_TyH {property: $pty, primitive_property : $prpty, inferred_property : $ifpty}]->(b)", 
                      typ_A=typ_A, typ_B=typ_B, pty=pty, prpty=prpty, ifpty=ifpty)


    # set super type of given type
    def set_super_type(self, typ, styp):
        with self.driver.session() as session:
            session.run("MATCH (a:Node) where a.Type=$typ set a.SuperType=$styp return a.typ", typ=typ, styp=styp)

    # get node details of given type
    def get_node(self, typ):
        with self.driver.session() as session:
            ret = session.run("MATCH (a:Node) where a.Type=$typ return a.SuperType, a.property, a.inferred_property", typ=typ)
            nodes = {}
            for record in ret:
                nodes[typ] = {"SuperType" : record["a.SuperType"], "property" : record["a.property"], "inferred_property" : record["a.inferred_property"]}
            return nodes

    # get node details of all types
    def get_nodes(self):
        with self.driver.session() as session:
            ret = session.run("MATCH (a:Node) return a.Type, a.SuperType, a.SuperType_inferred, a.property, a.inferred_property") 
            nodes = {}
            for record in ret:
                nodes[record["a.Type"]] = {"SuperType" : record["a.SuperType"], "SuperType_inferred" : record["a.SuperType_inferred"], "property" : record["a.property"], 
                                           "inferred_property" : record["a.inferred_property"]}
            return nodes

    ## retrieve edges based on source type and disregard direction of edges during retrieval
    def get_edges(self, srcType):
        with self.driver.session() as session:
            ret = session.run("MATCH (n1:Node)-[r:Edge]->(n2:Node) where n1.Type=$srcType return n2.Type, r.property, r.primitive_property, r.inferred_property", srcType=srcType)
            edge_lst = {}
            for record in ret:
                edge_lst[record["n2.Type"]] = {"inherited" : 0, "edge_inferred" : 0, "is_source" : 0, "property" : record["r.property"], "primitive_property" : record["r.primitive_property"], 
                                               "inferred_property" : record["r.inferred_property"]}

            ret = session.run("MATCH (n1:Node)-[r:Edge]->(n2:Node) where n2.Type=$srcType return n1.Type, r.property, r.primitive_property, r.inferred_property", srcType=srcType)
            for record in ret:
                edge_lst[record["n1.Type"]] = {"inherited" : 0, "edge_inferred" : 0, "is_source" : 1, "property" : record["r.property"], "primitive_property" : record["r.primitive_property"], 
                                               "inferred_property" : record["r.inferred_property"]}

            ret = session.run("MATCH (n1:Node)-[r:Edge_Inf]->(n2:Node) where n1.Type=$srcType return n2.Type, r.property, r.primitive_property, r.inferred_property", srcType=srcType)
            for record in ret:
                edge_lst[record["n2.Type"]] = {"inherited" : 0, "edge_inferred" : 1, "is_source" : 0, "property" : record["r.property"], "primitive_property" : record["r.primitive_property"], 
                                               "inferred_property" : record["r.inferred_property"]}

            ret = session.run("MATCH (n1:Node)-[r:Edge_Inf]->(n2:Node) where n2.Type=$srcType return n1.Type, r.property, r.primitive_property, r.inferred_property", srcType=srcType)
            for record in ret:
                edge_lst[record["n1.Type"]] = {"inherited" : 0, "edge_inferred" : 1, "is_source" : 1, "property" : record["r.property"], "primitive_property" : record["r.primitive_property"], 
                                               "inferred_property" : record["r.inferred_property"]}

            ret = session.run("MATCH (n1:Node)-[r:Edge_TyH]->(n2:Node) where n1.Type=$srcType return n2.Type, r.property, r.primitive_property, r.inferred_property", srcType=srcType)
            for record in ret:
                edge_lst[record["n2.Type"]] = {"inherited" : 1, "edge_inferred" : 0, "is_source" : 0, "property" : record["r.property"], "primitive_property" : record["r.primitive_property"], 
                                               "inferred_property" : record["r.inferred_property"]}

            ret = session.run("MATCH (n1:Node)-[r:Edge_TyH]->(n2:Node) where n2.Type=$srcType return n1.Type, r.property, r.primitive_property, r.inferred_property", srcType=srcType)
            for record in ret:
                edge_lst[record["n1.Type"]] = {"inherited" : 1, "edge_inferred" : 0, "is_source" : 1, "property" : record["r.property"], "primitive_property" : record["r.primitive_property"], 
                                               "inferred_property" : record["r.inferred_property"]}

            ret = session.run("MATCH (n1:Node)-[r:Edge_Inf_TyH]->(n2:Node) where n1.Type=$srcType return n2.Type, r.property, r.primitive_property, r.inferred_property", srcType=srcType)
            for record in ret:
                edge_lst[record["n2.Type"]] = {"inherited" : 1, "edge_inferred" : 1, "is_source" : 0, "property" : record["r.property"], "primitive_property" : record["r.primitive_property"], 
                                               "inferred_property" : record["r.inferred_property"]}

            ret = session.run("MATCH (n1:Node)-[r:Edge_Inf_TyH]->(n2:Node) where n2.Type=$srcType return n1.Type, r.property, r.primitive_property, r.inferred_property", srcType=srcType)
            for record in ret:
                edge_lst[record["n1.Type"]] = {"inherited" : 1, "edge_inferred" : 1, "is_source" : 1, "property" : record["r.property"], "primitive_property" : record["r.primitive_property"], 
                                               "inferred_property" : record["r.inferred_property"]}

            return edge_lst


## get node properties and relations from the type graph
def get_Types():
    client = DB(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWD)
    dty = client.get_nodes()
    
    for t,v in dty.items():
        edges = client.get_edges(t)
        dty[t]["edges"] = edges
    
    client.close()
    return dty


## add type as node and corresponding relations as edges into the type graph
def add_Type(typ, pty, styp, edges):
    client = DB(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWD)
    if styp == "Unknown":
        client.add_node(typ, pty, [], styp, 1)
    else:
        client.add_node(typ, pty, [], styp, 0)
    
    dty = get_Types()
    
    if styp != "Unknown":
        client.add_edge_tyh(styp, typ, list(set(pty).intersection(set(dty[styp]["property"]))), dty[styp]["property"], [])
    
    for ty,pr in edges.items():
        client.add_edge(typ, ty, list(set(pr["npr"]).union(set(pr["pr"]))), pr["pr"], [])
    
    client.close()
    return


## get the best location for input type based on maximum similarity of properties
def get_type_location(typ, pty, styp, edges, dty):
    best_score = (0, 0, "")
    
    opp = lambda x: x[1:] if x[0]=='!' else '!'+x 
    opp_pty = list(map(opp, pty))

    for t,v in dty.items():
        (sim, dsim, bty) = best_score
        
        ptyU = set(v["property"]).union(set(v["inferred_property"]))
        
        if len(set(pty).intersection(ptyU)) == 0:
            sim_score = 0
            dsim_score = len(set(pty).union(ptyU))
            
        else:
            ptyI = set(pty).intersection(ptyU)
            sim_score = len(ptyI)
            dsim_score = len(set(pty).union(ptyU) - set(ptyI))
        
        oppM = len(set(opp_pty).intersection(ptyU))
        sim_score = sim_score + oppM
        dsim_score = dsim_score - (2 * oppM)            
        
        if sim_score > sim:
            best_score = (sim_score, dsim_score, t)
        elif sim_score == sim:
            if dsim_score < dsim: 
                best_score = (sim_score, dsim_score, t)

    (sim, dsim, btyp) = best_score
    
    return btyp
    

## do type and edge inference when a new node is added to the type graph
def infer_Type(typ, pty, styp, edges):
    client = DB(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWD)

    ifpty = []
    dty = get_Types()
    client_edges = {}
    
    if styp != "Unknown" and styp in dty.keys():
        print("dty.keys: {}".format(dty.keys()))
        pr = set(dty[styp]["property"])
        prI = set(dty[styp]["inferred_property"])        
        ifpty = pr.union(prI) - set(pty)
        
        client.add_node(typ, pty, list(ifpty), styp, 0)
        client.add_edge_tyh(styp, typ, dty[styp]["property"], [], [])

        for t,v in edges.items():
            client.add_edge(typ, t, list(set(v["npr"]).union(set(v["pr"]))), v["pr"], [])
            client.update_node(t, list(set(dty[t]["property"]).union(set(v["npr"]))), dty[t]["inferred_property"])
            client_edges[t] = {"property" : list(set(v["npr"]).union(set(v["pr"]))), "primitive_property" : v["pr"]}
            
        for t,v in dty[styp]["edges"].items():
            prU = set(pty).union(ifpty)
                    
            if len(v["primitive_property"]) > 0 and set(v["primitive_property"]).issubset(prU):
                if t not in edges.keys():
                    inf_pty1 = "inf_p" + str(randint(0,1000));
                    inf_pty2 = "inf_p" + str(randint(0,1000));
                    
                    if set(v["primitive_property"]).issubset(set(pty)):
                        client.add_edge_inferred(typ, t, v["primitive_property"] + [inf_pty2], v["primitive_property"], [inf_pty2])
                    else:
                        client.add_edge_inferred(typ, t, v["primitive_property"] + [inf_pty1, inf_pty2], v["primitive_property"] + [inf_pty1], [inf_pty1, inf_pty2])
                        client.update_node(typ, dty[typ]["property"] + [inf_pty1], dty[typ]["inferred_property"] + [inf_pty1])
                        
                    client.update_node(t, dty[t]["property"] + [inf_pty2], dty[t]["inferred_property"] + [inf_pty2])
                else:
                    client.update_edge(typ, t, list(set(v["primitive_property"]).union(set(client_edges[t]["property"]))), 
                        list(set(v["primitive_property"]).union(set(client_edges[t]["primitive_property"]))), [])
    else:
        btyp = get_type_location(typ, pty, styp, edges, dty)
        print ("typ : {}, btyp : {}".format(typ, btyp))
        pr = set(dty[btyp]["property"])
        prI = set(dty[btyp]["inferred_property"])  
        
        client.add_node(typ, pty, ifpty, styp, 1)

        for t,v in edges.items():
            client.add_edge(typ, t, list(set(v["npr"]).union(set(v["pr"]))), v["pr"], [])
            client.update_node(t, list(set(dty[t]["property"]).union(set(v["npr"]))), dty[t]["inferred_property"])
            client_edges[t] = {"property" : list(set(v["npr"]).union(set(v["pr"]))), "primitive_property" : v["pr"]}
                
        if set(pty).issubset(pr.union(prI)):
            client.add_edge_inferred_tyh(typ, btyp, pty, [], [])
            client.set_super_type(btyp, typ)
       
            for t,v in dty[btyp]["edges"].items():
                prU = set(pty).union(set(ifpty))
                    
                if len(v["primitive_property"]) > 0 and set(v["primitive_property"]).issubset(prU):
                    if t not in edges.keys():
                        client.add_edge_inferred(typ, t, v["primitive_property"], v["primitive_property"], [])
                    else:
                        client.update_edge(typ, t, list(set(v["primitive_property"]).union(set(client_edges[t]["property"]))), 
                            list(set(v["primitive_property"]).union(set(client_edges[t]["primitive_property"]))), [])
       
        else:
            if dty[btyp]["SuperType"] == "Unknown": # have to create inferred node as superType to btyp and typ

                if styp == "Unknown":
                    styp = "inf_node" + str(randint(0, 1000))

                client.set_super_type(btyp, styp)
                client.set_super_type(typ, styp)
                
                cpty = list(set(pty).intersection(pr.union(prI)))
                client.add_node_inferred(styp, [], cpty, "node" + str(randint(0,1000)), 1)  # styp should be unknown here
                client.add_edge_inferred_tyh(styp, typ, cpty, [], [])
                client.add_edge_inferred_tyh(styp, btyp, cpty, [], [])
                
                for t,v in dty[btyp]["edges"].items():
                    
                    if len(v["primitive_property"]) > 0 and set(v["primitive_property"]).issubset(cpty):
                        if t not in edges.keys():
                            client.add_edge_inferred(styp, t, v["primitive_property"], v["primitive_property"], [])
                            #client.add_edge_inferred(typ, t, v["primitive_property"], v["primitive_property"], [])
                            inf_pty1 = "inf_p" + str(randint(0,1000));
                            inf_pty2 = "inf_p" + str(randint(0,1000));
                            
                            if set(v["primitive_property"]).issubset(set(pty)):
                                client.add_edge_inferred(typ, t, v["primitive_property"] + [inf_pty2], v["primitive_property"], [inf_pty2])
                            else:
                                client.add_edge_inferred(typ, t, v["primitive_property"] + [inf_pty1, inf_pty2], v["primitive_property"] + [inf_pty1], [inf_pty1, inf_pty2])
                                client.update_node(typ, dty[typ]["property"] + [inf_pty1], dty[typ]["inferred_property"] + [inf_pty1])
                            
                            client.update_node(t, dty[t]["property"] + [inf_pty2], dty[t]["inferred_property"] + [inf_pty2])
                        else:
                            client.update_edge(typ, t, list(set(v["primitive_property"]).union(set(client_edges[t]["property"]))), 
                                list(set(v["primitive_property"]).union(set(client_edges[t]["primitive_property"]))), [])
                
            else: # btyp supertype is the supertype for typ
                client.set_super_type(typ, dty[btyp]["SuperType"])
                
                cpty = list(set(pty).intersection(pr.union(prI)))
                client.add_edge_inferred_tyh(dty[btyp]["SuperType"], typ, cpty, [], [])
                bstyp = dty[btyp]["SuperType"]

                for t,v in dty[bstyp]["edges"].items():
                    prU = set(pty).union(set(ifpty))
                    
                    if len(v["primitive_property"]) > 0 and set(v["primitive_property"]).issubset(prU):
                        if t not in edges.keys():
                            #client.add_edge_inferred(typ, t, v["primitive_property"], v["primitive_property"], [])
                            inf_pty1 = "inf_p" + str(randint(0,1000));
                            inf_pty2 = "inf_p" + str(randint(0,1000));
                            if set(v["primitive_property"]).issubset(set(pty)):
                                client.add_edge_inferred(typ, t, v["primitive_property"] + [inf_pty2], v["primitive_property"], [inf_pty2])
                            else:
                                client.add_edge_inferred(typ, t, v["primitive_property"] + [inf_pty1, inf_pty2], v["primitive_property"] + [inf_pty1], [inf_pty1, inf_pty2])
                                client.update_node(typ, dty[typ]["property"] + [inf_pty1], dty[typ]["inferred_property"] + [inf_pty1])
                            
                            client.update_node(t, dty[t]["property"] + [inf_pty2], dty[t]["inferred_property"] + [inf_pty2])
                        else:
                            client.update_edge(typ, t, list(set(v["primitive_property"]).union(set(client_edges[t]["property"]))), 
                                list(set(v["primitive_property"]).union(set(client_edges[t]["primitive_property"]))), [])
                            
    client.close()
    return


## TODO when a new property is added to a type, infer how to propagate this information in the type graph
def compute_knowledge_extension(a1, a2, k, kt):
    pass


# traverse through the type tree and generate explanations
def anwser_query_with_explanation(pty, styp, dtyp, qtype):
    client = DB(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWD)
    dty = get_Types()
    types = {}
    
    # check if query type is 1
    if qtype == 1:
    
        # find types that are most relevant based on properties
        for t in dty.keys():
            types[t] = len(list(set(pty).intersection(set(dty[t]["property"]))))
    
        types = dict(sorted(types.items(), key=lambda item: item[1], reverse=True))
        types_k = list(types.keys())
        types_v = list(types.values())

        print("The best matching type is {} with properties {} and score {}\n".format(types_k[0], dty[types_k[0]]["property"], types_v[0]))
        print("The next best matches based on scores:")
    
        # return the list of next best matches
        for i in range(1, len(types_k)):
            if types_v[i] != 0:
                print("type: {}, properties: {}, score: {}".format(types_k[i], dty[types_k[i]]["property"], types_v[i]))
    
    # check if query type is 2
    elif qtype == 2:
    
        if dty[styp]["SuperType"] == dtyp:
    
            print("{} is the super type of {}".format(dtyp, styp))
    
            # check if the super type is inferred
            if dty[styp]["SuperType_inferred"] == 1:
                print("Properties {} of type {} in {} of type {}".format(dty[dtyp]["property"], dtyp, dty[styp]["property"], styp))
    
        elif dty[dtyp]["SuperType"] == styp:
    
            print("{} is the super type of {}".format(styp, dtyp))
    
            # check if the super type is inferred
            if dty[dtyp]["SuperType_inferred"] == 1:
                print("Properties {} of type {} in {} of type {}".format(dty[styp]["property"], styp, dty[dtyp]["property"], dtyp))
    
        elif dtyp in dty[styp]["edges"].keys() and dty[styp]["edges"][dtyp]["is_source"] == 0:
    
            print("{} relates to {} based on properties {}\n".format(styp, dtyp, dty[styp]["edges"][dtyp]["property"]))
            
            # check if edges are inferred to generate explanations
            if dty[styp]["edges"][dtyp]["edge_inferred"] == 1:
                print("I am inferring the edge because of the following reasons:")
                
                pr_pty = set(dty[styp]["edges"][dtyp]["primitive_property"]) - set(dty[styp]["edges"][dtyp]["inferred_property"])
                
                if dty[styp]["SuperType"] != "Unknown":
                    for k,v in dty[dty[styp]["SuperType"]]["edges"].items():
                        if v["inherited"] == 1:
                            if dty[k]["edges"][dtyp]["edge_inferred"] == 0 and set(pr_pty).issubset(set(dty[k]["edges"][dtyp]["property"])):
                                sibling = k
                                print("The properties {} of {} is common with sibling {}".format(dty[styp]["edges"][dtyp]["primitive_property"], styp, k))
                                
                                inf_pr = list(filter(lambda p: p[0:3] == "inf", dty[styp]["edges"][dtyp]["primitive_property"]))
                                
                                if len(inf_pr) > 0:
                                    rel_pr = list(set(dty[k]["edges"][dtyp]["primitive_property"]) - set(dty[styp]["edges"][dtyp]["primitive_property"]))
                                    print("The inferred property {} of {} relates to {} of {}".format(inf_pr, styp, rel_pr, k))
                                    
                                inf_pr_d = list(filter(lambda p: p[0:3] == "inf", dty[styp]["edges"][dtyp]["property"]))
                                inf_pr_d = list(set(inf_pr_d) - set(inf_pr))
                                
                                if len(inf_pr_d) > 0:
                                    rel_pr_d = list(set(dty[k]["edges"][dtyp]["property"]) - set(dty[styp]["edges"][dtyp]["property"]))
                                    print("The inferred property {} of {} relates to {} of {}".format(inf_pr_d, styp, rel_pr_d, k))
                                    
                                
            
        elif styp in dty[dtyp]["edges"].keys() and dty[styp]["edges"][dtyp]["is_source"] == 1:
    
            print("{} relates to {} based on properties {}\n".format(dtyp, styp, dty[dtyp]["edges"][styp]["property"]))

            # check if edges are inferred to generate explanations
            if dty[dtyp]["edges"][styp]["edge_inferred"] == 1:
                print("I am inferring the edge because of the following reasons:")
                
                pr_pty = set(dty[dtyp]["edges"][styp]["primitive_property"]) - set(dty[dtyp]["edges"][styp]["inferred_property"])
                
                if dty[dtyp]["SuperType"] != "Unknown":
                    for k,v in dty[dty[dtyp]["SuperType"]]["edges"].items():
                        if v["inherited"] == 1:
                            if dty[k]["edges"][styp]["edge_inferred"] == 0 and set(pr_pty).issubset(set(dty[k]["edges"][styp]["property"])):
                                sibling = k
                                print("The properties {} of {} is common with sibling {}".format(dty[dtyp]["edges"][styp]["primitive_property"], dtyp, k))
                                
                                inf_pr = list(filter(lambda p: p[0:3] == "inf", dty[dtyp]["edges"][styp]["primitive_property"]))
                                
                                if len(inf_pr) > 0:
                                    rel_pr = list(set(dty[k]["edges"][styp]["primitive_property"]) - set(dty[dtyp]["edges"][styp]["primitive_property"]))
                                    print("The inferred property {} of {} relates to {} of {}".format(inf_pr, dtyp, rel_pr, k))
                                    
                                inf_pr_d = list(filter(lambda p: p[0:3] == "inf", dty[dtyp]["edges"][styp]["property"]))
                                inf_pr_d = list(set(inf_pr_d) - set(inf_pr))
                                
                                if len(inf_pr_d) > 0:
                                    rel_pr_d = list(set(dty[k]["edges"][styp]["property"]) - set(dty[dtyp]["edges"][styp]["property"]))
                                    print("The inferred property {} of {} relates to {} of {}".format(inf_pr_d, dtyp, rel_pr_d, k))
    
        else:
    
            print("No relation exists between {} and {}".format(styp, dtyp))
    
    # check if query type is 3
    elif qtype == 3:
        
        isrc_pty = list(set(dty[styp]["property"]).intersection(set(pty)))
        
        for t in dty[styp]["edges"].keys():
            if dty[styp]["SuperType"] != t:
                types[t] = len(list(set(isrc_pty).intersection(set(dty[styp]["edges"][t]["property"]))))
    
        types = dict(sorted(types.items(), key=lambda item: item[1], reverse=True))
        types_k = list(types.keys())
        types_v = list(types.values())

        print("The best match to type {} is type {} with properties {} and score {}\n".format(styp, types_k[0], dty[styp]["edges"][types_k[0]]["property"], types_v[0]))
        
        # check if edges are inferred to generate explanations
        if dty[styp]["edges"][types_k[0]]["edge_inferred"] == 1:
             query_and_explanation([], styp, types_k[0], 2)
        
        print("The next best matches based on scores:")
    
        # return the list of next best matches
        for i in range(1, len(types_k)):
            if types_v[i] != 0:
                print("type: {}, properties: {}, score: {}".format(types_k[i], dty[styp]["edges"][types_k[i]]["property"], types_v[i]))

                if dty[styp]["edges"][types_k[i]]["edge_inferred"] == 1:
                    print()
                    anwser_query_with_explanation([], styp, types_k[i], 2)
            
        
## build the initial environment
def init_environment():

    add_Type("t1", ["p1"], "Unknown", {})
    add_Type("t2", ["p1", "p7"], "t1", {})
    add_Type("t3", ["p1", "p6"], "t1", {})

def grow_type_tree():

    init_environment()

    #inst_1
    add_Type("t4", ["p2", "p3", "p4", "p5"], "Unknown", {"t3" : {"pr" : ["p3"], "npr": ["p6"]}, "t2" : {"pr" : ["p3", "p4"], "npr" : ["p7"]}})
    #inst_2
    infer_Type("t5", ["p3", "p4", "p5"], "Unknown", {})
    #inst_3
    infer_Type("t6", ["p3", "p4", "p9"], "t5", {"t2" : {"pr" : [], "npr" : ["p8"]}})


# this component answers the queries
def generate_query():
    #answer queries with explanations
    print("Query Type 1: \n")
    anwser_query_with_explanation(["p2", "p3", "p4"], "", "", 1)
    print("=======================================\n")
    #print("Query Type 2: \n")
    #anwser_query_with_explanation([], "t6", "t3", 2)
    #print("=======================================\n")
    #print("Query Type 2: \n")
    #anwser_query_with_explanation([], "t3", "t6", 2)
    #print("=======================================\n")
    #print("Query Type 3: \n")
    #anwser_query_with_explanation(["p3", "p4"], "t6", "", 3)
    #print("=======================================\n")

if __name__ == "__main__":
    #grow_type_tree()
    generate_query()
