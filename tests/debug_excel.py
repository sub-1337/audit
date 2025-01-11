import openpyxl

# Give the location of the file
path = "D:\\git\\audit\\data\\1kurs.xlsx"

# To open the workbook 
# workbook object is created
wb_obj = openpyxl.load_workbook(path)

# Get workbook active sheet object
# from the active attribute
sheet_obj = wb_obj.active

# Cell objects also have a row, column, 
# and coordinate attributes that provide
# location information for the cell.

# Note: The first row or 
# column integer is 1, not 0.

# Cell object is created by using 
# sheet object's cell() method.
#cell_obj = sheet_obj.cell(row = 1, column = 1)

# Print value of cell object 
# using the value attribute
#print(cell_obj.value)

#for i in range(1,20):
#    print(i, "  ", sheet_obj.cell(row =  i, column = 2).value)

None