"""CSC148 Assignment 1

=== CSC148 Winter 2023 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Misha Schwartz, Mario Badr, Christine Murad, Diane Horton,
Sophia Huynh, Jaisie Sin, Tom Ginsberg, Jonathan Calver, and Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2023 Misha Schwartz, Mario Badr, Diane Horton, Sophia Huynh,
Jonathan Calver, and Jacqueline Smith

=== Module Description ===

This file contains classes that define different algorithms for grouping
students according to chosen criteria and the group members' answers to survey
questions. This file also contains a class that describes a group of students
as well as one that describes a grouping (a collection of groups).
"""
from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING, Any
from course import sort_students

if TYPE_CHECKING:
    from survey import Survey
    from course import Course, Student


# Provided helper
def slice_list(lst: list[Any], n: int) -> list[list[Any]]:
    """Return a list containing slices of <lst> in order. Each slice is a
    list of size <n> containing the next <n> elements in <lst>.

    The last slice may contain fewer than <n> elements in order to make sure
    that the returned list contains all elements in <lst>.

    Note: Here is a less efficient implementation of this function:
        slices = []
        for i in range(0, len(lst), n):
            slices.append(lst[i:i + n])
        return slices

    Preconditions:
        - n <= len(lst)

    >>> slice_list([3, 4, 6, 2, 3], 2) == [[3, 4], [6, 2], [3]]
    True
    >>> slice_list(['a', 1, 6.0, False], 3) == [['a', 1, 6.0], [False]]
    True
    """
    return [lst[i:i + n] for i in range(0, len(lst), n)]


# Provided helper
def find_best_addition_to_group(survey: Survey, members: list[Student],
                                non_members: list[Student]) -> Student:
    """Find the best student in <non_members> to add to the group <members>,
    i.e., the student that increases the group's score the most (or decreases
    it the least).

    Preconditions:
        - len(non_members) > 0
    """
    best_score = float('-inf')
    best_student = None
    for student in non_members:
        score = survey.score_students(members + [student])
        if score > best_score:
            best_score = score
            best_student = student
    return best_student


# Provided helper
def random_swap(lst: list[list[Any]], seed: int = 0) -> None:
    """Swap two random elements from distinct sublists of <lst>.

    Uses a random seed <seed> to allow for repeatable results.
    Note: This function mutates <lst>

    Preconditions:
        - len(lst) >= 2
        - each sub list has length >= 1

    >>> l = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    >>> random_swap(l, seed=0)
    >>> l # The 4 and the 8 have swapped positions
    [[1, 2, 3], [8, 5, 6], [7, 4, 9]]
    >>> random_swap(l, seed=0)
    >>> # Now we use the same seed again, so the positions where swapping
    >>> # occurs are the same as before, and we end up with the original list.
    >>> l
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    >>> for i in range(20):
    ...     random_swap(l, seed=i)
    >>> l # After many swaps the order will be random
    [[7, 2, 8], [1, 5, 4], [3, 9, 6]]
    """
    rnd = random.Random(seed)
    rng = range(len(lst))
    # find two distinct sub lists
    l_1, l_2 = rnd.sample(rng, 2)
    # find an element in each sub list
    i_1 = rnd.randint(0, len(lst[l_1]) - 1)
    i_2 = rnd.randint(0, len(lst[l_2]) - 1)
    # swap the elements
    lst[l_1][i_1], lst[l_2][i_2] = lst[l_2][i_2], lst[l_1][i_1]


# Provided helper
def total_score(survey: Survey, groups: list[list[Student]]) -> float:
    """Return the total score of the grouping of students in <groups> according
    to <survey>.

    Note: This function does the same thing as the following:
            g = Grouping()
            for group in groups:
                g.add_group(Group(group))
            return survey.score_grouping(g)

    Preconditions:
        - len(groups) > 0
    """
    return sum(survey.score_students(group) for group in groups) / len(groups)


# Provided helper
def accept(old_score: float, new_score: float, temperature: float, seed: int
           ) -> bool:
    """If <new_score> is at least as high as <old_score>, return True.
    Otherwise, return True with probability
        exp((<new_score> - <old_score>) / <temperature>)
    unless <temperature> is 0, in which case, return False.
    """
    diff = new_score - old_score

    if diff >= 0:
        return True
    elif temperature == 0:
        return False

    rnd = random.Random(seed)
    return rnd.random() < math.exp(diff / temperature)


class Group:
    """A group of one or more students

    === Private Attributes ===
    _members: a list of unique students in this group

    === Representation Invariants ===
    There is at least one member in this group
    No two students in _members have the same id
    """
    _members: list[Student]

    def __init__(self, members: list[Student]) -> None:
        """Initialize a group with members <members>

        If <members> contains the same student object more than once, include
        that student in the group just once.

        Preconditions:
            - len(members) >= 1
        """
        # implement this method!
        # create an empty member list first
        # set has no order
        self._members = []
        for i in members:
            if i not in self._members:
                self._members.append(i)

    def __len__(self) -> int:
        """Return the number of members in this group """
        # implement this method!
        count = 0
        for _ in self._members:
            count += 1
        return count

    def __contains__(self, member: Student) -> bool:
        """Return True iff this group contains a member with the same id
        as <member>.
        """
        # implement this method!
        for _ in self._members:
            if _.id == member.id:
                return True
        return False

    def __str__(self) -> str:
        """Return a string containing the names of all members in this group
        on a single line.

        You can choose the precise format of this string.
        """
        # implement this method!
        name_lst = [member.name for member in self._members]
        return ' * '.join(name_lst)

    def get_members(self) -> list[Student]:
        """Return a list of members in this group.

        This list should be a shallow copy of the self._members attribute.
        See the handout for more information about what a shallow copy is.
        """
        # implement this method! prevent aliasing
        return self._members[:]


class Grouping:
    """A collection of groups

    === Private Attributes ===
    _groups: a list of Groups

    === Representation Invariants ===
    No group in _groups contains zero members
    No student appears in more than one group in _groups
    """
    _groups: list[Group]

    def __init__(self) -> None:
        """Initialize a Grouping that contains zero groups. """
        # implement this method!
        self._groups = []

    def __len__(self) -> int:
        """Return the number of groups in this grouping """
        # implement this method!
        count = 0
        for _ in self._groups:
            count += 1
        return count

    def __str__(self) -> str:
        """Return a multi-line string that includes the names of all the
        members of all the groups in <self>. Each line should contain the names
        of members for a single group.

        You can choose the precise format of this string.
        """
        # implement this method!
        result = [f'{group}' for group in self._groups]
        return '\n'.join(result)

    def add_group(self, group: Group) -> bool:
        """Add <group> to this grouping and return True iff the addition does
        not violate a representation invariant; otherwise leave this grouping
        unchanged and return False.
        """
        # implement this method!
        check_not_zero_member = True
        if len(group.get_members()) == 0:
            check_not_zero_member = False

        check_student_appear_once = False
        temp = []
        for g in self._groups:
            temp += g.get_members()
        temp += group.get_members()
        temp_set = set(temp)
        if len(temp_set) == len(temp):
            check_student_appear_once = True

        if check_student_appear_once and check_not_zero_member:
            self._groups.append(group)
            return True
        else:
            return False

    def get_groups(self) -> list[Group]:
        """Return a list of all groups in this grouping.

        This list should be a shallow copy of the self._groups attribute.
        See the handout for more information about what a shallow copy is.
        """
        # implement this method!
        return self._groups[:]


class Grouper:
    """An abstract class representing a grouper used to create a grouping of
    students according to their answers to a survey.

    === Public Attributes ===
    group_size: the ideal number of students that should be in each group
        This group size will never be exceeded by a grouper, but if the class
        doesn't divide evenly into groups, there may be one group that is
        smaller than group_size.

    === Representation Invariants ===
    group_size > 1
    """
    group_size: int

    def __init__(self, group_size: int) -> None:
        """Initialize this grouper that creates groups of size <group_size>

        Preconditions:
            - group_size > 1
        """
        self.group_size = group_size

    def make_grouping(self, course: Course, survey: Survey) -> Grouping:
        """Return a grouping for all students in <course> using the questions
        in <survey> to create the grouping.
        """
        raise NotImplementedError


class AlphaGrouper(Grouper):
    """A grouper that groups students in a given course according to the
    alphabetical order of their names.

    === Public Attributes ===
    group_size: the ideal number of students that should be in each group
        This group size will never be exceeded by a grouper, but if the class
        doesn't divide evenly into groups, there may be one group that is
        smaller than group_size.

    === Representation Invariants ===
    group_size > 1
    """

    group_size: int

    def make_grouping(self, course: Course, survey: Survey) -> Grouping:
        """Return a grouping for all students in <course>.

        The first group should contain the students in <course> whose names come
        first when sorted alphabetically, the second group should contain the
        next students in that order, etc.

        All groups in this grouping should have exactly self.group_size members
        except for the last group which may have fewer than self.group_size
        members if that is required to make sure all students in <course> are
        members of a group.

        Hint: the sort_students function might be useful

        Preconditions:
            - <course> has more students than this Grouper's group_size
        """
        # implement this method!
        student_list = sort_students(course.students, 'name')
        result = Grouping()
        student_slice = slice_list(student_list, self.group_size)
        for sublist in student_slice:
            group = Group(sublist)
            result.add_group(group)
        return result


class GreedyGrouper(Grouper):
    """A grouper used to create a grouping of students according to their
    answers to a survey. This grouper uses a greedy algorithm to create
    groups.

    === Public Attributes ===
    group_size: the ideal number of students that should be in each group
        This group size will never be exceeded by a grouper, but if the class
        doesn't divide evenly into groups, there may be one group that is
        smaller than group_size.

    === Representation Invariants ===
    group_size > 1
    """
    group_size: int

    def _group_students(self, survey: Survey, students: list[Student]) \
            -> list[Group]:
        """Return a list of greedy group based on survey and students.
        Precondition: students are already sorted by student id.
        """
        if len(students) < self.group_size:
            return [Group(students)]
        else:
            member = [students[0]]
            non_member = students[1:]
            while len(member) < self.group_size:
                best = find_best_addition_to_group(survey, member, non_member)
                non_member.remove(best)
                member.append(best)
            return [Group(member)] + self._group_students(survey, non_member)

    def make_grouping(self, course: Course, survey: Survey) -> Grouping:
        """Return a grouping for all students in <course>.

        Starting with a list of all students in <course> obtained by calling
        the <course>.get_students() method, create groups of students using the
        following algorithm:

        1. Select the first student in the list that hasn't already been put
           into a group and put this student in a new group.
        2. Select a student in the list that hasn't already been put into a
           group that, if added to the new group, would increase the group's
           score the most (or reduce it the least). Add that student to the new
           group.
        3. Repeat step 2 until there are N students in the new group where N is
           equal to self.group_size.
        4. Repeat steps 1-3 until all students have been placed in a group.

        In step 2 above, use the <survey>.score_students method to determine
        the score of each group of students.

        The final group created may have fewer than N members if that is
        required to make sure all students in <course> are members of a group.

        Preconditions:
            - <course> has more students than this Grouper's group_size
        """
        # implement this method!
        student_list = list(course.get_students())
        result = Grouping()
        group_lst = self._group_students(survey, student_list)
        for group in group_lst:
            result.add_group(group)
        return result


class SimulatedAnnealingGrouper(Grouper):
    """A grouper used to create a grouping of students according to their
    answers to a survey. This grouper uses a simulated annealing algorithm to
    create groups.

    === Public Attributes ===
    group_size: the ideal number of students that should be in each group
        This group size will never be exceeded by a grouper, but if the class
        doesn't divide evenly into groups, there may be one group that is
        smaller than group_size.

    === Private Attributes ===
    _total_iterations: number of iterations that this algorithm takes.
    _initial_temp: the initial temperature of the simulation.

    === Representation Invariants ===
    group_size > 1
    _total_iterations > 1
    _initial_temp > 0.0
    """
    group_size: int
    _total_iterations: int
    _initial_temp: float

    def __init__(self,
                 group_size: int,
                 iterations: int = 10 ** 4,
                 initial_temperature: float = 1) -> None:
        """Initialize this simulated annealing grouper (that runs for
        <iterations> iterations and begins with temperature
        <initial_temperature>) to create groups of size <group_size>.
        """
        # implement this method!
        Grouper.__init__(self, group_size)
        self._total_iterations = iterations
        self._initial_temp = initial_temperature

    def _get_temp(self, curr_iter: int) -> float:
        """Return the current temperature of curr_iter.

        Precondition: 0 <= curr_iter <= self._total_iterations - 1
        """
        return self._initial_temp * \
            (1 - (curr_iter / (self._total_iterations - 1)))

    def _get_best_gp(self, student_lst: list[list[Student]], survey: Survey) \
            -> list[list[Student]]:
        """Return the optimal list of student_lst on survey.
        """
        best = [group[:] for group in student_lst]
        # best = deepcopy(student_lst)
        for i in range(0, self._total_iterations):
            prev = [group[:] for group in best]
            # prev = deepcopy(best)
            prev_score = total_score(survey, prev)
            random_swap(best, i)
            curr_score = total_score(survey, best)
            if not accept(prev_score, curr_score, self._get_temp(i), i):
                best = prev
        return best

    def make_grouping(self, course: Course, survey: Survey) -> Grouping:
        """Group students in <course> using the Simulated Annealing algorithm.

        Here is the Simulated Annealing algorithm for creating a grouping.

        Throughout this description of the algorithm, we talk about groups.
        However, your code in this method should work with objects of type
        list[list[Student]], rather than of type list[Group] or type Grouping.
        This will be simpler, because a Group object cannot be changed once it
        is created, and also because we have provided important helper methods
        that work with things of type list[list[Student]]. You can create a
        Grouping of Groups only once the groups have all been decided.

        To begin:

        1. Start with a list of all students in <course> obtained by calling the
            <course>.get_students() method.
        2. Create an initial list of groups by slicing the list of students in
            groups of size <group_size> using the <slice_list> function. This
            list of groups will not be random, since neither <get_students> nor
            <slice_list> has any randomness, but it is still an acceptable
            starting point for simulated annealing.
        3. Compute the group score of those groups according to <survey>
            using the <total_score> function.

        Then, repeat the following steps for each iteration of this grouper,
        keeping track of the best list of groups you have found so far:

        1. Swap two random students between groups using the <random_swap>
            helper function with the current iteration as the seed.
        2. Compute the total score of the new list of groups.
        3. Compute the temperature based on the iteration number, as described
            in the Grouping Algorithms document.
        3. Use the <accept> function to determine if the list of groups will be
            accepted. The <accept> function always accepts the new list of
            groups if the score is better than the old one. If it is not, it is
            accepted with probability
            exp((<new_score> - <old_score>) / <temperature>). Use the current
            iteration as the seed for <accept>. If the new list of groups is
            not accepted, revert to the previous one.

        After all the iterations are complete, temperature will be very close
        to 0. (It may not equal 0 exactly, due to imprecision in floating point
        calculations; this is not a problem, it's just an inherent reality
        of working with floating point numbers.)

        Return a grouping that contains the best list of groups found.

        NOTES:
            - Iteration numbers go from 0 to (# iterations) - 1
            - Throughout the process, keep track of the best list of groups so
                far
            - To make a copy of the current list of groups (so that you can
                do a random swap and compare the old and new versions)
                use the <deepcopy> function we have imported for you.
                <deepcopy> may also help for when a swap is not accepted.

        Optional: To learn more about random seeding for repeatable results:
        https://en.wikipedia.org/wiki/Random_seed

        Preconditions:
            - <course> has more students than this Grouper's group_size
        """
        # implement this method!
        result = Grouping()
        sliced_lst = slice_list(list(course.get_students()), self.group_size)
        best_lst = self._get_best_gp(sliced_lst, survey)
        for members in best_lst:
            g = Group(members)
            result.add_group(g)
        return result


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['typing',
                                                  'random',
                                                  'survey',
                                                  'course',
                                                  'math',
                                                  'copy'],
                                'disable': ['E9992']})
