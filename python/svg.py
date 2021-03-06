##################################################
# svg.py
#
##################################################

import os

# Transforms a proof in graphviz format to 
# SVG well formed XML format that can be
# embed to xhtml pages.
def parseToSVG(proof):
	generate_image(proof)
	svg = open_svg()
	
	return svg

# Help function. Calls the graphviz dot
# tool to generate the svg representation
# of a proof in graphviz format.
def generate_image(proof):
	dot = open("proof.dot", "w" )
	dot.write(proof)
	dot.close()
	
	cmd = "dot -Tsvg proof.dot -o proof.svg"
	
	os.system(cmd)
	
# Treats the svg representation of a proof
# generated by graphviz in way that it can 
# be embed to xhtml pages.
def open_svg():
    remove_header = True
    svg_str = ""
	
    svg_file = open("proof.svg", "r")

    while True:  
        line = svg_file.readline()
        if not line:
            break
		
        svg_str = svg_str + " " + line
        if remove_header == True:
            if svg_str[1:5] != "<svg":
                svg_str = ""
            else:
                remove_header = False
	
    svg_file.close()

    return svg_str
