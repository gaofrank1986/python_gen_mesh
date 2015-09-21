import numpy as np
import math

path2 = "./bb_body.txt"
path4 = "./body_mesh.txt"

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

# def read_model():
for line in open(path2):
	tmp = line.split()
	acc_line += 1
	nodeXYZ=[0,0,0]
	if acc_line <= 136:  # this need to be updated
		for j in range(3):
			nodeXYZ[j] = round(float(tmp[j+1]),digit_precision)
		# node_dict[int(tmp[0])] = nodeXYZ

		# node_dict_re[(nodeXYZ[0],nodeXYZ[1],nodeXYZ[2])] = int(tmp[0])
		node_dict[next_empty_node_id] = nodeXYZ
		node_dict_re[(nodeXYZ[0],nodeXYZ[1],nodeXYZ[2])] = next_empty_node_id
		# didn't check coincident nodes
		renumber_dict[int(tmp[0])] = next_empty_node_id
		next_empty_node_id += 1

	else:
		tmp_elem = [0,0,0,0]
		# elem_dict[int(tmp[0])] = [int(tmp[2]),int(tmp[3]),int(tmp[4]),int(tmp[5])]
		for i in range(4):
			tmp_elem[i] = renumber_dict[int(tmp[i+1])]
		elem_dict[next_empty_elem_id] = [i for i in tmp_elem]
		next_empty_elem_id += 1
	# if acc_line == 154:
	# 	break

print "element dictionary"
print elem_dict
print "reverse node dictionary"
# print node_dict_re
# print "node dictionary"
print node_dict

# def add_middle_node():
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
			middle_node = node_dict_re[(middle_nodeXYZ[0],middle_nodeXYZ[1],middle_nodeXYZ[2])]
		else :
			while(next_avail_nodeID in node_dict):
				next_avail_nodeID +=1
			middle_node = next_avail_nodeID
			node_dict[middle_node] = middle_nodeXYZ
			node_dict_re[(middle_nodeXYZ[0],middle_nodeXYZ[1],middle_nodeXYZ[2])] = middle_node			

		elem_dict[i_elem].append(middle_node)
		#maybe consider initialise elem_dict to have 8 or 9 zeros,and can manipulate here

# def swap_order():
for i_elem in elem_dict:
	tmp_swap = elem_dict[i_elem][2-1]
	elem_dict[i_elem][2-1] = elem_dict[i_elem][5-1]
	elem_dict[i_elem][5-1] = elem_dict[i_elem][3-1]
	elem_dict[i_elem][3-1] = tmp_swap
	tmp_swap = elem_dict[i_elem][4-1]
	elem_dict[i_elem][4-1] = elem_dict[i_elem][6-1]
	elem_dict[i_elem][6-1] = elem_dict[i_elem][7-1]
	elem_dict[i_elem][7-1] = tmp_swap


# print elem_dict


#                 !       4----7----3
#                 !       |         |
#                 !       8    9    6
#                 !       |         |
#                 !       1----5----2

#                 !         7     6     5

#                 !         8           4

#                 !         1     2     3

# # =====================================================================================
# print "topology analysis"
# node_topology_dict = {}
# for i_elem in elem_dict:
# 	for i_node in elem_dict[i_elem]:
# 		if (i_node in node_topology_dict):
# 			node_topology_dict[i_node].append(i_elem)
# 		else:
# 			node_topology_dict[i_node] = [i_elem]




# vetex_set = {}
# print "============================node_topology_dict==========================="
# print node_topology_dict






print "========establish elem face dict============"
for i_elem in elem_dict:
	v1 = np.array(node_dict[elem_dict[i_elem][2]]) - np.array(node_dict[elem_dict[i_elem][0]]);
	v2 = np.array(node_dict[elem_dict[i_elem][4]]) - np.array(node_dict[elem_dict[i_elem][2]]);
	v3 = np.cross(v1,v2)
	v3 = v3/math.sqrt(np.dot(v3,v3))
	v3_t = (v3[0],v3[1],v3[2])

	if (v3_t in face_dict_re):
		
		# face_dict_re[v3_t].append(next_face_id - 1)
		elem_face_rl[i_elem] = face_dict_re[v3_t]
		
	else:

		face_dict[next_face_id] = v3.tolist()
		face_dict_re[v3_t]= next_face_id
		elem_face_rl[i_elem] = next_face_id
		next_face_id += 1

# ========================================================================
normal_dict ={}
elem_norm_dict = {}
next_norm_id = 1
for i_elem in elem_dict:
	vector = [0,0,0]
	vector =  face_dict[elem_face_rl[i_elem]]
	elem_norm_dict[i_elem] =[]
	for i_norm in range(len(elem_dict[i_elem])):
		normal_dict[next_norm_id] = vector
		elem_norm_dict[i_elem].append(next_norm_id)
		next_norm_id+=1
print "========================"
print "========================"

# print normal_dict






f = open(path4,"w")
f.write('0\n') # write isys
# READ(2,*)   NELEMB, NNB, NNBD, IPOL
f.write('    '.join([' ',str((len(elem_dict))),str(len(node_dict)),str(len(normal_dict)),'1']))
f.write("\n")
f.write('1  1  0.0d0  0.0d0  0.0d0')
f.write("\n")

for i_node in node_dict:
	f.write(('{0:<5d}'.format(i_node)))
	f.write('1     ')
	f.write('    '.join('{0:<9.4f}'.format(i) for i in node_dict[i_node]))
	f.write("\n")

for i_norm in normal_dict:
	f.write(('{0:<5d}'.format(i_norm)))
	f.write('1     ')
	f.write('    '.join('{0:<9.4f}'.format(i) for i in normal_dict[i_norm]))
	f.write("\n")

for i_elem in elem_dict:
	f.write(('{0:<5d}   8\n').format(i_elem))
	#f.write(('{0:<5d}'.format(i_elem)))
	f.write('    '.join(str(i) for i in elem_dict[i_elem]))
	f.write("\n")

for i_elem in elem_dict:
	f.write(('{0:<5d}   8\n').format(i_elem))
	#f.write(('{0:<5d}'.format(i_elem)))
	f.write('    '.join(str(i) for i in elem_norm_dict[i_elem]))
	f.write("\n")

f.close()


