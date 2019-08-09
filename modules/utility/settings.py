#Tools for creating settings
import copy
import json

class settings():
    def __init__(self, default_settings):
        '''
        @param default_settings If a dict, treats that dict like the set of settings. If a string, loads the json file at the location indicated by the string. If a list, load all .json files indicated by the strings.
        '''
        if type(default_settings) is dict:
            loaded_default_settings = default_settings
        elif type(default_settings) is str:
            with open(default_settings) as o:
                loaded_default_settings = json.load(o)
        else:
            loaded_default_settings = {}
            for i in default_settings:
                with open(default_settings) as o:
                    file_default_settings = json.load(o)
                loaded_default_settings.update(file_default_settings)

        self.template = loaded_default_settings
        self.settings = self._evaluateAll(loaded_default_settings)

    def setSetting(self, key, value, recomputeAll = True, addToTemplate = False):
        '''
        Sets a setting.
        @param recomputeAll If true, all values will be recomputed based off of the new value.
        @param addToTemplate If true, all future calls to setSetting will use the new value. No effect when not an expression or when new key.
        '''
        if type(value) == str and value[0] == '@':
            pass
        else:
            self.template[key] = value

        if recomputeAll:
            if addToTemplate:
                self.template[key] = value
                self.settings = self._evaluateAll(self.template)
            else:
                templateCopy = copy.copy(self.template)
                templateCopy[key] = value
                self.settings = self._evaluateAll(templateCopy)
        else:
            if addToTemplate:
                self.template[key] = value
            self.settings[key] = value

    def _evaluate(self, expression, non_expressions):
        assert expression[0] == '@', "Not an expression!"
        
        return eval(expression[1:], copy.copy(non_expressions))
    
    def _evaluateAll(self, to_evaluate):
        non_expressions = {}
        expressions = {}
        for key, value in to_evaluate.items():
            if type(value) == str and value[0] == '@':
                expressions[key] = value
            elif type(value) == str and value[0] != '@':
                non_expressions[key] = value
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
        
def parseCommandLine(command_line, settings):
    '''
    Takes in some command line arguments, and transforms the settings based off of them. To set a setting from command line, syntax is:
    <setting>=<new_value>
    New value may be a string, int, or float. If it is a string, make sure that it is surrounded with quotes!

    @param command_line A list of strings from the command line. You can just put sys.argv here.
    @param settings The settings object to transform.
    @return The transformed settings object.
    '''
    new_settings = copy.copy(settings)
    for i in command_line:
        if '=' in i:
            key = i.split("=")[0]
            value = i.split("=")[1]
            if value[0] == "'" or value[0] == '"':
                value = value.replace("'","").replace('"',"")
            elif "." in value:
                value = float(value)
            else:
                value = int(value)
            new_settings.setSetting(key, value)
    return new_settings