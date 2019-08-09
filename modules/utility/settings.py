#Tools for creating settings
import copy

class settings():
    def __init__(self, defaultSettings):
        self.template = defaultSettings
        self.settings = self._evaluateAll(defaultSettings)
    
    #def loadFile(self, )

    def set(self, key, value, recomputeAll = True):
        templateCopy = copy.copy(self.template)
        self.settings = self._evaluateAll(templateCopy)

    def _evaluate(self, expression, non_expressions):
        assert expression[0] == '@', "Not an expression!"
        
        return eval(expression[1:], copy.copy(non_expressions))
    
    def _evaluateAll(self, to_evaluate):
        non_expressions = {}
        expressions = {}
        for key, value in to_evaluate.items():
            if type(value) == str and value[0] == '@':
                expressions[key] = value
            else:
                non_expressions[key] = value
        
        PASS_TOLERANCE = len(expressions)
        passes = 0
        
        while len(expressions) > 0:
            if (passes >= PASS_TOLERANCE):
                raise Exception(f"Could not parse all expressions. Try checking for circular references. Problematic Expressions: {expressions}")

            to_remove = [] #A list of keys to remove
            for key, value in expressions.items():
                try:
                    result = self._evaluate(value, non_expressions)
                    non_expressions[key] = result
                    to_remove.append(key)
                except NameError:
                    pass
            
            remaining_expressions = {}
            for key, value in expressions.items():
                if key not in to_remove:
                    remaining_expressions[key] = value
            
            expressions = remaining_expressions
            passes+=1

             
        
        return non_expressions
        
        



my_settings = settings(
    {
        'a': 5,
        'b': 2,
        'y': "@5*x",
        'x': "@a+b"
    }
)
print(my_settings.settings)