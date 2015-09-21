import numpy as np
import math

path2 = "./bb_sf.txt"
path4 = "./surface_mesh_2.txt"

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
# renumber_dict = {}


for line in open(path2):
	tmp = line.split()
	acc_line += 1
	nodeXYZ=[0,0,0]
	if acc_line <= 36:  # this need to be updated
		for j in range(3):
			nodeXYZ[j] = round(float(tmp[j+1]),digit_precision)
		node_dict[int(tmp[0])] = nodeXYZ
	
		node_dict_re[(nodeXYZ[0],nodeXYZ[1],nodeXYZ[2])] = int(tmp[0])
		# node_dict[next_empty_node_id] = nodeXYZ
		# node_dict_re[(nodeXYZ[0],nodeXYZ[1],nodeXYZ[2])] = next_empty_node_id
		# # didn't check coincident nodes
		#renumber_dict[int(tmp[0])] = next_empty_node_id
		# next_empty_node_id += 1

	else:
		tmp_elem = [0,0,0,0]
		elem_dict[int(tmp[0])] = [int(tmp[1]),int(tmp[2]),int(tmp[3]),int(tmp[4])]
		# for i in range(4):
		# 	tmp_elem[i] = renumber_dict[int(tmp[i+2])]
		# elem_dict[next_empty_elem_id] = [i for i in tmp_elem]
		# next_empty_elem_id += 1
	# if acc_line == 154:
	# 	break

#print "element dictionary"
#print elem_dict
#print "reverse node dictionary"
# print node_dict_re
# print "node dictionary"
#print node_dict




# print "===================add middle node====================="
for i_elem in elem_dict:
	for j in range(4):
		middle_nodeXYZ=[0,0,0]
		start_node = elem_dict[i_elem][j]
		if (j == 3):
			end_node = elem_dict[i_elem][0]
		else:
			end_node = elem_dict[i_elem][j+1]

		middle_nodeXYZ[0] = round(0.5*(node_dict[start_node][0]+node_dict[end_node][0]),digit_precision)
		middle_nodeXYZ[1] = round(0.5*(node_dict[start_node][1]+node_dict[end_node][1]),digit_precision)
		middle_nodeXYZ[2] = round(0.5*(node_dict[start_node][2]+node_dict[end_node][2]),digit_precision)

		if ((middle_nodeXYZ[0],middle_nodeXYZ[1],middle_nodeXYZ[2]) in node_dict_re) :
			middle_node_id = node_dict_re[(middle_nodeXYZ[0],middle_nodeXYZ[1],middle_nodeXYZ[2])]
		else :
			while(next_avail_nodeID in node_dict):
				next_avail_nodeID +=1
			middle_node_id = next_avail_nodeID
			node_dict[middle_node] = middle_nodeXYZ
			node_dict_re[(middle_nodeXYZ[0],middle_nodeXYZ[1],middle_nodeXYZ[2])] = middle_node_id

		elem_dict[i_elem].append(middle_node_id)
		#maybe consider initialise elem_dict to have 8 or 9 zeros,and can manipulate here

print elem_dict

## swap node list order to teng's order
for i_elem in elem_dict:
	tmp_swap = elem_dict[i_elem][2-1]
	elem_dict[i_elem][2-1] = elem_dict[i_elem][5-1]
	elem_dict[i_elem][5-1] = elem_dict[i_elem][3-1]
	elem_dict[i_elem][3-1] = tmp_swap
	tmp_swap = elem_dict[i_elem][4-1]
	elem_dict[i_elem][4-1] = elem_dict[i_elem][6-1]
	elem_dict[i_elem][6-1] = elem_dict[i_elem][7-1]
	elem_dict[i_elem][7-1] = tmp_swap
# =====================================================================================


# output surface mesh
f_sf = open(path4,"w")
f_sf.write('{0:<5d}'.format(len(elem_dict)) + '{0:<5d}\n'.format(len(node_dict)))
acc_sf_elem = 1
for i_elem in elem_dict:
	str1 = ''
	str2 = ''
	for j in range(8):
		str1 += '{0:<9.6f}     '.format(node_dict[elem_dict[i_elem][j]][0])
		str2 += '{0:<9.6f}     '.format(node_dict[elem_dict[i_elem][j]][1])
	f_sf.write(('{0:<5d}   8\n').format(acc_sf_elem))
	f_sf.write(str1+'\n')
	f_sf.write(str2+'\n')
	acc_sf_elem += 1
f_sf.close()



