# michael zaychikov
import fraud_detection as fd
import math


def test_ones_and_tens_digit_histogram():
    # Easy to calculate case: 5 numbers, clean percentages.
    actual = fd.ones_and_tens_digit_histogram([127, 426, 28, 9, 90])
    expected = [0.2, 0.0, 0.3, 0.0, 0.0, 0.0, 0.1, 0.1, 0.1, 0.2]
    for i in range(len(actual)):
        assert math.isclose(actual[i], expected[i])

    # Obscure and hard (by hand) to calculate frequencies
    input = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89,
             144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]
    actual = fd.ones_and_tens_digit_histogram(input)
    expected = [0.21428571428571427, 0.14285714285714285, 0.047619047619047616,
                0.11904761904761904, 0.09523809523809523, 0.09523809523809523,
                0.023809523809523808, 0.09523809523809523, 0.11904761904761904,
                0.047619047619047616]
    for i in range(len(actual)):
        assert math.isclose(actual[i], expected[i])


def test_calculate_mse_with_uniform(histogram):
    # test to see if mse is close to predicted output
    # assert fails if it isnt close
    # use isclose as they are float values
    vote_tally = fd.extract_election_votes(
        "election-iran-2009.csv", ["Ahmadinejad", "Rezai", "Karrubi",
                                   "Mousavi"])
    histogram = fd.ones_and_tens_digit_histogram(vote_tally)
    predicted_output = 0.000739583333333
    final_output = fd.calculate_mse_with_uniform(histogram)
    assert math.isclose(predicted_output, final_output)
    print("assert test mse uni passed")


def test_mean_squared_error(numbers_1, numbers_2):
    # test to see if the mean squared errors are close
    # to one another use isclose as it is a float
    numbers_1 = [1, 2, 3]
    numbers_2 = [5, 10, 15]
    expected_output = 74.6666666666667
    actual_output = fd.mean_squared_error(numbers_1, numbers_2)
    assert math.isclose(expected_output, actual_output)
    print("assert test mse passed")


def main():
    test_ones_and_tens_digit_histogram()
    # call other test functions here
    test_calculate_mse_with_uniform([3, 2, 1])
    test_mean_squared_error([15, 10, 2], [8, 4, 5])


if __name__ == "__main__":
    main()
