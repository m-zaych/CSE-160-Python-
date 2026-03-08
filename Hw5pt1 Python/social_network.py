# Name: michael zaychikov
# CSE 160
# Homework 5

import utils  # noqa: F401, do not remove if using a Mac
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter


###
#  Problem 1a
###

def get_practice_graph():
    """Builds and returns the practice graph
    """
    practice_graph = nx.Graph()
    practice_graph.add_edge("A", "B")
    practice_graph.add_edge("A", "C")
    practice_graph.add_edge("B", "C")
    # (Your code for Problem 1a goes here.)
    practice_graph.add_edge("B", "D")
    practice_graph.add_edge("C", "D")
    practice_graph.add_edge("C", "F")
    practice_graph.add_edge("D", "F")
    practice_graph.add_edge("D", "E")
    return practice_graph


def draw_practice_graph(graph):
    """Draw practice_graph to the screen.
    """
    nx.draw_networkx(graph)
    plt.show()


###
#  Problem 1b
###

def get_romeo_and_juliet_graph():
    """Builds and returns the romeo and juliet graph
    """
    rj = nx.Graph()
    # (Your code for Problem 1b goes here.)
    rj.add_edge("Nurse", "Juliet")
    rj.add_edge("Juliet", "Tybalt")
    rj.add_edge("Juliet", "Capulet")
    rj.add_edge("Tybalt", "Capulet")
    rj.add_edge("Juliet", "Romeo")
    rj.add_edge("Juliet", "Friar Laurence")
    rj.add_edge("Friar Laurence", "Romeo")
    rj.add_edge("Romeo", "Benvolio")
    rj.add_edge("Benvolio", "Montague")
    rj.add_edge("Montague", "Romeo")
    rj.add_edge("Romeo", "Mercutio")
    rj.add_edge("Montague", "Escalus")
    rj.add_edge("Escalus", "Mercutio")
    rj.add_edge("Capulet", "Escalus")
    rj.add_edge("Capulet", "Paris")
    rj.add_edge("Escalus", "Paris")
    rj.add_edge("Mercutio", "Paris")
    return rj


def draw_rj(graph):
    """Draw the rj graph to the screen and to a file.
    """
    nx.draw_networkx(graph)
    plt.savefig("romeo-and-juliet.pdf")
    plt.show()


###
#  Problem 2
###

def friends(graph, user):
    """Returns a set of the friends of the given user, in the given graph.
    """
    # This function has already been implemented for you.
    # You do not need to add any more code to this (short!) function.
    return set(graph.neighbors(user))


def friends_of_friends(graph, user):
    """Find and return the friends of friends of the given user.

    Arguments:
        graph: the graph object that contains the user and others
        user: a string

    Returns: a set containing the names of all of the friends of
    friends of the user. The set should not contain the user itself
    or their immediate friends.
    """
    friends_of_friends_set = set()
    friends_set = friends(graph, user)
    for friend in friends_set:
        fof = friends(graph, friend)
        friends_of_friends_set = friends_of_friends_set | fof
    return friends_of_friends_set - set([user]) - friends_set


def common_friends(graph, user1, user2):
    """Finds and returns the set of friends that user1 and user2 have in common

    Arguments:
        graph:  the graph object that contains the users
        user1: a string representing one user
        user2: a string representing another user

    Returns: a set containing the friends user1 and user2 have in common
    """

    friends_u1 = set()
    friends_set_u1 = friends(graph, user1)
    friends_u2 = set()
    friends_set_u2 = friends(graph, user2)
    for homies in friends_set_u1:
        fof1 = friends(graph, homies)
        friends_u1 = friends_u1 | fof1 - set([user2]) - set([user1])
    for other_homies in friends_set_u2:
        fof2 = friends(graph, other_homies)
        friends_u2 = friends_u2 | fof2 - set([user2]) - set([user1])
    shared_friends = friends_set_u1 & friends_set_u2
    return shared_friends


def number_of_common_friends_map(graph, user):
    """Returns a map (a dictionary), mapping a person to the number of friends
    that person has in common with the given user. The map keys are the
    people who have at least one friend in common with the given user,
    and are neither the given user nor one of the given user's friends.
    Example: a graph called my_graph and user "X"
    Here is what is relevant about my_graph:
        - "X" and "Y" have two friends in common
        - "X" and "Z" have one friend in common
        - "X" and "W" have one friend in common
        - "X" and "V" have no friends in common
        - "X" is friends with "W" (but not with "Y" or "Z")
    Here is what should be returned:
      number_of_common_friends_map(my_graph, "X")  =>   { 'Y':2, 'Z':1 }

    Arguments:
        graph: the graph object that contains the user and others
        user: a string

    Returns: a dictionary mapping each person to the number of (non-zero)
    friends they have in common with the user
    """

    sim_bros = {}
    for other_person in friends_of_friends(graph, user):
        sim_bros[other_person] = len(common_friends(graph, user, other_person))
    return sim_bros


def number_map_to_sorted_list(map_with_number_vals):
    """Given a dictionary, return a list of the keys in the dictionary.
    The keys are sorted by the number value they map to, from greatest
    number down to smallest number.
    When two keys map to the same number value, the keys are sorted by their
    natural sort order for whatever type the key is, from least to greatest.

    Arguments:
        map_with_number_vals: a dictionary whose values are numbers

    Returns: a list of keys, sorted by the values in map_with_number_vals
    """

    list_of_keys = []
    alpha_sort = sorted(list(map_with_number_vals.items()), key=itemgetter(0))
    sorted_list = sorted(alpha_sort, key=itemgetter(1), reverse=True)
    for i in sorted_list:
        list_of_keys.append(i[0])
    return list_of_keys


def rec_number_common_friends(graph, user):
    """
    Returns a list of friend recommendations for the user, sorted
    by number of friends in common.

    Arguments:
        graph: the graph object that contains the user and others
        user: a string

    Returns: A list of friend recommendations for the given user.
    The friend recommendation list consists of names/IDs of people in
    the graph who are not yet a friend of the given user.  The order
    of the list is determined by the number of common friends (people
    with the most common friends are listed first).  In the
    case of a tie in number of common friends, the names/IDs are
    sorted by their natural sort order, from least to greatest.
    """
    friends_list = number_of_common_friends_map(graph, user)
    advised_homies_common = number_map_to_sorted_list(friends_list)
    return advised_homies_common

###
#  Problem 3
###


def influence_map(graph, user):
    """Returns a map (a dictionary) mapping from each person to their
    influence score, with respect to the given user. The map only
    contains people who have at least one friend in common with the given
    user and are neither the user nor one of the users's friends.
    See the assignment writeup for the definition of influence scores.
    """

    influ_dictionary = {}
    solo_results = 0
    total_combined_value = 0
    for homies in number_of_common_friends_map(graph, user):
        solo_results = 0
        total_combined_value = total_combined_value + 1
        for lifeform in common_friends(graph, user, homies):
            fof = len(friends(graph, lifeform))
            solo_results = solo_results + 1/fof
        influ_dictionary[homies] = solo_results
    return influ_dictionary


def recommend_by_influence(graph, user):
    """Return a list of friend recommendations for the given user.
    The friend recommendation list consists of names/IDs of people in
    the graph who are not yet a friend of the given user.  The order
    of the list is determined by the influence score (people
    with the biggest influence score are listed first).  In the
    case of a tie in influence score, the names/IDs are sorted
    by their natural sort order, from least to greatest.
    """
    friends_list = []
    list_of_recommended = []
    friends_list = influence_map(graph, user)
    list_of_recommended = number_map_to_sorted_list(friends_list)
    return list_of_recommended


###
#  Problem 5
###

def get_facebook_graph():
    """Builds and returns the facebook graph
    """

    # (Your Problem 5 code goes here.)
    pass


def main():
    practice_graph = get_practice_graph()
    # Comment out this line after you have visually verified your practice
    # graph.
    # Otherwise, the picture will pop up every time that you run your program.
    draw_practice_graph(practice_graph)

    rj = get_romeo_and_juliet_graph()
    # Comment out this line after you have visually verified your rj graph and
    # created your PDF file.
    # Otherwise, the picture will pop up every time that you run your program.
    draw_rj(rj)

    ###
    #  Problem 4
    ###
    altered_list = []
    original_list = []
    for i in rj.nodes:
        if list(recommend_by_influence(rj, i)) \
                == list(rec_number_common_friends(rj, i)):
            original_list.append(i)
        else:
            altered_list.append(i)
    original_list_alphabetized = sorted(original_list)
    altered_list_alphabetized = sorted(altered_list)
    print("Problem 4:")

    print("Unchanged Recommendations: ", original_list_alphabetized)
    print("Changed Recommendations: ", altered_list_alphabetized)

    ###
    #  Problem 5
    ###

    # (Your Problem 5 code goes here. Make sure to call get_facebook_graph.)

    # assert len(facebook.nodes()) == 63731
    # assert len(facebook.edges()) == 817090

    ###
    #  Problem 6
    ###
    print()
    print("Problem 6:")
    print()

    # (Your Problem 6 code goes here.)

    ###
    #  Problem 7
    ###
    print()
    print("Problem 7:")
    print()

    # (Your Problem 7 code goes here.)

    ###
    #  Problem 8
    ###
    print()
    print("Problem 8:")
    print()

    # (Your Problem 8 code goes here.)


if __name__ == "__main__":
    main()


###
#  Collaboration
###

# Please write your collaboration statement below:
