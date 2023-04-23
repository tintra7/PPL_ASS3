from MT22Visitor import MT22Visitor
from MT22Parser import MT22Parser
from AST import *
# MSSV: 2010702


class ASTGeneration(MT22Visitor):
    
    # program: mt22 EOF ;
    def visitProgram(self, ctx: MT22Parser.ProgramContext):
        return Program(self.visit(ctx.mt22()))
    
    # mt22: decllist mt22 | decllist;
    def visitMt22(self, ctx: MT22Parser.Mt22Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.decllist())
        return self.visit(ctx.decllist()) + self.visit(ctx.mt22())  
    
    # decllist: vardecl | function;
    def visitDecllist(self, ctx: MT22Parser.DecllistContext):
        if ctx.vardecl():
            return self.visit(ctx.vardecl())
        return [self.visit(ctx.function())]

    # vardecl: idlist COLON vartype SEMI | initialdecl SEMI ;
    def visitVardecl(self, ctx: MT22Parser.VardeclContext):
        if ctx.getChildCount() == 4:
            vartype = self.visit(ctx.vartype()) #Intype()
            idlist = self.visit(ctx.idlist()) #Id(x), Id(y)
            return list(map(lambda x: VarDecl(x, vartype, None), idlist))
        # for initial case
        return self.visit(ctx.initialdecl())

    # idlist: ID COMMA idlist | ID;
    def visitIdlist(self, ctx: MT22Parser.IdlistContext):
        if ctx.getChildCount() == 1:
            return [ctx.ID().getText()]
        return [ctx.ID().getText()] + self.visit(ctx.idlist())
   
    # vartype: atomtype | arraytype;
    def visitVartype(self, ctx: MT22Parser.VartypeContext):
        if ctx.atomtype():
            return self.visit(ctx.atomtype())
        return self.visit(ctx.arraytype())
    
    # initialdecl: ID COMMA initialdecl COMMA value
	# 		     | ID COLON paratype ASSIGN value
	
    def helperID(self, ctx: MT22Parser.InitialdeclContext):
        if ctx.ASSIGN():
            return [ctx.ID().getText()]
        return [ctx.ID().getText()] + self.helperID(ctx.initialdecl())
    
    def helperValue(self, ctx: MT22Parser.InitialdeclContext):
        if ctx.ASSIGN():
            return [self.visit(ctx.value())]
        return [self.visit(ctx.value())] + self.helperValue(ctx.initialdecl())

    def helperType(self, ctx: MT22Parser.InitialdeclContext):
        if ctx.ASSIGN():
            return self.visit(ctx.paratype())
        return self.helperType(ctx.initialdecl())

    # initialdecl: ID COMMA initialdecl COMMA exp
	# 		     | ID COLON paratype ASSIGN exp
    def visitInitialdecl(self, ctx: MT22Parser.InitialdeclContext):
        if ctx.paratype():
            return [VarDecl(ctx.ID().getText(), self.visit(ctx.paratype()), self.visit(ctx.value()))]
        left = [ctx.ID().getText()] + self.helperID(ctx.initialdecl())
        paratype = self.helperType(ctx.initialdecl())
        right = [self.visit(ctx.value())] + self.helperValue(ctx.initialdecl())
        return list(map(lambda a,b: VarDecl(a, paratype, b), left, right[::-1]))

    # paratype: vartype | AUTO;
    def visitParatype(self, ctx: MT22Parser.ParatypeContext):
        if ctx.AUTO():
            return AutoType()
        return self.visit(ctx.vartype())
    
    # function: ID COLON FUNCTION functype LB paralist RB functionbody | ID COLON FUNCTION functype LB paralist RB INHERIT ID functionbody;
    def visitFunction(self, ctx: MT22Parser.FunctionContext):
        if ctx.INHERIT():
            name = ctx.ID(0).getText()
            functype = self.visit(ctx.functype())
            params = self.visit(ctx.paralist())
            functionbody = self.visit(ctx.functionbody())
            inherit = ctx.ID(1).getText()
            return FuncDecl(name, functype, params, inherit, functionbody)
        name = ctx.ID(0).getText()
        functype = self.visit(ctx.functype())
        params = self.visit(ctx.paralist())
        functionbody = self.visit(ctx.functionbody())
        return FuncDecl(name, functype, params, False, functionbody)
    
    # functionbody: blockstatement;
    def visitFunctionbody(self, ctx: MT22Parser.FunctionbodyContext):
        return self.visit(ctx.blockstatement())
    
    # exp: exp1 DCOLON exp1 | exp1 | functioncall;
    def visitExp(self, ctx:MT22Parser.ExpContext):
        if ctx.getChildCount() == 1:
            if ctx.exp1():
                return self.visit(ctx.exp1(0))
            return self.visit(ctx.functioncall())
        return BinExpr(ctx.DCOLON().getText(), self.visit(ctx.exp1(0)), self.visit(ctx.exp1(1)))
    
    # exp1: exp2 EQUAL exp2 | exp2 NOTEQUAL exp2 | exp2 GT exp2 | exp2 LT exp2 | exp2 LTE exp2 | exp2 GTE exp2 | exp2;
    def visitExp1(self, ctx:MT22Parser.Exp1Context):
        if ctx.EQUAL():
            return BinExpr(ctx.EQUAL().getText(), self.visit(ctx.exp2(0)),self.visit(ctx.exp2(1)) )
        
        if ctx.NOTEQUAL():
            return BinExpr(ctx.NOTEQUAL().getText(), self.visit(ctx.exp2(0)),self.visit(ctx.exp2(1)) )
        
        if ctx.GT():
            return BinExpr(ctx.GT().getText(), self.visit(ctx.exp2(0)),self.visit(ctx.exp2(1)) )
        
        if ctx.GTE():
            return BinExpr(ctx.GTE().getText(), self.visit(ctx.exp2(0)),self.visit(ctx.exp2(1)) )
        
        if ctx.LT():
            return BinExpr(ctx.LT().getText(), self.visit(ctx.exp2(0)),self.visit(ctx.exp2(1)) )
        
        if ctx.LTE():
            return BinExpr(ctx.LTE().getText(), self.visit(ctx.exp2(0)),self.visit(ctx.exp2(1)) )
        
        return self.visit(ctx.exp2(0))
    # exp2: exp2 (AND | OR) exp3 | exp3;
    def visitExp2(self, ctx:MT22Parser.Exp2Context):
        
        if ctx.AND():
            return BinExpr(ctx.AND().getText(), self.visit(ctx.exp2()), self.visit(ctx.exp3()))
        if ctx.OR():
            return BinExpr(ctx.OR().getText(), self.visit(ctx.exp2()), self.visit(ctx.exp3()))
        return self.visit(ctx.exp3())

    # exp3: exp3 (ADD | MINUS) exp4 | exp4;
    def visitExp3(self, ctx:MT22Parser.Exp3Context):
        if ctx.ADD():
            return BinExpr(ctx.ADD().getText(), self.visit(ctx.exp3()), self.visit(ctx.exp4()))
        if ctx.MINUS():
            return BinExpr(ctx.MINUS().getText(), self.visit(ctx.exp3()), self.visit(ctx.exp4()))
        return self.visit(ctx.exp4())
    
    # exp4: exp4 (MUL | DIVIDE | MOD) exp5 | exp5;
    def visitExp4(self, ctx:MT22Parser.Exp4Context):
        if ctx.MUL():
            return BinExpr(ctx.MUL().getText(), self.visit(ctx.exp4()), self.visit(ctx.exp5()))
        if ctx.DIVIDE():
            return BinExpr(ctx.DIVIDE().getText(), self.visit(ctx.exp4()), self.visit(ctx.exp5()))
        if ctx.MOD():
            return BinExpr(ctx.MOD().getText(), self.visit(ctx.exp4()), self.visit(ctx.exp5()))
        return self.visit(ctx.exp5())
   
    # exp5: NOT exp5 | exp6;
    def visitExp5(self, ctx:MT22Parser.Exp5Context):
        if ctx.NOT():
            return UnExpr(ctx.NOT().getText(), self.visit(ctx.exp5()))
        return self.visit(ctx.exp6())
   
    # exp6: MINUS exp6 | exp7;
    def visitExp6(self, ctx:MT22Parser.Exp6Context):
        if ctx.MINUS():
            return UnExpr(ctx.MINUS().getText(), self.visit(ctx.exp6()))
        return self.visit(ctx.exp7())
   
    # exp7: ID LSB explist RSB | exp8;
    def visitExp7(self, ctx:MT22Parser.Exp7Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp8())
        return ArrayCell(ctx.ID().getText(), self.visit(ctx.explist()))
    
    # exp8: LB exp RB | INTLIT | ID | STRINGLIT | BOOLLIT | FLOATLIT | functioncall;
    def visitExp8(self, ctx:MT22Parser.Exp8Context):
        if ctx.exp():
            return self.visit(ctx.exp())
        if ctx.INTLIT():
            return IntegerLit(int(ctx.INTLIT().getText()))
        if ctx.ID():
            return Id(ctx.ID().getText())
        if ctx.STRINGLIT():
            return StringLit(ctx.STRINGLIT().getText())
        if ctx.BOOLLIT():
            return BooleanLit(ctx.BOOLLIT().getText() == "true")
        if ctx.FLOATLIT():
            return FloatLit(float('0' + ctx.FLOATLIT().getText()))
        if ctx.arraylit():
            return self.visit(ctx.arraylit())
        return self.visit(ctx.functioncall())

    
    # explist: exp COMMA explist | exp;
    def visitExplist(self, ctx: MT22Parser.ExplistContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.exp())]
        return [self.visit(ctx.exp())] + self.visit(ctx.explist())
   
    # functioncall: ID LB valuelist RB;
    def visitFunctioncall(self, ctx: MT22Parser.FunctioncallContext):
        return FuncCall(ctx.ID().getText(), self.visit(ctx.valuelist()))
  
    # valuelist: valueprime | ;
    def visitValuelist(self, ctx: MT22Parser.ValuelistContext):
        if ctx.getChildCount() == 0:
            return []

        return self.visit(ctx.valueprime())
   
    # valueprime: value COMMA valueprime | value;
    def visitValueprime(self, ctx: MT22Parser.ValueprimeContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.value())]
        return [self.visit(ctx.value())] + self.visit(ctx.valueprime())
   
    # value: exp | arraylit;
    def visitValue(self, ctx: MT22Parser.ValueContext):
        if ctx.exp():
            return self.visit(ctx.exp())
        return self.visit(ctx.arraylit())
   
    # paralist : paraprime | ;
    def visitParalist(self, ctx: MT22Parser.ParalistContext):
        if ctx.getChildCount() == 0:
            return []
        return self.visit(ctx.paraprime())
   
    # paraprime: para COMMA paraprime | para;
    def visitParaprime(self, ctx: MT22Parser.ParaprimeContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.para())]
        return [self.visit(ctx.para())] + self.visit(ctx.paraprime())
        
    # para: ID COLON paratype | INHERIT ID COLON paratype | OUT ID COLON paratype | INHERIT OUT ID COLON paratype;
    def visitPara(self, ctx: MT22Parser.ParaContext):
        if ctx.getChildCount() == 3:
            return ParamDecl(ctx.ID().getText(), self.visit(ctx.paratype()), False, False)
        if ctx.getChildCount() == 4:
            if ctx.INHERIT():
                return ParamDecl(ctx.ID().getText(), self.visit(ctx.paratype()), False, True)
            if ctx.OUT():
                return ParamDecl(ctx.ID().getText(), self.visit(ctx.paratype()), True, False)
        return ParamDecl(ctx.ID().getText(), self.visit(ctx.paratype()), True, True)
    
    
    # functype: vartype | VOID | AUTO ;
    def visitFunctype(self, ctx: MT22Parser.FunctypeContext):
        if ctx.VOID():
            return VoidType()
        if ctx.AUTO():
            return AutoType()
        return self.visit(ctx.vartype())
    
    # atomtype: BOOLEAN | INTEGER | FLOAT | STRING | AUTO;
    def visitAtomtype(self, ctx: MT22Parser.AtomtypeContext):
        if ctx.BOOLEAN():
            return BooleanType()
        elif ctx.INTEGER():
            return IntegerType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.AUTO():
            return AutoType()
        return StringType()
    
   
    # arraytype: ARRAY LSB dimension RSB OF atomtype;
    def visitArraytype(self, ctx: MT22Parser.ArraytypeContext):
        return ArrayType(self.visit(ctx.dimension()), self.visit(ctx.atomtype()))
    
   
    # dimension: INTLIT COMMA dimension | INTLIT;
    def visitDimension(self, ctx: MT22Parser.DimensionContext):
        if ctx.getChildCount() == 1:
            return [int(ctx.INTLIT().getText())]
        return [int(ctx.INTLIT().getText())] + self.visit(ctx.dimension())
    

    # arraylit: LCB item RCB;
    def visitArraylit(self, ctx: MT22Parser.ArraylitContext):
        return ArrayLit(self.visit(ctx.item()))
   
    # item : itemprime |; 
    def visitItem(self, ctx: MT22Parser.ItemContext):
        if ctx.getChildCount() == 0:
            return []
        return self.visit(ctx.itemprime())
   
    # itemprime: variable COMMA itemprime | variable;
    def visitItemprime(self, ctx: MT22Parser.ItemprimeContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.variable())]
        return [self.visit(ctx.variable())] + self.visit(ctx.itemprime())
  
    # variable: exp | arraylit;
    def visitVariable(self, ctx: MT22Parser.VariableContext):
        if ctx.exp():
            return self.visit(ctx.exp())
        return self.visit(ctx.arraylit())
    
    # statementlist: statement | blockstatement;
    def visitStatementlist(self, ctx: MT22Parser.StatementlistContext):
        if ctx.statement():
            return self.visit(ctx.statement())[0]
        return self.visit(ctx.blockstatement())
   
    # assignstatement: lhs ASSIGN exp SEMI | lhs ASSIGN arraylit SEMI;
    def visitAssignstatement(self, ctx: MT22Parser.AssignstatementContext):
        if ctx.exp():
            return AssignStmt(self.visit(ctx.lhs()), self.visit(ctx.exp()))
        return AssignStmt(self.visit(ctx.lhs()), self.visit(ctx.arraylit()))
   
    # lhs: ID | ID LSB explist RSB;
    def visitLhs(self, ctx: MT22Parser.LhsContext):
        if ctx.getChildCount() == 1:
            return Id(ctx.ID().getText())
        name = ctx.ID().getText()
        explist = self.visit(ctx.explist())
        return ArrayCell(name, explist)
   
    # ifstatement: IF LB exp RB  statementlist | IF LB exp RB statementlist ELSE statementlist;
    def visitIfstatement(self, ctx: MT22Parser.IfstatementContext):
        if ctx.ELSE():
            return IfStmt(self.visit(ctx.exp()), self.visit(ctx.statementlist(0)), self.visit(ctx.statementlist(1)))
        return IfStmt(self.visit(ctx.exp()), self.visit(ctx.statementlist(0)))
    
    # forstatement: FOR LB lhs ASSIGN exp COMMA exp COMMA exp RB statementlist;
    def visitForstatement(self, ctx: MT22Parser.ForstatementContext):
        
        lhs = self.visit(ctx.lhs())
        exp = self.visit(ctx.exp(0))
        assign = AssignStmt(lhs, exp)
        statementlist = self.visit(ctx.statementlist())
        return ForStmt(assign, self.visit(ctx.exp(1)), self.visit(ctx.exp(2)), statementlist)

   
    # whilestatement: WHILE LB exp RB statementlist;
    def visitWhilestatement(self, ctx: MT22Parser.WhilestatementContext):
        
        statementlist = self.visit(ctx.statementlist())
        return WhileStmt(self.visit(ctx.exp()), statementlist)

   
    # dowhilestatement: DO blockstatement WHILE LB exp RB SEMI;
    def visitDowhilestatement(self, ctx: MT22Parser.DowhilestatementContext):
        stmt = self.visit(ctx.blockstatement())
        cond = self.visit(ctx.exp())
        return DoWhileStmt(cond, stmt)
   
    # breakstatement: BREAK SEMI;
    def visitBreakstatement(self, ctx: MT22Parser.BreakstatementContext):
        return BreakStmt()
   
    # continuestatement: CONTINUE SEMI;
    def visitContinuestatement(self, ctx: MT22Parser.ContinuestatementContext):
        return ContinueStmt()
   
    # returnstatement: RETURN exp SEMI | RETURN SEMI | RETURN arraylit SEMI;
    def visitReturnstatement(self, ctx: MT22Parser.ReturnstatementContext):
        if ctx.getChildCount() == 2:
             return ReturnStmt(None)
        if ctx.exp():
            return ReturnStmt(self.visit(ctx.exp()))
        return ReturnStmt(self.visit(ctx.arraylit()))
   
    # callstatement: ID LB valuelist RB SEMI;
    def visitCallstatement(self, ctx: MT22Parser.CallstatementContext):
        name = ctx.ID().getText()
        args = self.visit(ctx.valuelist())
        return CallStmt(name, args)
   
    # blockstatement: LCB statementprime RCB | LCB RCB;
    def visitBlockstatement(self, ctx: MT22Parser.BlockstatementContext):
        if ctx.getChildCount() == 2:
            return BlockStmt([])
        body = self.visit(ctx.statementprime())
        return BlockStmt(body)
   
    # statementprime: statement statementprime | statement;
    def visitStatementprime(self, ctx: MT22Parser.StatementprimeContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.statement())
        return self.visit(ctx.statement()) + self.visit(ctx.statementprime())
   
    # statement: vardecl | assignstatement | ifstatement | forstatement | whilestatement | dowhilestatement | breakstatement | continuestatement | returnstatement | callstatement;
    def visitStatement(self, ctx: MT22Parser.StatementContext):
        if ctx.vardecl():
            return self.visit(ctx.vardecl())
        elif ctx.assignstatement():
            return [self.visit(ctx.assignstatement())]
        elif ctx.ifstatement():
            return [self.visit(ctx.ifstatement())]
        elif ctx.forstatement():
            return [self.visit(ctx.forstatement())]
        elif ctx.whilestatement():
            return [self.visit(ctx.whilestatement())]
        elif ctx.dowhilestatement():
            return [self.visit(ctx.dowhilestatement())]
        elif ctx.breakstatement():
            return [self.visit(ctx.breakstatement())]
        elif ctx.continuestatement():
            return [self.visit(ctx.continuestatement())]
        elif ctx.returnstatement():
            return [self.visit(ctx.returnstatement())]
        elif ctx.blockstatement():
            return [self.visit(ctx.blockstatement())]
        return [self.visit(ctx.callstatement())]