import utils  # noqa: F401, do not remove if using a Mac
# add your imports BELOW this line
import matplotlib.pyplot as plt
# import matplotlib as plt
import csv
import random


def ones_and_tens_digit_histogram(numbers):
    '''
    Input:
        a list of numbers.
    Returns:
        a list where the value at index i is the frequency in which digit i
        appeared in the ones place OR the tens place in the input list. This
        returned list will always have 10 numbers (representing the frequency
        of digits 0 - 9).

    For example, given the input list
        [127, 426, 28, 9, 90]
    This function will return
        [0.2, 0.0, 0.3, 0.0, 0.0, 0.0, 0.1, 0.1, 0.1, 0.2]

    That is, the digit 0 occurred in 20% of the one and tens places; 2 in 30%
    of them; 6, 7, and 8 each in 10% of the ones and tens, and 9 occurred in
    20% of the ones and tens.

    See fraud_detection_tests.py for additional cases.
    '''
    histogram = [0] * 10

    # first fill histogram with counts
    for i in numbers:
        # 1's place
        histogram[i % 10] += 1

        # 10's place
        histogram[i // 10 % 10] += 1

    # normalize over total counts
    for i in range(len(histogram)):
        histogram[i] /= len(numbers) * 2

    return histogram


# Your Set of Functions for this assignment goes in here
def extract_election_votes(filename, column_names):
    '''
    input:
    filename and list of column names
    returns:
    a list of integers that contains the values in those columns from
    every row (the order of the integers does not matter).
    '''
    # initiliaze a list
    list_of_col_name = []
    data_file = open(filename)
    # use dict reader to read the csv file
    reader = csv.DictReader(data_file)
    for row in reader:
        for column in column_names:
            vote = row[column].replace(",", "")
            # maybe its an empty string
            list_of_col_name.append(int(vote))
    data_file.close()
    # will have integers thaat contain values in columns for every row
    return list_of_col_name


def plot_iran_least_digits_histogram(histogram):
    '''
    input: takes a histogram (as created by ones_and_tens_digit_histogram)
    returns: saves the plot to a file named iran-digits.png and returns nothing
    '''
    # inititalized list of length 10
    x = list(range(10))
    yideal = []
    # every element in the loop will create 0.1
    for i in range(1, 11):
        yideal.append(0.1)
    # necessary conventions to create the plot
    # .plot will have the lines show up
    # .label cretes axis label
    # .title is the title of the graph
    plt.plot(x, yideal, label="ideal")
    plt.plot(x, histogram, label="iran")
    plt.legend(loc='best')
    plt.xlabel("Digit")
    plt.ylabel("Frequency")
    plt.title("Distribution of the last two digits in Iranian dataset")
    # plt.show()
    plt.savefig("iran-digits.png")
    plt.clf()


def rando_gen(size_quant):
    '''
    input: takes in a size
    return: returns a list of random numbers
    '''
    # initalize storage list that will hold random values
    storage_list = []
    # list of random nums
    for i in range(size_quant + 1):
        storage_list.append(random.randint(0, 99))
    return storage_list


def plot_dist_by_sample_size():
    '''
    input: creates five diff collections (sizes 10, 50, 100, 1000 and 10,000)
    of random numbers where every element in the collection is a different
    random number x such that 0 <= x < 100
    return: saves the plot as random-digits.png and returns nothing
    '''
    # initalize list of length 10
    x = list(range(10))
    y_start = []
    # created values of 0.1
    for i in range(1, 11):
        y_start.append(0.1)
    # go through the sample values in the loop
    plt.plot(x, y_start, label="ideal")
    for size_quant in [10, 50, 100, 1000, 10000]:
        theoretical = rando_gen(size_quant)
        # indented to have all lines show up on one graph
        plugged_in = ones_and_tens_digit_histogram(theoretical)
        plt.plot(x, plugged_in, label=(str(size_quant) + " random samples"))
    # .title names graph
    # .legend will display legend in best position
    plt.xlabel("Digit")
    plt.ylabel("Frequency")
    plt.title("Distibution of the last two digits" +
              "in randomly generated samples")
    plt.legend(loc="best")
    plt.savefig("random-digits.png")
    # remember to mute plot show before submission
    # plt.show()
    plt.clf()


def mean_squared_error(numbers1, numbers2):
    '''
    input: takes two lists of numbers
    return: returns the mean squared error between the lists
    '''
    # initlaized total value
    total = 0
    for i in range(len(numbers1)):
        # calculates difference and squares it
        squared_totals = ((numbers1[i] - numbers2[i]) ** 2)
        # sum of squared totals
        total = total + squared_totals
        # finds mean squre error
        mean_square_error = total / (len(numbers1))
    # return statement for mean square error
    return mean_square_error


def calculate_mse_with_uniform(histogram):
    '''
    input: takes in histogram
    return: returns the mean squared error between the
    given histogram and the uniform distribution
    '''
    # list place holder is a list
    list_placeholder = list(0.1 for i in range(len(histogram)))
    # returns mean squared error
    return mean_squared_error(histogram, list_placeholder)


def compare_iran_mse_to_samples(iran_mse, number_of_iran_datapoints):
    '''
    input: takes in iran_mse and number_of_iran_data_points
    return: does not return anything, prints: 2009 data, mse larger,
    mse smaller, and null
    '''
    # total number of iranian data points is shown here
    number_of_iran_datapoints = len((extract_election_votes
                                     ("election-iran-2009.csv",
                                      ["Ahmadinejad", "Rezai",
                                       "Karrubi", "Mousavi"])))
    elect_votes_extracted = extract_election_votes(
        "election-iran-2009.csv", ["Ahmadinejad", "Rezai",
                                   "Karrubi", "Mousavi"])
    mean_sqr_err_iran = calculate_mse_with_uniform(
        ones_and_tens_digit_histogram(elect_votes_extracted))
    print("2009 Iranian election MSE:", iran_mse)
    initialized_smaller = 0
    initialized_larger = 0
    group_size = 10000
    # randomly generates values
    for i in range(10000):
        sample_values = rando_gen(number_of_iran_datapoints)
        user_input_vals = ones_and_tens_digit_histogram(sample_values)
        sample_mean_square_err = calculate_mse_with_uniform(user_input_vals)
        # compares size between sample and mean error
        # if sample is smaller than the mean error add to the count for smaller
        if sample_mean_square_err < mean_sqr_err_iran:
            initialized_smaller = initialized_smaller + 1
        # at this line count should be bigger therefore add count to  larger
        else:
            initialized_larger = initialized_larger + 1
    # formula for null
    null_hyp_reject_lev = initialized_larger / group_size
    # print statements that show what we are looking for
    # (mse larger, mse smaller, null rejection level)
    print("Quantity of MSEs larger than or equal" +
          " to the 2009 Iranian election MSE:",
          initialized_larger)
    # prints smaller values
    print("Quantity of MSEs smaller than the 2009 Iranian election MSE:",
          initialized_smaller)
    # prints null rejection level p
    print("2009 Iranian election null hypothesis rejection level p:",
          null_hyp_reject_lev)


# The code in this function is executed when this
# file is run as a Python program
def main():
    # Code that calls functions you have written above
    # e.g. extract_election_vote_counts() etc.
    # This code should produce the output expected from your program.

    # raise NotImplementedError("Delete this line and start writing code")
    extracted_values_elect = extract_election_votes("election-iran-2009.csv",
                                                    ["Ahmadinejad", "Rezai",
                                                     "Karrubi", "Mousavi"])
    one_and_ten_histo = ones_and_tens_digit_histogram(extracted_values_elect)
    data_length = len(extracted_values_elect)
    plot_iran_least_digits_histogram(one_and_ten_histo)
    plot_dist_by_sample_size()
    iran_mse = calculate_mse_with_uniform(one_and_ten_histo)
    compare_iran_mse_to_samples(iran_mse, data_length)


if __name__ == "__main__":
    main()
