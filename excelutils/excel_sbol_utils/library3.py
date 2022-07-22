import re
import logging
import sbol3
import excel_sbol_utils.helpers as helpers


def objectType(rowobj):
	# used to decide the object type in the converter function
	pass

def types(rowobj):
	pass

def displayId(rowobj):
	# used to set the object display id in converter function
	pass

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

def subcomponents(rowobj): #UPDATE TO WORK WITH CELL DICT, ALLOW CONSTRAINTS
	if 'subcomp' in rowobj.col_cell_dict:
		subcomps = list(rowobj.col_cell_dict['subcomp'].values())
	if 'constraint' in rowobj.col_cell_dict:
		constraints = list(rowobj.col_cell_dict['constraint'].values())
	else:
		constraints = []

	if len(constraints) > 0:
		logging.warning(f'Constraints have not yet been implemented')

	# if type is compdef do one thing, if combdev do another, else error
	if isinstance(rowobj.obj, sbol3.component.Component):
		for sub in subcomps:
			sub_part = sbol3.SubComponent(f'{sbol3.get_namespace()}{sub}')
			rowobj.obj.features.append(sub_part)
		# self.obj.assemblePrimaryStructure(self.cell_val)
		# self.obj.compile(assembly_method=None)

	elif isinstance(rowobj.obj, sbol3.combderiv.CombinatorialDerivation):
		comp_list = subcomps
		comp_ind = 0
		variant_comps = {}
		for ind, comp in enumerate(comp_list):
			if "," in comp:
				comp_list[ind] = f'{rowobj.obj.displayId}_subcomponent_{comp_ind}'
				uri = f'{rowobj.obj.displayId}_subcomponent_{comp_ind}'
				sub_comp = sbol3.Component(uri, sbol3.SBO_DNA)
				sub_comp.displayId = f'{rowobj.obj.displayId}_subcomponent_{comp_ind}'
				rowobj.doc.add(sub_comp)
				variant_comps[f'subcomponent_{comp_ind}'] = {'object': sub_comp, 'variant_list': comp}
				comp_ind += 1

		template = rowobj.obj_dict[f'{rowobj.obj.displayId}_template']['object']

		for sub in comp_list:
			name = f'{sbol3.get_namespace()}{helpers.check_name(sub)}'
			sub_part = sbol3.SubComponent(name)
			template.features.append(sub_part)
		# template.assemblePrimaryStructure(comp_list)
		# template.compile(assembly_method=None)

		rowobj.obj.masterTemplate = template
		for var in variant_comps:
			var_comp = sbol3.VariableFeature(cardinality=sbol3.SBOL_ONE,
												variable=f'var_{var}')
			var_comp.displayId = f'var_{var}'
			var_comp.variable = variant_comps[var]['object']

			var_list = re.split(",", variant_comps[var]['variant_list'])
			var_list = [f'{sbol3.get_namespace()}{helpers.check_name(x.strip())}' for x in var_list]
			var_comp.variants = var_list
			rowobj.obj.variable_features.append(var_comp)

	else:
		raise KeyError(f'The object type "{type(rowobj.obj)}" does not allow subcomponents. (sheet:{rowobj.sheet}, row:{rowobj.sht_row}, sbol term dict:{rowobj.col_cell_dict})')

def dataSource(rowobj):
	prefs = rowobj.col_cell_dict['pref']
	vals = rowobj.col_cell_dict['val']
	for colnum in range(len(prefs.keys())):
		# as column names are different for the different multicol values
		pref = prefs[list(prefs.keys())[colnum]]
		val = vals[list(vals.keys())[colnum]]

		datasource_dict = {'GenBank':{'Replace Example':'https://www.ncbi.nlm.nih.gov/nuccore/{REPLACE_HERE}', 'Literal Part':'TRUE'},
						'PubMed':{'Replace Example':'https://pubmed.ncbi.nlm.nih.gov/{REPLACE_HERE}/', 'Literal Part':'FALSE'},
						'iGEM registry':{'Replace Example':'http://parts.igem.org/Part:{REPLACE_HERE}', 'Literal Part':'TRUE'},
						'AddGene':{'Replace Example':'https://www.addgene.org/{REPLACE_HERE}/', 'Literal Part':'FALSE'},
						'Seva plasmids':{'Replace Example':'http://www.sevahub.es/public/Canonical/{REPLACE_HERE}/1', 'Literal Part':'TRUE'},
						'Tax_id':{'Replace Example':'https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Info&id={REPLACE_HERE}', 'Literal Part':'FALSE'},
						'SynBioHub':{'Replace Example':'{REPLACE_HERE}', 'Literal Part':'TRUE'},
						'Local Sequence File':{'Replace Example':'', 'Literal Part':'FALSE'},
						'URL for GenBank file':{'Replace Example':'{REPLACE_HERE}', 'Literal Part':'TRUE'},
						'URL for FASTA file':{'Replace Example':'{REPLACE_HERE}', 'Literal Part':'TRUE'}
						}

		literal = datasource_dict[pref]['Literal Part']

		if literal == 'FALSE':
			rowobj.obj.wasDerivedFrom = val

		else:
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
				sequence = sbol3.Sequence(f"{rowobj.obj.displayId}_sequence",
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

def circular(rowobj):
	# if false add to linear collection if true add to types
	pass

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
			if 'FinalProducts' not in sbol_objs:
				colec = sbol3.Collection('FinalProducts', name='FinalProducts')
			else:
				colec = sbol_objs[sbol_objs_names.index('FinalProducts')]
			
			#add obj as member to final products
			colec.members.append(rowobj.obj_uri)
