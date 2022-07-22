import sbol2
import re
import logging



def objectType(rowobj):
    # used to decide the object type in the converter function
    pass

def displayId(rowobj):
    # used to set the object display id in converter function
    pass

def types(rowobj):
    pass
    # # overwrites standard #DnaRegion biopax where another type is given
    # if self.cell_val not in self.obj.types[0] and len(self.obj.types) == 1:
    #     self.obj.types = self.cell_val

def addToDescription(rowobj):
    pass
    # current = getattr(self.obj, 'description')
    # if isinstance(current, type(None)):
    #     current = ""
    # new = current + "\n" + self.sht_col + ": " + self.cell_val
    # setattr(self.obj, 'description', new)


def moduleModuleDefiniton(rowobj):
    pass
    # module_name_pref = self.obj_uri.split("/")[-1]
    # module_name_suf = self.cell_val.split("/")[-1]
    # mod1 = sbol2.Module(f"{module_name_pref}_{module_name_suf}")
    # mod1.definition = self.cell_val

    # self.obj.modules.add(mod1)

def additionalFuncComponent(rowobj):
    pass
    # fc_name_pref = self.obj_uri.split("/")[-1]
    # fc_name_suf = self.cell_val.split("/")[-1]

    # fc1 = sbol2.FunctionalComponent(f"{fc_name_pref}_{fc_name_suf}")
    # fc1.definition = self.cell_val
    # self.obj.functionalComponents.add(fc1)

def definedFunComponent(rowobj):
    pass
    # if isinstance(self.cell_val, list):
    #     # pulling the functional component object
    #     # by the name (hence the split) from the obj_cit
    #     fcobj = self.obj_dict[self.cell_val[0].split("/")[-1]]['object']
    # else:
    #     # pulling the functional component object
    #     # by the name (hence the split) from the obj_cit
    #     fcobj = self.obj_dict[self.cell_val.split("/")[-1]]['object']

    # # print(self.obj, fcobj)
    # self.obj.functionalComponents.add(fcobj.copy())

def subcomponents(rowobj):
    pass
    # # if type is compdef do one thing, if combdev do another, else error
    # if isinstance(self.obj, sbol2.componentdefinition.ComponentDefinition):
    #     self.obj.assemblePrimaryStructure(self.cell_val)
    #     self.obj.compile(assembly_method=None)

    # elif isinstance(self.obj, sbol2.combinatorialderivation.CombinatorialDerivation):
    #     comp_list = self.cell_val
    #     comp_ind = 0
    #     variant_comps = {}
    #     for ind, comp in enumerate(comp_list):
    #         if "," in comp:
    #             comp_list[ind] = f'{self.obj.displayId}_subcomponent_{comp_ind}'
    #             uri = f'{self.obj.displayId}_subcomponent_{comp_ind}'
    #             sub_comp = sbol2.ComponentDefinition(uri)
    #             sub_comp.displayId = f'{self.obj.displayId}_subcomponent_{comp_ind}'
    #             self.doc.add(sub_comp)
    #             variant_comps[f'subcomponent_{comp_ind}'] = {'object': sub_comp, 'variant_list': comp}
    #             comp_ind += 1

    #     template = sbol2.ComponentDefinition(f'{self.obj.displayId}_template')
    #     template.displayId = f'{self.obj.displayId}_template'
    #     self.doc.add(template)

    #     template.assemblePrimaryStructure(comp_list)
    #     template.compile(assembly_method=None)

    #     self.obj.masterTemplate = template
    #     for var in variant_comps:
    #         var_comp = sbol2.VariableComponent(f'var_{var}')
    #         var_comp.displayId = f'var_{var}'
    #         var_comp.variable = variant_comps[var]['object']

    #         var_list = re.split(",", variant_comps[var]['variant_list'])
    #         var_list = [f'{sbol2.getHomespace()}{x.strip()}' for x in var_list]
    #         var_comp.variants = var_list
    #         self.obj.variableComponents.add(var_comp)

    # else:
    #     raise KeyError(f'The object type "{type(self.obj)}" does not allow subcomponents. (sheet:{self.sheet}, row:{self.sht_row}, col:{self.sht_col})')

def dataSource(rowobj):
    pass
    # self.obj.wasDerivedFrom = self.cell_val
    # if "pubmed.ncbi.nlm.nih.gov/" in self.cell_val:
    #     if 'obo' not in self.doc_pref_terms:
    #         self.doc.addNamespace('http://purl.obolibrary.org/obo/', 'obo')
    #         self.doc_pref_terms.append('obo')

    #     self.obj.OBI_0001617 = sbol2.TextProperty(self.obj,
    #                                                     'http://purl.obolibrary.org/obo/OBI_0001617',
    #                                                     0, 1, [])
    #     self.obj.OBI_0001617 = self.cell_val.split(".gov/")[1].replace("/", "")

def sequence(rowobj):
    pass
    # # might need to be careful if the object type is sequence!
    # if re.fullmatch(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', self.cell_val):
    #     # if a url
    #     self.obj.sequences = self.cell_val

    # elif re.match(r'^[a-zA-Z \s*]+$', self.cell_val):
    #     # if a sequence string

    #     # removes spaces, enters, and makes all lower case
    #     self.cell_val = "".join(self.cell_val.split())
    #     self.cell_val = self.cell_val.replace(u"\ufeff", "").lower()

    #     # create sequence object
    #     sequence = sbol2.Sequence(f"{self.obj.displayId}_sequence",
    #                                 self.cell_val, sbol2.SBOL_ENCODING_IUPAC)
    #     if self.obj.name is not None:
    #         sequence.name = f"{self.obj.name} Sequence"

    #     self.doc.addSequence(sequence)

    #     # link sequence object to component definition
    #     self.obj.sequences = sequence

    # else:
    #     self.obj.sequences = self.cell_val
    #     logging.warning(f'The cell value for {self.obj.identity} is not an accepted sequence type but it has been left for post processing. Sequence value provided: {self.cell_val} (sheet:{self.sheet}, row:{self.sht_row}, col:{self.sht_col})')
    #     # raise ValueError(f'The cell value for {self.obj.identity} is not an accepted sequence type, please use a sequence string or uri instead. Sequence value provided: {self.cell_val} (sheet:{self.sheet}, row:{self.sht_row}, col:{self.sht_col})')
