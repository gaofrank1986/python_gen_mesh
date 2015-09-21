import numpy as np
import math

path2 = "./bb.txt"
path3 = "./bb_body.txt"
path4 = "./bb_sf.txt"

elem_dict = {}
# no intention to have elem_dict_re,since node list order is permutable
node_dict = {}
node_dict_re = {}
face_dict = {}
face_dict_re = {}
elem_face_rl = {}

acc_line = 0
digit_precision = 4
next_avail_nodeID = 1
next_face_id = 1
next_empty_node_id = 1
next_empty_elem_id = 1
renumber_dict = {}

print "======================================================================="
print "Attention!!!Please revise the line number in for loop before running!!!"
print "======================================================================="
for line in open(path2):
	tmp = line.split()
	acc_line += 1
	nodeXYZ=[0,0,0]
	if acc_line <= 152:  # this need to be updated
		for j in range(3):
			nodeXYZ[j] = round(float(tmp[j+1]),digit_precision)
			
		node_dict[next_empty_node_id] = nodeXYZ
		node_dict_re[(nodeXYZ[0],nodeXYZ[1],nodeXYZ[2])] = next_empty_node_id
		
		# didn't check coincident nodes
		renumber_dict[int(tmp[0])] = next_empty_node_id
		next_empty_node_id += 1

	else:
		tmp_elem = [0,0,0,0]
		for i in range(4):
			tmp_elem[i] = renumber_dict[int(tmp[i+2])]
		elem_dict[next_empty_elem_id] = [i for i in tmp_elem]
		next_empty_elem_id += 1

print "======================================================================="
print "Model file reading finished,Renumbering applied for node!!!"
print "node pos rouned to precision digit given"
print "Element ID renumbering applied"
print "======================================================================="



print "element dictionary"
print elem_dict
print "reverse node dictionary"
# print node_dict_re
# print "node dictionary"
print node_dict



surface_elem_set = set()
for i_elem in elem_dict:
	is_surface_elem = True
	for i in range(4):
		#print i
		#print elem_dict[i_elem][i]
		#print node_dict[elem_dict[i_elem][i]][2]
		#print "================="
		if (abs(node_dict[elem_dict[i_elem][i]][2]) > 1e-5):
			is_surface_elem = False
	if(is_surface_elem):
		surface_elem_set.add(i_elem)
	# if i_elem > 5:
	# 	break

print "===========surface_elem_set====================="
print surface_elem_set

surface_node_set = set()
for i_node in node_dict:
	if (abs(node_dict[i_node][2]) < 1e-5):
		surface_node_set.add(i_node)

print "=======surface_node_set========================="
print surface_node_set
print "number of node is",len(surface_node_set)

print "======================================================================="
print "Generated surface elem set,surface node set!!!"
print "======================================================================="

body_elem_set = set(range(1,len(elem_dict)+1)) - surface_elem_set
body_node_set = set()
print "===========body elem set====================="
print body_elem_set
print "number of body elem is",len(body_elem_set)


for i_elem in body_elem_set:
	for j in range(4):
		body_node_set.add(elem_dict[i_elem][j])
		
print "===========body node set====================="
print body_node_set
print "======================================================================="
print "Generated body elem set!!!"
print "======================================================================="



f = open(path3,"w")
# f.write('{0:<5d}'.format(len(surface_elem_set)) + '{0:<5d}\n'.format(len(surface_node_set)))
# acc_sf_elem = 1
str1 = ''
for i_node in body_node_set:
	str1 = '{0:>5d}   '.format(i_node)
	for j in range(3):
		str1 += '{0:<9.6f}  '.format(node_dict[i_node][j])
	f.write(str1+'\n')

str1 = ''
for i_elem in body_elem_set:
	str1 = '{0:>5d}   '.format(i_elem)
	for j in range(4):
		str1 += '{0:<5d}  '.format(elem_dict[i_elem][j])
	f.write(str1+'\n')
f.close()
# =============================================================
f = open(path4,"w")
# f.write('{0:<5d}'.format(len(surface_elem_set)) + '{0:<5d}\n'.format(len(surface_node_set)))
# acc_sf_elem = 1
str1 = ''
for i_node in surface_node_set:
	str1 = '{0:>5d}    '.format(i_node)
	for j in range(3):
		str1 += '{0:<9.6f}  '.format(node_dict[i_node][j])
	f.write(str1+'\n')

str1 = ''
for i_elem in surface_elem_set:
	str1 = '{0:>5d}   '.format(i_elem)
	for j in range(4):
		str1 += '{0:<5d}  '.format(elem_dict[i_elem][j])
	f.write(str1+'\n')
f.close()