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

This file contains a class that describes a survey as well as classes that
describe different types of questions that can be asked on a survey.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Union, Any
from criterion import InvalidAnswerError, HomogeneousCriterion

if TYPE_CHECKING:
    from criterion import Criterion
    from grouper import Grouping
    from course import Student


class Question:
    """An abstract class representing a question used in a survey

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Representation Invariants ===
    text is not the empty string
    """
    id: int
    text: str

    def __init__(self, id_: int, text: str) -> None:
        """Initialize this question with the text <text>."""
        # implement this method!
        self.id = id_
        self.text = text

    def __str__(self) -> str:
        """Return a string representation of this question that contains both
        the text of this question and a description of all possible answers
        to this question.

        You can choose the precise format of this string.
        """
        # implement this method!
        return f'The text of the question is ' \
               f'( {self.text} )'

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff <answer> is a valid answer to this question.
        """
        # implement this method!
        raise NotImplementedError

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return a float between 0.0 and 1.0 indicating how similar two
        answers are.

        Preconditions:
            - <answer1> and <answer2> are both valid answers to this question
        """
        # implement this method!
        raise NotImplementedError


class YesNoQuestion(Question):
    # make this a child class of another class defined in this file
    """A question whose answer is either yes (represented by True) or
    no (represented by False).

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Private Attributes ===
    _options: two possible answer to this question (Yes/ No)

    === Representation Invariants ===
    text is not the empty string
    """
    id: int
    text: str
    _options: list[bool]

    def __init__(self, id_: int, text: str) -> None:
        """Initialize a question with the text <text> and id <id>.
        """
        Question.__init__(self, id_, text)
        self._options = [True, False]

    def __str__(self) -> str:
        """Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        # implement this method or remove it (to inherit it as is)
        first_line = Question.__str__(self)
        second_line = f'Answer can be chosen from ' \
                      f'{self._options}'
        lst = [first_line, second_line]
        return '\n'.join(lst)

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff <answer> is a valid answer to this question.

        An answer is valid if its content is one of the answer options for this
        question.
        """
        # implement this method or remove it (to inherit it as is)
        return answer.content in self._options

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return 1.0 iff <answer1>.content and <answer2>.content are equal and
        0.0 otherwise.

        Preconditions:
            - <answer1> and <answer2> are both valid answers to this question.
        """
        # implement this method or remove it (to inherit it as is)
        if answer1.content == answer2.content:
            return 1.0
        else:
            return 0.0


class MultipleChoiceQuestion(YesNoQuestion):
    # make this a child class of another class defined in this file
    """A question whose answers can be one of several options

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Private Attributes ===
    _options: all possible options of this question.

    === Representation Invariants ===
    text is not the empty string
    """
    id: int
    text: str
    _options: list[str]

    def __init__(self, id_: int, text: str, options: list[str]) -> None:
        """Initialize a question with the text <text> and id <id> and
        possible answers given in <options>.

        Preconditions:
            - No two elements in <options> are the same string
            - <options> contains at least two elements
        """
        # implement this method or remove it (to inherit it as is)
        YesNoQuestion.__init__(self, id_, text)
        self._options = options


class NumericQuestion(Question):
    # make this a child class of another class defined in this file
    """A question whose answer can be an integer between some minimum and
    maximum value (inclusive).

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Private Attributes ===
    _min: the minimal value of the answer.
    _max: the maximal value of the answer.

    === Representation Invariants ===
    text is not the empty string
    """
    id: int
    text: str
    _min: int
    _max: int

    def __init__(self, id_: int, text: str, min_: int, max_: int) -> None:
        """Initialize a question with id <id_> and text <text> whose possible
        answers can be any integer between <min_> and <max_> (inclusive)

        Preconditions:
            - min_ < max_
        """
        Question.__init__(self, id_, text)
        self._min = min_
        self._max = max_

    def __str__(self) -> str:
        """Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        # implement this method or remove it (to inherit it as is)
        first_line = Question.__str__(self)
        second_line = f'An integer can be chosen between {self._min} ' \
                      f'and {self._max} (inclusive)'
        lst = [first_line, second_line]
        return '\n'.join(lst)

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff the content of <answer> is an integer between the
        minimum and maximum (inclusive) possible answers to this question.
        """
        # implement this method or remove it (to inherit it as is)
        return self._min <= answer.content <= self._max

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return the similarity between <answer1> and <answer2> over the range
        of possible answers to this question.

        Similarity is calculated as follows:
        1. first find the absolute difference between <answer1>.content and
           <answer2>.content.
        2. divide the value from step 1 by the difference between the maximum
           and minimum possible answers.
        3. subtract the value of step 2 from 1.0

        For example:
        - Maximum similarity is 1.0 and occurs when <answer1> == <answer2>
        - Minimum similarity is 0.0 and occurs when <answer1> is the minimum
            possible answer and <answer2> is the maximum possible answer
            (or vice versa).

        Preconditions:
            - <answer1> and <answer2> are both valid answers to this question
        """
        # implement this method or remove it (to inherit it as is)
        abs_difference = abs(answer1.content - answer2.content)
        ratio = abs_difference / (self._max - self._min)
        result = 1.0 - ratio
        return result


class CheckboxQuestion(YesNoQuestion):
    # make this a child class of another class defined in this file
    """A question whose answers can be one or more of several options

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Private Attributes ===
    _options: all the possible answers of this question.

    === Representation Invariants ===
    text is not the empty string
    """
    id: int
    text: str
    _options: list[str]

    def __init__(self, id_: int, text: str, options: list[str]) -> None:
        """Initialize a question with the text <text> and id <id> and
        possible answers given in <options>.

        Preconditions:
            - No two elements in <options> are the same string
            - <options> contains at least two elements
        """
        # implement this method or remove it (to inherit it as is)
        YesNoQuestion.__init__(self, id_, text)
        self._options = options

    def __str__(self) -> str:
        """Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        result = YesNoQuestion.__str__(self)
        extra = '(One or more options can be chosen)'
        return '\n'.join([result, extra])

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff <answer> is a valid answer to this question.

        An answer is valid iff:
            * It is a non-empty list.
            * It has no duplicate entries.
            * Every item in it is one of the answer options for this question.
        """
        # implement this method or remove it (to inherit it as is)
        check_non_empty = False
        if len(answer.content) > 0:
            check_non_empty = True
        check_non_duplicates = False
        non_duplicates = set(answer.content)
        if len(answer.content) == len(non_duplicates):
            check_non_duplicates = True
        check_answer_in_options = False
        invalid_count = 0
        for a in answer.content:
            if a not in self._options:
                invalid_count += 1
        if invalid_count == 0:
            check_answer_in_options = True
        return check_non_empty and check_non_duplicates and \
            check_answer_in_options

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return the similarity between <answer1> and <answer2>.

        Similarity is defined as the ratio between the number of strings that
        are common to both <answer1>.content and <answer2>.content over the
        total number of unique strings that appear in both <answer1>.content and
        <answer2>.content. If there are zero unique strings in common,
        return 1.0.

        For example, if <answer1>.content == ['a', 'b', 'c'] and
        <answer2>.content == ['c', 'b', 'd'], there are 2 strings common to
        both: 'c' and 'b'; and there are 4 unique strings that appear in both:
        'a', 'b', 'c', and 'd'. Therefore, the similarity between these two
        answers is 2/4 = 0.5.

        Preconditions:
            - <answer1> and <answer2> are both valid answers to this question
        """
        # implement this method or remove it (to inherit it as is)
        set_1 = set(answer1.content)
        set_2 = set(answer2.content)
        intersection = set_1 & set_2
        union = set_1 | set_2
        return len(intersection) / len(union)


class Answer:
    """An answer to a question used in a survey

    === Public Attributes ===
    content: an answer to a single question
    """
    content: Union[str, bool, int, list[str]]

    def __init__(self,
                 content: Union[str, bool, int, list[str]]) -> None:
        """Initialize this answer with content <content>"""
        # implement this method!
        self.content = content

    def is_valid(self, question: Question) -> bool:
        """Return True iff this answer is a valid answer to <question>"""
        # implement this method!
        return question.validate_answer(self)


class Survey:
    """A survey containing questions as well as criteria and weights used to
    evaluate the quality of a group based on their answers to the survey
    questions.

    === Private Attributes ===
    _questions: a dictionary mapping a question's id to the question itself
    _criteria: a dictionary mapping a question's id to its associated criterion
    _weights: a dictionary mapping a question's id to a weight -- an integer
              representing the importance of this criteria.

    === Representation Invariants ===
    No two questions on this survey have the same id
    Each key in _questions equals the id attribute of its value
    The dictionaries _questions, _criteria, and _weights all have the same keys
    Each value in _weights is greater than 0

    NOTE: The weights associated with the questions in a survey do NOT have to
          sum up to any particular amount.
    """
    _questions: dict[int, Question]
    _criteria: dict[int, Criterion]
    _weights: dict[int, int]

    def __init__(self, questions: list[Question]) -> None:
        """Initialize a new survey that contains every question in <questions>.

        This new survey should use a HomogeneousCriterion as a default criterion
        and should use 1 as a default weight.
        """
        # implement this method!
        id_lst = []
        for q in questions:
            id_lst.append(q.id)
        id_set = set(id_lst)
        if len(id_set) != len(id_lst):
            raise SameQuestionIDError
        else:
            self._questions = {}
            self._criteria = {}
            self._weights = {}
            for q in questions:
                self._questions[q.id] = q
                self._criteria[q.id] = HomogeneousCriterion()
                self._weights[q.id] = 1

    def __len__(self) -> int:
        """Return the number of questions in this survey """
        # implement this method!
        return len(self._questions)

    def __contains__(self, question: Question) -> bool:
        """Return True iff there is a question in this survey with the same
        id as <question>.
        """
        # implement this method!
        if question.id in self._questions:
            return True
        return False

    def __str__(self) -> str:
        """Return a string containing the string representation of all
        questions in this survey.

        You can choose the precise format of this string.
        """
        # implement this method!
        result = []
        for questions in self._questions.values():
            result.append(f'{questions}\n')
        return '\n'.join(result)

    def get_questions(self) -> list[Question]:
        """Return a list of all questions in this survey """
        # implement this method!
        result = []
        for question in self._questions.values():
            result.append(question)
        return result

    def _get_criterion(self, question: Question) -> Criterion:
        """Return the criterion associated with <question> in this survey.

        Preconditions:
            - <question>.id occurs in this survey
        """
        # implement this method!
        return self._criteria[question.id]

    def _get_weight(self, question: Question) -> int:
        """Return the weight associated with <question> in this survey.

        Preconditions:
            - <question>.id occurs in this survey
        """
        # implement this method!
        return self._weights[question.id]

    def set_weight(self, weight: int, question: Question) -> bool:
        """Set the weight associated with <question> to <weight> and
        return True.

        If <question>.id does not occur in this survey, do not set the <weight>
        and return False instead.
        """
        # implement this method!
        if question.id not in self._questions:
            return False
        else:
            self._weights[question.id] = weight
            return True

    def set_criterion(self, criterion: Criterion, question: Question) -> bool:
        """Set the criterion associated with <question> to <criterion> and
        return True.

        If <question>.id does not occur in this survey, do not set the <weight>
        and return False instead.
        """
        # implement this method!
        if question.id not in self._questions:
            return False
        else:
            self._criteria[question.id] = criterion
            return True

    def _get_student_answers(self, students: list[Student],
                             question: Question) -> list[Answer]:
        """Return the list of answers of students on question."""
        result = []
        for student in students:
            result.append(student.get_answer(question))
        return result

    def _check_all_valid_answers(self, students: list[Student]) -> Any:
        """Return True iff <students> has all valid answer to all questions
        in this survey.

        Precondition:
        - All students in <students> have an answer to all questions in this
            survey
        - len(students) > 0
        - There are at least one question in <self>.
        """
        for question in self._questions.values():
            answer_list = self._get_student_answers(students, question)
            for answer in answer_list:
                if answer is None or not answer.is_valid(question):
                    raise InvalidAnswerError
        return True

    def _get_weighted_score(self, question: Question, answers: list[Answer]) \
            -> float:
        """Return the weighted score of answers to question.

        Precondition:
        <answers> contains all valid answers to question.
        """
        criterion = self._get_criterion(question)
        weight = self._get_weight(question)
        score = criterion.score_answers(question, answers)
        return score * weight

    def score_students(self, students: list[Student]) -> float:
        """Return a quality score for <students> calculated based on their
        answers to the questions in this survey, and the associated criterion
        and weight for each question.

        The score is determined using the following algorithm:
        1. For each question in this survey, find the question's associated
           criterion (do we want homogeneous answers, for instance), weight,
           and <students> answers to the question. Use the score_answers method
           for its criterion to calculate how well the <students> answers
           satisfy the criterion. Multiply this quality score by the question's
           weight.
        2. Find the average of all quality scores from step 1.

        This method should NOT throw an InvalidAnswerError. If one occurs
        during the execution of this method or if there are no questions in
        <self>, return zero.

        Preconditions:
            - All students in <students> have an answer to all questions in this
            survey
            - len(students) > 0
        """
        #  implement this method!
        if len(self._questions) == 0:
            return 0.0
        try:
            self._check_all_valid_answers(students)
            weighted_score_lst = []
            for question in self._questions.values():
                answer_lst = self._get_student_answers(students, question)
                single_score = self._get_weighted_score(question, answer_lst)
                weighted_score_lst.append(single_score)
        except InvalidAnswerError:
            return 0.0
        return sum(weighted_score_lst) / len(weighted_score_lst)

    def score_grouping(self, grouping: Grouping) -> float:
        """Return a score for <grouping> calculated based on the answers of
        each student in each group in <grouping> to the questions in <self>.

        If there are no groups in <grouping> return 0.0. Otherwise, the score
        is determined using the following algorithm:
        1. For each group in <grouping>, calculate the score for the members of
           this based on their answers to the questions in this survey.
        2. Return the average of all the scores calculated in step 1.

        Preconditions:
            - All students in the groups in <grouping> have an answer to
              all questions in this survey
        """
        # implement this method!
        if not grouping.get_groups():
            return 0.0
        else:
            weighted_score_lst = []
            for group in grouping.get_groups():
                weighted_score_lst.append(self.score_students(
                    group.get_members()))
            return sum(weighted_score_lst) / len(weighted_score_lst)


class SameQuestionIDError(Exception):
    """Raise SameQuestionIDError when 2 questions have same ID."""

    def __str__(self) -> str:
        return 'RI violation -- 2 questions have same ID.'


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['typing',
                                                  'criterion',
                                                  'course',
                                                  'grouper'],
                                'disable': ['E9992']})
