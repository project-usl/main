filename = None
import shutil as sh
import sys
import os
import math
from random import random
from random import choices

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  E = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

if not filename:
  try : 
    filename = sys.argv[1:][0]
    outfilename = sys.argv[1:][1] if len(sys.argv) > 2 else None
  except IndexError :
    print(bcolors.FAIL,'fatal : filename was not provided.')
    exit()
if not os.path.exists(filename):
    print(bcolors.FAIL,f'fatal : not file was found with the path >{filename}<.')
    exit()
file = open(filename,'r')
instructions = file.read()
strict = False
def formatInstr(instr):
  return instr.replace('{\n','{').replace('\\\n','').replace('?\n','?').replace('\n}','}').replace('\n)',')').replace(',,\n',',,').replace('(\n','(').replace(',\n',',').replace('||\n','||').replace(':\n ','; ').replace('\n',';').split(';')
instructions = formatInstr(instructions)
file.close()
i = 0
Active = False
cmd_cmdArgSep = '@'
cmd_ArgSep = ' '
nullArgOp = '0'
safe = True
stopLoop = False 
continueLoop = False
isFunctionRunning = False
c_argumentsObject = {}
c_funcData = {}
c_classData = {}
c_paramsObject = {}
arthOp = '+-*/%<>~^|&'
indentationMark = '  '

Vars = {'object':'<empty>','cache':'null'}
SuperVars = {'version':'usl.misc.1.13','auth':'yaver','I':None,'n1':-1,'nl':'\n',
'cache' : '#CACHE', 'chn' : ':', 'bs' : '(','bc': ')','c':',','inf':math.inf,'r':None,
'fr':None, 'PI': 22/7
}
Scopes = {}
UniversalFuncs = ['up','low','str','int','bool','len','complex','type','long','flip','n','float','input','abs','typeof','rand','list','split','of','replace','rsplit','trim','triml','trimr','round','parseInt','index','isDecimal','version','part','extract','abbr','gc']
MathFuncs = ['acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 'comb', 'copysign', 'cos', 'cosh', 'degrees', 'dist', 'erf', 'erfc', 'exp', 'expm1', 'fabs', 'factorial', 'floor', 'fmod', 'frexp', 'fsum', 'gamma', 'gcd', 'hypot', 'inf', 'isclose', 'isfinite', 'isinf', 'isnan', 'isqrt', 'lcm', 'ldexp', 'lgamma', 'log', 'log10', 'log1p', 'log2', 'modf', 'nextafter', 'perm', 'pow', 'prod', 'radians', 'remainder', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'trunc', 'ulp']
['sin','cos','tan','cot','cosec','sec','sqrt','gcd']
Functions =  {}
math = ''
operatorSeparator = '¢'
whichFunctionRunning = ''
warnings = True
WarningsObject = {'disableWarningMessage':'Simply Turn Off Warings By Runing "warnings False"'}
cachedExprs = {}
imports = []
libs = []
module_ext = '.hx.py'
moddir = 'modules'
superCommand = None
isLooping = False
funcId = 0
Classes = {}
isClassRunning = False
whichClassRunning = ''
whichBlockRunning = 'global'
errorHeader = f"  error at File {filename} at line"
SuperVars["errorHeader"] = errorHeader
modules = []
fors = {}
linesToSkip = set()
Errors = [
  'UnknownError',
  'SizeNotDeclaredError',
  'DatabaseNotFoundError',
  'DatabaseCorruptedError',
  'UnsafeToProceed',
  'Type Error',
  'Type Error',
  'Line was out of range.',
  'InvalidCommandError',
  'Block Not Given',
  'File Was Not Found.',
  'Invalid Python.',
  'No locals In Block Methods',
  '13',
  'The Functional Group Was Not Found.',
  'Only command given.',
  'Function was not found.',
  'Mismatch In Arguments',
  'NoArgumentsInGlobal',
  'Only Inside A Function',
  'InvalidArgumentError',
  'Cannot Delete Super Varibles. Super Varibles Are Immutable',
  'Arguments Are Not Avalible In Global Block.',
  'Object Was Not Found.',
  'Varible Was Not Found.',
  'Argument Was Not Found.',
  'Super Varible Was Not Found.',
  'Key Was Not Found.',
  'Arguments Not Formatted As Expected.',
  'Index Not Found In String.',
  'The Module Was Not Found.',
  'Illegal Name Of Module Given During Import.',
  'Module resulted in an error.',
  'Int Function Gave An Error.',
  'Class was not found.',
  '"local" is not available outside function block',
  'Local was not found.',
  "Can't return from Global.",
  'Duplicate Arguments Found.',
  'Syntax Error.',
  'No local object binded to block.',
  'Linker File Was Not Found.',
  'Cannot Divide by Zero',
  'Invalid Name.',
  'No for statement found for given id.',
  'Index Out Of Range',
  'Array Was Not Found.',
  'Object/Array Was Not Found.',
  'Unexpected Intended block.'

]

def split_outside_quotes(string, sep):
  substrings = []
  in_quote = False
  split_from = 0
  string_len = len(string)
  sep_len = len(sep)
  i = 0
  while i < string_len:
    if string[i] == "'":
      in_quote = not in_quote
    elif not in_quote:
      if string[i:i+sep_len] == sep:
        substrings.append(string[split_from:i])
        i = split_from = i + sep_len
        continue
    i += 1
  substrings.append(string[split_from:])
  return substrings

def addFunction(name):
  UniversalFuncs.append(name)


def split_outside_esqbrs(string, sep):
  substrings = []
  in_quote = False
  split_from = 0
  string_len = len(string)
  sep_len = len(sep)
  i = 0
  while i < string_len:
    if string[i] == ']':
      in_quote = not in_quote
    elif not in_quote:
      if string[i:i+sep_len] == sep:
        substrings.append(string[split_from:i])
        i = split_from = i + sep_len
        continue
    i += 1
  substrings.append(string[split_from:])
  return substrings

def sort(array):
  if typeof(array) != 'list':
    Error(5)
  return sorted(array)

addFunction("sort")

def addition(array):
  if typeof(array) != 'list':
    Error(5)
  return sum(array)

addFunction("addition")

def abbr(s):
  s = s.split(' ')
  abbr = ''
  for i in range(0,len(s)):
    abbr += s[i][0]
  return abbr


def of(string,i):
  if(str(i).isdecimal()):
    i = int(i)
    if(i >= len(string)):
      Error(29)
    else : return string[i]
  else: Error(5)

def isValidName(string):
  if len(string) == 0: 
    print('name cannot be empty')
    return False
  if string[0].isdecimal():
    print('name cannot start with a number')
    return False
  allowed_chars = set(("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"))
  validation = set((string))
  return validation.issubset(allowed_chars)

def isValidFuncName(string):
  if len(string) == 0: 
    print('method name cannot be empty')
    return False
  if string[0].isdecimal():
    print('method name cannot start with a number')
    return False
  allowed_chars = set(("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_."))
  validation = set((string))
  return validation.issubset(allowed_chars)

def index(string,i,newValue):
  if(str(i).isdecimal()):
    i = int(i)
    if(i > len(string)):
      Error(29)
    else :
      string = string[:i] + str(newValue)[0] + string[i + 1:]
      return string
  else: Error(5)

def Error(index,line = None, details=None):
  if (type(details).__name__ == 'function'):
    details ()
  global i,safe,Active
  line = line or i
  errorLine2 = ''
  if isFunctionRunning and whichBlockRunning == "function":
    print(f'error in method >{whichFunctionRunning}< .')
    if Functions[whichFunctionRunning]["type"] in ["func","block","=>"]:
      errorLine = c_funcData[whichFunctionRunning]['instrs'][c_funcData[whichFunctionRunning]['c_blockIndex']][2:]
    else:
      errorLine = c_funcData[whichFunctionRunning]['instrs'][c_funcData[whichFunctionRunning]['c_blockIndex']][7:]
    line = f'f({whichFunctionRunning}):{c_funcData[whichFunctionRunning]["c_blockIndex"]+1}'
  elif isClassRunning and whichBlockRunning == 'class':
    print(f'error in class >{whichClassRunning}< .')
    errorLine = Classes[whichClassRunning]['instrs'][c_classData[whichClassRunning]['line']]
    line = f'@{whichClassRunning}:{c_classData[whichClassRunning]["line"]+1}'
  else:
    errorLine = instructions[line-1]
  if Active:
    ErrorString = """err"""
  else:
    ErrorString = f"""{errorHeader}, {line}
    {errorLine2}  {bcolors.OKCYAN} '{errorLine}'
{bcolors.FAIL + Errors[index].upper() + bcolors.E}"""
  print(ErrorString)
  import sys
  sys.exit()

n = lambda n:n*-1
flip = lambda cond: not eval(parseExpr(str(cond)))
typeof = lambda t: type(t).__name__
trim = lambda s: s.strip()
triml = lambda s: s.lstrip()
trimr = lambda s: s.rstrip()
up = lambda s: s.upper()
low = lambda s: s.lower()
rand = lambda i : random() * i
replace = lambda string,a,b: string.replace(a,b)
rsplit = lambda s,d,l = -1: s.rsplit(d,l)
split = lambda s,d=None,l = -1: s.split(d,l)
isDecimal = lambda i: str(i).isdecimal()
version = lambda : 'v.1.57.0'
Function = lambda args,instrs : {'args':args,'instrs':instrs}
extract = lambda v,ex : eval(str(v) + f'["{ex}"]')
part = lambda s,a,b='*' : s[a:] if b == '*' else s[a:b]
removeSpaces = lambda expr: ''.join(split_outside_quotes(expr," "))
gc = lambda : i - 1

def parseInt(x):
  try:
    return int(x)
  except Exception as e:
    print('Debug:  ',e)
    Error(33)

def hasDuplicateArgs(arr):
  duplicateArgs = []
  if len(set(arr)) == len(arr) :
      print('Here')

    return True
  else:
    for arg in arr:
      if arr.count(arg) > 1 and not arg in duplicateArgs:
        duplicateArgs.append(arg)
    print('Here')
    print(duplicateArgs)
    return False


def writeFile(args,data):
  filename =  eval(parseExpr(objectifyArgs(args)['f']))
  f = open(filename,'w')
  f.write(str(eval(parseExpr(data).replace('\n','\\n'))))
  f.close()

def appendFile(args,data):
  filename =  eval(parseExpr(objectifyArgs(args)['f']))
  f = open(filename,'a')
  f.write(str(eval(parseExpr(data).replace('\n','\\n'))))
  f.close()

def readFile(path):
  if os.path.exists(path):
    f = open(path,'r')
    data = f.read()
    f.close()
  else:
    print (f'No file found with path >{path}<.')
    Error(10)
  return data

def addVar(name,value,isGlobal,scope):
  if isGlobal:
    if isValidName(name):
      Vars[name] = value
    else:
      print(f'invalid name of the varible >{name}<.')
      Error(43)
  else:
    if not isValidName(scope):
      print(f'invalid name of the object >{scope}<.')
      Error(43)
    if not isValidName(name):
      print(f'invalid name of the key >{name}<.')
      Error(43)
    if not scope in Scopes:
      Scopes[scope] = {}
    Scopes[scope][name] = value

def createVar(arg,cmdArgs):
  argA = arg.split('=',1)
  if not ':' in argA[0]:
    updateVar(arg)
    return
  varName = arg.split('=',1)[0].split(':',1)[1]
  varType = arg.split('=',1)[0].split(':',1)[0]
  varVal = eval(parseExpr(arg.split('=')[1]))
  isGlobal = True if cmdArgs == '0' else False
  scope = None if isGlobal else objectifyArgs(cmdArgs)['sc']
  if(varType == 'int'):
    addVar(varName,int(varVal),isGlobal,scope)
  elif(varType == 'str'):
    addVar(varName,str(varVal),isGlobal,scope)
  elif(varType == 'float'):
    addVar(varName,float(varVal),isGlobal,scope)
  elif(varType == 'bool'):
    varVal = False if arg.split('=')[1] == 'False' else True
    addVar(varName,varVal,isGlobal,scope)
  else:
    print(f'type >{varType}< is not recognised')
    Error(6)



def parseExpr(expr):
  if not expr :
    return "None"
  exk = expr
  err = False
  brokenExpr = breakExpr(expr)
  exprs = brokenExpr["exprs"]
  current_ops = brokenExpr["operators"]
  for i in range(0,len(exprs)):
    exprObject = exprs[i].replace(')','(').split('(')
    startingBrackets = False
    exprIndex = None
    for j in range(0,len(exprObject)):
      if exprObject[j]:
        exprs[i] = exprObject[j]
        exprsIndex = j
        startingBrackets = True
      else:
        exprObject[j]= ')' if startingBrackets else '('
    if exprs[i] == '':
      print('empty unit given')
      Error(39)
    if(exprs[i][0] == "'" and exprs[i][-1] == "'"): pass
    elif exprs[i][0:2] == "f'" and exprs[i][-1] == "'":
      formats = list(set([ t for t in exprs[i].split() if t.startswith('#') and not t.endswith("'")]))
      for f in formats: exprs[i] = exprs[i].replace(' '+f+' ',f"' + str({parseExpr(f[1:])})+'")
      exprs[i] = exprs[i][1:]
    elif exprs[i][0] == '!': exprs[i] = f'not( {parseExpr(exprs[i][1:])} )'
    elif exprs[i][0] in '1234567890-' : pass
    elif exprs[i][-1] == ']' and exprs[i][0] != '[':
      exprs[i] = exprs[i].split('[',1)
      exprs[i] = parseFunclExpr(exprs[i][0], exprs[i][1][:-1])
    elif exprs[i][0] == '$':
      if exprs[i][1] == '$':
        if(exprs[i][2:] in SuperVars):
          exprs[i] = 'SuperVars["'+exprs[i][2:]+'"]'
        else:
          print(f'super varible >{exprs[i][2:]}< was not found.')
          Error(26)
      elif (isFunctionRunning and not isClassRunning) or (isFunctionRunning and isClassRunning and whichBlockRunning == 'function'):
        if '..' in exprs[i]:
          exprs[i] = exprs[i][1:].split('..',1)
          exprs[i] = 'c_funcData[whichFunctionRunning]["c_argumentsObject"]["' + exprs[i][0] + '"]["' + str(eval(parseExpr(exprs[i][1]))) + '"]'
        elif('.' in exprs[i]):
          exprs[i] = exprs[i][1:].split('.',1)
          exprs[i] = 'c_funcData[whichFunctionRunning]["c_argumentsObject"]["' + exprs[i][0] + '"]["' + exprs[i][1] + '"]'
        else:
          exprs[i] = 'c_funcData[whichFunctionRunning]["c_argumentsObject"]["' + exprs[i][1:] + '"]'
      elif (isClassRunning and not isFunctionRunning) or (isFunctionRunning and isClassRunning and whichBlockRunning == 'class'):
        if '..' in exprs[i]:
          exprs[i] = exprs[i][1:].split('..',1)
          exprs[i] = 'c_classData[whichClassRunning]["arguments"]["' + exprs[i][0] + '"]["' + str(eval(parseExpr(exprs[i][1]))) + '"]'
        elif('.' in exprs[i]):
          exprs[i] = exprs[i][1:].split('.',1)
          exprs[i] = 'c_classData[whichClassRunning]["arguments"]["' + exprs[i][0] + '"]["' + exprs[i][1] + '"]'
        else:
          exprs[i] = 'c_classData[whichClassRunning]["arguments"]["' + exprs[i][1:] + '"]'
      else:
        print(f'no block found to provide arguments, here at >{exprs[i]}< .')
        Error(22)
    elif exprs[i][0] == '@':
      new(exprs[i][1:])
      exprs[i] = str(SuperVars['r'])
    elif(exprs[i][0] == '.'):
      if not isFunctionRunning:
        print(f'no function found to provide locals, here at >{exprs[i]}< .')
        Error(35)
      if exprs[i] == '.':
        if whichFunctionRunning in Scopes:
          exprs[i] = 'Scopes[whichFunctionRunning]'
        else:
          print('no local object binded to block, here at >.<')
          Error(40)
      else:
        if not whichFunctionRunning in Scopes:
          print(f'no local object binded to block, here at >{exprs[i]}<')
          Error(40)
        else:
          if exprs[i][1:] in Scopes[whichFunctionRunning]:
            exprs[i] = f'Scopes[whichFunctionRunning]["{exprs[i][1:]}"]'
          else:
            print(f'local >{exprs[i]}< was not found.')
            Error(36)
    elif(exprs[i][0] == ':' and ':' != exprs[i][1] and exprs[i].count(':') % 2 == 0):
      func = exprs[i].split(':',2)[1]
      funcExpr = exprs[i].split(':',2)[2]
      exprs[i] = parseFunclExpr(func,funcExpr)
    elif(exprs[i][0] == ":" and exprs[i][-1] == ":"):
      exprs[i] = parseFunclExpr(exprs[i][1:-1],"")
    elif('..' in exprs[i] and '..' != exprs[i][0:2]):
       exprs[i] = exprs[i].split('..',1)
       if(exprs[i][0] in Scopes):
         key = eval(parseExpr(exprs[i][1]))
         if(typeof(Scopes[exprs[i][0]]) == 'list'):
           if int(key) < len(Scopes[exprs[i][0]]):
             exprs[i] = f'Scopes["{exprs[i][0]}"][{key}]'
           else:
             print(f'length is just >{len(Scopes[exprs[i][0]])}<, tried to access >{key}< \nhere at >{"..".join(exprs[i])}<')
             Error(45)
         else:
           if ( key in Scopes[exprs[i][0]]):
             exprs [i] = 'Scopes["' + exprs[i][0] +'"][' + parseExpr(exprs[i][1]) + ']'
           else:
             print(f'key {exprs[i][1]} was not found here at, >{"..".join(exprs[i])}< .')
             Error(27)
       else:
         print(f'object/array >{exprs[i][0]}< was not found here at >{"..".join(exprs[i])}<.')
         Error(47)
    elif('.' in exprs[i] and '.' != exprs[i][0]):
      exprs[i] = exprs[i].split('.',1)
      if (exprs[i][0] in Scopes):
        if typeof(Scopes[exprs[i][0]]) == 'list':
          print(f'>{exprs[i][0]}< is not a object, but is an array')
          Error(5)
        if (exprs[i][1] in Scopes[exprs[i][0]]):
          exprs[i] = 'Scopes["' + exprs[i][0] + '"]["' + exprs[i][1] + '"]'
        else:
          print(f'key >{exprs[i][1]}< was not found here at, >{".".join(exprs[i])}<')
          Error(27)
      else:
        print(f'object >{exprs[i][0]}< was not found here at, >{".".join(exprs[i])}<')
        Error(23)
    elif(exprs[i] == 'False' or exprs[i] == 'True'): pass
    elif exprs[i][0] in ['{','['] and exprs[i][-1] in ['}',']']:
      if(exprs[i][1:-1] in Scopes):
        exprs[i] = 'Scopes["' + exprs[i][1:-1] + '"]'
      else:
        if exprs[i][0] == '{':
          print(f'object >{exprs[i][1:-1]}< was not found here at, >{exprs[i]}<')
          Error(23)
        else:
          print(f'array >{exprs[i][1:-1]}< was not found here at, >{exprs[i]}<')
          Error(46)
    else:
      if exprs[i] in Vars:
        exprs[i] = 'Vars["'+exprs[i]+'"]'
      else:
        if not isValidName(exprs[i]):
          print(f'>{exprs[i]}< is an invalid expression' )
          Error(39)
        if(exprs[i] in Scopes):
          print(f'for >{exprs[i]}< did you mean ',end='')
          if typeof(Scopes[exprs[i]]) == 'list':
            print('[' + exprs[i] + ']' )
          else:
            print('{' + exprs[i] + '}' )
        else : print(f'varible >{exprs[i]}< was not found.')
        Error(24)
    exprObject[exprsIndex] = exprs[i]
    exprs[i] =  ''.join(exprObject)
  expr = ''
  for i in range(0,len(exprs)):
    expr += exprs[i]
    if i < len(current_ops):
      expr += current_ops[i]
  return '""' if err else expr


def parseFunclExpr(func,expr=""):
  global math
  pexpr = expr
  if(expr == ""): 
    pass
  else:
    expr = breakArgsList(expr)
    for i in range(0,len(expr)):
      expr[i] = parseExpr(expr[i])
    expr = ','.join(expr)
  if(func in UniversalFuncs):
    return f'{func}({expr})'
  elif func in MathFuncs:
    if not math: import math
    return f'math.{func}({expr})'
  elif func in Functions:
    SuperVars['r'] = None
    if expr.strip() == '':
      call(func,'0')
      returnedValue = SuperVars['r']
    else:
      call(func+':'+pexpr,'0')
      returnedValue = SuperVars['r']
    if typeof(returnedValue) == 'str':
      return "'" + returnedValue.replace("'","\\'").replace('/n','\\n') + "'"
    else:
      return str(returnedValue)
  else:
    print(f'This Function >{func}< Was Not Found.')
    Error(14)



def printOut(arg):
  arg = split_outside_quotes(arg,',,')
  for i in range(0,len(arg)):
    print(eval(parseExpr(arg[i]).replace('\n','\\n')),end=" ")
  print('')


def breakExpr(expr):
  string = False
  temp = False
  exprList = list(expr)
  opList = []
  for c in exprList:
    if c == "'" : string = not string
    if c == "[" and not string : temp = True
    elif c == ']' and not string : temp = False
    if string or temp : continue
    if c in arthOp:
      match c:
        case '^' : opList.append('!=')
        case '~' : opList.append('==')
        case '|' : opList.append(' or ')
        case '&' : opList.append(' and ')
        # := WARLUS OPERATIOR IS HIGHLY EXPERIMENTAL;
        # case ':' : opList.append(' := ')
        case _ : opList.append(c)
      expr = expr.replace(c,operatorSeparator)
  return {"exprs" : expr.split(operatorSeparator), "operators" : opList}

def breakArgsList(expr):
    string = False
    temp = False
    expr = list(expr)
    for i,c in enumerate(expr):
      if c == "'" : string = not string
      if c == "[" and not string : temp = True
      elif c == ']' and not string : temp = False
      if string or temp : continue
      if c == ',':
        expr[i] = operatorSeparator
    return ''.join(expr).split(operatorSeparator)
  


def parsePrimitveObject(pre_obj):
  if pre_obj == '{}' : return {}
  pre_obj = split_outside_quotes(pre_obj[1:-1],',')
  obj = {}
  for i in range(0,len(pre_obj)):
    if(':' in pre_obj[i]):
      pre_obj[i] = split_outside_quotes(pre_obj[i],':')
      if not isValidName(pre_obj[i][0]):
        print(f'invalid name for key >{pre_obj[i][0]}<')
        Error(43)
      obj[pre_obj[i][0]] = eval(parseExpr(pre_obj[i][1]))
    else:
      if(pre_obj[i][0:2] == '$$'):
        if pre_obj[i][2:] in SuperVars:
          obj[pre_obj[i]] = SuperVars[pre_obj[i][2:]]
        else:
          Error(26)
      else:
        if pre_obj[i] in Vars:
          obj[pre_obj[i]] = Vars[pre_obj[i]]
        else:
          Error(24)
  return obj

def colorise(string):
  print(string.replace('>',bcolors.FAIL).replace('<',bcolors.E))

def updateObject(arg):
  arg = arg.split('=',1)
  objectName = arg[0]
  if not isValidName(objectName):
    print(f'invalid name of the object >{objectName}<.')
    Error(43)
  objectValue = arg[1]
  if not objectName in Scopes:
    Scopes[objectName] = {}
    Scopes[objectName] = parsePrimitveObject(objectValue)
  else:
    Scopes[objectName].update(parsePrimitveObject(objectValue))



 
def updateVar(arg):
  varName = arg.split('=')[0]
  varVal = arg.split('=')[1]
  if '..' in varName and varName[0:2] != '..':
    varName = varName.split('..')
     #      key                            value  idenfr objectname
    addVar(str(eval(parseExpr(varName[1]))),varVal,False,varName[0])
    return
  elif '.' in varName and varName[0] != '.':
    varName = varName.split('.')
    #      key        value  idenfr objectname
    addVar(varName[1],varVal,False,varName[0])
    return
  addVar(varName,eval(parseExpr(varVal)),True,'')
  

def read(cmdArgs,arg):
  arg = eval(parseExpr(arg))
  if 'v' in objectifyArgs(cmdArgs):
    addVar(objectifyArgs(cmdArgs)['v'],readFile(arg),True,'')
  else:
    SuperVars['r'] = readFile(arg)

def condLoop(arg):
  global i
  instructions[i - 1] = f'loop _ while {arg}'
  i -= 1

def loop(count,args):
  global continueLoop
  args = objectifyArgs(args)
  variable = args['v'] if 'v' in args else None
  isLooping = True
  if 'while' in count:
    count = count.rsplit('while',1)
    condition = count[1]
    count = count[0]
  else:
    condition = None
  count = int(eval(parseExpr(count))) if count != "_" else  None
  currentLoopInstr = []
  gi = 0
  SuperVars['n'] = 1
  if isFunctionRunning:
    global whichFunctionRunning,stopLoop
    c_funcData[whichFunctionRunning]['c_blockIndex'] += 1
    for j in range(c_funcData[whichFunctionRunning]['c_blockIndex'],len(c_funcData[whichFunctionRunning]['instrs'])):
      if c_funcData[whichFunctionRunning]['instrs'][j][2:4] == '  ':
        currentLoopInstr.append(c_funcData[whichFunctionRunning]['instrs'][j][2:])
        c_funcData[whichFunctionRunning]['c_blockIndex'] = j - 1
      else : 
        c_funcData[whichFunctionRunning]['c_blockIndex'] = j - 1
        break
  else:
    global i
    while i < len(instructions):
      if instructions[i][0:2] != '  ' and len(instructions[i].replace(' ','')) != 0:
        break
      currentLoopInstr.append(instructions[i])
      i += 1
  k = 0
  if condition: currentLoopInstr.insert(0,f"if ({condition}) ? pass '' ? break loop")
  if len(currentLoopInstr) == 0:
    print('No block given to the loop.')
    Error(9)
  while True:
    if count != None :
      if gi == count : break
    if variable == None: SuperVars['I'] = gi
    else: Vars[variable] = gi
    for k in range(0,len(currentLoopInstr)):
      instr = parseInstructions(currentLoopInstr[k].lstrip())
      if stopLoop :
        stopLoop = False
        isLooping = False
        return
      elif continueLoop:
        continueLoop = False
        break
      execute(instr['cmd'],instr['cmdArgs'],instr['arg'])
    gi += 1
  SuperVars['I'] = None
  isLooping = False
# c_instr.strip() == '' 
def cloop(arg):
  global i
  loop_instructions = []
  c_i = i - 1
  while(i < len(instructions)):
    c_instr = instructions[i]
    if c_instr[:2] != '  ':
      breakIndex = i
      break
    loop_instructions.append(c_instr[2:])
    instructions[i] = instructions[i][2:]
    i += 1
  looplen = len(loop_instructions)
  instructions[c_i] = f'ifnot {arg} ? move {c_i + looplen + 2}'
  instructions.insert(breakIndex,f'move {c_i}')
  i = c_i
  f = open('ssl','w')
  f.write('\n'.join(instructions))
  f.close

def createFunction(arg,cmd):
  if ':' in arg:
    name = arg.split(':',1)[0]
    params = arg.split(':',1)[1].split(',')
  else:
    name = arg
    params = []
  if hasDuplicateArgs(params):
    Error(38)
  if not isValidFuncName(name):
    print(f'>{name}< is not a valid name of a method.')
    Error(43)
  instrs = []
  global i
  while i < len(instructions):
    if instructions[i][0:2] != '  ' and len(instructions[i].replace(' ','')) != 0: break
    instrs.append(instructions[i])
    i += 1
  if len(instrs) == 0:
    print('No block given with method.')
    Error(9)
  f_data = Function(params, instrs)
  f_data['type'] = cmd
  Functions[name] = f_data


def delete(arg):
  if(arg[0] == '$'):
    if(arg[1] == '$'):
      Error(21)
    elif isFunctionRunning:
      if(arg[1:] in c_funcData[whichFunctionRunning]['c_argumentsObject']):
        del c_funcData[whichFunctionRunning]['c_argumentsObject'][arg[1:]]
      else:
        Error(25)
    elif not isFunctionRunning:
      Error(22)
  elif(arg[0] == '{' and arg[-1] == '}'):
    if(arg[1:-1] in Scopes):
      del Scopes[arg[1:-1]]
    else:
      Error(23)
  else:
    if(arg in Vars):
      del Vars[arg]
    else:
      Error(24)
      

def call(arg,cmdArgs):
  global c_argumentsObject,isFunctionRunning,c_funcData,whichFunctionRunning,funcId,whichBlockRunning
  if ':' in arg:
    name = arg.split(':',1)[0]
    arguments = arg.split(':',1)[1]
    if ('=') in arguments : 
      arguments = arguments.rsplit('=',1)
      varible = arguments[1]
      arguments = split_outside_quotes(arguments[0],',')
    else:
      varible = None
      arguments = split_outside_quotes(arguments,',')
  else:
    if '=' in arg:
      arg = arg.rsplit('=',1)
      varible = arg[1]
      name = arg[0]
    else:
      name = arg
      varible = None
    arguments = []
  if not name in Functions:
    Error(16)
    return
  whichFunctionRunning = name
  c_funcData[name] = Functions[name]
  if len(c_funcData[name]['args']) != len(arguments):
    print('expected',len(c_funcData[name]['args']),'argument(s)',len(arguments),'given.')
    Error(17)
    return
  isFunctionRunning = True
  whichFunctionRunning = name
  c_funcData[name]['c_argumentsObject'] = {}
  if(Functions[name]['type'] != 'block'): Scopes[name] = {}
  for i in range(0, len(arguments)):
    if '@' in c_funcData[name]['args'][i]:
      argName =  c_funcData[name]['args'][i].split('@')[0]
      argFunc =  c_funcData[name]['args'][i].split('@')[1]
      c_funcData[name]['c_argumentsObject'][argName] = eval(argFunc + '(' + parseExpr(arguments[i]) + ')')
    else:
      c_funcData[name]['c_argumentsObject'][c_funcData[name]['args'][i]] = eval(parseExpr(arguments[i]))
  c_funcData[whichFunctionRunning]['c_blockIndex'] = 0
  while c_funcData[name]['c_blockIndex'] < len(c_funcData[name]['instrs']):
    whichFunctionRunning = name
    instr = parseInstructions(c_funcData[name]['instrs'][c_funcData[name]['c_blockIndex']].lstrip())
    whichBlockRunning = 'function'
    if instr['cmd'] == 'return':
      if varible:
        if varible == '>>' : printOut(instr['arg'])
        else : expression(varible + '=' + str(eval(parseExpr(instr['arg']))))
      else:
        SuperVars['r'] = eval(parseExpr(instr['arg']))
      isFunctionRunning = False
      c_argumentsObject = {}
      c_funcData[name] = {}
      if(Functions[name]['type'] != 'block'): del Scopes[name]
      return
    execute(instr['cmd'],instr['cmdArgs'],instr['arg'])
    isFunctionRunning = True
    c_funcData[name]['c_blockIndex'] += 1
  isFunctionRunning = False
  c_argumentsObject = {}
  c_funcData[name] = {}
  if(Functions[name]['type'] != 'block'): del Scopes[name]



def terinary(arg,flip=False):
  arg = split_outside_quotes(arg,'?')
  cond = eval(parseExpr(removeSpaces(arg[0])))
  if flip : cond = not cond
  if len(arg) == 2 and (not cond) : return
  toBeExecuted = 1 if cond else 2
  if arg[toBeExecuted].strip() == '_' : return
  arg[toBeExecuted] = split_outside_quotes(arg[toBeExecuted],'||')
  for i in range(0,len(arg[toBeExecuted])):
    instrs = parseInstructions(arg[toBeExecuted][i].strip())
    execute(instrs['cmd'],instrs['cmdArgs'],instrs['arg'])

def init_cond_statement(cond):
  pass

def exitProgram(arg):
  if not arg in ['force','program','block','function','loop']:
    print(f'cannot break, >{arg}< is not recognised.')
    Error(20)
    return
  if(arg == 'program'):
    exit()
  elif arg == 'loop':
    global stopLoop
    stopLoop = True

def as_obj(arg):
  try:
    arg = arg.split('=',1)
    value = eval(parseExpr(arg[1]))
    if(type(value).__name__  == 'dict'):
      Scopes[arg[0]] = value
    else:
      print(f">obj< does not take type >{type(value).__name__}<.")
      Error(5)
  except Exception as e:
    print(e)
    Error(28)

def as_arr(arg):
  try:
    arg = arg.split('=',1)
    value = eval(parseExpr(arg[1]))
    if(type(value).__name__  == 'list'):
      Scopes[arg[0]] = value
    else:
      print(f">arr< does not take type >{type(value).__name__}<.")
      Error(5)
  except Exception as e:
    print(e)
    Error(28)

def expression(arg,printable=False):
  arg = removeSpaces(arg)
  if ('++' in arg): arg = arg.replace('++','') + '+=1'
  elif ('--' in arg): arg = arg.replace('--','') + '-=1'
  if  ('+=' in arg): arg = [arg.split('+=',1),'+=']
  elif('-=' in arg): arg = [arg.split('-=',1),'-=']
  elif('*=' in arg): arg = [arg.split('*=',1),'*=']
  elif('/=' in arg): arg = [arg.split('/=',1),'/=']
  elif('@=' in arg): arg = [arg.split('@=',1),'@=']
  elif('%=' in arg): arg = [arg.split('%=',1),'%=']
  elif('&=' in arg): arg = [arg.split('&=',1),'&=']
  elif('=' in arg): arg = [arg.split('=',1),'=']
  else:
    print(f'keyword >{instructions[i-1].split(" ")[0]}< is not recognised')
    Error(8)
    return
  var = arg[0][0]
  expr = arg[0][1]
  operator = arg[1]
  if operator == '@=':
    arr = expr.split(':',2)
    arr[1] =  ':' + arr[1] + ':' + var
    if not arr[2] == '' : arr[1] += ','
    expression = var + "=" + ''.join(arr)
    updateVar(expression)
    return
  if len(operator) == 2:
    expression = var + "=" + var + operator[0] + expr
  else:
    expression = var + "=" + expr
  updateVar(expression)


def import_module(module_name,moddir = moddir,module = False):
  if('/' in module_name or '\\' in module_name):
    Error(31)
    return
  module = readFile(moddir + '/' + module_name + module_ext)
  
  try:
    exec(module,globals(),globals())
    if module: modules.append(module_name)
    else: libs.append(module_name)
    
  except Exception as e:
    print('debug : ',e)
    Error(32)

def local(arg):
  if isFunctionRunning:
    if Functions[whichFunctionRunning]['type'] =='block':
      print(f'cannnot create locals, >{whichFunctionRunning}<is a block not a function')
      Error(12)
    if '=' in arg:
      arg = arg.split('=',1)
      name = arg[0]
      value = arg[1]
    else:
      print(f'no lhs found for local >{arg}<')
      Error(39)
    Scopes[whichFunctionRunning][name] = eval(parseExpr(value))
  else:
    Error(35)

  
def createLambda(arg):
  arg = arg.split(':',2)
  name = arg[0]
  arguments = arg[1].split(',')
  if not isValidFuncName(name):
    print(f'>{name}< is not a valid name of a lambda.')
    Error(43)
  if len(arguments) == 1 and arguments[0] == '' : arguments = []
  if hasDuplicateArgs(arguments):
    Error(38)
  expression = ['return ' + arg[2]]
  Functions[name] = Function(arguments, expression)
  Functions[name]['type'] = 'lambda'

def link(arg):
  global i
  filename = str(eval(parseExpr(arg)))
  if not os.path.exists(filename):
    print(f'linker file >{filename}< was not found.')
    Error(41)
  file = open(filename,'r')
  instrs = formatInstr(file.read())
  file.close()
  instructions[i - 1] = '# ' + instructions[i - 1]
  for j in range(0,len(instrs)):
    pos = i + j
    instructions.insert(pos,instrs[j])
  file.close()

def createGetter(arg):
  arg = arg.split(':',1)
  name = arg[0]
  if not isValidFuncName(name):
    print(f'>{name}< is not a valid name of a getter.')
    Error(43)
  expression = ['return ' + arg[1]]
  Functions[name] = Function([],expression)
  Functions[name]['type'] = 'getter'

def py(arg):
  try:  exec(eval(parseExpr(arg)))
  except Exception as e:
    print('Debug : ',e)
    Error(11)

def exec_pydi(arg):
  parsedInstr = parseInstructions(eval(parseExpr(arg)))
  execute(parsedInstr['cmd'], parsedInstr['cmdArgs'], parsedInstr['arg'])

def init_class(arg):
  global i
  line = i
  arg = arg.split(':',1)
  name = arg[0]
  arguments =  arg[1].split(',') if len(arg) ==  2 else []
  if hasDuplicateArgs(arguments):
    Error(38)
  Classes[name] = {}
  Classes[name]['instrs'] = []
  Classes[name]['arguments'] = arguments
  for j in range(i,len(instructions)):
    if instructions[i].strip() == '' or instructions[i][0:2] == '  ':
      if not instructions[i].strip() == '': Classes[name]['instrs'].append(instructions[i][2:])
      i += 1
    else: break

def new(arg):
  global isClassRunning,whichClassRunning,c_classData,whichBlockRunning
  returnee = False if ' as ' in arg else True
  try:
    arg = arg.split(' as ', 1)
    arg[0] = removeSpaces(arg[0]).split(':',1)
    arguments = arg[0][1].split(',') if len(arg[0]) == 2 else []
    className = arg[0][0]
  except IndexError as e:
    print('Debug : ',e)
    Error(39)
  isClassRunning = True
  whichClassRunning = className
  if not returnee: 
    objectName =  arg[1]
    if not isValidName(objectName):
      print(f'invalid name for object >{objectName}<.')
      Error(43)
  if not className in Classes:
    print(f'no class named >{className}< was found.')
    Error(34)
  if len(arguments) != len(Classes[className]['arguments']):
    print('expected' , len(Classes[className]['arguments']) , 'argument(s)', len(arguments) , 'given.')
    Error(17)
  for j in range(0,len(arguments)):
    if '@' in Classes[className]['arguments'][j]:
      func = Classes[className]['arguments'][j].split('@',1)[1]
      argName = Classes[className]['arguments'][j].split('@',1)[0]
      c_paramsObject[argName] = eval(func + '(' + parseExpr(arguments[j]) + ')')
    else:
      c_paramsObject[Classes[className]['arguments'][j]] = eval(parseExpr(arguments[j]))
  c_classData[className] = {}
  c_classData[className]['arguments'] = c_paramsObject
  c_classData[className]['this'] = {}
  c_classData[className]['line'] = 0
  for j in range(0,len(Classes[className]['instrs'])):
    whichBlockRunning = 'class'
    whichClassRunning = className
    c_classData[className]['line'] = j
    instrs = Classes[className]['instrs'][j]
    if instrs.split(' ',1)[0] != 'this':
      instrs = parseInstructions(instrs)
      execute(instrs['cmd'],instrs['cmdArgs'],instrs['arg'])
    else:
      instrs = instrs.split(' ',1)[1].split('=',1)
      c_classData[className]['this'][instrs[0].replace(' ','')] = eval(parseExpr(removeSpaces(instrs[1])))
  if returnee:
    SuperVars['r'] = c_classData[className]['this']
  else:
    Scopes[objectName] = c_classData[className]['this']
  isClassRunning = False
  whichClassRunning = ''

def cmd_obj2obj(args):
  if args == '0' : return {}
  args = args.split(',')
  obj = {}
  for i in range(0,len(args)):
    if ':' in args[i]:
      args[i] = args[i].split(':',1)
      obj[args[i][0]] = args[i][1]
    else:
      print(f'Invalid Syntax ":" & expression missing here at >{args[i]}<. Expected {args[i]}:<<<expr>>>')
      Error(0)
  return obj
objectifyArgs = cmd_obj2obj

def for_statement(args,body):
  global fors,Vars,i
  args = cmd_obj2obj(args)
  var = args['v'] if 'v' in args else None
  if var == None: pass
  elif not isValidName(var):
    print(f'invalid name for varible >{var}<.')
    Error(43)
  try:
    body = body.split(':',1)
    name = body[0]
    statements = body[1].split(',')
    st1 = statements[0]
    st2 = statements[1]
    st3 = statements[2]
  except IndexError as e:
    Error(39)
  if name == 'loop':
    for j in range(i,len(instructions)):
      if instructions[j][0:2] != '  ' and len(instructions[j].strip()) != 0 :
        instructions.insert(j,'reset looper')
        break
    Vars['looper'] = True
    instructions[i-1] = 'loop _'
    instructions.insert(i,f'  for@v:looper looper :' + ','.join(statements))
    instructions.insert(i+1,'  ? looper ? _ ? break loop')
    i = i - 1
    return
  if not name in fors :
    expression(st1)
    if var : Vars[var] = eval(parseExpr(st2))
    else : SuperVars['fr'] = eval(parseExpr(st2))
  else:
    if st1 == '_' : st1 = fors[name]['st1']
    if st2 == '_' : st2 = fors[name]['st2']
    if st3 == '_' : st3 = fors[name]['st3']
    if var : Vars[var] = eval(parseExpr(st2))
    else : SuperVars['fr'] = eval(parseExpr(st2))
    expression(st3)
  fors[name] = {
      'st1':st1,
      'st2':st2,
      'st3':st3,
  }



def for_reset(name):
  if not name in fors:
    print(f"No 'for statement' found for given id >{name}<.")
    Error(45)
  del fors[name]



def this(arg):
  if not isClassRunning:
    print(f'here at >{arg}<.')
    Error(44)
  arg = arg.split('=',1)
  if len(arg) == 1:
    print(f'no rhs found for key >{"=".join(arg)}<')
    Error(39)
  key = arg[0]
  if not isValidName(key):
    print(f'invalid name of key >{key}<')
    Error(43)
  value = eval(parseExpr(arg[1]))
  c_classData[whichClassRunning]['this'][key] = value



def parsePrimitveArray(arg):
  final_array = []
  if arg == '[]' : return []
  arg = arg[1:-1]
  if arg[-1] == ',' : arg = arg[:-1]
  elems = split_outside_quotes(arg,',')
  for i in range(0,len(elems)):
    final_array.append(eval(parseExpr(elems[i])))
  return final_array

def array(arg):
  arg = arg.split('=',1)
  name = arg[0]
  if not isValidName(name):
    print(f'invalid name of array >{name}<')
    Error(43)
  proto_array = arg[1]
  array = parsePrimitveArray(proto_array)
  Scopes[name] = array

def push(arg):
  arg = arg.split(':',1)
  name = arg[0]
  element = eval(parseExpr(arg[1]))
  if not isValidName(name):
    print(f'cannot push : >{name}< is not a valid name, here at >{":".join(arg)}<')
    Error(43)
  if not name in Scopes:
    print(f'cannot push : array >{name}< was not found, here at >{":".join(arg)}<')
    Error(46)
  if not typeof(Scopes[name]) == 'list':
    print(f'>{name}< is an object not an array, here at >{":".join(arg)}<')
    Error(5)
  Scopes[name].append(element)


def push_all(arg):
  arg = arg.split(':',1)
  name = arg[0]
  if not isValidName(name):
    print(f'cannot push : >{name}< is not a valid name, here at >{":".join(arg)}<')
    Error(43)
  if not name in Scopes:
    print(f'cannot push : array >{name}< was not found, here at >{":".join(arg)}<')
    Error(46)
  if not typeof(Scopes[name]) == 'list':
    print(f'cannot push : >{name}< is an object not an array, here at >{":".join(arg)}<')
    Error(5)
  array = parsePrimitveArray(arg[1])
  Scopes[name] += array

def push_all_expr(arg):
  arg = arg.split(':',1)
  name = arg[0]
  if not isValidName(name):
    print(f'cannot push : >{name}< is not a valid name, here at >{":".join(arg)}<')
    Error(43)
  if not name in Scopes:
    print(f'cannot push : array >{name}< was not found, here at >{":".join(arg)}<')
    Error(46)
  if not typeof(Scopes[name]) == 'list':
    print(f'cannot push : >{name}< is an object not an array, here at >{":".join(arg)}<')
    Error(5)
  array = eval(parseExpr(arg[1]))
  if typeof(array) == 'list':
    Scopes[name] += array
  else:
    print(f'cannot push : value is of type >{typeof(array)}<, expected of "list" type.')
    Error(5)


def insert(arg):
  arg = arg.split(':',1)
  name = arg[0]
  if not isValidName(name):
    print(f'cannot insert : >{name}< is not a valid name, here at >{":".join(arg)}<')
    Error(43)
  if not name in Scopes:
    print(f'cannot insert : array >{name}< was not found, here at >{":".join(arg)}<')
    Error(46)
  if not typeof(Scopes[name]) == 'list':
    print(f'cannot insert : >{name}< is an object not an array, here at >{":".join(arg)}<')
    Error(5)
  arg = arg[1].split('=',1)
  index = int(arg[0])
  if (index) >= len(Scopes[name]):
    print(f"the list >{name}< has a length of >{len(Scopes[name])}<,\ntried to insert at >{index}<.")
    Error(45)
  elem = eval(parseExpr(arg[1]))
  Scopes[name].insert(index,elem)

def update_element(arg):
  arg = arg.split(':',1)
  name = arg[0]
  if not isValidName(name):
    print(f'>{name}< is not a valid name, here at >{":".join(arg)}<')
    Error(43)
  if not name in Scopes:
    print(f'array >{name}< was not found, here at >{":".join(arg)}<')
    Error(46)
  if not typeof(Scopes[name]) == 'list':
    print(f'>{name}< is an object not an array, here at >{":".join(arg)}<')
    Error(5)
  arg = arg[1].split('=',1)
  index = int(arg[0])
  if (index) >= len(Scopes[name]):
    print(f"the list >{name}< has a length of >{len(Scopes[name])}<,\ncannot update at >{index}< : element does not exist.")
    Error(45)
  elem = eval(parseExpr(arg[1]))
  Scopes[name][index] = elem
  


def update_chars(arg,to=1):
  arg = arg.split(':',1)
  name = arg[0]
  arg = arg[1].split('=',1)
  index = int(eval(parseExpr(arg[0])))
  char = eval(parseExpr(arg[1]))[0:to]
  if not isValidName(name):
    print(f'>{name}< is not a valid name.')
    Error(43)
  if not name in Vars:
    print(f'String >{name}< was not found.')
    Error(24)
  if not typeof(Vars[name]) == 'str':
    print(f'{name}< is of type >{typeof(Vars[name])}<, not of "str".')
    Error(5)
  if (index) >= len(Vars[name]):
    print(f"the string >{name}< has a length of >{len(Vars[name])}<,\ncannot update at >{index}< : char does not exist.")
    Error(45)
  Vars[name] = list(Vars[name])
  if not to == -1:
    Vars[name][index] = char
  else:
    Vars[name][index] += char
  Vars[name] = ''.join(Vars[name])

def move(arg):
  global i
  line = int(eval(parseExpr(arg)))
  i = line


def skip(arg):
  global i
  line = int(eval(parseExpr(arg)))
  if line > len(instructions)-1:
    print('line was out of range')
    Error(7)
  linesToSkip.add(line)

def unskip(arg):
  global i
  line = int(eval(parseExpr(arg)))
  if line > len(instructions)-1:
    print('line was out of range')
    Error(7)
  try:
    linesToSkip.remove(line)
  except Exception as KeyError:
    return

def continue_statement(arg):
  if arg == 'loop':
    global continueLoop
    continueLoop = True

def returnf(arg):
  if not isFunctionRunning: Error(37)

def execute(cmd,cmdArgs,arg):
  try:
    global safe,warnings,moddir,superCommand
    match cmd:
      case '//'|'#' : pass
      case 'print'|'>>': printOut(arg)
      case 'py' : py(arg)
      case 'move'|'JMP' : move(arg)
      case 'skip'|'SK' : skip(arg)
      case 'unskip'|'USK' : unskip(arg)
      case 'var'|'let' : createVar(arg,cmdArgs)
      case 'read' : read(cmdArgs,arg)
      case 'write' : writeFile(cmdArgs,arg)
      case 'append' : appendFile(cmdArgs,arg)
      case 'type' : print(typeof(eval(parseExpr(arg))))
      case 'loop' : loop(arg,cmdArgs)
      case '**cloop'|'cloop' : cloop(arg)
      case 'while' : condLoop(arg)
      case 'printE' : print(parseExpr(arg))
      case 'super'|'*' : superCommand = arg
      case 'local'|'.' : local(arg)
      case 'Ⲗ'|'lambda' : createLambda(arg)
      case 'block'|'func'|'=>' : createFunction(arg,cmd)
      case 'getter'|'<==' : createGetter(arg)
      case '()'|'call' :call(arg,cmdArgs)
      case '{}'|'object' : updateObject(arg)
      case 'if'|'?' : terinary(arg)
      case 'ifnot'|'?!' : terinary(arg,flip=True)
      case 'return' : returnf(arg)
      case 'break'|'end' : exitProgram(arg)
      case 'continue' : continue_statement(arg)
      case 'warnings' : warnings = eval(parseExpr(arg))
      case 'del' : delete(arg)
      case 'obj'|'{_}' : as_obj(arg)
      case 'array'|'[]' : array(arg)
      case 'push' : push(arg)
      case 'push-all' : push_all(arg)
      case 'push-arr' : push_all_expr(arg)
      case 'insert' : insert(arg)
      case 'arr'|'[_]' : as_arr(arg)
      case 'uchar'|'^' : update_chars(arg)
      case 'abstr' : update_chars(arg,-1)
      case 'uelem'|'[^]' : update_element(arg)
      case 'class' : init_class(arg)
      case 'new' : new(arg)
      case 'for' : for_statement(cmdArgs,arg)
      case 'reset' : for_reset(arg)
      case 'exec': exec_pydi(arg)
      case 'moddir': moddir = str(eval(parseExpr(arg)))
      case 'use'|'include': import_module(arg,__file__.rsplit('/',1)[0]+'/modules', True)
      case 'import' : import_module(arg,moddir = moddir)
      case 'link' : link(arg)
      case '**'|'sqr' : expression(arg + ' *= ' + arg)
      case '++'|'incr' : expression(arg + ' += 1')
      case '--'|'decr' : expression(arg + ' -= 1')
      case 'this'|'.': this(arg)
      case 'helper' : print(NotImplemented)
      case 'str' : addVar(arg.split('=',1)[0],arg.split('=',1)[1][1:-1] ,True,'')
      case '' : Error(48)
      case _ if cmd in imports: eval(cmd+'(arg)')
      case _ : expression(cmd + arg)
  except IndexError as e:
    print('Debug:',e)
    Error(39)
  except TypeError as e:
    print('Debug: ', e)
    Error(0)
  except ValueError as e:
    print('Debug: ', e)
    Error(5)
  except ZeroDivisionError:
    print('cannot divide by zero')
    Error(42)
  except KeyboardInterrupt:
    print(bcolors.FAIL+ 'Keyboard Interrupt'+ bcolors.E)
    print('Exiting...')
    exit()

def parseInstructions(instruction):
  global i,superCommand
  try:
    if not instruction.strip():
      return {'cmd':'#','arg':'5','cmdArgs':0}
    if instruction.split(' ')[0] == 'norm' :
      superCommand = None
      return {'cmd':'#','arg':'5','cmdArgs':0}
    if superCommand:
      cmd = superCommand
      arg = instruction
    else:
      cmd = instruction.split(cmd_ArgSep,1)[0]
      arg = instruction.split(cmd_ArgSep,1)[1]
    if not cmd in ['?','if','new','?!','ifnot'] : arg = removeSpaces(arg)
    if len(cmd.split(cmd_cmdArgSep)) == 2:
      cmdArgs = cmd.split(cmd_cmdArgSep)[1]
      cmd = cmd.split(cmd_cmdArgSep)[0]
    else:
      cmdArgs = '0'
  except Exception as e:
    print(e)
    Error(15,i+1)
    return {'cmd':'#','arg':'5','cmdArgs':0}
  return {'cmd':cmd,'arg':arg,'cmdArgs':cmdArgs}

while i < len(instructions):
  if i in linesToSkip: 
    i += 1
    continue
  parsedInstr = parseInstructions(instructions[i])
  cmd = parsedInstr['cmd']
  cmdArgs = parsedInstr['cmdArgs']
  arg = parsedInstr['arg']
  i += 1
  execute(cmd,cmdArgs,arg)

if not outfilename == None:
  outfile = open(outfilename,'w')
  outfile.write(';\n'.join([x for x in instructions if x]))
  outfile.close()
