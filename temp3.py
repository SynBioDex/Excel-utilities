import rdflib
import os
import sbol3
import excel_sbol_utils.helpers as h

direct = os.path.split(__file__)[0]
file_path_in = os.path.join(direct, 'SBOL3_simple_library4.nt')


# read in the document as an rdf graph
g = rdflib.Graph()
result = g.parse(file_path_in)

# Creating the Sbol document to be changed from the conversion
doc = sbol3.Document()
doc.read(file_path_in)

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

parent_dict_copy = parent_dict

print(parent_dict)

# objects that are only children are objects that are not also parents
child_only = children - set(parent_dict).intersection(children)

# Loop through children create a dictionary for the object and the type of the object to look at in while loop
# Keep track of the old uris and new uris in case they change - function already exists to change in document

old_uris = [] # Correlates index to index with each of the new uris
new_uris = []

# process the children only objects and update the 'tree'
while len(parent_dict) > 0:
    # do something to deal with child_only
    # for this you probably need to read in the sbol document at the top and perform actions using pysbol

    # Import SBOL document as the SBOL document type
    # Go through each of the children and determine if it is a combinatorial derivation - may have to save a copy of the parent dictionary
    # Go through each of the uris in the child object and look to see if those uris in parent dictionary are combinatorial derivations - going to need pysbol
    # Take it out as a string and check what the type is in the object in the sbol document 
    # May have to write in another file for now
    # Object stays combinatorial derivation if one of its subcomponents is a combinatorial derivation
        # Else: Becomes a component
    # For collection: If has a variable feature and nothing else
    
    # loop over parents

    for parent in parent_dict:
        if parent_dict[parent].issubset(child_only): # If the parent's children are a subset of childOnly
            print(parent) # Print the name of the parent object
            child_types = [] # Create a list of all of the types of child objects
            for child in parent_dict[parent]:
                children_of_parent = set()
                obj = doc.find(child)
                children_of_parent.add(type(obj))

            # if len(child_types) == len(parent_dict[parent]): # Check to see that it's the end of the loop
            # Trying to see if it can be a collection object
            if len(children_of_parent) == 0: # Checking to see if there aren't any children and only contains a variable feature
                parentObj = doc.find(parent) # In template not in the parent
                template = doc.find(f'{parent}_template') # Get the template object from the parent

                if len(template.features) == 1 and type(template.features[0]) == sbol3.VariableFeature: # If it only has 1 variable feature and nothing else - collection object
                    col = sbol3.Collection()
                    for variant in template.features[0]: # Add all variants of the variable feature to the collection
                        col.members.append(variant)

                    # Delete original comb der + template after adding in uris to appropriate arrays
                    old_uris.append(parentObj.identity)
                    new_uris.append(col.identity)

                    doc.remove_object(parentObj)
                    doc.remove_object(template)




            
            if sbol3.CombinatorialDerivation not in children_of_parent: # If there is no child that is a combinatorial derivation
                # Delete the template that's currently in the document
                # Create a new component object and carry over all of the features from the combinatorial derivation (including exact name)
                    # Name, (references to) subcomponents, (references to) constraints, name, displayId, role, type
                # Delete the previous combinatorial derivation object 
                # Put the new component object into the document

                parentObj = doc.find(parent) # Get the object that the parent is supposed to be

                template = doc.find(f'{parent}_template') # Get the template object from the parent

                # print(parentObj._properties)
                old_uris.append(parentObj.identity) # Add the uri of the old parent object to the list

                componentObj = sbol3.Component(identity=parentObj.identity, types=parentObj.type_uri) # Create a new component object

                new_uris.append(componentObj.identity) # Add its URI to the list of new uris

                componentObj.name = parentObj.name # Set the name

                print(parentObj._properties)

                for feature in template.features:
                    if type(feature) != sbol3.LocalSubComponent:
                        subComp = sbol3.SubComponent(instance_of=feature.instance_of)
                        componentObj.features.append(subComp) # 

                for role in template.roles:
                    componentObj.roles.append(role) 

                # Still need to find out how to attribute subcomponents, constraints (Both subcomponents and constraints and roles in template)
                for prop in parentObj._properties:
                    for subProp in parentObj._properties[prop]:
                        if prop == "http://sbols.org/v3#template":
                            continue
                        
                        if type(subProp) == rdflib.term.URIRef:
                            setattr(componentObj, prop,
                                    sbol3.URIProperty(componentObj,
                                                    f'{prop}',
                                                    '0', '*', initial_value=[subProp]))
                        else:
                            setattr(componentObj, prop,
                                    sbol3.TextProperty(componentObj,
                                                    prop,
                                                    '0', '*', initial_value=str(subProp)))
                
                for constraint in template.constraints:
                    newConstraint = sbol3.Constraint(constraint.restriction, constraint.subject, constraint.object)
                    newConstraint.derived_from = constraint.derived_from
                    componentObj.constraints.append(newConstraint)
                    # Add all to component
                    # Eventually should be more filtered

                componentObj.types[0] = sbol3.component.SBOL_COMPONENT

                print(componentObj._properties)


                doc.remove_object(parentObj) # Remove the old object
                doc.remove_object(template) # Remove the old template

                doc.add(componentObj) # Add the new object
                    
        # print(child, parent_dict_copy[child])

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

# Update uris on document using the old uri and new uri comparison
oldToNew = {}
for i in range(len(old_uris)):
    oldToNew[old_uris[i]] = new_uris[i]
    
h.update_uri_refs(doc, oldToNew) 

# return updated sbol document
file_path_out = "SampleTemp3Output.nt"
doc.write(file_path_out)