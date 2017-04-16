from munkres import Munkres, print_matrix

# matrix = [[5, 9, 1],
#           [10, 3, 2],
#           [8, 7, 4],
#           [5, 2, 4],
#           [9, 8, 4]]
matrix=[[82.0,83.0,69.0,92.0],
[77.0,37.0,49.0,92.0],
[11.0,69.0,5.0,86.0],
[8.0,9.0,98.0,23.0],
[8.0,9.0,9.0,2.0]]



m = Munkres()
indexes = m.compute(matrix)
# print_matrix(matrix, msg='Lowest cost through this matrix:')
total = 0
for row, column in indexes:
    value = matrix[row][column]
    total += value
    print '(%d, %d) -> %d' % (row, column, value)
print 'total cost: %d' % total


                #
                # if column in Physical_VM_SS_active_map: ###column referes to the Physical VM to which bin is mapped
                #     l=Physical_VM_SS_active_map[column]
                #     l.append(superstep)
                #     Physical_VM_SS_active_map[column]=l
                # else:
                #     Physical_VM_SS_active_map[column]=[superstep]
