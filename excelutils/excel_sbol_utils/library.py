def hello(rowobj):
	print("hello world")
	
def add(rowobj):
	num1 = rowobj.B
	num2 = rowobj.C
	total = num1 + num2
	return total

def objectType(rowobj):
	# used to decide the object type in the converter function
        pass

def types(rowobj):
        pass

def displayId(rowobj):
        # used to set the object display id in converter function
        pass

def addToDescription(rowobj):
	pass
#         current = getattr(self.obj, 'description')
#         if isinstance(current, type(None)):
#             current = ""
#         for col in self.col_cell_dict.keys():
#             val = self.col_cell_dict[col]
#             if isinstance(val, str):
#                 current = current + "\n" + col + ": " + val
#             else:
#                 raise TypeError(f"A multicolumn value was unexpectedly given in {self.sbol_term}, {self.col_cell_dict}")
#         setattr(self.obj, 'description', current)

def subcomponents(rowobj): #UPDATE TO WORK WITH CELL DICT, ALLOW CONSTRAINTS
	pass
#         # if type is compdef do one thing, if combdev do another, else error
#         if isinstance(self.obj, sbol3.component.Component):
#             for sub in self.cell_val:
#                 sub_part = sbol3.SubComponent(f'{sbol3.get_namespace()}{sub}')
#                 self.obj.features.append(sub_part)
#             # self.obj.assemblePrimaryStructure(self.cell_val)
#             # self.obj.compile(assembly_method=None)

#         elif isinstance(self.obj, sbol3.combderiv.CombinatorialDerivation):
#             comp_list = self.cell_val
#             comp_ind = 0
#             variant_comps = {}
#             for ind, comp in enumerate(comp_list):
#                 if "," in comp:
#                     comp_list[ind] = f'{self.obj.displayId}_subcomponent_{comp_ind}'
#                     uri = f'{self.obj.displayId}_subcomponent_{comp_ind}'
#                     sub_comp = sbol3.Component(uri, sbol3.SBO_DNA)
#                     sub_comp.displayId = f'{self.obj.displayId}_subcomponent_{comp_ind}'
#                     self.doc.add(sub_comp)
#                     variant_comps[f'subcomponent_{comp_ind}'] = {'object': sub_comp, 'variant_list': comp}
#                     comp_ind += 1

#             # # move this to the object creation section
#             # template = sbol2.ComponentDefinition(f'{self.obj.displayId}_template')
#             # template.displayId = f'{self.obj.displayId}_template'
#             # self.doc.add(template)


#             template = self.obj_dict[f'{self.obj.displayId}_template']['object']

#             for sub in comp_list:
#                 name = f'{sbol3.get_namespace()}{sub}'
#                 name = hf.check_name(name)
#                 sub_part = sbol3.SubComponent(name)
#                 template.features.append(sub_part)
#             # template.assemblePrimaryStructure(comp_list)
#             # template.compile(assembly_method=None)

#             self.obj.masterTemplate = template
#             for var in variant_comps:
#                 var_comp = sbol3.VariableFeature(cardinality=sbol3.SBOL_ONE,
#                                                  variable=f'var_{var}')
#                 var_comp.displayId = f'var_{var}'
#                 var_comp.variable = variant_comps[var]['object']

#                 var_list = re.split(",", variant_comps[var]['variant_list'])
#                 var_list = [f'{sbol3.get_namespace()}{x.strip()}' for x in var_list]
#                 var_comp.variants = var_list
#                 self.obj.variable_features.append(var_comp)

#         else:
#             raise KeyError(f'The object type "{type(self.obj)}" does not allow subcomponents. (sheet:{self.sheet}, row:{self.sht_row}, col:{self.sht_col})')

def dataSource(rowobj): #UPDATE TO WORK ON MULTI COLUMN??? WITH CELL DICT
	pass
#         self.obj.wasDerivedFrom = self.cell_val
#         if "pubmed.ncbi.nlm.nih.gov/" in self.cell_val:
#             if 'obo' not in self.doc_pref_terms:
#                 self.doc.addNamespace('http://purl.obolibrary.org/obo/', 'obo')
#                 self.doc_pref_terms.append('obo')

#             self.obj.OBI_0001617 = sbol3.TextProperty(self.obj,
#                                                             'http://purl.obolibrary.org/obo/OBI_0001617',
#                                                             0, 1, [])
#             self.obj.OBI_0001617 = self.cell_val.split(".gov/")[1].replace("/", "")

def sequence(rowobj):
	pass
#         for col in self.col_cell_dict.keys():
#             val = self.col_cell_dict[col]
#             if isinstance(val, str):
#                 # might need to be careful if the object type is sequence!
#                 # THIS MIGHT HAVE BUGS IF MULTIPLE SEQUENCES ARE PROVIDED FOR
#                 # ONE OBJECT. E.g overwrite in self.obj.sequences = [val] ?
#                 if re.fullmatch(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', val):
#                     # if a url
#                     self.obj.sequences = [val]

#                 elif re.match(r'^[a-zA-Z \s*]+$', val):
#                     # if a sequence string

#                     # removes spaces, enters, and makes all lower case
#                     val = "".join(val.split())
#                     val = val.replace(u"\ufeff", "").lower()

#                     # create sequence object
#                     sequence = sbol3.Sequence(f"{self.obj.displayId}_sequence",
#                                             elements=val)
#                     if self.obj.name is not None:
#                         sequence.name = f"{self.obj.name} Sequence"

#                     self.doc.add(sequence)

#                     # link sequence object to component definition
#                     self.obj.sequences = [sequence]

#                 else:
#                     logging.warning(f'The cell value for {self.obj.identity} is not an accepted sequence type, it has been added as a uri and left for post processing. Sequence value provided: {val} (sheet:{self.sheet}, row:{self.sht_row}, col:{col})')
#                     self.obj.sequences = [val]
#             else:
#                 raise TypeError(f"A multicolumn value was unexpectedly given in {self.sbol_term}, {self.col_cell_dict}")
