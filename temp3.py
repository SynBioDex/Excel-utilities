import rdflib
import os
import sbol3

direct = os.path.split(__file__)[0]
file_path_in = os.path.join(direct, 'SBOL3_simple_library4.nt')


# read in the document as an rdf graph
g = rdflib.Graph()
result = g.parse(file_path_in)

# collect all the objects which are combinatorial derivations and their featured components
knows_query = """
SELECT
    ?subject
    ?object
WHERE {
    ?subject <http://sbols.org/v3#template> ?template .
    ?template <http://sbols.org/v3#hasFeature> ?feature .
    ?feature <http://sbols.org/v3#instanceOf> ?object .
}"""
qres = g.query(knows_query)

# create a tree structure
children = set() # all objects that are referenced by another object
parent_dict = {} # all objects that reference another object and the objects they reference as a set
for row in qres:
    s = str(row.subject)
    o = str(row.object)
    children.add(o)
    if s in parent_dict:
        parent_dict[s].add(o)
    else:
        parent_dict[s] = {o}

# objects that are only children are objects that are not also parents
child_only = children - set(parent_dict).intersection(children)

# process the children only objects and update the 'tree'
while len(parent_dict) > 0:
    # do something to deal with child_only
    # for this you probably need to read in the sbol document at the top and perform actions using pysbol

    # remove child only children from dictionary
    new_parent_dict = {}
    for key in parent_dict:
        current_children = parent_dict[key]
        remaining_children = current_children - current_children.intersection(child_only)
        if len(remaining_children) > 0:
            new_parent_dict[key] = remaining_children
    parent_dict = new_parent_dict

    # update child_only list
    child_only = children - set(parent_dict).intersection(children)

# return updated sbol document