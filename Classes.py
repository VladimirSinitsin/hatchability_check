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
    # Для запоминания структуры формул используем вложенную функцию, чтобы хранить общие переменные во внешнем фрейме.
    ax_dict = {}
    form_dict = {}
    ax_structure = []
    form_structure = []

    def update_structure(expression, feature):
        """
        Обновляет словари и порядки.
        :param expression: функция.
        :param feature: характеристика (аксиома или формула), какие переменные обновлять.
        :return: None
        """
        nonlocal ax_dict
        nonlocal form_dict
        nonlocal ax_structure
        nonlocal form_structure

        if feature == 'axiom':
            if expression not in ax_dict:
                # Задаём каждому выражению свой номер, который потом используем в структуре вызовов.
                ax_dict[expression] = len(ax_dict)
            ax_structure.append(ax_dict[expression])
        else:
            if expression not in form_dict:
                # Задаём каждому выражению свой номер, который потом используем в структуре вызовов.
                form_dict[expression] = len(form_dict)
            form_structure.append(form_dict[expression])

    def equal_tree(axiom, formula):
        """
        Вложенная функция, выполняющая основную работу по выявлению соответствия.
        :param axiom: аксиома
        :param formula: формула
        :return: соответсвует или нет
        """
        if axiom.operation == 'symbol':
            # Если дошли до "листа" дерева структуры акиомы, то обновляем структуры и сравниваем их.
            update_structure(axiom.right, 'axiom')
            update_structure(formula.raw_formula, 'formula')
            return ax_structure == form_structure

        if axiom.operation != formula.operation:
            return False

        # Если можно идти вглубь, то смотрим на соответствие левых и правых "ветвей".
        right_trees_equal = equal_tree(Formula(axiom.right), Formula(formula.right))
        left_trees_equal = equal_tree(Formula(axiom.left), Formula(formula.left)) if axiom.operation != '¬' else True
        return right_trees_equal and left_trees_equal

    return equal_tree(axiom, formula)


def formulas_builder(left, operation, right):
    return Formula(f'({left}{operation}{right})')
