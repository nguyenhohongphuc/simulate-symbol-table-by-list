from StaticError import *
from Symbol import *
from functools import *


def simulate(list_of_commands):
    def process_command(acc,command):
        
        result, symbol_table, count_scope = acc
        part = command.split()
        if not part: 
            raise InvalidInstruction("Invalid command")
        cmd = part[0]
        identifier_name = part[1] if len(part) > 1 else None
        value = part[2] if len(part) > 2 else None
        current_scope = symbol_table[-1] if symbol_table else {}    
        def is_valid_identifier(identifier):
            invalid_chars = "!@#$%^&*()<>~`"
            return (
                identifier[0].islower()
                and all(c.isalnum() or c == "_" for c in identifier)
                and not any(c in invalid_chars for c in identifier)
            )
        if cmd == "INSERT" :
            if command.startswith(" "):
                raise InvalidInstruction("Invalid command")
                
            if len(command.split(" ")) != 3: 
                raise InvalidInstruction(command)
            if not is_valid_identifier(identifier_name):
                raise InvalidInstruction(command)
            if identifier_name in current_scope:
                raise Redeclared(command)
            if value not in ["number", "string"]:  raise InvalidInstruction(command)
            current_scope[identifier_name] = value
            return result + ["success"] , symbol_table, count_scope
        elif cmd == "ASSIGN":
            if command.startswith(" "):
                raise InvalidInstruction("Invalid command")
            invalid_char = "!@#$%^&*_()<>~`"
            if len(command.split(" ")) != 3: 
                raise InvalidInstruction(command)
            if not identifier_name[0].islower() or not is_valid_identifier(identifier_name):
                raise InvalidInstruction(command)
            def find_in_scopes(scopes, identifier):
                if not scopes:
                    raise Undeclared(command)
                if identifier in scopes[-1]:
                    return True
                return find_in_scopes(scopes[:-1], identifier)
           
                
            
            
            if not value.isdigit():
                if not (value.startswith("'") and value.endswith("'")):
                    if not value[0].islower():
                        raise InvalidInstruction(command)
                    else :
                        if not is_valid_identifier(value):
                            raise InvalidInstruction(command)
                        if identifier_name not in current_scope:
                            raise Undeclared(command)
                        if value not in current_scope:
                            raise Undeclared(command)
                        else:
                            if not find_in_scopes(symbol_table, identifier_name):
                                raise Undeclared(command)
                            if current_scope[value] == current_scope[identifier_name]:
                                current_scope[identifier_name] = current_scope[value]
                                return result + ["success"], symbol_table, count_scope
                            else:
                                raise TypeMismatch(command)
                elif not any(char in invalid_char for char in value[1:-1]):
                    if not find_in_scopes(symbol_table, identifier_name):
                        raise Undeclared(command)
                    if current_scope[identifier_name] == "string":
                        
                        current_scope[identifier_name] = value
                        return result + ["success"], symbol_table, count_scope
                    else:
                        raise TypeMismatch(command)
                else:
                    raise InvalidInstruction(command)
            else:
                if not find_in_scopes(symbol_table, identifier_name):
                    raise InvalidInstruction(command)
                if current_scope[identifier_name] == "number":
                    current_scope[identifier_name] = int(value)
                    return result + ["success"], symbol_table, count_scope
                else:
                    raise TypeMismatch(command)
                    
                
                    
            

                        
                        
            #     if value.isdigit():
            #         value = int(value)
            #         if current_scope[identifier_name] == "number":
            #             current_scope[identifier_name] = value
            #             return result + ["success"], symbol_table, count_scope
            #         else:
            #             raise TypeMismatch(command)
            #     elif isinstance(value,str):
            #         value_str = value[1:-1]
            #         invalid_char = "!@#$%^&*()<>"
            #         if any(char in invalid_char for char in value_str):
            #             raise InvalidInstruction(command) 
            #         elif current_scope[identifier_name] == "string":
            #             current_scope[identifier_name] = value
            #             return result + ["success"], symbol_table, count_scope
            #         else:
            #             raise TypeMismatch(command)
        elif cmd == "BEGIN":
            if command.startswith(" "):
                raise InvalidInstruction("Invalid command")
            if len(command.split(" ")) != 1: 
                raise InvalidInstruction(command)
            return result,symbol_table + [{}], count_scope + 1
        elif cmd == "END":
            if command.startswith(" "):
                raise InvalidInstruction("Invalid command")
            if len(command.split(" ")) != 1: 
                raise InvalidInstruction(command)
            if count_scope > 0 :
                return result, symbol_table[:-1], count_scope - 1
            else:
                raise UnknownBlock()
        elif cmd == "LOOKUP":
            if command.startswith(" "):
                raise InvalidInstruction("Invalid command")
            if len(command.split(" ")) != 2:
                raise InvalidInstruction(command)
            if not identifier_name[0].islower() or not is_valid_identifier(identifier_name):
                raise InvalidInstruction(command)
            def find_identifier(symbol_table, identifier, level=len(symbol_table) -1):
                if not symbol_table:
                    return False, -1
                current_scope1 = symbol_table[-1]
                if identifier in current_scope1:
                    return True, level
                return find_identifier(symbol_table[:-1], identifier, level - 1)
            found, level = find_identifier((symbol_table), identifier_name)
            if found:
                return result + [str(level)], symbol_table, count_scope
            else:   
                raise Undeclared(command)
        elif cmd == "PRINT":
            if command.startswith(" "):
                raise InvalidInstruction("Invalid command")
            if len(command.split(" ")) != 1:
                raise InvalidInstruction(command)
            def process_scopes(scopes, level, seen):
                if not scopes:
                    return []
                current_scope2 = scopes[-1]
                return [
                    f"{key}//{level}"
                    for key in reversed(list(current_scope2.keys()))
                    if key not in seen and not seen.add(key)
                ] + process_scopes(scopes[:-1], level - 1, seen)
            return result + [' '.join(reversed(process_scopes(symbol_table, len(symbol_table) - 1, set())))], symbol_table, count_scope
        elif cmd == "RPRINT":
            if command.startswith(" "):
                raise InvalidInstruction("Invalid command")
            if len(command.split(" ")) != 1:
                raise InvalidInstruction(command)
            def process_scopes(scopes, level, seen):
                if not scopes:
                    return []
                current_scope3 = scopes[-1]
                keys = [
                    f"{key}//{level}"
                    for key in reversed(list(current_scope3.keys()))
                    if key not in seen and not seen.add(key)
                ]
                return keys + process_scopes(scopes[:-1], level - 1, seen)

            seen = set()
            level = len(symbol_table) - 1
            stack = process_scopes(symbol_table, level, seen)
            return result + [' '.join((stack))], symbol_table, count_scope
        else:
            raise InvalidInstruction("Invalid command")

                
                
                    


                    

            

    init = ([],[{}],0)
    result, symbol_table, count_scope = reduce(process_command,list_of_commands,init)
    if count_scope > 0:
        raise UnclosedBlock(count_scope)
    
    
    return result
    
    """
    Executes a list of commands and processes them sequentially.

    Args:
        list_of_commands (list[str]): A list of commands to be executed.

    Returns:
        list[str]: A list of return messages corresponding to each command.
    """
