# You may need to import pytest in order to run your tests.
# You are free to import hypothesis and use hypothesis for testing.
# This file will not be graded for style with PythonTA


from course import Course, Student
from survey import NumericQuestion, MultipleChoiceQuestion, \
    CheckboxQuestion, YesNoQuestion, Answer, Survey
from criterion import HomogeneousCriterion, HeterogeneousCriterion, \
    LonelyMemberCriterion
from grouper import Group, Grouping, AlphaGrouper, GreedyGrouper, \
    SimulatedAnnealingGrouper
import pytest
import hypothesis
from hypothesis import given


###############################################################################
# Task 2 Test cases
###############################################################################
# Add your test cases below
def test_student_has_answer() -> None:
    Mario = Student(1, 'Mario')
    question = NumericQuestion(21, 'Choose your level of happiness:', 1, 10)
    answer = Answer(9)
    Mario.set_answer(question, answer)
    assert Mario.has_answer(question)


def test_student_set_valid_answer() -> None:
    Mario = Student(1, 'Mario')
    question = NumericQuestion(21, 'Choose your level of happiness:', 1, 10)
    answer = Answer(9)
    Mario.set_answer(question, answer)
    answer_2 = Answer(10)
    Mario.set_answer(question, answer_2)
    assert Mario.get_answer(question) == answer_2


def test_student_get_answer() -> None:
    Mario = Student(1, 'Mario')
    question = NumericQuestion(21, 'Choose your level of happiness:', 1, 10)
    answer = Answer(9)
    Mario.set_answer(question, answer)
    question_2 = YesNoQuestion(7, "Are you happy?")
    assert Mario.get_answer(question_2) is None


###############################################################################
# Task 3 Test cases
###############################################################################
# Add your test cases below

def test_enroll_student_same_id() -> None:
    a = Student(1, "a")
    b = Student(1, "b")
    c = Student(5, "c")
    d = Student(3, "d")
    students = [a, b, c, d]
    new_course = Course('CSC148')
    new_course.enroll_students(students)
    assert new_course.students == []


def test_all_answer() -> None:
    s1 = Student(1, 'April')
    s2 = Student(2, 'Casey')
    s3 = Student(3, 'Bobby')
    q = MultipleChoiceQuestion(2, 'Grade', ['A', 'B', 'C'])
    q2 = YesNoQuestion(3, 'Are you happy?')
    s = Survey([q, q2])
    c = Course('ENG199: Tree Story')
    c.enroll_students([s1, s2, s3])
    a1 = Answer('A')
    a2 = Answer('B')
    a3 = Answer(True)
    a4 = Answer(False)
    s1.set_answer(q, a1)
    s2.set_answer(q, a2)
    s3.set_answer(q, a1)
    s1.set_answer(q2, a3)
    s2.set_answer(q2, a4)
    assert c.all_answered(s) is False


def test_get_three_students() -> None:
    c = Course('CSC148')
    maria = Student(1, 'Maria')
    lila = Student(4, 'Lila')
    tony = Student(2, 'Tony')
    students_list = [maria, lila, tony]
    c.enroll_students(students_list)
    assert c.get_students() == (maria, tony, lila)


###############################################################################
# Task 4 Test cases
###############################################################################
# Add your test cases below
def test_yesno_validity() -> None:
    yn_question = YesNoQuestion(2, "Are you happy?")
    answer = Answer(True)
    assert yn_question.validate_answer(answer) is True


def test_yesno_similarity() -> None:
    answer_1 = Answer(True)
    answer_2 = Answer(False)
    yn_question = YesNoQuestion(2, "Are you happy?")
    assert yn_question.get_similarity(answer_1, answer_2) == 0.0


###############################################################################
# Task 5 Test cases
###############################################################################
# Add your test cases below
def test_answer_is_valid_numeric() -> None:
    question = NumericQuestion(1, 'Choose your mood:', 1, 6)
    answer = Answer(7)
    assert answer.is_valid(question) is False


###############################################################################
# Task 6 Test cases
###############################################################################
# Add your test cases below
def test_homogenous_score_answers() -> None:
    q = MultipleChoiceQuestion(1, "Choose one letter",
                               ['A', 'B', 'C', 'D'])
    a1 = Answer('A')
    a2 = Answer('B')
    a3 = Answer('A')
    a4 = Answer('A')
    lst = [a1, a2, a3, a4]
    c = HomogeneousCriterion()
    assert c.score_answers(q, lst) == 0.5


def test_hetero_score_answers() -> None:
    q = MultipleChoiceQuestion(1, "Choose one letter",
                               ['A', 'B', 'C', 'D'])
    a1 = Answer('C')
    a2 = Answer('B')
    a3 = Answer('A')
    a4 = Answer('A')
    lst = [a1, a2, a3, a4]
    c = HeterogeneousCriterion()
    assert c.score_answers(q, lst) == 5 / 6


def test_lonely_score_answer() -> None:
    q = MultipleChoiceQuestion(1, "Choose one letter",
                               ['A', 'B', 'C', 'D'])
    a1 = Answer('C')
    a2 = Answer('B')
    a3 = Answer('A')
    a4 = Answer('A')
    lst = [a1, a2, a3, a4]
    c = LonelyMemberCriterion()
    assert c.score_answers(q, lst) == 0.0


###############################################################################
# Task 7 Test cases
###############################################################################
# Add your test cases below
def test_group_length() -> None:
    group_1 = Group([Student(9, 'Mario'), Student(8, 'Kat')])
    assert len(group_1) == 2


def test_group_contain() -> None:
    group_1 = Group([Student(9, 'Mario'), Student(8, 'Kat')])
    member = Student(000, 'Mario')
    assert member not in group_1


def test_group_get_member() -> None:
    members = [Student(9, 'Mario'), Student(8, 'Kat')]
    group_1 = Group(members)
    assert group_1.get_members() == members
    assert group_1.get_members() is not members


###############################################################################
# Task 8 Test cases
###############################################################################
# Add your test cases below
def test_grouping_add_group() -> None:
    g = Grouping()
    s1 = Student(1, 'Mario')
    s2 = Student(3, 'Kat')
    s3 = Student(6, 'Lilian')
    s4 = Student(99, 'Boo')
    gp = Group([s1, s2])
    gp2 = Group([s3, s4])
    assert g.add_group(gp) is True
    assert g.add_group(gp2) is True
    assert g.get_groups() == [gp, gp2]


def test_grouping_add_group_duplicate() -> None:
    g = Grouping()
    s1 = Student(1, 'Mario')
    s2 = Student(3, 'Kat')
    s3 = Student(6, 'Lilian')
    s4 = Student(99, 'Boo')
    gp = Group([s1, s2])
    gp2 = Group([s3, s4])
    gp3 = Group([s1, s4])
    g.add_group(gp)
    g.add_group(gp2)
    assert g.add_group(gp3) is False
    assert g.get_groups() == [gp, gp2]
    assert len(g) == 2


def test_grouping_add_group_empty() -> None:
    g = Grouping()
    gp = Group([])
    assert g.add_group(gp) is False
    assert g.get_groups() == []
    assert len(g) == 0


###############################################################################
# Task 9 Test cases
###############################################################################
# Add your test cases below

def test_survey_get_question() -> None:
    q1 = YesNoQuestion(2, 'ABbb')
    q2 = CheckboxQuestion(3, 'Hoo', ['A', 'B'])
    s = Survey([q1, q2])
    assert s.get_questions() == [q1, q2]


def test_survey_set_weight() -> None:
    q1 = YesNoQuestion(2, 'ABbb')
    q2 = CheckboxQuestion(3, 'Hoo', ['A', 'B'])
    q3 = MultipleChoiceQuestion(7, 'Hola', ['A', 'B', 'C'])
    s = Survey([q1, q2])
    assert s.set_weight(50, q2) is True
    assert s.set_weight(1000000, q3) is False
    assert s.set_weight(20, q2) is True


def test_survey_set_criterion() -> None:
    q1 = YesNoQuestion(2, 'ABbb')
    q2 = CheckboxQuestion(3, 'Hoo', ['A', 'B'])
    q3 = MultipleChoiceQuestion(7, 'Hola', ['A', 'B', 'C'])
    s = Survey([q1, q2])
    assert s.set_criterion(HeterogeneousCriterion(), q1) is True
    assert s.set_criterion(LonelyMemberCriterion(), q3) is False


def test_survey_score_student() -> None:
    s1 = Student(1, 'Mary')
    s2 = Student(9, 'Ken')
    s3 = Student(10, 'Rio')
    s4 = Student(33, 'L')
    q = MultipleChoiceQuestion(10,
                               'What is your year of study', ['first',
                                                              'second',
                                                              'third',
                                                              'forth'])
    a1 = Answer('first')
    a2 = Answer('second')
    a3 = Answer('third')
    s1.set_answer(q, a1)
    s2.set_answer(q, a2)
    s3.set_answer(q, a3)
    s4.set_answer(q, a1)
    s = Survey([q])
    s.set_criterion(LonelyMemberCriterion(), q)
    s.set_weight(100, q)
    assert s.score_students([s1, s2, s3, s4]) == 0.0
    assert s.score_students([s1, s4]) == 100.0


def test_survey_score_group() -> None:
    s1 = Student(1, 'Mary')
    s2 = Student(9, 'Ken')
    s3 = Student(10, 'Rio')
    s4 = Student(33, 'L')
    q = MultipleChoiceQuestion(10,
                               'What is your year of study', ['first',
                                                              'second',
                                                              'third',
                                                              'forth'])
    a1 = Answer('first')
    a2 = Answer('second')
    a3 = Answer('third')
    s1.set_answer(q, a1)
    s2.set_answer(q, a2)
    s3.set_answer(q, a3)
    s4.set_answer(q, a1)
    s = Survey([q])
    s.set_criterion(LonelyMemberCriterion(), q)
    s.set_weight(100, q)
    g1 = Group([s1, s4])
    g2 = Group([s2, s3])
    gp = Grouping()
    gp.add_group(g1)
    gp.add_group(g2)
    assert s.score_grouping(gp) == 50.0


###############################################################################
# Task 10 Test cases
###############################################################################
# Add your test cases below

def test_alpha_make_grouping() -> None:
    gper = AlphaGrouper(2)
    s1 = Student(1, 'April')
    s2 = Student(2, 'Casey')
    s3 = Student(3, 'Bobby')
    s = Survey([MultipleChoiceQuestion(2, 'Grade', ['A', 'B', 'C'])])
    c = Course('ENG199: Tree Story')
    c.enroll_students([s1, s2, s3])
    g1 = Group([s1, s3])
    g2 = Group([s2])
    result = Grouping()
    result.add_group(g1)
    result.add_group(g2)
    actual = gper.make_grouping(c, s)
    lst1 = actual.get_groups()
    lst2 = result.get_groups()
    assert lst1[0].get_members() == lst2[0].get_members()
    assert lst1[1].get_members() == lst2[1].get_members()


def test_greedy_grouper_make_grouping() -> None:
    gper = GreedyGrouper(2)
    s1 = Student(1, 'April')
    s2 = Student(2, 'Casey')
    s3 = Student(3, 'Bobby')
    q = MultipleChoiceQuestion(2, 'Grade', ['A', 'B', 'C'])
    s = Survey([q])
    c = Course('ENG199: Tree Story')
    c.enroll_students([s1, s2, s3])
    a1 = Answer('A')
    a2 = Answer('B')
    s1.set_answer(q, a1)
    s2.set_answer(q, a2)
    s3.set_answer(q, a1)
    s.set_criterion(LonelyMemberCriterion(), q)
    s.set_weight(100, q)
    expect = Grouping()
    g1 = Group([s1, s3])
    g2 = Group([s2])
    expect.add_group(g1)
    expect.add_group(g2)
    expect_lst = expect.get_groups()
    actual_lst = gper.make_grouping(c, s).get_groups()
    assert expect_lst[0].get_members() == actual_lst[0].get_members()
    assert expect_lst[1].get_members() == actual_lst[1].get_members()


if __name__ == '__main__':
    pytest.main(['tests.py'])
