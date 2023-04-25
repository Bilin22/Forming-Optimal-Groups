# Forming-Optimal-Groups

## Introduction

In the field of teaching university courses, a question that has received considerable attention is this:

> **What is the best way to put students into groups?**

There are arguments for making groups heteregenous, and other arugments for making them homogeneous. What is best may depend on the kind of work, the size of the group, or what attributes we are basing the grouping on. For example, we might want groups with heterogeneous programs of study, so students bring different perspectives. Or we might want homogeneous neighbourhoods, so students from who live nearby can meet to work together in person. Or we may want a combination of these criteria. Of course, to apply criteria like these, we need the relevant information about the students (their program of study, or college, for instance). We can get that by surveying the students.

This project complete a program that analyzes an instructor’s criteria for good groups, plus data extracted from a student survey, to make groups that are optimal with respect to the criteria. 

The visualization HTML file contains a plot of the scores of the groups created by the different algorithms, as well as some simple statistics about how well they do.
![Visualization of Group Scores Stats](https://github.com/Bilin22/Forming-Optimal-Groups/blob/main/newplot.png)

## Grouping Algorithms

- **AlphaGrouper**
    - The AlphaGrouper class will group students alphabetically.
    - The groups will be sorted by the first letter of the students’ last names, and then by the first letter of their first names.
- **GreedyGrouper**
  - The GreedyGrouper class forms groups in a "greedy" manner: We first get a list of students ordered by ID. The first student who is not part of a group is placed into the first group.Afterwards, the student that would increase this group's score the most (or reduce it the least) will be added to that group, breaking ties by ID.
  - Repeat the previous step until the group reaches our intended size, finding the change in scores for the remaining students and adding the student that would increase the score the most (or decrease it the least) into the group.
- **SimulatedAnnealingGrouper**
  - The SimulatedAnnealingGrouper class forms groups using a simulated annealing algorithm. The algorithm starts with a random grouping of students, and then tries to improve the score of the groups by swapping students between groups. The algorithm will continue to swap students until it reaches a local minimum, where no more swaps can be made to improve the score of the groups.
  - The algorithm will then restart with a new random grouping of students, and repeat the process until it reaches a global minimum, where no more swaps can be made to improve the score of the groups.
  - The algorithm will then return the best grouping of students that it found.

## Acknowledgements
The starter code for this project was provided by:

University of Toronto

CSC148: Introduction to Computer Science - Winter 2023

Professor: Diane Horton
