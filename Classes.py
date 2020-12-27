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

        for i, symbol in enumerate(self.raw_formula):
            if symbol in ['(', ')']:
                brackets_count += 1

            if symbol == '(':
                brackets_checker += 1
            elif symbol == ')':
                brackets_checker -= 1

            if brackets_checker == -1:
                # Закрытая скобка до открытой.
                raise Exception(f"Ошибка со скобками в формуле: {self.raw_formula}")

            if symbol in ['∨', '∧', '¬', '→']:
                self.count_operations += 1

                if self.raw_formula[i-1] in ['∨', '∧', '¬', '→'] or self.raw_formula[i+1] in ['∨', '∧', '¬', '→']:
                    raise Exception(f"Ошибка с повторной операцией в формуле: {self.raw_formula}")

                elif symbol in ['∨', '∧', '→'] and (self.raw_formula[i-1] == '(' or self.raw_formula[i+1] == ')'):
                    raise Exception(f"Ошибка с операциями в формуле: {self.raw_formula}")

                elif symbol == '¬' and (self.raw_formula[i-1] != '(' or self.raw_formula[i+1] == ')'):
                    raise Exception(f"Ошибка в использовании операции ¬ в формуле: {self.raw_formula}")

                elif brackets_checker == 1:
                    if index != -1:
                        # Неверная формула, например: (А→В→С)
                        raise Exception(f"Ошибка с операциями в формуле: {self.raw_formula}")
                    index = i

            elif brackets_count > 0 and brackets_checker == 0:
                raise Exception(f"Ошибка в формуле: {self.raw_formula}")

        # Несоотвествие пар открытых и закрытых скобок.
        if brackets_checker != 0:
            raise Exception(f"Ошибка со скобками в формуле: {self.raw_formula}")

        if self.count_operations != 0 and brackets_count == 0:
            raise Exception(f"Ошибка! Нет скобок в формуле: {self.raw_formula}")

        return index


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
