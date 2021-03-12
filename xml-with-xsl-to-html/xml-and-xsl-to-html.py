import lxml.etree as ET
import glob

# This script was created to help my friend with his University work
# He had to display .xml data along with .xsl styling in Chrome
# But Chrome restricts using .xml with .xsl due to security concerns
# Therefore a simple workaround was to convert it to html for easier display

# It takes in the first files with .xml and .xsl extensions it can find
# Translates it into a new .html file so the .xml and .xsl content can be displayed easily in chrome
dom = ET.parse(str((glob.glob('*.xml')[0])))
xslt = ET.parse(str(glob.glob('*.xsl')[0]))
transform = ET.XSLT(xslt)
newdom = transform(dom)
output = str(newdom)
output_file = open('index.html', 'w')
with open('index.html', "w", encoding="utf-8") as f:
    f.write(output)
