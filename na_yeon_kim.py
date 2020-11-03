from scipy import stats
from scipy.stats import t as t_dist
from scipy.stats import chi2

from abtesting_test import *

# You can comment out these lines! They are just here to help follow along to the tutorial.
print(t_dist.cdf(-2, 20)) # should print .02963
print(t_dist.cdf(2, 20)) # positive t-score (bad), should print .97036 (= 1 - .2963)

print(chi2.cdf(23.6, 12)) # prints 0.976
print(1 - chi2.cdf(23.6, 12)) # prints 1 - 0.976 = 0.023 (yay!)

# TODO: Fill in the following functions! Be sure to delete "pass" when you want to use/run a function!
# NOTE: You should not be using any outside libraries or functions other than the simple operators (+, **, etc)
# and the specifically mentioned functions (i.e. round, cdf functions...)

def slice_2D(list_2D, start_row, end_row, start_col, end_col):
    '''
    Splices a the 2D list via start_row:end_row and start_col:end_col
    :param list: list of list of numbers
    :param nums: start_row, end_row, start_col, end_col
    :return: the spliced 2D list (ending indices are exclsive)
    '''
    to_append = []
    for l in range(start_row, end_row):
        to_append.append(list_2D[l][start_col:end_col])

    return to_append

def get_avg(nums):
    '''
    Helper function for calculating the average of a sample.
    :param nums: list of numbers
    :return: average of list
    '''
    #TODO: fill me in!
    sum = 0
    for i in nums:
        sum = sum + i
    avg = sum / len(nums)
    return avg 

def get_stdev(nums):
    '''
    Helper function for calculating the standard deviation of a sample.
    :param nums: list of numbers
    :return: standard deviation of list
    '''
    #TODO: fill me in!
    mean = get_avg(nums) 
    x = 0
    y = 0
    
    for i in nums:
        x = ((i - mean) ** 2) + x 
    y = x / (len(nums)-1)
    return y ** 0.5 




def get_standard_error(a, b):
    '''
    Helper function for calculating the standard error, given two samples.
    :param a: list of numbers
    :param b: list of numbers
    :return: standard error of a and b (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    stda_squared = get_stdev(a) ** 2
    stdb_squared = get_stdev(b) ** 2

    part1 = stda_squared / len(a)
    part2 = stdb_squared / len(b)

    return (part1 + part2) ** 0.5 


def get_2_sample_df(a, b):
    '''
    Calculates the combined degrees of freedom between two samples.
    :param a: list of numbers
    :param b: list of numbers
    :return: integer representing the degrees of freedom between a and b (see studio 6 guide for this equation!)
    HINT: you can use Math.round() to help you round!
    '''
    #TODO: fill me in!
    standard_error_to_four = (get_standard_error(a, b) ** 4)
    stda_squared = get_stdev(a) ** 2
    stdb_squared = get_stdev(b) ** 2

    part1 = ((stda_squared / len(a)) ** 2) / (len(a) - 1)
    part2 = ((stdb_squared / len(b)) ** 2) / (len(b) - 1)
    part3 = part1 + part2

    return round(standard_error_to_four / part3)

def get_t_score(a, b):
    '''
    Calculates the t-score, given two samples.
    :param a: list of numbers
    :param b: list of numbers
    :return: number representing the t-score given lists a and b (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    avg_a = get_avg(a)
    avg_b = get_avg(b)
    avg_a_minus_avg_b = avg_a - avg_b
    t_score = avg_a_minus_avg_b / get_standard_error(a, b)

    if (t_score > 0):
        return t_score * -1 
    else:
        return t_score

def perform_2_sample_t_test(a, b):
    '''
    ** DO NOT CHANGE THE NAME OF THIS FUNCTION!! ** (this will mess with our autograder)
    Calculates a p-value by performing a 2-sample t-test, given two lists of numbers.
    :param a: list of numbers
    :param b: list of numbers
    :return: calculated p-value
    HINT: the t_dist.cdf() function might come in handy!
    '''
    #TODO: fill me in!
    return t_dist.cdf(get_t_score(a,b), get_2_sample_df(a, b))




# [OPTIONAL] Some helper functions that might be helpful in get_expected_grid().
# def row_sum(observed_grid, ele_row):
# def col_sum(observed_grid, ele_col):
# def total_sum(observed_grid):
# def calculate_expected(row_sum, col_sum, tot_sum):

def row_sum(observed_grid, ele_row):

    sum = 0

    for i in observed_grid[ele_row]:
        sum = sum + i 
    return sum 

def col_sum(observed_grid, ele_col):

    sum = 0

    for i in observed_grid:
            sum = sum + i[ele_col]
    return sum 

def total_sum(observed_grid):

    sum =0

    for i in observed_grid:
        for j in i:
            sum = sum + j
    return sum 


def get_expected_grid(observed_grid):
    '''
    Calculates the expected counts, given the observed counts.
    ** DO NOT modify the parameter, observed_grid. **
    :param observed_grid: 2D list of observed counts
    :return: 2D list of expected counts
    HINT: To clean up this calculation, consider filling in the optional helper functions below!
    '''
    #TODO: fill me in!
    num_rows = len(observed_grid)
    num_cols = len(observed_grid[0])

    expected_grid = [[0 for i in range(num_cols)] for j in range(num_rows)]

    i=0
    c=0
    for i in range(len(observed_grid)):
        for c in range(len(observed_grid[0])):
            expected_grid[i][c] = (row_sum(observed_grid, i) * col_sum(observed_grid, c)) / total_sum(observed_grid)
            c += 1
        i +=1 
    return expected_grid






def df_chi2(observed_grid):
    '''
    Calculates the degrees of freedom of the expected counts.
    :param observed_grid: 2D list of observed counts
    :return: degrees of freedom of expected counts (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    num_rows = len(observed_grid) 
    num_cols = len(observed_grid[0]) 

    return (num_rows - 1) * (num_cols - 1)


    

def chi2_value(observed_grid):
    '''
    Calculates the chi^2 value of the expected counts.
    :param observed_grid: 2D list of observed counts
    :return: associated chi^2 value of expected counts (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    expected_grid = get_expected_grid(observed_grid)
    chi2_value = 0

    for i in range(len(observed_grid)):
        for c in range(len(observed_grid[0])): 
            chi2_value = chi2_value + (((observed_grid[i][c] - expected_grid[i][c]) ** 2) / expected_grid[i][c])
            c +=1
        i +=1
    return chi2_value







def perform_chi2_homogeneity_test(observed_grid):
    '''
    ** DO NOT CHANGE THE NAME OF THIS FUNCTION!! ** (this will mess with our autograder)
    Calculates the p-value by performing a chi^2 test, given a list of observed counts
    :param observed_grid: 2D list of observed counts
    :return: calculated p-value
    HINT: the chi2.cdf() function might come in handy!
    '''
    #TODO: fill me in!
    return 1- chi2.cdf(chi2_value(observed_grid), df_chi2(observed_grid))

# These commented out lines are for testing your main functions. 
# Please uncomment them when finished with your implementation and confirm you get the same values :)
def data_to_num_list(s):
  '''
    Takes a copy and pasted row/col from a spreadsheet and produces a usable list of nums. 
    This will be useful when you need to run your tests on your cleaned log data!
    :param str: string holding data
    :return: the spliced list of numbers
    '''
  return list(map(float, s.split()))


# t_test 1:
a_t1_list = data_to_num_list(a1) 
b_t1_list = data_to_num_list(b1)
print(get_t_score(a_t1_list, b_t1_list)) # this should be -129.500
print(perform_2_sample_t_test(a_t1_list, b_t1_list)) # this should be 0.0000
# why do you think this is? Take a peek at a1 and b1 in abtesting_test.py :)



# t_test 2:
a_t2_list = data_to_num_list(a2) 
b_t2_list = data_to_num_list(b2)
print(get_t_score(a_t2_list, b_t2_list)) # this should be -1.48834
print(perform_2_sample_t_test(a_t2_list, b_t2_list)) # this should be .082379


# t_test 3:
a_t3_list = data_to_num_list(a3) 
b_t3_list = data_to_num_list(b3)
print(get_t_score(a_t3_list, b_t3_list)) # this should be -2.88969
print(perform_2_sample_t_test(a_t3_list, b_t3_list)) # this should be .005091


# chi2_test 1:
a_c1_list = data_to_num_list(a_count_1) 
b_c1_list = data_to_num_list(b_count_1)
c1_observed_grid = [a_c1_list, b_c1_list]
print(chi2_value(c1_observed_grid)) # this should be 4.103536
print(perform_chi2_homogeneity_test(c1_observed_grid)) # this should be .0427939

# chi2_test 2:
a_c2_list = data_to_num_list(a_count_2) 
b_c2_list = data_to_num_list(b_count_2)
c2_observed_grid = [a_c2_list, b_c2_list]
print(chi2_value(c2_observed_grid)) # this should be 33.86444
print(perform_chi2_homogeneity_test(c2_observed_grid)) # this should be 0.0000
# Again, why do you think this is? Take a peek at a_count_2 and b_count_2 in abtesting_test.py :)

# chi2_test 3:
a_c3_list = data_to_num_list(a_count_3) 
b_c3_list = data_to_num_list(b_count_3)
c3_observed_grid = [a_c3_list, b_c3_list]
print(chi2_value(c3_observed_grid)) # this should be .3119402
print(perform_chi2_homogeneity_test(c3_observed_grid)) # this should be .57649202





#mytests

#t_test for the time completion 
a_t_list = data_to_num_list(mya) 
b_t_list = data_to_num_list(myb)
print(get_t_score(a_t_list, b_t_list)) 
print(perform_2_sample_t_test(a_t_list, b_t_list)) 


# t_test for return rate 
my_a_list = data_to_num_list(my_a_count) 
my_b_list = data_to_num_list(my_b_count)
c_observed_grid = [my_a_list, my_b_list]
print(chi2_value(c_observed_grid)) 
print(perform_chi2_homogeneity_test(c_observed_grid)) 


 



