from .expr_tree import simpler, k_degree
from .logic_rules import *
from .parse import parse_expr


def logic_simplify_expr_string(ex_str: str):
    try:
        ex = parse_expr(ex_str)
    except Exception:
        raise
    return logic_simplify(ex)


def logic_simplify(ex: BooleanFunction):
    def apply_found_rule(_ex, _rule):
        nonlocal ex_list, rules, min_ex, temp_ex, old_ex_set
        # rules: tập hợp các luât
        rules.append(_rule)
        ex_list.append(_ex)
        old_ex_set.add(_ex)
        temp_ex = _ex
        if simpler(_ex, min_ex):
            min_ex = _ex

    def find_rules(_ex, rules_list, find_simple=True):
        nonlocal ex_list, rules, min_ex, temp_ex, old_ex_set
        new_ex_count = 0
        found_result = True

        while found_result:
            found_result = False
            found_ex = None
            found_rule = None

            for _rule in rules_list:
                # _temp_rules: danh sách tất cả các biểu thức con được
                # sinh ra từ việc áp dụng luật rule lên biểu thức _ex
                _temp_rules = sorted(_rule(_ex),
                                     key=lambda _x: _x[1].atoms(
                                         Symbol).__len__() + _x[2].atoms(Symbol).__len__(),
                                     reverse=False)

                for _name, _old_ex, _new_ex in _temp_rules:

                    _new_temp_ex = _ex.xreplace({_old_ex: _new_ex})
                    if not old_ex_set.__contains__(_new_temp_ex):
                        if found_result:
                            # so sánh biểu thức vừa thay thế(từng ptu) có đơn giản nhất
                            # trong nhóm luật đang xét ko
                            # chọn lưu trong found_ex
                            if (find_simple and simpler(_new_temp_ex, found_ex)) or (
                                    not find_simple and simpler(found_ex, _new_temp_ex)):
                                found_ex = _new_temp_ex
                                found_rule = _name
                        else:
                            # vòng lặp đầu tiên
                            found_result = True
                            found_ex = _new_temp_ex
                            found_rule = _name

            if found_result:
                apply_found_rule(found_ex, found_rule)
                _ex = found_ex
                new_ex_count += 1
                if not find_simple:
                    found_result = False

        return new_ex_count > 0

    # loại bỏ các bước dư thừa
    def remove_useless_steps():
        nonlocal ex_list, rules
        if min_ex == temp_ex:
            return
        if min_ex in ex_list:
            i = ex_list.index(min_ex)
            ex_list = ex_list[0:i + 1]
            rules = rules[0:i + 1]

    
    
    # Các nhóm tương ứng trong thuật toán
    rules_1 = [negation_law, domination_and_identity, constant_negative]
    rules_2 = [double_negative, idempotent, absorption]
    rules_3 = [absorption_and_distribution]
    rules_4 = [conditional]
    rules_5 = [double_negative, negation_law, domination_and_identity, idempotent, absorption_and_distribution,
               de_morgan_expand, constant_negative]
    rules_6_1 = [de_morgan_expand]
    rules_6_2 = [distribution_expand]
    rules_7 = [de_morgan_reduce]
    rules_2_1 = [distribution_reduce]

    g = ex
    rules = []  # danh sách các luật

    ex_list = []  # danh sách các biểu thức tương ứng với từng luật
    min_ex = g  # biểu thức đơn giản nhất tìm được
    temp_ex = g  # biểu thức tìm được sau mỗi bước
    old_ex_set = {g}  # tập hợp các biểu thức được biến đổi sau từng bước

    found = True
    distribution_count = 0
    found_distribution = False
    # Bước 1: Tìm các luật để rút gọn biểu thức
    while found and k_degree(temp_ex) > 0:
        found = False
        # Tìm các luật trong nhóm 1
        # found_in_group_1: tập hợp phép phủ định hoặc hằng đúng hoặc hằng sai
        found_in_group_1 = temp_ex.atoms(Not).__len__() > 0 or temp_ex.atoms(
            BooleanTrue).__len__() > 0 or temp_ex.atoms(
            BooleanFalse).__len__() > 0
        while found_in_group_1:
            found_in_group_1 = find_rules(temp_ex, rules_1)
            found_in_group_1 = found_in_group_1 and (temp_ex.atoms(Not).__len__() > 0 or temp_ex.atoms(
                BooleanTrue).__len__() > 0 or temp_ex.atoms(
                BooleanFalse).__len__() > 0)

        found = found_in_group_1 or found
        print('found in group 1', found)

        # Tìm các luật trong nhóm 3
        while find_rules(temp_ex, rules_3):
            found = True
        print('found in group 3', found)

        # Tìm các luật trong nhóm 2
        while find_rules(temp_ex, rules_2):
            found = True

        print('found in group 2', found)

        # Tìm các luật trong nhóm 2.1
        if not found_distribution:
            while find_rules(temp_ex, rules_2_1):
                found = True

        print('found in group 2.1', found)

        # Tìm các luật trong nhóm 4
        found_implies = False  # số phép kéo theo trong biểu thức temp_ex
        implies_count = temp_ex.atoms(Implies).__len__()
        while implies_count > 0:
            found_implies = find_rules(temp_ex, rules_4) or found_implies
            implies_count = temp_ex.atoms(Implies).__len__()

        print('found in group 4', found_implies)

        # Tìm các luật trong nhóm 5
        if found_implies:
            found = True
            while find_rules(temp_ex, rules_5):
                print('found in group 5')
        # Tìm các luật trong nhóm 6
        if found is False:
            found = find_rules(temp_ex, rules_6_1) or found

        if found is False and distribution_count < 5:
            found_distribution = find_rules(
                temp_ex, rules_6_2, find_simple=False)
            found = found_distribution or found
            if found:
                distribution_count += 1
        else:
            found_distribution = False
        # Tìm các luật trong nhóm 7
        if found is False:
            found = find_rules(temp_ex, rules_7) or found

    remove_useless_steps()

    return min_ex, rules, ex_list


"""

def equivalent_expr_string(ex_str_1: str, ex_str_2: str):
    ex1 = parse_expr(ex_str_1)
    ex2 = parse_expr(ex_str_2)
    return equivalent(ex1, ex2)

"""


def equivalent(ex1: BooleanFunction, ex2: BooleanFunction):
    if ex1 == ex2:
        return True, None, None

    if simpler(ex1, ex2):
        ex1, ex2 = ex2, ex1

    min_ex1, rules_1, expr_list_1 = logic_simplify(ex1)

    for i, _expr in enumerate(expr_list_1):
        if _expr == ex2:
            return True, (ex1, rules_1, expr_list_1[:i]), None

    min_ex2, rules_2, expr_list_2 = logic_simplify(ex2)

    if expr_list_1[-1] == expr_list_2[-1]:
        return True, (ex1, rules_1, expr_list_1), (ex2, rules_2, expr_list_2)

    return False, None, None
