

from urllib.parse import quote

link = "https://ebugs.synbiohub.org/public/EBUGSCollection/araC_cidar+PC439195/1/sbol"
encoded_link = quote(link)
print(encoded_link)