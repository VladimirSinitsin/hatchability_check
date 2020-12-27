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
h_reader = open("hypotheses.txt", 'r')
try:
    raw_hypotheses = h_reader.read().split('\n')
    # Преобразуем к виду формул, игнорируя пустые строки.
    hypotheses = [Classes.Formula(h) for h in raw_hypotheses if h]
except Exception as ex:
    print('Ошибка в файле hypotheses.txt:')
    print(ex)
    sys.exit(0)
finally:
    h_reader.close()

ax_reader = open("axioms.txt", 'r')
try:
    raw_axioms = ax_reader.read().split('\n')
    # Преобразуем к виду формул, игнорируя пустые строки.
    axioms = [Classes.Formula(ax) for ax in raw_axioms if ax]
except Exception as ex:
    print('Ошибка в файле axioms.txt:')
    print(ex)
    sys.exit(0)
finally:
    ax_reader.close()

p_reader = open("proof.txt", 'r')
try:
    raw_formulas = p_reader.read().split('\n')
    # Преобразуем к виду формул, игнорируя пустые строки.
    formulas = [Classes.Formula(f) for f in raw_formulas if f]
except Exception as ex:
    print('Ошибка в файле proof.txt:')
    print(ex)
    sys.exit(0)
finally:
    p_reader.close()


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
with open("proof_with_notes.txt", 'w') as writer:
    writer.write(result)
