grammar MT22;
// MSSV: 2010702
@lexer::header {
from lexererr import *
}

options{
	language=Python3;
}

program: mt22 EOF ;
mt22: decllist mt22 | decllist;

decllist: vardecl | function;
vardecl: idlist COLON vartype SEMI | initialdecl SEMI;
idlist: ID COMMA idlist | ID;//
vartype: atomtype | arraytype;
initialdecl: ID COMMA initialdecl COMMA value
			| ID COLON paratype ASSIGN value;
			
			
paratype: vartype | AUTO;
// function declaration
function: ID COLON FUNCTION functype LB paralist RB functionbody | ID COLON FUNCTION functype LB paralist RB INHERIT ID functionbody;
functionbody: blockstatement;
// expression
exp: exp1 DCOLON exp1 | exp1 | functioncall;
exp1: exp2 EQUAL exp2 | exp2 NOTEQUAL exp2 | exp2 GT exp2 | exp2 LT exp2 | exp2 LTE exp2 | exp2 GTE exp2 | exp2;
exp2: exp2 AND exp3 | exp2 OR exp3 | exp3;
exp3: exp3 ADD exp4 | exp3 MINUS exp4 | exp4;
exp4: exp4 MUL exp5 | exp4 DIVIDE exp5 | exp4 MOD exp5 | exp5;
exp5: NOT exp5 | exp6;
exp6: MINUS exp6 | exp7;
exp7: ID LSB explist RSB | exp8;
exp8: LB exp RB | INTLIT | ID | STRINGLIT | BOOLLIT | FLOATLIT | functioncall | arraylit;
explist: exp COMMA explist | exp;
functioncall: ID LB valuelist RB;
valuelist: valueprime | ;
valueprime: value COMMA valueprime | value;
value: exp | arraylit;
paralist : paraprime | ;
paraprime: para COMMA paraprime | para;
para: ID COLON paratype | INHERIT ID COLON paratype | OUT ID COLON paratype | INHERIT OUT ID COLON paratype;
functype: vartype | VOID | AUTO ;
// atomic type
atomtype: BOOLEAN | INTEGER | FLOAT | STRING | AUTO ;//

// array type
arraytype: ARRAY LSB dimension RSB OF atomtype;//
dimension: INTLIT COMMA dimension | INTLIT;//
arraylit: LCB item RCB;
item : itemprime |; //
itemprime: variable COMMA itemprime | variable;//
variable: exp | arraylit;

// statement
statementlist: statement | blockstatement;
assignstatement: lhs ASSIGN exp SEMI | lhs ASSIGN arraylit SEMI;
lhs: ID | ID LSB explist RSB;//
ifstatement: IF LB exp RB  statementlist | IF LB exp RB statementlist ELSE statementlist;
forstatement: FOR LB lhs ASSIGN exp COMMA exp COMMA exp RB statementlist;
whilestatement: WHILE LB exp RB statementlist;
dowhilestatement: DO blockstatement WHILE LB exp RB SEMI;
breakstatement: BREAK SEMI;//
continuestatement: CONTINUE SEMI;//
returnstatement: RETURN exp SEMI | RETURN SEMI | RETURN arraylit SEMI;
callstatement: ID LB valuelist RB SEMI;
blockstatement: LCB statementprime RCB | LCB RCB;
statementprime: statement statementprime | statement;
statement: vardecl | assignstatement | ifstatement 
			| forstatement | whilestatement 
			| dowhilestatement | breakstatement | continuestatement 
			| returnstatement | callstatement | blockstatement;


// Keyword
AUTO: 'auto';
BREAK: 'break';
BOOLEAN: 'boolean';
DO: 'do';
ELSE: 'else';
fragment FALSE: 'false';
FLOAT: 'float';
FOR: 'for';
FUNCTION: 'function';
IF: 'if';
INTEGER: 'integer';
RETURN: 'return';
STRING: 'string';
fragment TRUE: 'true';
WHILE: 'while';
VOID: 'void';
OUT: 'out';
CONTINUE: 'continue';
OF: 'of';
INHERIT: 'inherit';
ARRAY: 'array';

// Operation
ADD: '+';
MINUS: '-';
MUL: '*';
DIVIDE: '/';
MOD: '%';
NOT: '!';
AND: '&&';
OR: '||';
EQUAL: '==';
NOTEQUAL: '!=';
LT: '<';
LTE: '<=';
GT: '>';
GTE: '>=';
DCOLON: '::';


// Seperator
LB: '(';
RB: ')';
LCB: '{';
RCB: '}';
LSB: '[';
RSB: ']';
DOT: '.';
COMMA: ',';
SEMI: ';';
COLON: ':';
ASSIGN: '=';

// Literals

fragment INTPART: [1-9] [0-9]* ('_' [0-9]+)* | [0];//DIGIT | ([1-9] UNDERSCORE? (DIGIT UNDERSCORE? DIGIT?)*)
INTLIT:  INTPART {self.text = self.text.replace('_', '')};
FLOATLIT: (INTPART DECIMAPART | INTPART DECIMAPART? EXPONENT | DECIMAPART EXPONENT ) {self.text = self.text.replace('_', '')};
BOOLLIT: TRUE | FALSE;
STRINGLIT: DOUBLE_QUOTE (ESC | CHARACTER)* DOUBLE_QUOTE {self.text = str(self.text)[1:-1]}; 
fragment ESC: '\\' [bnfrt'"\\];
fragment CHARACTER: ~[\\"];
fragment DOUBLE_QUOTE: '"';
// fragment INTPART: '0' | [1-9]+ ('_' [0-9]+)* [0-9]*;
fragment DECIMAPART: [.] [0-9]*;
fragment EXPONENT: [Ee] [+-]? [0-9]+;


// Identifier
ID: [A-Za-z_] [A-Za-z_0-9]*;

// Comment
BLOCKCOMMENT: '/*' .*? '*/' -> skip;
LINECOMMENT: '//' ~[\n\r]* -> skip; 


WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines

UNCLOSE_STRING: DOUBLE_QUOTE (ESC | CHARACTER)* {
	unclose_str = str(self.text);
	possible = ['\b', '\t', '\f', '\n', '\r', '"', '\\']
	if unclose_str[-1] in possible:
		raise UncloseString(unclose_str[1:-1])
	else:
		raise UncloseString(unclose_str[1:])};
ILLEGAL_ESCAPE: DOUBLE_QUOTE CHARACTER* '\\' ~[bnfrt'"\\] {
	illegal_str = str(self.text)
	raise IllegalEscape(illegal_str[1:])
};
ERROR_CHAR: .{raise ErrorToken(self.text)};
