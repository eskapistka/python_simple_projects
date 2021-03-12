import xlsxwriter
from xlsxwriter.utility import xl_range, xl_rowcol_to_cell

# This script is supposed to help my friend who is a teacher in creating
# Excel spreadsheet reports about mock exams in her school in a specific format
# It takes in a number of student, names for columns (elements) that is a category
# such as "reading comprehension" or "writing" and a number of exercises inside this category
# It also produces a summary table including the overall student's score
# and student's score for every column (element)


# List of lists for columns in form [col_title, ex_num]
column_data = []

def ask_for_input():
    # "Name of the file .xlsx to create"
    print('Jak ma nazywać się plik (z rozszerzeniem .xlsx)?:')
    file_name = input()

    # 'Number of students'
    print('Ilu uczniów powinno znaleźć się w tabeli?:')
    # It has to be a number, validating input
    try:
        student_num = int(input())
    except:
        # 'It's not a number. The programme has ended it's execution. Try again.'
        print('Nie została podana liczba. Program zakończył swoje działanie. Proszę spróbować ponownie.')
        exit(0)

    # 'The programme asks for column (element) names and number of exercises inside of it'
    print('Program pyta o kolejne nazwy kolumn (elementów) i liczbę zadań na dany element.')
    # 'Enter 0 to stop the programme from asking for column values'
    print('Proszę wpisać 0 (zero) w miejsce tytułu kolumny albo liczby zadań, aby program przestał pytać o kolejne kolumny')
    while 1:
        # 'Title of column (element)'
        print('Jak powinna nazywać się kolumna (element)?:')
        col_title = input()
        if col_title == '0':
            break

        # 'Number of exercises inside the column'
        print('Ile zadań przypada na tę kolumnę?:')
        # It has to be a number, validating input
        try:
            ex_num = int(input())
        except:
            # 'It's not a number. The programme has ended it's execution. Try again.'
            print('Nie została podana liczba. Program zakończył swoje działanie. Proszę spróbować ponownie.')
            exit(0)
        if ex_num == 0:
            break
        # Append the data to an external list
        column_data.append([col_title, ex_num])
    return student_num, file_name

def write_first_col(col):
    # Set the width of the first column
    worksheet.set_column(col, col, 15)

    # Write 'student name'
    worksheet.write(1, 0, 'Uczeń')
    temp_row = 2

    temp_row = student_num + 2
    # 'Maximum number of points for this exercise'
    worksheet.write(temp_row, col, 'Max pkt za zad')
    # 'Mode'
    worksheet.write(temp_row + 1, col, 'Dominanta')
    # 'Average score'
    worksheet.write(temp_row + 2, col, 'Śr. pkt')
    # 'Median'
    worksheet.write(temp_row + 3, col, 'Mediana')
    # 'Average exercise score in percentage'
    worksheet.write(temp_row + 4, col, 'Śr. zadania')
    # 'Average column (element) score'
    worksheet.write(temp_row + 5, col, 'Śr. elementu')
    col += 1

    return col

def create_table(title, ex_num, col):
    # Check if I'm not merging a single cell
    if col != col + ex_num - 1:
        worksheet.merge_range(xl_range(0, col, 0, col+ex_num-1), title, merge_format)
    else:
        worksheet.write(0, col, title)
    temp_col = col
    temp_row = student_num + 2

    # Go through every column (exercise) in that element column
    for i in range(ex_num):
        # 'Exercise number'
        worksheet.write(1, temp_col, 'zad n')
        temp_range = xl_range(2, temp_col, student_num+1, temp_col)
        temp_max_p = xl_range(temp_row, temp_col, student_num + 2, temp_col)
        worksheet.write(temp_row + 1, temp_col, '=MODE('+temp_range+')')
        worksheet.write(temp_row + 2, temp_col, '=AVERAGE('+temp_range+')')
        worksheet.write(temp_row + 3, temp_col, '=MEDIAN('+temp_range+')')
        worksheet.write(temp_row + 4, temp_col, '=SUM('+temp_range+')/'+str(student_num)+'/'+ temp_max_p, merge_per_format)
        temp_col += 1

    # Check if I'm not merging a single cell
    if col != col + ex_num - 1:
        el_avg_range = xl_range(temp_row+5, col, temp_row+5, col + ex_num - 1)
        el_avg_data_range = xl_range(temp_row+4, col, temp_row+4, col + ex_num - 1)
        worksheet.merge_range(el_avg_range, '=AVERAGE('+el_avg_data_range+')', merge_per_format)
    else:
        worksheet.write(temp_row + 5, col,'=AVERAGE('+xl_rowcol_to_cell(temp_row+4, col)+')', merge_per_format)

    col += ex_num
    return col

def create_summary_table(col):
    # 'Points'
    worksheet.write(1, col, 'Punkty')
    # Column with student's score in points
    temp_row = 2
    # This also calculates the max point num
    for i in range(student_num+1):
        temp_range_row = xl_range(temp_row, 1, temp_row, col-1)
        worksheet.write(temp_row, col, '=SUM(' + temp_range_row + ')')
        temp_row += 1
    temp_row = student_num + 2
    temp_range_col = xl_range(2, col, student_num + 1, col)
    worksheet.write(temp_row + 2, col, '=AVERAGE(' + temp_range_col + ')')

    # Column with student's score in %
    worksheet.write(1, col + 1, '%')
    temp_row = 2
    max_p = xl_rowcol_to_cell(2 + student_num, col)
    for i in range(student_num):
        temp_range_row = xl_range(temp_row, 1, temp_row, col-1)
        worksheet.write(temp_row, col+1, '=SUM(' + temp_range_row + ')/' + max_p, merge_per_format)
        temp_row += 1
    temp_row = student_num + 2
    temp_range_col = xl_range(2, col+1, student_num + 1, col+1)
    worksheet.write(temp_row + 2, col+1, '=AVERAGE(' + temp_range_col + ')', merge_per_format)

    temp_col = col + 2

    # For every element create a table that shows a student's score in that area (element)
    temp_start_col = 1
    for t, col_n in column_data:
        worksheet.write(1, temp_col, t)
        temp_row = 2
        temp_end_col = temp_start_col + col_n - 1
        max_p_range = xl_range(2 + student_num, temp_start_col, 2 + student_num, temp_end_col)

        # Get the average of every student
        for i in range(student_num):
            temp_range_row = xl_range(temp_row, temp_start_col, temp_row, temp_end_col)
            worksheet.write(temp_row, temp_col, '=SUM(' + temp_range_row + ')/' + 'SUM(' + max_p_range + ')', merge_per_format)
            temp_row += 1

        temp_row = student_num + 2
        temp_range_col = xl_range(2, temp_col, student_num + 1, temp_col)
        worksheet.write(temp_row+5, temp_col, '=AVERAGE('+ temp_range_col +')', merge_per_format)
        temp_col += 1

        temp_start_col += col_n

    return col

# Main programme

# Ask user for input and get the number of students and name of the file to save into
student_num, file_name = ask_for_input()

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook(file_name + '.xlsx')
worksheet = workbook.add_worksheet()

# Formatting for merging cells and showing percentages
merge_format = workbook.add_format({'align': 'center'})
merge_per_format = workbook.add_format({'align': 'center', 'num_format': '0%'})
percentage_format = workbook.add_format({'num_format': '0%'})

# Start from the first column. Rows and columns are zero indexed.
col = 0

# Write into the first column
col = write_first_col(col)

# Creating tables (elements)
for title, c in column_data:
    col = create_table(title, c, col)

# Create summary table
col = create_summary_table(col)

# Close workbook after writing into it
workbook.close()
