import sys

import Classes


def is_axiom(formula):
    """
    Проверяет на соответсвие формулы аксиоме.
    :param formula: формула
    :return: либо вывод, либо ложь (т.е. не соответсвует)
    """
    for i, axiom in enumerate(axioms):
        if Classes.equal_formulas(axiom, formula):
            return f'аксиома {i+1}\n'
    return False


def is_hypothesis(formula):
    """
    Является ли формула гипотезой.
    :param formula: формула
    :return: либо вывод, либо ложь (т.е. не является)
    """
    for i, hypothesis in enumerate(hypotheses):
        if formula == hypothesis:
            return f'гипотеза {i+1}\n'
    return False


def is_mp_rule(formula, formulas):
    """
    Выводима ли формула через MP.
    :param formula: формула
    :param formulas: формулы до исследуемой
    :return: либо вывод, либо ложь (т.е. не выводима)
    """
    for ind_left, left in enumerate(formulas):
        check = Classes.formulas_builder(left.raw_formula, '→', formula.raw_formula)
        if check in formulas:
            return f'MP: {ind_left+1}, {formulas.index(check)+1}\n'
    return False


#%% Чтение из всех файлов и запись в виде формул.
# Именно тут происходит проверка на то, является ли строка формулой или нет (выбрасывается ошибка в консоль/терминал).
with open("data/hypotheses.txt", 'r') as h_reader:
    raw_hypotheses = h_reader.read().split('\n')
    # Преобразуем к виду формул, игнорируя пустые строки.
    hypotheses = []
    for hyp in raw_hypotheses:
        if hyp:
            try:
                hypotheses.append(Classes.Formula(hyp))
            except:
                print('Ошибка в файле hypotheses.txt:')
                print(f"Ошибка в формуле: {hyp}")
                sys.exit(1)

with open("data/axioms.txt", 'r') as ax_reader:
    raw_axioms = ax_reader.read().split('\n')
    # Преобразуем к виду формул, игнорируя пустые строки.
    axioms = []
    for ax in raw_axioms:
        if ax:
            try:
                axioms.append(Classes.Formula(ax))
            except:
                print('Ошибка в файле axioms.txt:')
                print(f"Ошибка в формуле: {ax}")
                sys.exit(1)

with open("data/proof.txt", 'r') as p_reader:
    raw_formulas = p_reader.read().split('\n')
    # Преобразуем к виду формул, игнорируя пустые строки.
    formulas = []
    for p in raw_formulas:
        if p:
            try:
                formulas.append(Classes.Formula(p))
            except:
                print('Ошибка в файле proof.txt:')
                print(f"Ошибка в формуле: {p}")
                sys.exit(1)


#%% Проверка вывода.
result = ''
is_deduce = True
for line, formula in enumerate(formulas):
    if result_hyp := is_hypothesis(formula):
        result += f'{line+1}. {formula.raw_formula}; {result_hyp}'
    elif result_ax := is_axiom(formula):
        result += f'{line+1}. {formula.raw_formula}; {result_ax}'
    elif result_mp := is_mp_rule(formula, formulas[:line]):
        result += f'{line+1}. {formula.raw_formula}; {result_mp}'
    else:
        result += f'{line+1}. {formula.raw_formula}; не выводима\n\n Вывод не корректен.'
        is_deduce = False
        break

if is_deduce:
    result += '\nВывод корректен.'


#%% Вывод в консоль/терминал и запись в файл.
print(result)
with open("data/proof_with_notes.txt", 'w') as writer:
    writer.write(result)
