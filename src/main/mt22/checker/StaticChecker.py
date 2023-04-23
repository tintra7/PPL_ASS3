from Visitor import Visitor
from StaticError import *
from AST import *
from abc import ABC
from functools import reduce
# inherit(function, param), super, preven
# MSSV: 2010702
class Symbol(ABC):
    pass

class Func(Symbol):
    def __init__(self, name, typ, params, inherit: str or None, active=False, curr=False, is_return=False):
        self.name = name
        self.typ = typ
        self.params = params
        self.inherit = inherit
        self.active = active
        self.curr = curr
        self.is_return = is_return

class Var(Symbol):
    def __init__(self, name, typ):
        self.name = name
        self.typ = typ
# a = {{1,2,3}} a[0] = {4,5,6}
class Array(Symbol):
    def __init__(self, name, typ):
        self.name = name
        self.typ = typ

class Param(Symbol):
    def __init__(self, name, typ, out, inherit):
        self.name = name
        self.typ = typ
        self.out = out
        self.inherit = inherit

class Utils:
    def infer(ctx , typ, env):
        for symbol_list in env:
            for symbol in symbol_list:
                if symbol.name == ctx.name:
                    symbol.typ = typ
    
    def infer_param(func, name, typ, env):
        for symbol_list in env:
            for symbol in symbol_list:
                if symbol.name == func.name:
                    for i, param in enumerate(symbol.params):
                        if param.name == name:
                            
                            symbol.params[i].typ = typ
                            

                   

class GetEnv(Visitor):

    def __init__(self, ast):
        self.ast = ast
    def check(self):
        return self.visitProgram(self.ast, [])
    def visitProgram(self, ctx: Program, o):
        o = [[]]
        readI = Func("readInteger", IntegerType(), [], None, True)
        printI = Func("printInteger", VoidType(), [Param("anArg", IntegerType(), None, None)], None, True)
        readF = Func("readFloat", FloatType(), [], None, True)
        printF = Func("writeFloat", VoidType(), [Param("anArg", FloatType(), None, None)], None, True)
        readS = Func("readString", StringType(), [], None, True)
        printS = Func("printString", VoidType(), [Param("anArg", StringType(), None, None)], None, True)
        readB = Func("readBoolean", BooleanType(), [], None, True)
        printB = Func("printBoolean", VoidType(), [Param("anArg", BooleanType(), None, None)], None, True)
        superF = Func("super", AutoType(), [], None, True)
        prevenF = Func("preventDefault", VoidType(), None, None, True)
        for decl in ctx.decls:
            if type(decl) is FuncDecl:
                o = self.visit(decl, o)
        o[0] += [readI, printI, readF, printF, readS, printS, readB, printB, superF, prevenF]
        return o

    def visitVarDecl(self, ctx: VarDecl, o):
        pass
        
    def visitFuncDecl(self, ctx: FuncDecl, o):
        params = []
        for param in ctx.params:
            params = self.visit(param, params)
        o[0] += [Func(ctx.name, ctx.return_type, params, ctx.inherit)]
        return o

    # name: str, typ: Type, out: bool = False, inherit: bool = False
    def visitParamDecl(self, ctx: ParamDecl, o):
        o += [Param(ctx.name, ctx.typ, ctx.out, ctx.inherit)]
        return o


class StaticChecker(Visitor):
    def __init__(self, ast):
        self.ast = ast
 
    def check(self):
        return self.visitProgram(self.ast, [])

    def visitArrayType(self, ctx: ArrayType, o):
        return ctx.typ, ctx.dimensions

    def visitProgram(self, ctx: Program, o):
        flag = False
        o = GetEnv(self.ast).visit(ctx, o)
        for decl in ctx.decls:
            o = self.visit(decl, o)
        for func in o[0]:
            if func.name == 'main' and type(func.typ) is VoidType and func.params == []:
                flag = True
        if flag == False:
            raise NoEntryPoint()
        
    # name: str, typ: Type, init: Expr or None = None
    def visitVarDecl(self, ctx: VarDecl, o):
        
        for symbol in o[0]:
            if symbol.name == ctx.name:
                if type(symbol) is Func and symbol.active == False:
                    continue
                raise Redeclared(Variable(), ctx.name)

        if ctx.init is None:
            if type(ctx.typ) is AutoType:
                raise Invalid(Variable(), ctx.name)
            elif type(ctx.typ) is ArrayType:
                # array_type = self.visit(ctx.typ, o) 
                # dimensions: List[int], typ: AtomicType
                o[0] += [Array(ctx.name, ctx.typ)]
                return o
            else:
                o[0] += [Var(ctx.name, ctx.typ)]
                return o
        else:
            init_type = self.visit(ctx.init, o)
            
            if type(ctx.typ) is ArrayType:
                print(init_type)
                array_type = self.visit(ctx.typ, o)
                o[0] += [Array(ctx.name, ctx.typ)]
                return o
            elif type(ctx.typ) is not AutoType and type(init_type) is AutoType:
                Utils.infer(ctx.init, ctx.typ, o)
                o[0] += [Var(ctx.name, ctx.typ)]
                return o
            elif type(ctx.typ) is AutoType or type(ctx.typ) == type(init_type):
                o[0] += [Var(ctx.name, init_type)]
                return o
            else:
                if type(ctx.typ) is FloatType and type(init_type) is IntegerType:
                    o[0] += [Var(ctx.name, FloatType)]
                    return o
                else:
                  
                    raise TypeMismatchInVarDecl(ctx)
    # name: str, return_type: Type, params: List[ParamDecl], inherit: str or None, body: BlockStmt
    def getParentParams(self, func_name, o):
        for symbol_list in o:
            for symbol in symbol_list:
                if symbol.name == func_name and type(symbol) is Func:
                    return symbol.params
        raise Undeclared(Function(), func_name)

    def get_first_stmt(self, ctx, o):
        if len(ctx.body)>0:
            return ctx.body[0]
        else:
            return None

    def visitFuncDecl(self, ctx: FuncDecl, o):
        func_cur = None
        for symbol in o[0]:
            if symbol.name == ctx.name:
                if type(symbol) is Func:
                    if symbol.active == False:
                        symbol.active = True
                    else:
                        raise Redeclared(Function(), ctx.name)
                    func_cur = symbol
                    func_cur.curr = True
                else:
                    raise Redeclared(Function(), ctx.name)
        env = [[]] + o
        parent_param = []
        
        if ctx.inherit:
            parent_param = self.getParentParams(ctx.inherit, o)
            first_stmt = self.get_first_stmt(ctx.body, o)
            if len(parent_param) > 0:
                if first_stmt is None:
                    raise InvalidStatementInFunction(ctx.name)
                elif type(first_stmt) is not CallStmt:
                    raise InvalidStatementInFunction(ctx.name)
                elif first_stmt.name not in ['super', 'preventDefault']:
                    raise InvalidStatementInFunction(ctx.name)
            

        for param in ctx.params:
            env = self.visit(param, env)
        for i, symbol in enumerate(env[0]):
            if type(symbol.typ) is AutoType and type(symbol) is Param:
                for param in func_cur.params:
                    if symbol.name == param.name:
                        symbol.typ = param.typ    
        # check redecl param in child function
        if ctx.inherit:
            first_stmt = self.get_first_stmt(ctx.body, o)
            for param in env[0]:
                if type(param) is Param:
                    for i in parent_param:
                        if i.inherit:
                            for symbol in env[0]:
                                if symbol.name == i.name:
                                    raise Redeclared(Parameter(), symbol.name)
                            if param.name == i.name:
                                raise Invalid(Parameter(), i.name)
                            elif first_stmt is not None and first_stmt.name is 'super':
                                env[0] += [Var(i.name, i.typ)]
        
            first_stmt = self.visit(ctx.body, env)
            
            if parent_param == []:
                
                if type(first_stmt) is CallStmt and first_stmt.name in ['preventDefault']:
                    
                    if len(first_stmt.args) > 0:
                        raise TypeMismatchInExpression(first_stmt.args[0])
            else:
                if type(first_stmt) is not CallStmt:
                    raise InvalidStatementInFunction(ctx.name)
                elif first_stmt.name in ['preventDefault']:
                    
                    if len(first_stmt.args) > 0:
                        raise TypeMismatchInExpression(first_stmt.args[0])
                elif first_stmt.name == "super":
                    if len(parent_param) > len(first_stmt.args):
                        raise TypeMismatchInExpression(None)
                    elif len(parent_param) < len(first_stmt.args):
                        n = len(parent_param)
                        raise TypeMismatchInExpression(first_stmt.args[n])
                    else:
                        
                        for i in range(len(parent_param)):
                            arg = self.visit(first_stmt.args[i], env)
                            
                            if type(arg) is not type(parent_param[i].typ):
                                if type(arg) is IntegerType and type(parent_param[i].typ) is FloatType:
                                    continue
                                elif type(arg) is AutoType:
                                    Utils.infer(first_stmt.args[i], parent_param[i].typ, o)
                                    continue
                                elif type(parent_param[i].typ) is AutoType:
                                    Utils.infer_param(self.get_func(ctx.inherit, o), parent_param[i].name, arg, o)
                                    continue
                                else: 
                                    raise TypeMismatchInExpression(first_stmt.args[i])
                else:
                    raise InvalidStatementInFunction(ctx.name)
        else:
            temp = self.visit(ctx.body, env)
        func_cur.curr = False
        return o    

    
    def get_func(self, name, o):
        for symbol_list in o:
            for symbol in symbol_list:
                if symbol.name == name and type(symbol) is Func:
                    return symbol

    # name: str, typ: Type, out: bool = False, inherit: bool = False
    def visitParamDecl(self, ctx: ParamDecl, o):
        for symbol in o[0]:
            if symbol.name == ctx.name:
                raise Redeclared(Parameter(), ctx.name)
        o[0] += [Param(ctx.name, ctx.typ, ctx.out, ctx.inherit)]
        return o

    def visitBinExpr(self, ctx: BinExpr, o):
        e1t = self.visit(ctx.left, o)
        e2t = self.visit(ctx.right, o)
        # Case e1t or e2t is auto type
        if type(e1t) is AutoType and type(e2t) is AutoType:
            if ctx.op in ['+','-','*','/','%']:
                return IntegerType()
            elif ctx.op in ['==','!=','<','>','<=','>=']:
                return BooleanType()
            elif ctx.op in ['&&', '||']:
                e1t = BooleanType()
                e2t = BooleanType()
                Utils.infer(ctx.left, BooleanType(), o)
                Utils.infer(ctx.right, BooleanType(), o)
            elif ctx.op in ['::']:
                e1t = StringType()
                e2t = StringType()
                Utils.infer(ctx.left, StringType(), o)
                Utils.infer(ctx.right, StringType(), o)
            return e1t
        elif type(e1t) is AutoType:
            e1t = e2t
            Utils.infer(ctx.left, e2t, o)
            return e1t
        elif type(e2t) is AutoType:
            e2t = e1t
            Utils.infer(ctx.right, e1t, o)
            return e1t
        else: 
            if ctx.op in ['+','-','*','/']:
                if type(e1t) is IntegerType and type(e2t) is IntegerType:
                    return IntegerType()
                elif all(type(item) in [IntegerType, FloatType] for item in [e1t, e2t]):
                    return FloatType()
                raise TypeMismatchInExpression(ctx)
            elif ctx.op in ['%']:
                if type(e1t) is IntegerType and type(e2t) is IntegerType:
                    return IntegerType()
                raise TypeMismatchInExpression(ctx)
            elif ctx.op in ['::']:
                if type(e1t) is StringType and type(e2t) is StringType:
                    return StringType()
                raise TypeMismatchInExpression(ctx)
            elif ctx.op in ['&&', '||']:
                if type(e1t) is BooleanType and type(e2t) is BooleanType:
                    return BooleanType()
                raise TypeMismatchInExpression(ctx)
            elif ctx.op in ['==','!=','<','>','<=','>=']:
                if all(type(item) in [IntegerType, BooleanType] for item in [e1t, e2t]):
                    return BooleanType()
                raise TypeMismatchInExpression(ctx)

    # op: str, val: Expr
    def visitUnExpr(self, ctx: UnExpr, o):
        et = self.visit(ctx.val, o)
        if ctx.op == '-':
            if type(et) is IntegerType or type(et) is FloatType:
                return et
            if type(et) is AutoType:
                Utils.infer(ctx.val, IntegerType(), o)
                return IntegerType()
            raise TypeMismatchInExpression(ctx)
        if ctx.op == '!':
            if type(et) is BooleanType:
                return BooleanType()
            if type(et) is AutoType:
                Utils.infer(ctx.val, BooleanType(), o)
                return BooleanType()
            raise TypeMismatchInExpression(ctx)

    # name: str, cell: List[Expr]
    def visitArrayCell(self, ctx: ArrayCell, o):
        for symbol_list in o:
            for symbol in symbol_list:
                if symbol.name == ctx.name:
                    if type(symbol) is Array:
                        for exp in ctx.cell:
                            if type(exp) is not IntegerType:
                                raise TypeMismatchInExpression(ctx)
                        if len(ctx.cell) == len(symbol.typ.dimensions):
                            return symbol.typ.typ
                        elif len(ctx.cell) > len(symbol.typ.dimensions):
                            raise TypeMismatchInExpression(ctx)
                        else:
                            n = len(symbol.typ.dimensions) - len(ctx.cell)
                            return ArrayType(symbol.typ.dimensions[n:], symbol.typ.typ)
                    else:
                        raise TypeMismatchInExpression(ctx)
        raise Undeclared(Identifier(), ctx.name)
        
    def visitIntegerLit(self, ctx: IntegerLit, o):
        return IntegerType()

    def visitFloatLit(self, ctx: FloatLit, o):
        return FloatType()

    def visitStringLit(self, ctx: StringLit, o):
        return StringType()

    def visitBooleanLit(self, ctx: BooleanLit, o):
        return BooleanType()
        
    def check_arraylit(self, ctx: ArrayLit, o):
        
        typ = self.visit(ctx.explist[0], o)
        if type(typ) is ArrayType:
            for i in range(len(ctx.explist)):
                exp = self.visit(ctx.explist[i], o)
                if type(exp) is not ArrayType and exp.dimensions != typ.dimensions and exp.typ is not typ.typ:
                    return False
            return self.check_arraylit(ctx.explist[0], o) 
        else:
            for i in range(len(ctx.explist)):
                exp = self.visit(ctx.explist[i], o)
                if type(exp) is not type(typ):
                    return False
            return True
    
        
                

    def visitArrayLit(self, ctx: ArrayLit, o):
        if not self.check_arraylit(ctx, o):
            raise IllegalArrayLiteral(ctx)
        dimensions = []
        temp = ctx.explist
        exp = self.visit(temp[0], o)
            
        if type(temp) is List:
            dimensions += [len(temp)]
        if type(exp) is not ArrayType:
            return ArrayType(dimensions, exp)
        else:
            dimensions += exp.dimensions
        return ArrayType(dimensions, exp)
        
    
    # name: str, args: List[Expr]
    def visitFuncCall(self, ctx: FuncCall, o):
        if ctx.name in ["super", "preventDefault"]:
            raise TypeMismatchInExpression(ctx)
        
        found = False
        for symbol_list in o:
            for symbol in symbol_list:
                if symbol.name == ctx.name:
                    if type(symbol) is Func:
                        found = True
                        if type(symbol.typ) is VoidType:
                            raise TypeMismatchInExpression(ctx)
                        else:
                            print(ctx.name)
                            if len(ctx.args) != len(symbol.params):
                                raise TypeMismatchInExpression(ctx)
                            for i in range(len(ctx.args)):
                                arg = self.visit(ctx.args[i], o)
                                
                                if type(arg) is not type(symbol.params[i].typ):
                                    if type(arg) is IntegerType and type(symbol.params[i].typ) is FloatType:
                                        continue
                                    elif type(arg) is AutoType:
                                        Utils.infer(ctx.args[i], symbol.params[i].typ, o)
                                        continue
                                    elif type(symbol.params[i].typ) is AutoType:
                                
                                        Utils.infer_param(symbol, symbol.params[i].name, arg, o)
                                        continue
                                    else: 
                                        raise TypeMismatchInExpression(ctx)
                            return symbol.typ
                    else:
                        raise TypeMismatchInExpression(ctx)
        if not found:
            raise Undeclared(Function(), ctx.name)             
                            

    # lhs: LHS, rhs: Expr
    def visitAssignStmt(self, ctx: AssignStmt, o):
        
        
        
        if type(ctx.lhs) is ArrayCell:
            left, nd = self.visit(ctx.lhs, o)
        
        right = self.visit(ctx.rhs, o)
        left = self.visit(ctx.lhs, o)
        if type(left) is VoidType or type(right) is VoidType:
            raise TypeMismatchInStatement(ctx)
        if type(left) is not type(right):
            if type(left) is FloatType and type(right) is IntegerType:
                return FloatType()
            if type(right) is AutoType:
                Utils.infer(ctx.rhs, left, o)
                return left
            if type(left) is AutoType:
                Utils.infer(ctx.lhs, right, o)
                return right
            raise TypeMismatchInStatement(ctx)
        return left

    def visitBlockStmt(self, ctx: BlockStmt, o):
        # [1,2,3] => 0,1 1,2 2,3
        for i, stmt in enumerate(ctx.body):
            if type(ctx.body[0]) is CallStmt and ctx.body[0].name in ['super','preventDefault'] and i == 0:
                continue
            if type(stmt) is VarDecl:
                o = self.visit(stmt, o)
            elif type(stmt) is BlockStmt:
                env = [[]] + o
                self.visit(stmt, env)
            else:
                self.visit(stmt, o)
        if len(ctx.body) > 0:
            return ctx.body[0] # Get first in blockstmt for super call
        return VarDecl("super", VoidType(), None)
                
    
    def visitIfStmt(self, ctx: IfStmt, o):
        cond = self.visit(ctx.cond, o)
        if type(cond) is not BooleanType:
            if type(cond) is AutoType:
                Utils.infer(ctx.cond, BooleanType, o)
            else:
                raise TypeMismatchInStatement(ctx)
        is_loop = [[Var("if", VoidType())]]
        for symbol_list in o:
            for symbol in symbol_list:
                if symbol.name == "for":
                    is_loop = [[Var("for", VoidType())]]
        env = is_loop + o
        self.visit(ctx.tstmt, env)
        if ctx.fstmt is not None:
            self.visit(ctx.fstmt, env)

    def visitForStmt(self, ctx: ForStmt, o):
        init = self.visit(ctx.init, o)
        if type(init) is not IntegerType:
            raise TypeMismatchInStatement(ctx)
        cond = self.visit(ctx.cond, o)
        if type(cond) is not BooleanType:
            if type(cond) is AutoType:
                Utils.infer(ctx.cond, BooleanType, o)
            else: 
                raise TypeMismatchInStatement(ctx)
        upd = self.visit(ctx.upd, o)
        if type(upd) is not IntegerType:
            raise TypeMismatchInStatement(ctx)
        env = [[Var("for", VoidType())]] + o
        self.visit(ctx.stmt, env)

    def visitWhileStmt(self, ctx: WhileStmt, o):
        cond = self.visit(ctx.cond, o)
        if type(cond) is not BooleanType:
            if type(cond) is AutoType:
                Utils.infer(ctx.cond, BooleanType, o)
            else: 
                raise TypeMismatchInStatement(ctx)
        env = [[Var("for", VoidType())]] + o
        self.visit(ctx.stmt, env)
        

    def visitDoWhileStmt(self, ctx: DoWhileStmt, o):
        cond = self.visit(ctx.cond, o)
        if type(cond) is not BooleanType:
            if type(cond) is AutoType:
                Utils.infer(ctx.cond, BooleanType, o)
            else:
                raise TypeMismatchInStatement(ctx)
        env = [[Var("for", VoidType())]] + o
        self.visit(ctx.stmt, env)
        

    def visitBreakStmt(self, ctx: BreakStmt, o):
        for symbol_list in o:
            for symbol in o[0]:
                if symbol.name == "for":
                    return
        raise MustInLoop(ctx)

    def visitContinueStmt(self, ctx: ContinueStmt, o):
        for symbol_list in o:
            for symbol in o[0]:
                if symbol.name == "for":
                    return
        raise MustInLoop(ctx)

    def visitReturnStmt(self, ctx: ReturnStmt, o):
        in_if = False
        for symbol in o[0]:
            if symbol.name in ['if', 'for']:
                in_if = True
        for symbol_list in o:
            for symbol in symbol_list:
                if type(symbol) is Func and symbol.curr == True:
                    if symbol.is_return:
                        return None
                    if not in_if:
                        symbol.is_return = True 
                    if type(symbol.typ) is VoidType: 
                        if ctx.expr is not None:
                            raise TypeMismatchInStatement(ctx)
                        else:
                            return None
                    else:
                        if ctx.expr is not None:
                            exp = self.visit(ctx.expr, o)
                            if type(symbol.typ) is not type(exp):
                                if type(symbol.typ) is FloatType and type(exp) is IntegerType:
                                    return FloatType()
                                elif type(symbol.typ) is AutoType:
                                    Utils.infer(symbol, exp, o)
                                    return exp
                                elif type(exp) is AutoType:
                                    Utils.infer(ctx.expr, symbol.typ, o)
                                    return symbol.typ
                                else:
                                    raise TypeMismatchInStatement(ctx)
                            else:
                                return exp
                        else:
                            raise TypeMismatchInStatement(ctx)

    def visitCallStmt(self, ctx: CallStmt, o):
        if ctx.name in ['super', 'preventDefault']:
            raise TypeMismatchInStatement(ctx)
        found = False
        for symbol_list in o:
            for symbol in symbol_list:
                if symbol.name == ctx.name:
                    if type(symbol) is Func:
                        found = True
                        if len(ctx.args) != len(symbol.params):
                            raise TypeMismatchInStatement(ctx)
                        for i in range(len(ctx.args)):
                            arg = self.visit(ctx.args[i], o)
                            if type(arg) is not type(symbol.params[i].typ):
                                if type(arg) is IntegerType and type(symbol.params[i].typ) is FloatType:
                                    continue
                                elif type(arg) is AutoType:
                                    Utils.infer(ctx.args[i], symbol.params[i].typ, o)
                                    continue
                                elif type(symbol.params[i].typ) is AutoType:

                                    Utils.infer_param(symbol, symbol.params[i].name, arg, o)
                                    continue
                                else: 
                                    raise TypeMismatchInStatement(ctx)
                        break
                    else:
                        raise TypeMismatchInStatement(ctx)
        if not found: 
            raise Undeclared(Function(), ctx.name)      

    def visitId(self, ctx: Id, o):
        
        for symbol_list in o:
            for symbol in symbol_list:
                if symbol.name == ctx.name:
                    return symbol.typ
        raise Undeclared(Identifier(), ctx.name)