import sbol2
import sbol3
import excel_sbol_utils.library2 as l2
import excel_sbol_utils.library3 as l3
import excel_sbol_utils.helpers as help
import excel2sbol.comp_column_functions2 as ccf
import excel2sbol.converter as conv
import os

# Build a barebones combinatorial derivation object
# Attempt to build subcomponent on it

obj = sbol2.combinatorialderivation()

doc = sbol2.Document()
obj_dict = {}
sheet = 'Composite Parts'




