class Formula:
    def __init__(self, raw_formula):
        self.raw_formula = raw_formula
        # Ищем индекс операции, если -1, то формула - символ.
        index_operation = self._find_ind_operation()
        if index_operation == -1:
            self.operation = 'symbol'
            self.left = ''
            # Все символы кроме скобок. Например, для (((A))) оставим только А.
            self.right = str.replace(self.raw_formula.replace('(', ''), ')', '')
        else:
            self.operation = self.raw_formula[index_operation]
            self.left = self.raw_formula[1:index_operation]
            self.right = self.raw_formula[index_operation + 1:-1]

            if self.operation == '¬' and self.left:
                raise Exception

        if not _rec_checker(self):
            raise Exception

    def __eq__(self, other):
        if self.raw_formula == other.raw_formula:
            return True
        return False

    def __repr__(self):
        return f"{self.raw_formula} | Operation: {self.operation}, Left: {self.left}, Right: {self.right}"

    def _find_ind_operation(self):
        """
        Находит индекс операции. А также проверяет, является ли строка формулой.
        :return: индекс.
        """
        self.count_operations = 0
        brackets_checker = 0
        brackets_count = 0
        index = -1

        if len(self.raw_formula) == 0:
            raise Exception

        elif len(self.raw_formula) == 1:
            if self.raw_formula[0] in ['∨', '∧', '¬', '→', '(', ')']:
                raise Exception
            return index

        else:
            if self.raw_formula[0] != '(' and self.raw_formula[-1] != ')':
                raise Exception

            for i, symbol in enumerate(self.raw_formula):
                if symbol in ['(', ')']:
                    brackets_count += 1

                if symbol == '(':
                    brackets_checker += 1
                elif symbol == ')':
                    brackets_checker -= 1

                elif symbol in ['∨', '∧', '¬', '→']:
                    self.count_operations += 1

                    if brackets_checker == 1:
                        index = i

                if brackets_count > 0 and brackets_checker == 0 and i < len(self.raw_formula)-1:
                    raise Exception

            # Несоотвествие пар открытых и закрытых скобок.
            if brackets_checker != 0:
                raise Exception

            if self.count_operations == 0 and brackets_count != 0:
                raise Exception

        return index


def _rec_checker(formula):
    if formula.operation == 'symbol':
        return True

    left_check = _rec_checker(Formula(formula.left)) if formula.operation != '¬' else True
    right_check = _rec_checker(Formula(formula.right))

    return left_check and right_check


def equal_formulas(axiom, formula):
    """
    Соответствие формулы аксиоме.
    :param axiom: аксиома
    :param formula: формула
    :return: соответсвует или нет
    """
    ax_dict = {}

    def equal_tree(axiom, formula):
        """
        Вложенная функция, выполняющая основную работу по выявлению соответствия.
        :param axiom: аксиома
        :param formula: формула
        :return: соответсвует или нет
        """
        nonlocal ax_dict

        if axiom.operation == 'symbol':
            if axiom.right not in ax_dict:
                ax_dict[axiom.right] = formula.raw_formula
                return True
            else:
                return ax_dict[axiom.right] == formula.raw_formula

        if axiom.operation != formula.operation:
            return False

        # Если можно идти вглубь, то смотрим на соответствие левых и правых "ветвей".
        right_trees_equal = equal_tree(Formula(axiom.right), Formula(formula.right))
        left_trees_equal = equal_tree(Formula(axiom.left), Formula(formula.left)) if axiom.operation != '¬' else True
        return right_trees_equal and left_trees_equal

    return equal_tree(axiom, formula)


def formulas_builder(left, operation, right):
    return Formula(f'({left}{operation}{right})')
