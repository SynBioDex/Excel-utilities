import sbol2
import excel_sbol_utils.helpers as hf
import re
import logging
# might be better if some of the ones like data sources were put in a library
# which contained both sbol2 and sbol3. Then excel converter could check
# if in lib2 or lib_both for version 2 and lib3 or lib_both for version 3
# would reduce code duplication?



def objectType(rowobj):
    # used to decide the object type in the converter function
    pass

def displayId(rowobj):
    # used to set the object display id in converter function
    pass

def types(rowobj):
    for col in rowobj.col_cell_dict.keys():
        # overwrites standard #DnaRegion biopax where another type is given
        val = rowobj.col_cell_dict[col]
        if val not in rowobj.obj.types[0] and len(rowobj.obj.types) == 1:
            rowobj.obj.types = val

def addToDescription(rowobj):
	current = getattr(rowobj.obj, 'description')
	if isinstance(current, type(None)):
		current = ""
	for col in rowobj.col_cell_dict.keys():
		val = rowobj.col_cell_dict[col]
		if isinstance(val, str):
			current = current + "\n" + col + ": " + val
		else:
			raise TypeError(f"A multicolumn value was unexpectedly given in addToDescription, {rowobj.col_cell_dict}")
	setattr(rowobj.obj, 'description', current)

def moduleModuleDefiniton(rowobj): #NOT IMPLEMENTED
    # module_name_pref = self.obj_uri.split("/")[-1]
    # module_name_suf = self.cell_val.split("/")[-1]
    # mod1 = sbol2.Module(f"{module_name_pref}_{module_name_suf}")
    # mod1.definition = self.cell_val

    # self.obj.modules.add(mod1)
    pass

def additionalFuncComponent(rowobj): #NOT IMPLEMENTED
    # fc_name_pref = self.obj_uri.split("/")[-1]
    # fc_name_suf = self.cell_val.split("/")[-1]

    # fc1 = sbol2.FunctionalComponent(f"{fc_name_pref}_{fc_name_suf}")
    # fc1.definition = self.cell_val
    # self.obj.functionalComponents.add(fc1)
    pass

def definedFunComponent(rowobj): #NOT IMPLEMENTED
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
    pass

def subcomponents(rowobj):
	sbol2.Config.setOption(sbol2.ConfigOptions.SBOL_TYPED_URIS, True)
	if 'subcomp' in rowobj.col_cell_dict:
		subcomps = list(rowobj.col_cell_dict['subcomp'].values())
	if 'constraint' in rowobj.col_cell_dict:
		constraints = list(rowobj.col_cell_dict['constraint'].values())
	else:
		constraints = []

	if len(constraints) > 0:
		logging.warning(f'Constraints have not yet been implemented')

	#print(type(rowobj.obj))

    # if type is compdef do one thing, if combdev do another, else error
	if isinstance(rowobj.obj, sbol2.componentdefinition.ComponentDefinition):
		rowobj.obj.assemblePrimaryStructure(subcomps)
		rowobj.obj.compile(assembly_method=None)

	elif isinstance(rowobj.obj, sbol2.combinatorialderivation.CombinatorialDerivation):
		comp_list = subcomps
		#print(f'comp list:{comp_list}')
		comp_ind = 0
		variant_comps = {}
		non_var_comps = []
		for ind, comp in enumerate(comp_list):
			if "," in comp or type(rowobj.obj_dict[comp]['object']) == \
									sbol2.combinatorialderivation.CombinatorialDerivation:
				comp_list[ind] = f'{rowobj.obj.displayId}_subcomponent_{comp_ind}'
				uri = f'{rowobj.obj.displayId}_subcomponent_{comp_ind}'
				sub_comp = sbol2.ComponentDefinition(uri)
				sub_comp.displayId = f'{rowobj.obj.displayId}_subcomponent_{comp_ind}'
				rowobj.doc.add(sub_comp)
				variant_comps[f'subcomponent_{comp_ind}'] = {'object': sub_comp, 'variant_list': comp}
				comp_ind += 1
			else:
				comp_list[ind] = hf.check_name(comp_list[ind])
				non_var_comps.append(hf.check_name(comp_list[ind]))

		template = sbol2.ComponentDefinition(f'{rowobj.obj.displayId}_template')
		template.displayId = f'{rowobj.obj.displayId}_template'
		rowobj.doc.add(template)

		print(comp_list)
		print(non_var_comps)
		template.assemblePrimaryStructure(comp_list)
		#template.compile(assembly_method=None)

		rowobj.obj.masterTemplate = template
		for var in variant_comps:
			#var = hf.check_name(var)
			var_comp = sbol2.VariableComponent(f'var_{var}')
			var_comp.displayId = f'var_{var}'
			var_comp.variable = variant_comps[var]['object']

			var_list = re.split(",", variant_comps[var]['variant_list'])
			var_list = [f'{sbol2.getHomespace()}{hf.check_name(x.strip())}' for x in var_list]
			var_comp.variants = var_list
			rowobj.obj.variableComponents.add(var_comp)

	else:
		raise KeyError(f'The object type "{type(rowobj.obj)}" does not allow subcomponents. (sheet:{rowobj.sheet}, row:{rowobj.sht_row}, col:{rowobj.col_cell_dict})')

def dataSource(rowobj):
	prefs = rowobj.col_cell_dict['pref']
	vals = rowobj.col_cell_dict['val']
	for colnum in range(len(prefs.keys())):
		# as column names are different for the different multicol values
		pref = prefs[list(prefs.keys())[colnum]]
		val = vals[list(vals.keys())[colnum]]

		datasource_dict = {'GenBank':{'Replace Example':'https://www.ncbi.nlm.nih.gov/nuccore/{REPLACE_HERE}', 'Literal Part':'FALSE'},
						'PubMed':{'Replace Example':'https://pubmed.ncbi.nlm.nih.gov/{REPLACE_HERE}/', 'Literal Part':'FALSE'},
						'iGEM registry':{'Replace Example':'http://parts.igem.org/Part:{REPLACE_HERE}', 'Literal Part':'FALSE'},
						'AddGene':{'Replace Example':'https://www.addgene.org/{REPLACE_HERE}/', 'Literal Part':'FALSE'},
						'Seva plasmids':{'Replace Example':'http://www.sevahub.es/public/Canonical/{REPLACE_HERE}/1', 'Literal Part':'FALSE'},
						'Tax_id':{'Replace Example':'https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Info&id={REPLACE_HERE}', 'Literal Part':'FALSE'},
						'SynBioHub':{'Replace Example':'{REPLACE_HERE}', 'Literal Part':'FALSE'},
						'Local Sequence File':{'Replace Example':'', 'Literal Part':'FALSE'},
						'URL for GenBank file':{'Replace Example':'{REPLACE_HERE}', 'Literal Part':'FALSE'},
						'URL for FASTA file':{'Replace Example':'{REPLACE_HERE}', 'Literal Part':'FALSE'},
				   		'DOI':{'Replace Example':'{REPLACE_HERE}', 'Literal Part':'FALSE'}
						}
		#datasource_dict = {'GenBank':{'Replace Example':'https://www.ncbi.nlm.nih.gov/nuccore/{REPLACE_HERE}', 'Literal Part':'TRUE'},
		#				'PubMed':{'Replace Example':'https://pubmed.ncbi.nlm.nih.gov/{REPLACE_HERE}/', 'Literal Part':'FALSE'},
		#				'iGEM registry':{'Replace Example':'http://parts.igem.org/Part:{REPLACE_HERE}', 'Literal Part':'TRUE'},
		#				'AddGene':{'Replace Example':'https://www.addgene.org/{REPLACE_HERE}/', 'Literal Part':'FALSE'},
		#				'Seva plasmids':{'Replace Example':'http://www.sevahub.es/public/Canonical/{REPLACE_HERE}/1', 'Literal Part':'TRUE'},
		#				'Tax_id':{'Replace Example':'https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Info&id={REPLACE_HERE}', 'Literal Part':'FALSE'},
		#				'SynBioHub':{'Replace Example':'{REPLACE_HERE}', 'Literal Part':'TRUE'},
		#				'Local Sequence File':{'Replace Example':'', 'Literal Part':'FALSE'},
		#				'URL for GenBank file':{'Replace Example':'{REPLACE_HERE}', 'Literal Part':'TRUE'},
		#				'URL for FASTA file':{'Replace Example':'{REPLACE_HERE}', 'Literal Part':'TRUE'}
		#				}

		literal = datasource_dict[pref]['Literal Part']

		if literal == 'FALSE':
			rowobj.obj.wasDerivedFrom = datasource_dict[pref]['Replace Example'].replace('{REPLACE_HERE}', val)

		else:
			#replace_str = datasource_dict[pref]['Replace Example']
			#rowobj.obj.wasDerivedFrom = 
			logging.warning('Literal data sources are not yet supported.')

def sequence(rowobj):
	for col in rowobj.col_cell_dict.keys():
		val = rowobj.col_cell_dict[col]
		if isinstance(val, str):
			# might need to be careful if the object type is sequence!
			# THIS MIGHT HAVE BUGS IF MULTIPLE SEQUENCES ARE PROVIDED FOR
			# ONE OBJECT. E.g overwrite in self.obj.sequences = [val] ?
			if re.fullmatch(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', val):
				# if a url
				rowobj.obj.sequences = [val]

			elif re.match(r'^[a-zA-Z \s*]+$', val):
				# if a sequence string

				# removes spaces, enters, and makes all lower case
				val = "".join(val.split())
				val = val.replace(u"\ufeff", "").lower()

				# create sequence object
				sequence = sbol2.Sequence(f"{rowobj.obj.displayId}_sequence",
										elements=val)
				if rowobj.obj.name is not None:
					sequence.name = f"{rowobj.obj.name} Sequence"

				rowobj.doc.add(sequence)

				# link sequence object to component definition
				rowobj.obj.sequences = [sequence]

			else:
				logging.warning(f'The cell value for {rowobj.obj.identity} is not an accepted sequence type, it has been added as a uri and left for post processing. Sequence value provided: {val} (sheet:{rowobj.sheet}, row:{rowobj.sht_row}, col:{col})')
				rowobj.obj.sequences = [val]
		else:
			raise TypeError(f"A multicolumn value was unexpectedly given in sequence, {rowobj.col_cell_dict}")

def finalProduct(rowobj):
	# create final products collection if it doesn't yet exist
	# add object to collection
	columns = rowobj.col_cell_dict
 
	for col in columns:
		# check if the cell value is true
		if columns[col]:
			doc = rowobj.doc

			sbol_objs = doc.objects
			sbol_objs_names = [x.name for x in sbol_objs]
			if 'FinalProducts' not in sbol_objs_names:
				colec = sbol2.Collection('FinalProducts', name='FinalProducts')

				sbol_objs = doc.objects
				sbol_objs_names = [x.name for x in sbol_objs]

				doc.add(colec)
			else:
				colec = sbol_objs[sbol_objs_names.index('FinalProducts')]
			
			# add obj as member to final products
			colec.members.append(rowobj.obj_uri)

def circular(rowobj): # NOT IMPLEMENTED
    pass
