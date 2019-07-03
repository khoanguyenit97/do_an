from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_protect
from json import dumps, loads

#from .search import SearchResult
from inference.logic import logic_simplify
from inference.logic.logic_inference import LogicInference
from inference.logic.parse import parse_expr
from sympy.printing.pretty import pretty
import re
from inference.logic.parseBool import parse


@csrf_protect
def solve(request):
    results = {'success': False}
    if request.method == 'POST':
        data = loads(request.POST.get("data"))
        question_type = data["type"]
        question = data["question"]
        if question_type == "1":
            results = _bool(question)
        elif question_type == "2":
            results = _simplify(question)
        elif question_type == "3":
            results = _equivalent(question)
        elif question_type == "4":
            results = _resolve_logic(question)           
        
        else:
            results = {'success': False, 'msg': "Không tìm thấy dạng bài toán"}

    return HttpResponse(_dict_to_json(results), content_type='application/json')


def _bool(question):  
    
    if question.__len__() > 0:        
        try:          
            if parse(question) == 0:                           
                return {'success': False, 'msg': "Cú pháp không hợp lệ"}
            else:
                question, Karf, te_bao_lon, cac_phu_tu_karf,da_thuc_toi_tieu, de_quy = parse(question)      
        except SyntaxError:
            print("ra try")
            return {'success': False, 'msg': "Cú pháp không hợp lệ"}        
        answer = {
            "ques": pretty(question),
            "karf":Karf,
            "te_bao_lon": te_bao_lon,
            "cac_phu_tu_karf":cac_phu_tu_karf,
            "da_thuc_toi_tieu":da_thuc_toi_tieu,
            "de_quy":de_quy,
        }
        return {'success': True, "type": "1", "answer": answer}
    return {'success': False, 'msg': "Cú pháp không hợp lệ"}


def _simplify(_expr_str):     
    print("đề =",_expr_str)
    
    if _expr_str.__len__() > 0:
        try:
            _expr = parse_expr(_expr_str)          
        except SyntaxError:
            return {'success': False, 'msg': "Cú pháp không hợp lệ"}        
        print("đề đã chuyển đổi = ",_expr)
        min_ex, rules, expr_list = logic_simplify.logic_simplify(_expr)
        print("min_ex :", min_ex)
        print("rules :", rules)
        print("list :", expr_list)
        steps = []
        for ex, r in zip(expr_list, rules):
            step_detail = {
                "expr": pretty(ex),
                "rule": r
            }
            steps.append(step_detail)
        print("step :",steps)
        answer = {
            "expr": pretty(_expr),
            "steps": steps,
            "min": pretty(min_ex)
        }
        return {'success': True, "type": "2", 'answer': answer}
    return {'success': False, 'msg': "Cú pháp không hợp lệ"}


def _equivalent(question):
    def parse(text: str):
        tok = re.compile("{(.*),(.*)}")
        results = tok.findall(text)

        if results.__len__() > 0:
            ex_1, ex_2 = results[0]
            ex_1 = ex_1.strip()
            ex_2 = ex_2.strip()
            return ex_1, ex_2

        return None

    if question.__len__() < 1:
        return {'success': False, 'msg': "Cú pháp không hợp lệ"}

    parse_result = parse(question)

    if parse_result is None:
        return {'success': False, 'msg': "Cú pháp không hợp lệ"}

    _expr_str_1, _expr_str_2 = parse_result
    if _expr_str_1.__len__() < 1 or _expr_str_2.__len__() < 1:
        return {'success': False, 'msg': "Cú pháp không hợp lệ"}

    try:
        _expr_1 = parse_expr(_expr_str_1)
    except SyntaxError:
        return {'success': False, 'msg': "Cú pháp không hợp lệ"}

    try:
        _expr_2 = parse_expr(_expr_str_2)
    except SyntaxError:
        return {'success': False, 'msg': "Cú pháp không hợp lệ"}

    result, step_1, step_2 = logic_simplify.equivalent(_expr_1, _expr_2)

    _ex1 = _expr_1
    _ex2 = _expr_2

    steps_1 = []
    if step_1 is not None:
        _ex1, rules_1, expr_list_1 = step_1
        for ex, r in zip(expr_list_1, rules_1):
            step_detail = {
                "expr": pretty(ex),
                "rule": r
            }
            steps_1.append(step_detail)

    steps_2 = []
    if step_2 is not None:
        _ex2, rules_2, expr_list_2 = step_2
        for ex, r in zip(expr_list_2, rules_2):
            step_detail = {
                "expr": pretty(ex),
                "rule": r
            }
            steps_2.append(step_detail)

    answer = {
        "expr_1": pretty(_ex1),
        "expr_2": pretty(_ex2),
        "steps_1": steps_1,
        "steps_2": steps_2,
        "result": result
    }
    return {'success': True, "type": "3", 'answer': answer}


def _resolve_logic(question):
    def parse(text: str):
        tok = re.compile("{(.*)}( )*,( )*(.*)")
        results1 = tok.findall(text)
        if results1.__len__() > 0:
            _premises, _, _, con = results1[0]
            results2 = _premises.split(",")
            if results2.__len__() > 0:
                con = con.strip()
                pre = list(map(lambda x: x.strip(), results2))
                return pre, con

        return None

    if question.__len__() < 1:
        return {'success': False, 'msg': "Cú pháp không hợp lệ"}

    parse_result = parse(question)

    if parse_result is None:
        return {'success': False, 'msg': "Cú pháp không hợp lệ"}

    premises, conclusion = parse_result
    if premises.__len__() < 1:
        return {'success': False, 'msg': "Cần cung cấp giả thuyết!"}

    if conclusion.__len__() < 1:
        return {'success': False, 'msg': "Cần cung cấp kết luận!"}

    _premise_exprs = list()
    try:
        _premise_exprs = list(map(lambda x: parse_expr(x), premises))
    except SyntaxError:
        return {'success': False, 'msg': "Cú pháp của giả thuyết không hợp lệ"}

    try:
        _conclusion_expr = parse_expr(conclusion)
    except SyntaxError:
        return {'success': False, 'msg': "Cú pháp của kết luận không hợp lệ"}

    resolved, solution = LogicInference.resolve(
        _premise_exprs, _conclusion_expr)
    
    steps = []
    
    for rule_name, rules, fact in solution:        
        pretty_rules = list(map(lambda x: pretty(x), rules))
        step_detail = {
            "rules": pretty_rules,
            "rule": rule_name,
            "fact": pretty(fact)
        }
        steps.append(step_detail)
    answer = {
        "steps": steps,
        "result": resolved
    }
    return {'success': True, "type": "4", 'answer': answer}




def _dict_to_json(dic):
    return dumps(dic, sort_keys=True, indent=2, ensure_ascii=False).encode('utf8')

"""
def _parse_relation(text: str):
    tok = re.compile("{(.*)}( )*,( )*{(.*)}")
    re_tok = re.compile("[(]([0-9, .]*)[)]")
    text = text.strip()
    results1 = tok.findall(text)

    if results1.__len__() != 1:
        return None

    set_a, _, _, relation_set = results1[0]
    results2 = set_a.split(",")

    try:
        results2 = set(map(lambda x: int(x.strip()), results2))
    except ValueError:
        return None

    if results2.__len__() > 0:
        results3 = set()
        for pair_string in re_tok.findall(relation_set):
            pair = pair_string.split(",")

            if pair.__len__() != 2:
                return None
            try:
                pair = list(map(lambda x: int(x.strip()), pair))
            except ValueError:
                return None

            results3.add((pair[0], pair[1]))

        return results2, results3

    return None
"""