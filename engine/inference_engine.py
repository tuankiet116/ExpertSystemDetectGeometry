import re
import sys
sys.path.append('..')
from basic.basic_rule import Rule
from Picture_handler.cv_handler2 import Handler, FactGenerator

re_a_rule = re.compile(r'(\{.*?\})')
re_if_part = re.compile(r'^\{IF:\s+(\[.*?\])')
re_then_part = re.compile(r'THEN:\s+(\'.*?\')')
re_description_part = re.compile(r'DESCRIPTION:\s+(\'.*?\')')


def generate_a_rule(rule):
    if_part = re_if_part.findall(rule)[0]
    if_part = re.sub(', ', ',', if_part)
    if_part = re.sub('\[', '', if_part)
    if_part = re.sub(']', '', if_part)
    if_part = re.sub("'", '', if_part)
    if_part = if_part.split(',')
    then_part = re_then_part.findall(rule)[0]
    description_part = re_description_part.findall(rule)[0]
    return Rule(if_part, then_part.strip('"\''), description_part.strip('"\'')) #trả về 1 đối tượng Rule 


def separate_rules(rules):
    rule_group = re_a_rule.findall(rules)
    return list(map(generate_a_rule, rule_group))

#Đọc rule từ file và xử lý rule vào từng đối tượng Rule()
def read_rules(rule_file):
    with open('../rules/' + rule_file) as f:
        rules = ''.join(f.read().splitlines())
    return separate_rules(rules)


class Engine:
    """

    """
    def __init__(self, rule_library, fact_library):
        self.target = None
        self.rule_library = rule_library
        self.fact_library = fact_library
        self.condition_stack = []            # using Python list as stack
        self.matched_facts = {}
        self.hit_rules = {}

    #Thêm điều kiện vào hàng đợi
    def push_condition_stack(self, condition):
        self.condition_stack.append(condition)

    def pop_condition_stack(self):
        return self.condition_stack.pop()

    def top_condition_stack(self):
        try:
            return self.condition_stack[-1]
        except IndexError:
            return None

    def condition_stack_is_empty(self):
        return not self.condition_stack

    def __match_facts__(self, ant, contour_index):
        facts = self.fact_library['Contour' + str(contour_index)]
        matched = False
        #Kiểm tra cạnh
        for fact in facts.line_facts:
            
            if str(ant) == fact.fact:
                matched = True
                self.matched_facts['Contour' + str(contour_index)].append(fact)
                return matched
        #Kiểm tra góc
        for fact in facts.angle_facts:
            if ant == fact.fact:
                matched = True
                self.matched_facts['Contour' + str(contour_index)].append(fact)
                return matched

        return matched

    #Tham số con truyền vào điều kiện hình học cần kiểm tra trả về True nếu tồn tại điều kiện có thể kiểm tra trong luật
    def __hit_consequent__(self, cons, contour_index):
        hit = False
        for rule in self.rule_library:
            if cons == getattr(rule, 'consequent'): #Kiểm tra thuộc tính đã chọn để kiểm tra với các consequent của luật xem có trùng khớp?
                hit = True
                self.hit_rules['Contour' + str(contour_index)].append(rule)
                ants = getattr(rule, 'antecedent')
                for ant in ants:
                    if not self.__match_facts__(ant, contour_index):
                        self.push_condition_stack(ant)
                break
        return hit

    # Đặt mục tiêu kiểm tra vào stack
    def goal(self, target):
        self.target = target
        self.condition_stack = []
        self.matched_facts = {}
        self.hit_rules = {}
        self.push_condition_stack(target)

    # Chạy công cụ suy luận 
    # Tham số là id biên đã được tính
    def run(self, contour_index):
        self.matched_facts['Contour' + str(contour_index)] = []
        self.hit_rules['Contour' + str(contour_index)] = []
        found = True
        while self.condition_stack:
            cons = self.pop_condition_stack() #Lấy điều kiện trong stack
            if not self.__hit_consequent__(cons, contour_index):
                found = False
                break
        self.condition_stack = [self.target]
        if found:
            return 'SUCCESS: Find Required Shape in Contour%d' % contour_index
        else:
            self.matched_facts['Contour' + str(contour_index)] = []
            self.hit_rules['Contour' + str(contour_index)] = []
            return 'ERROR: No Sufficient Facts in Contour%d' % contour_index

    def get_rule_library(self):
        return '\n'.join(list(map(str, self.rule_library)))

    def __str__(self):
        s = ''
        s += ('*' * 60 + '\n')
        s += 'Shape Detection Engine -- a Rule-based Expert System\n'
        s += '--------------- Below is all the rules ---------------\n'
        s += self.get_rule_library()
        s += '---------------- End of all the rules ----------------\n'
        return s


def setup_engine(image_source):
    handler = Handler(image_source)
    handler.generate_contour_dict() # Lấy các đường biên thành dictionary
    generator = FactGenerator(handler.contour_dict) #sinh ra các fact
    generator.generate_fact()
    r = read_rules('rules.txt')
    e = Engine(r, generator.handled_facts) #tạo mới 1 công cụ suy luận bao gồm luật và fact đã được tính toán
    return e

#set goal cho máy phân tích
def set_goal(e, my_goal):
    e.goal(my_goal)


#Chạy công cụ suy luận trong đó e là 1 đối tượng công cụ suy luận
def main_run(e):
    results = []
    for i in range(len(e.fact_library)):
        result = e.run(i) # Chạy công cụ suy luận dựa vào id của fact
        results.append(result)
    return results, e.matched_facts, e.hit_rules


if __name__ == '__main__':
    # test
    e = setup_engine('../test/test40.png')
    set_goal(e, 'the shape is right triangle')
    results, matched_facts, hit_rules = main_run(e)
    for result in results:
        print(result)
    for fact in matched_facts['Contour0']:
        print(fact.fact)
    for rule in hit_rules['Contour0']:
        print(rule)
    # print('\n')
    # set_goal(e, 'the shape is triangle')
    # results, matched_facts, hit_rules = main_run(e)
    # for result in results:
    #     print(result)
    pass

