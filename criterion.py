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

This file contains classes that describe different types of criteria used to
evaluate a group of answers to a survey question.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from survey import Question, Answer


class InvalidAnswerError(Exception):
    """Error that should be raised when an answer is invalid for a given
    question.
    """


class Criterion:
    """An abstract class representing a criterion used to evaluate the quality
    of a group based on the group members' answers for a given question.
    """

    def score_answers(self, question: Question, answers: list[Answer]) -> float:
        """Return score between 0.0 and 1.0 indicating how well the group
        of <answers> to the question <question> satisfy this Criterion.

        Raise InvalidAnswerError if any answer in <answers> is not a valid
        answer to <question>.

        Each implementation of this abstract class will measure satisfaction of
        a criterion differently.
        """
        raise NotImplementedError

    def _all_valid_answers(self, question: Question,
                           answers: list[Answer]) -> bool:
        """Return true iff all answers in answers are valid answer to
        question, return False otherwise.
        """
        for answer in answers:
            if not answer.is_valid(question):
                return False
        return True


class HomogeneousCriterion(Criterion):
    # make this a child class of another class defined in this file
    """A criterion used to evaluate the quality of a group based on the group
    members' answers for a given question.

    This criterion gives a higher score to answers that are more similar.
    """

    def _get_similarity_score(self, question: Question,
                              answers: list[Answer]) -> float:
        """Return the average of similarity score of all paired
        combinations of answers in answers to question.

        Precondition: all answer in answers are valid to question.
                      len(answers) >= 1
        """
        if len(answers) == 1:
            return 1.0
        else:
            combination_lst = []
            for po1 in range(len(answers)):
                for po2 in range(po1 + 1, len(answers)):
                    answer_pair = (answers[po1], answers[po2])
                    combination_lst.append(answer_pair)
            total_similarity = sum([question.get_similarity(tup[0], tup[1])
                                    for tup in combination_lst])
            return total_similarity / len(combination_lst)

    def score_answers(self, question: Question, answers: list[Answer]) -> float:
        """Return a score between 0.0 and 1.0 indicating how similar the
        answers in <answers> are.

        This score is calculated by finding the similarity of every combination
        of two answers in <answers> and taking the average of all of these
        similarity scores.
            * Don't include a pair of answers twice while finding the
              similarity scores.  For example, don't compare answer 1 and
              answer 2, then later compare answer 2 and answer 1.
            * Don't compare an answer with itself while computing the similarity
              scores.
            * Don't do any rounding.
        If there is only one answer in <answers> and it is valid, return 1.0
        since a single answer is always identical to itself.

        Raise InvalidAnswerError if any answer in <answers> is not a valid
        answer to <question>.

        Preconditions:
            - len(answers) > 0
        """
        # implement this method or remove it (to inherit it as is)
        if not self._all_valid_answers(question, answers):
            raise InvalidAnswerError
        else:
            return self._get_similarity_score(question, answers)


class HeterogeneousCriterion(HomogeneousCriterion):
    # make this a child class of another class defined in this file
    """A criterion used to evaluate the quality of a group based on the group
    members' answers for a given question.

    This criterion gives a higher score to answers that are more different.
    """

    def score_answers(self, question: Question, answers: list[Answer]) -> float:
        """Return a score between 0.0 and 1.0 indicating how different the
        answers in <answers> are.

        This score is calculated by finding the similarity of every
        combination of two answers in <answers>, finding the average of all
        of these similarity scores, and then subtracting this average from 1.0
            * Don't include a pair of answers twice while finding the
              similarity scores.  For example, don't compare answer 1 and
              answer 2, then later compare answer 2 and answer 1.
            * Don't compare an answer with itself while computing the similarity
              scores.
            * Don't do any rounding.
        If there is only one answer in <answers> and it is valid, return 0.0
        since a single answer is never different from itself.

        Raise InvalidAnswerError if any answer in <answers> is not a valid
        answer to <question>.

        Preconditions:
            - len(answers) > 0
        """
        # implement this method or remove it (to inherit it as is)
        if not self._all_valid_answers(question, answers):
            raise InvalidAnswerError
        else:
            return 1.0 - self._get_similarity_score(question, answers)


class LonelyMemberCriterion(Criterion):
    # make this a child class of another class defined in this file
    """A criterion used to measure the quality of a group of students
    according to the group members' answers to a question.

    This criterion gives a higher score to a group if no member of the group
    gives a unique answer to a question, that is, an answer that no other
    member gave.

    This criterion could be used, for example, to avoid putting a student into
    a group where they are the only one from their college.
    """

    def _has_unique_content(self, answers: list[Answer]) -> float:
        """Return True iff there exists answer with unique content in
        answers, return False otherwise.

        Precondition: all answer in answers are valid.
        """
        content_lst = [answer.content for answer in answers]
        for content in content_lst:
            if content_lst.count(content) == 1:
                return True
        return False

    def score_answers(self, question: Question, answers: list[Answer]) -> float:
        """Return score between 0.0 and 1.0 indicating the quality of the group
        of <answers> to the question <question>.

        The score returned will be 0.0 iff there are any unique answers in
        <answers> and will be 1.0 otherwise. An answer is unique if there is
        no other answer in <answers> with identical content. If there is only
        one answer in <answers> and it is valid, return 0.0 since the student
        with that answer is by definition the only one with that answer in the
        group.

        Raise InvalidAnswerError if any answer in <answers> is not a valid
        answer to <question>.

        Preconditions:
            - len(answers) > 0
        """
        # implement this method or remove it (to inherit it as is)
        if not self._all_valid_answers(question, answers):
            raise InvalidAnswerError
        else:
            if self._has_unique_content(answers):
                return 0.0
            else:
                return 1.0


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['typing',
                                                  'survey',
                                                  'E9992'],
                                'disable': ['E9992']})
