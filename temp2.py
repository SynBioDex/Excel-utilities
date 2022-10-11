import sbol3
import os
import rdflib

cwd = os.getcwd()
print(cwd)

file_path_in = os.path.join(cwd, 'SBOL3_simple_library4.nt')
file_path_out = os.path.join(cwd, 'out_test.nt')

update_dict = {'http://sbolstandard.org/testfiles/J23101': 'http://parts.igem.org/J23101', 'http://sbolstandard.org/testfiles/J23105': 'http://parts.igem.org/J23105', 'http://sbolstandard.org/testfiles/K592100': 'http://parts.igem.org/K592100', 'http://sbolstandard.org/testfiles/mCerulean3': 'https://www.ncbi.nlm.nih.gov/nuccore/ATP07149_u46_1', 'http://sbolstandard.org/testfiles/E0040': 'http://parts.igem.org/E0040', 'http://sbolstandard.org/testfiles/E1010': 'http://parts.igem.org/E1010', 'http://sbolstandard.org/testfiles/J06504': 'http://parts.igem.org/J06504', 'http://sbolstandard.org/testfiles/R0040': 'http://parts.igem.org/R0040', 'http://sbolstandard.org/testfiles/I20270': 'http://parts.igem.org/I20270', 'http://sbolstandard.org/testfiles/J364001': 'http://parts.igem.org/J364001', 'http://sbolstandard.org/testfiles/J364002': 'http://parts.igem.org/J364002', 'http://sbolstandard.org/testfiles/J364007': 'http://parts.igem.org/J364007', 'http://sbolstandard.org/testfiles/J364009': 'http://parts.igem.org/J364009'}
seq_update = [f'{x}_sequence' for x in  update_dict.keys()]
print(seq_update)

g = rdflib.Graph()
g.parse(file_path_in)
for index, (subject, predicate, _object) in enumerate(g):
    if str(_object) in update_dict:
        g.remove((subject, predicate, _object))
        new = rdflib.URIRef(update_dict[str(_object)])
        g.add((subject, predicate, new))
        # print(subject, predicate, _object)
    elif str(_object) in seq_update:
        g.remove((subject, predicate, _object))
        old = str(_object)
        new = f"{update_dict[old.replace('_sequence', '')]}_sequence"
        new = rdflib.URIRef(new)
        g.add((subject, predicate, new))
        # print(subject, predicate, _object)

nt_text = g.serialize(format='nt')
lines = [line for line in nt_text.splitlines() if line]
lines.sort()

lines_type = type(lines[0])
if lines_type is bytes:
    # rdflib 5
    result =  b'\n'.join(lines) + b'\n'
elif lines_type is str:
    # rdflib 6
    result =  '\n'.join(lines) + '\n'

with open(file_path_out, 'w') as outfile:
    outfile.write(result)

# doc =sbol3.Document()
# doc.read(file_path_in)

# comp = sbol3.Component('hello', sbol3.SBO_DNA)

# print(comp._properties)