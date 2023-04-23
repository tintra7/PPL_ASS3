# Generated from main/mt22/parser/MT22.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MT22Parser import MT22Parser
else:
    from MT22Parser import MT22Parser

# This class defines a complete generic visitor for a parse tree produced by MT22Parser.

class MT22Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by MT22Parser#program.
    def visitProgram(self, ctx:MT22Parser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#mt22.
    def visitMt22(self, ctx:MT22Parser.Mt22Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#decllist.
    def visitDecllist(self, ctx:MT22Parser.DecllistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#vardecl.
    def visitVardecl(self, ctx:MT22Parser.VardeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#idlist.
    def visitIdlist(self, ctx:MT22Parser.IdlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#vartype.
    def visitVartype(self, ctx:MT22Parser.VartypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#initialdecl.
    def visitInitialdecl(self, ctx:MT22Parser.InitialdeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#paratype.
    def visitParatype(self, ctx:MT22Parser.ParatypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#function.
    def visitFunction(self, ctx:MT22Parser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#functionbody.
    def visitFunctionbody(self, ctx:MT22Parser.FunctionbodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#exp.
    def visitExp(self, ctx:MT22Parser.ExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#exp1.
    def visitExp1(self, ctx:MT22Parser.Exp1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#exp2.
    def visitExp2(self, ctx:MT22Parser.Exp2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#exp3.
    def visitExp3(self, ctx:MT22Parser.Exp3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#exp4.
    def visitExp4(self, ctx:MT22Parser.Exp4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#exp5.
    def visitExp5(self, ctx:MT22Parser.Exp5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#exp6.
    def visitExp6(self, ctx:MT22Parser.Exp6Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#exp7.
    def visitExp7(self, ctx:MT22Parser.Exp7Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#exp8.
    def visitExp8(self, ctx:MT22Parser.Exp8Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#explist.
    def visitExplist(self, ctx:MT22Parser.ExplistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#functioncall.
    def visitFunctioncall(self, ctx:MT22Parser.FunctioncallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#valuelist.
    def visitValuelist(self, ctx:MT22Parser.ValuelistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#valueprime.
    def visitValueprime(self, ctx:MT22Parser.ValueprimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#value.
    def visitValue(self, ctx:MT22Parser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#paralist.
    def visitParalist(self, ctx:MT22Parser.ParalistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#paraprime.
    def visitParaprime(self, ctx:MT22Parser.ParaprimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#para.
    def visitPara(self, ctx:MT22Parser.ParaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#functype.
    def visitFunctype(self, ctx:MT22Parser.FunctypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#atomtype.
    def visitAtomtype(self, ctx:MT22Parser.AtomtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#arraytype.
    def visitArraytype(self, ctx:MT22Parser.ArraytypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#dimension.
    def visitDimension(self, ctx:MT22Parser.DimensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#arraylit.
    def visitArraylit(self, ctx:MT22Parser.ArraylitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#item.
    def visitItem(self, ctx:MT22Parser.ItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#itemprime.
    def visitItemprime(self, ctx:MT22Parser.ItemprimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#variable.
    def visitVariable(self, ctx:MT22Parser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#statementlist.
    def visitStatementlist(self, ctx:MT22Parser.StatementlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#assignstatement.
    def visitAssignstatement(self, ctx:MT22Parser.AssignstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#lhs.
    def visitLhs(self, ctx:MT22Parser.LhsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#ifstatement.
    def visitIfstatement(self, ctx:MT22Parser.IfstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#forstatement.
    def visitForstatement(self, ctx:MT22Parser.ForstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#whilestatement.
    def visitWhilestatement(self, ctx:MT22Parser.WhilestatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#dowhilestatement.
    def visitDowhilestatement(self, ctx:MT22Parser.DowhilestatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#breakstatement.
    def visitBreakstatement(self, ctx:MT22Parser.BreakstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#continuestatement.
    def visitContinuestatement(self, ctx:MT22Parser.ContinuestatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#returnstatement.
    def visitReturnstatement(self, ctx:MT22Parser.ReturnstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#callstatement.
    def visitCallstatement(self, ctx:MT22Parser.CallstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#blockstatement.
    def visitBlockstatement(self, ctx:MT22Parser.BlockstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#statementprime.
    def visitStatementprime(self, ctx:MT22Parser.StatementprimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#statement.
    def visitStatement(self, ctx:MT22Parser.StatementContext):
        return self.visitChildren(ctx)



del MT22Parser