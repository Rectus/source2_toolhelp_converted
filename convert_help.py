# Converts old Source 2 tool help files into localization files.

import fileinput
import re

match_val = r"(?<!\\)([\"])(?:[^\"\\]+|\\.)*\1"

schema = "<!-- schema text {7e125a45-3d83-4043-b292-9e24f8ef27b4} generic {198980d8-3a93-4919-b4c6-dd1fb07a3a4b} -->"

header = '''"lang" 
{ 
	"Language" "English" 
	"Tokens" 
	{	
'''
footer = '''	}
}
'''

def reformat_val(input):
	return input[1:-1].replace('\\"', "''").replace("\\n", "\n").replace("\\t", "\t").replace("\\'", "\'")

with fileinput.input() as file:
	key = ""
	outfile = None

	for line in file:
		if file.isfirstline():

			# Finish previous file
			if outfile:
				outfile.write(footer)
				outfile.close()
				print("Converted: " + file.filename() + "\n")
				key = ""

			if not file.filename().endswith("_help.txt"):
				print("Invalid filename: " + file.filename() + "\n")
				continue

			if not schema in line:
				print("Invalid file header: " + file.filename() + "\n")
				continue

			outname = "toolhelp_" + file.filename()[0:-9] + "_english.txt"
			outfile = open(outname, mode ='x', encoding = "utf-8")
			if not outfile:
				print("Failed to create file: " + outname + "\n")
				continue

			outfile.write(header)

		elif "string m_Id" in line:
			val = re.search(match_val, line)
			if not val:
				print("Invalid key: " + file.filename() + ", line " + file.lineno() + "\n")
				outfile.close()
				continue

			key = val.group(0)[1:-1]
			outfile.write('\n')

		elif "string m_FriendlyName" in line:
			val = re.search(match_val, line)
			if val:
				outfile.write('\t\t"' + key + '" "' + reformat_val(val.group(0)) + '"\n')

			else:
				outfile.write('\t\t"' + key + '" ""\n')

		elif "string m_TooltipOverride" in line:
			val = re.search(match_val, line)
			if val:
				outfile.write('\t\t"' + key + ':shorthelp" "' + reformat_val(val.group(0)) + '"\n')

			else:
				outfile.write('\t\t"' + key + ':shorthelp" ""\n')

		elif "string m_HelpText" in line:
			val = re.search(match_val, line)
			if val:
				outfile.write('\t\t"' + key + ':help" "' + reformat_val(val.group(0)) + '"\n')

			else:
				outfile.write('\t\t"' + key + ':help" ""\n')

	outfile.write(footer)
	outfile.close()
	print("Converted: " + file.filename() + "\n")