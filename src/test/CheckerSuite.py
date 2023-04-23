# import unittest
# from TestUtils import TestChecker
# from AST import *


# class CheckerSuite(unittest.TestCase):
#     def test_no_entry_point(self):
#         self.assertTrue(TestChecker.test("""
#         main: function void() {
#             a: array[3] of integer = {1,2,3,4};
#         }
        
#         """, "No entry point", 401))
import unittest
from TestUtils import TestChecker
from AST import *


class CheckerSuite(unittest.TestCase):
    def test_no_entry_point(self):
        self.assertTrue(TestChecker.test("""any: function void () {
 printInteger(4);
 }""", "No entry point", 401))

    def test_valid_main_func_1(self):
        self.assertTrue(TestChecker.test("""
 main: function integer () {}
 """, "No entry point", 402))

    def test_valid_main_func_2(self):
        self.assertTrue(TestChecker.test("""
 main: function void (a: string) {}
 """, "No entry point", 403))

    def testVarSameNameAsFunc1(self):
        self.assertTrue(TestChecker.test("""
 main: integer;
 main: function void () {}
 """, "Redeclared Function: main", 404))

    def testVarSameNameAsFunc2(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {}
 main: integer;
 """, "Redeclared Variable: main", 405))

    def testRedeclaredFunc(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {}
 a: function void() {}
 a: function void() {}
 """, "Redeclared Function: a", 406))

    def testRedeclaredParam(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {}
 a: function void() {}
 b: function void(a: integer, a: string) inherit a {}
 """, "Redeclared Parameter: a", 407))

    def testRedeclaredVarInsideBlock(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a: integer;
 a: string;
 }
 """, "Redeclared Variable: a", 406))

    def testVarNameSameAsParamOne(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {}
 a: function void() {}
 b: function void(a: integer) inherit a {
 a: integer;
 }
 """, "Redeclared Variable: a", 408))

    def testRedeclarationInAnotherBlock(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {}
 a: function void() {}
 b: function void(a: integer) inherit a {
 {
 a: integer;
 }
 }
 """, "", 409))

    def testUndeclarationVar1(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a = b;
 }
 """, "Undeclared Identifier: b", 410))

    def testUndeclarationVar2(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a: integer = c;
 }
 """, "Undeclared Identifier: c", 411))

    def testUndeclarationFunc1(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a: integer = c();
 }
 """, "Undeclared Function: c", 412))

    def testUndeclarationFunc2(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 c();
 }
 """, "Undeclared Function: c", 413))

    def testUndeclaredArray(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a[1] = 5;
 }
 """, "Undeclared Identifier: a", 414))

    def testUseFunctionBeforeDecl(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 c();
 }
 c: function void() {}
 """, "", 415))

    def testAutoDeclNoInit(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a: auto;
 }
 """, "Invalid Variable: a", 416))

    def testParamInNoParentFunc(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {}
 x: function void (a: integer) {}
 """, "", 417))

    def testAccessArray1(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a: array[2] of integer;
 a[1] = 5;
 }
 """, "", 418))

    def testAccessArrayWithNonArray(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a: integer;
 a[1] = 5;
 }
 """, "Type mismatch in expression: ArrayCell(a, [IntegerLit(1)])", 419))

    def testAccessArrayWithNonIntegerIndex(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a: array[2] of integer;
 a["a string"] = 5;
 }
 """, "Type mismatch in expression: ArrayCell(a, [StringLit(a string)])", 420))

    def testBinOpType1(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a: integer = 5 + 6;
 }
 """, "", 421))

    def testBinOpType2(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a: integer = 5 + 6.5;
 }
 """, "Type mismatch in Variable Declaration: VarDecl(a, IntegerType, BinExpr(+, IntegerLit(5), FloatLit(6.5)))", 422))

    def testBinOpType3(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a: float = 5 + 6.5;
 }
 """, "", 423))

    def testBinOpType4(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a: float = 5;
 }
 """, "", 424))

    def testBinOpType4(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a: auto = 5 + 5 == 5;
 }
 """, "", 425))

    def testUnOpType1(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a: float = --6;
 }
 """, "", 426))

    def testUnOpType2(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a: boolean = !!true;
 }
 """, "", 427))

    def testFuncCall1(self):
        self.assertTrue(TestChecker.test("""
 return5: function integer() {
 return 5;
 }
 main: function void () {
 a: integer = return5();
 }
 """, "", 428))

    def testReturnWrongType(self):
        self.assertTrue(TestChecker.test("""
 return5: function void() {
 return 5;
 }
 main: function void () {
 a: integer = return5();
 }
 """, "Type mismatch in statement: ReturnStmt(IntegerLit(5))", 429))

    def testCallNonVoidInStmt(self):
        self.assertTrue(TestChecker.test("""
 return5: function integer() {
 return 5;
 }
 main: function void () {
 return5(); // thay noi ok tren forum
 }
 """, "", 430))

    def testParamMatch1(self):
        self.assertTrue(TestChecker.test("""
 nothing: function void() {}
 ok: function void(a: integer) inherit nothing {
 return;
 }
 main: function void () {
 ok(5);
 }
 """, "", 431))

    def testParamMatch2(self):
        self.assertTrue(TestChecker.test("""
 nothing: function void() {}
 ok: function void(a: integer) inherit nothing {
 return;
 }
 main: function void () {
 a: array[1] of integer;
 ok(a);
 }
 """, "Type mismatch in statement: CallStmt(ok, Id(a))", 432))

    def testParamMatch3(self):
        self.assertTrue(TestChecker.test("""
 nothing: function void() {}
 ok: function void(a: integer, b: array[3] of integer) inherit nothing {
 return;
 }
 main: function void () {
 ok(3, {1,2,3});
 }
 """, "", 433))

    def testParamMatch4(self):
        self.assertTrue(TestChecker.test("""
 nothing: function void() {}
 ok: function void(a: integer, b: array[3] of integer) inherit nothing {
 return;
 }
 main: function void () {
 ok(3, {1,2,3,4});
 }
 """,
                                         "Type mismatch in statement: CallStmt(ok, IntegerLit(3), ArrayLit([IntegerLit(1), IntegerLit(2), IntegerLit(3), IntegerLit(4)]))",
                                         434))

    def testParamMatch5(self):
        self.assertTrue(TestChecker.test("""
 nothing: function void() {}
 ok: function void(a: integer, b: array[2,2] of integer) inherit nothing {
 {
 a: integer;
 }
 }
 main: function void () {
 ok(3, {{1,2},{1,2}});
 }
 """, "", 435))

    def testIfStmt1(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a: auto = false;
 if (a) {
 a: auto = 3;
 } else
 main();
 }
 """, "", 436))

    def testIfStmt2(self):
        self.assertTrue(TestChecker.test("""
 a: function auto() {
 return true;
 }
 main: function void () {
 if (a()) {
 a: auto = 3;
 } else
 main();
 }
 """, "", 437))

    def testIfStmt3(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 if (a()) {
 a: auto = 3;
 }
 }
 a: function auto() {
 return true;
 } 
 """, "", 438))

    def testWhile(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 x: auto = 5;
 while (a())
 x = a();
 }
 a: function auto() {
 return true;
 } 
 """, "Type mismatch in statement: AssignStmt(Id(x), FuncCall(a, []))", 439))

    def testDoWhile(self):
        self.assertTrue(TestChecker.test("""

 main: function void () {
 do {
 while (false) {
 a: auto = 5;
 }
 } while(x());
 }
 x: function boolean() {}
 """, "", 440))

    def testFor(self):
        self.assertTrue(TestChecker.test("""

 main: function void () {
 a: integer;
 i: integer;
 for (i = 3, i <= a, a) {
 i: integer = i;
 }
 }
 """, "", 441))

    def testArrayDecl2(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a: array[2,2] of float = {{1,2.5},{foo(),4}}; // {1, 2.5} => illegal array lit
 }
 foo: function auto() {
 return 5;
 } 
 """, "Illegal array literal: ArrayLit([IntegerLit(1), FloatLit(2.5)])", 443))

    def testArrayDecl4(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a: array[2,2] of integer = {1,2,{1}};
 }
 """, "Illegal array literal: ArrayLit([IntegerLit(1), IntegerLit(2), ArrayLit([IntegerLit(1)])])", 445))

    def testFirstStmt(self):
        self.assertTrue(TestChecker.test("""
 x: function string (a: integer) {

 }
 y: function void () {}

 main: function void () inherit x {
 //preventDefault();
 super(5);
 //super(); # error
 a: integer;
 }
 """, "", 446))

    def testFirstStmt1(self):
        self.assertTrue(TestChecker.test("""
 x: function string (a: integer) {

 }
 y: function void () {}

 main: function void () inherit x {
 super(5);
 a: integer;
 }
 """, "", 447))

    def testFirstStmt2(self):
        self.assertTrue(TestChecker.test("""
 x: function string (a: integer) {

 }
 y: function void () {}

 main: function void () inherit x {
 super("Hello World");
 a: integer;
 }
 """, "Type mismatch in expression: StringLit(Hello World)", 448))

    def testFirstStmt3(self):
        self.assertTrue(TestChecker.test("""
 x: function string (a: integer) {

 }
 y: function void () {}

 main: function void () inherit x {
 preventDefault();
 a: integer;
 }
 """, "", 449))

    def testFirstStmt4(self):
        self.assertTrue(TestChecker.test("""
 x: function string (a: integer) {

 }
 y: function void () {}

 main: function void () inherit x {
 a: integer;
 }
 """, "Invalid statement in function: main", 450))

    def testFirstStmt5(self):
        self.assertTrue(TestChecker.test("""
 x: function string (a: integer) {

 }
 y: function void () {}

 main: function void () inherit y {
 a: integer;
 }
 """, "", 451))

    def testFirstStmt6(self):
        self.assertTrue(TestChecker.test("""
 x: function string (a: integer) {

 }
 y: function void () {}

 main: function void () inherit y {
 preventDefault();
 a: integer;
 }
 """, "", 452))

    def testFirstStmt7(self):
        self.assertTrue(TestChecker.test("""
 x: function string (a: integer) {

 }
 y: function void () {}

 main: function void () inherit y {
 super();
 a: integer;
 }
 """, "", 453))

    def testFirstStmt8(self):
        self.assertTrue(TestChecker.test("""
 y: function void () {}
 main: function void () inherit y {
 super(1,2);
 a: integer;
 }
 """, "Type mismatch in expression: IntegerLit(1)", 454))

    def testMisplacedPreventDefault1(self):
        self.assertTrue(TestChecker.test("""
 x: function string (a: integer) {

 }
 y: function void () {}

 main: function void () inherit y {
 a: integer;
 preventDefault();
 }
 """, "", 455))

    def testMisplacedPreventDefault2(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a: integer;
 preventDefault();
 }
 """, "", 456))

    def testInheritNon_existentFunc(self):
        self.assertTrue(TestChecker.test("""
 main: function void () inherit x {
 a: integer;
 }
 """, "Undeclared Function: x", 457))

    def testInheritNon_existentFunc(self):
        self.assertTrue(TestChecker.test("""
 main: function void () inherit x {
 a: integer;
 }
 """, "Undeclared Function: x", 458))

    def testInvalidParam1(self):
        self.assertTrue(TestChecker.test("""
 x: function void(inherit a: integer) {}
 y: function void(inherit b: string) inherit x {
 preventDefault();
 }
 z: function void (a: boolean) inherit y {
 super("a string");
 }
 main: function void () {}
 """, "", 459))

    def testInvalidParam2(self):
        self.assertTrue(TestChecker.test("""
 x: function void(inherit a: integer) {}
 y: function void(inherit b: string) inherit x {
 preventDefault();
 }
 z: function void (b: boolean) inherit y {
 super("a string");
 }
 main: function void () {}
 """, "Invalid Parameter: b", 460))

    def testInheritParam1(self):
        self.assertTrue(TestChecker.test("""
 y: function void(inherit b: string) {
 preventDefault();
 }
 z: function void (c: boolean) inherit y {
 super("a string");
 d: boolean = c;
 e: auto = b;
 y(e);
 }
 main: function void () {}
 """, "", 461))

    def testInheritParam2(self):
        self.assertTrue(TestChecker.test("""
 y: function void(inherit b: string, c: string) {
 preventDefault();
 }
 z: function void (c: boolean) inherit y {
 super("a string", "another string");
 d: boolean = c;
 e: auto = b;
 y(e, e);
 }
 main: function void () {}
 """, "", 462))

    def testReturnStmtsInSameBlock1(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 return;
 return 3;
 }
 """, "", 463))

    def testReturnStmtsInSameBlock2(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 return 3;
 return;
 }
 """, "Type mismatch in statement: ReturnStmt(IntegerLit(3))", 464))

    def testReturnStmtsInSameBlock3(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 if (true) {
 return;
 } else {
 return;
 return {1,2,3};
 }
 return 3; // it should've been ignored but maybe too complicated to do so
 }
 """, "Type mismatch in statement: ReturnStmt(IntegerLit(3))", 465))

    def testBreakNotInLoop1(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 if (true) {
 break;
 }
 }
 """, "Must in loop: BreakStmt()", 466))

    def testBreakNotInLoop2(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 while (true) {
 if (true) {
 continue;
 }
 }
 }
 """, "", 467))

    def testAutoParam1(self):
        self.assertTrue(TestChecker.test("""
 x: function void (a: auto, b: auto) {
 c: integer = a;
 printBoolean(5 == a); // asssure that a is integer
 e: string = b;
 f: string = e :: "Hello"; // asssure that a is string
 }
 main: function void () {} 
 """, "", 468))

    def testAutoParam2(self):
        self.assertTrue(TestChecker.test("""
 y: function auto() {}
 x: function void (a: auto) {
 i: integer;
 for (i = a, i < 5, i + 1) {
 printBoolean(5 == a); // asssure that a is integer
 }
 i = y; // ref: https://e-learning.hcmut.edu.vn/mod/forum/discuss.php?d=8943
 }
 main: function void () {} 
 """, "Undeclared Identifier: y", 469))

    def testAutoParam3(self):
        self.assertTrue(TestChecker.test("""
 x: function void (a: auto) {
 i: integer;
 a = i;
 printBoolean(5 == a); // asssure that a is integer
 }
 main: function void () {} 
 """, "", 470))

    def testAutoParam4(self):
        self.assertTrue(TestChecker.test("""
 y: function void (a: string) {}
 x: function void (a: auto) {
 y(a);
 b: string = a :: "Hello"; // asssure that a is string
 }
 main: function void () {
 x("a string");
 } 
 """, "", 471))

    def testAutoParam5(self):
        self.assertTrue(TestChecker.test("""
 y: function void (a: string) {}
 x: function void (a: auto) {
 y(a);
 b: string = a :: "Hello"; // asssure that a is string
 }
 main: function void () {
 x(5);
 } 
 """, "Type mismatch in statement: CallStmt(x, IntegerLit(5))", 472))

    def testAutoParam6(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 x(5, {1,2,3});
 } 
 x: function void (a: integer, a: auto) {} 
 """, "Redeclared Parameter: a", 473))

    def testAutoParam7(self):
        self.assertTrue(TestChecker.test("""
 x: function void (a: auto, b: integer) {
 a = a + b;
 }
 main: function void () {
 x(5, 6); // asssure that a is integer
 } 
 """, "", 474))

    def testInferVoidFunc(self):
        self.assertTrue(TestChecker.test("""
 x: function auto() {}
 main: function void () {
 // according to https://e-learning.hcmut.edu.vn/mod/forum/discuss.php?d=8936
 // func in call stmt will no longer be inferred to void anymore
 x();
 a: integer = x(); // now it become int
 } 
 """, "", 475))

    def testAutoParam8(self):
        self.assertTrue(TestChecker.test("""
 y: function auto() {}
 x: function void (a: auto) {
 a = a + y() + 1;
 printInteger(a + y());
 }
 main: function void () {} 
 """, "", 476))

    def testBinOpType5(self):
        self.assertTrue(TestChecker.test("""
 y: function auto() {}
 main: function void () {
 a: auto = 5 + y() + 2.5;
 printFloat(a);
 } 
 """, "", 477))

    def testBinOpType6(self):
        self.assertTrue(TestChecker.test("""
 y: function auto() {}
 main: function void () {
 a: auto = true && y() == false || (5 < 5.5);
 printBoolean(a);
 } 
 """, "", 478))

    def testBinOpType7(self):
        self.assertTrue(TestChecker.test("""
 x: function auto() {}
 y: function auto() {}
 z: function auto() {}
 t: function auto() {}
 m: function auto() {}
 main: function void () {
 a: auto = z() && y() == false || (5 < x());
 printBoolean(a);
 b: auto = m() :: (t() :: "sfdgd");
 printString(b);
 } 
 """, "", 479))

    def testRedeclareSpecialFunc(self):
        self.assertTrue(TestChecker.test("""
 super: string;
 main: function void () {} 
 """, "Redeclared Variable: super", 480))

    def testParamSameNameAsFunc(self):
        self.assertTrue(TestChecker.test("""
 a: function void(a: integer) {
 a();
 }
 main: function void () {} 
 """, "Type mismatch in statement: CallStmt(a, )", 481))

    def testAccessArray2(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a: auto = {{1,2,3}, {3,4,5}, {5,6,7}};
 b: array[3] of integer = a[1];
 c: array[2] of integer = a[2];
 } 
 """, "Type mismatch in Variable Declaration: VarDecl(c, ArrayType([2], IntegerType), ArrayCell(a, [IntegerLit(2)]))",
                                         482))

    def testAccessArray3(self):
        self.assertTrue(TestChecker.test("""
 printArray: function void (arr: array[2] of integer) {
 i: integer;
 for (i = 0, i < 5, i % 2)
 printInteger(arr[i]);
 }
 main: function void () {
 a: array[3,2] of integer = {{1,2}, {3,4}, {6,7}};
 printArray(a[1]);
 i: integer;
 for (i = a[0,99], i < 92929, i % a[1010,93939]) {}
 } 
 """, "", 483))

    def testBinOpType8(self):
        self.assertTrue(TestChecker.test("""
 x: function auto() {}
 y: function auto() {}
 z: function auto() {}
 t: function auto() {}
 m: function auto() {}
 main: function void () {
 a: auto = z() && y() == false || (t() + m() + 1 < x());
 printInteger(t());
 printInteger(x());
 } 
 """, "", 484))

    def testRedeclareInDifferentBlock(self):
        self.assertTrue(TestChecker.test("""
 x: integer;
 mainx: function void (x: string) {
 {
 x: boolean;
 }
 } 
 main: function void () {}
 """, "", 485))

    def testBinOpType9(self):
        self.assertTrue(TestChecker.test("""
 x: function auto() {}
 main: function void () {
 a: auto = -5 + 2 + x();
 printInteger(a);
 printFloat(a);
 b: auto = -5 * 2e5 / x();
 printFloat(b); 
 printInteger(b); // error here
 } 
 """, "Type mismatch in statement: CallStmt(printInteger, Id(b))", 486))

    def testAutoParam9(self):
        self.assertTrue(TestChecker.test("""
 x: function auto(x: auto) {
 x = 4; // param x type is inferred here
 printInteger(x);
 }
 main: function void () {
 printString(x(3)); // x return_type is inferred here
 } 
 """, "", 487))

    def testArgsNumber1(self):
        self.assertTrue(TestChecker.test("""
 x: function auto(x: auto) {
 x = 4;
 printInteger(x);
 }
 main: function void () {
 x();
 } 
 """, "Type mismatch in statement: CallStmt(x, )", 488))

    def testArgsNumber2(self):
        self.assertTrue(TestChecker.test("""
 x: function auto(x: auto) {
 x = 4;
 printInteger(x);
 }
 main: function void () {
 x(4,6); // error ref: https://e-learning.hcmut.edu.vn/mod/forum/discuss.php?d=8891
 } 
 """, "Type mismatch in statement: CallStmt(x, IntegerLit(4), IntegerLit(6))", 489))

    def testAutoParent(self):
        self.assertTrue(TestChecker.test("""
 a: float = foo(1, 2) + 1.5;
 foo: function auto(a: integer, b: integer) {
 return a + b; 
 }
 x: function auto() {
 printFloat(foo(1,2));
 }
 main: function void () inherit x {
 //super(); // x return_type still remains auto after super call, not void
 // just do as what the TA said
 printInteger(x()); // now x return_type should become integer
 } 
 """, "", 490))

    def testRandom1(self):
        self.assertTrue(TestChecker.test("""
 x: function auto() {
 return false;
 }
 main: function void () {
 a: integer = readInteger();
 if (true) {
 a: integer = 5;
 } else if (false) {
 a: auto = readFloat();
 } else {
 x();
 i: auto = 123 + 34445;
 for (i = i, i == i, i)
 i = i;
 }
 }
 """, "", 491))

    def testRandom2(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 // ref for the error: https://e-learning.hcmut.edu.vn/mod/forum/discuss.php?d=9023
 x();
 }
 x: function auto() {}
 x: function auto(a: auto, b: auto) {}
 """, "Redeclared Function: x", 492))

    def testRandom3(self):
        self.assertTrue(TestChecker.test("""
 x: function auto(a: auto, b: auto) {}
 main: function void () {
 x(); 
 }
 x: function auto() {}
 """, "Type mismatch in statement: CallStmt(x, )", 493))

    def testRandom4(self):
        self.assertTrue(TestChecker.test("""
 x: function auto() inherit y {
 super(kjhgfd);
 a = hdhdhdhddhdhdhdh;
 }
 main: function void () {}
 y: function auto(inherit a: auto, inherit b: auto, inherit a: auto, inherit b: integer) {} 
 """, "Redeclared Parameter: a", 494))

    def testRandom5(self):
        self.assertTrue(TestChecker.test("""
 y: function void(c: auto) {}
 x: function void(a: integer) inherit y {
 super(a);
 }
 main: function void () {
 x(1);
 y("a string");
 }
 """, "Type mismatch in statement: CallStmt(y, StringLit(a string))", 495))

    def testRandom6(self):
        self.assertTrue(TestChecker.test("""
 y: function void(inherit c: auto) {}
 x: function void(a: integer) inherit y {
 super(6);
 a = c;
 } 
 z: function void(a: integer) inherit y {
 preventDefault();
 a = c; // error here, https://e-learning.hcmut.edu.vn/mod/forum/discuss.php?d=9112
 }
 main: function void () {}
 """, "", 496))

    def testRandom7(self):
        self.assertTrue(TestChecker.test("""
 y: function void(inherit c: auto, d: auto, e: auto) {}
 x: function void(a: integer) inherit y {
 super(5,6); // error here
 } 
 main: function void () {}
 """, "Type mismatch in expression: ", 497))

    def testRandom8(self):
        self.assertTrue(TestChecker.test("""
 y: float = -foo(1,1); 
 foo: function auto(a: auto, b:auto){
 x: auto = a;
 } 
 bar: function void() {}
 main: function void() {
 bar: integer = 1;
 x: float = bar();
 x = bar;
 } 
 """, "Type mismatch in expression: FuncCall(bar, [])", 498))

    def testRandom9(self):
        self.assertTrue(TestChecker.test("""
 foo: function void(a: integer){}
 main: function void() {
 foo(1, a); // https://e-learning.hcmut.edu.vn/mod/forum/discuss.php?d=8834#p25359
 } 
 """, "Type mismatch in statement: CallStmt(foo, IntegerLit(1), Id(a))", 499))

    def testRandom10(self):
        self.assertTrue(TestChecker.test("""
 foo: function auto(a: integer){}
 main: function void() {
 x: boolean = 1 == true; // https://e-learning.hcmut.edu.vn/mod/forum/discuss.php?d=9221
 y: array [1,2,3] of integer;
 z: auto = y[1,1+1-0];
 t: integer = foo(1, a);
 } 
 """, "Type mismatch in expression: FuncCall(foo, [IntegerLit(1), Id(a)])", 500))

    def testRandom11(self):
        self.assertTrue(TestChecker.test("""
 M: function void (a: integer) inherit N {} 
 N: function void (inherit a: integer) {} 
 // https://e-learning.hcmut.edu.vn/mod/forum/discuss.php?d=9346
 """, "Invalid Parameter: a", 501))

    def testRandom11(self):
        self.assertTrue(TestChecker.test("""
 M: function array[3] of integer (a: integer) {
 return {a + 1, a - 1, a, a + 1};
 } 
 """,
                                         "Type mismatch in statement: ReturnStmt(ArrayLit([BinExpr(+, Id(a), IntegerLit(1)), BinExpr(-, Id(a), IntegerLit(1)), Id(a), BinExpr(+, Id(a), IntegerLit(1))]))",
                                         502))

    def testRandom12(self):
        self.assertTrue(TestChecker.test("""
 foo: function auto() {}
 main: function void () {
 a: array[2,3] of integer = foo();
 b: auto = foo();
 c: array[3] of integer = b[0];
 } 
 """, "", 503))

    def testRandom13(self):
        self.assertTrue(TestChecker.test("""
 foo: function auto() {}
 bar: function void (a: auto) {
 a = foo() + foo();
 } 
 main: function void() {}
 """, "", 504))

    def testRandom14(self):
        self.assertTrue(TestChecker.test("""
 bar: function void () {}
 foo: function auto() inherit bar {
 preventDefault(4); // item 3, https://e-learning.hcmut.edu.vn/mod/forum/discuss.php?d=9403
 }
 main: function void () {} 
 """, "Type mismatch in expression: IntegerLit(4)", 505))

    def testRandom15(self):
        self.assertTrue(TestChecker.test("""
 main: function void () {
 a: auto = {{{1,2},{4,1}},{{3.5,4.6},{4.5,7.7}}};
 } 
 """,
                                         "Illegal array literal: ArrayLit([ArrayLit([ArrayLit([IntegerLit(1), IntegerLit(2)]), ArrayLit([IntegerLit(4), IntegerLit(1)])]), ArrayLit([ArrayLit([FloatLit(3.5), FloatLit(4.6)]), ArrayLit([FloatLit(4.5), FloatLit(7.7)])])])",
                                         506))

    def testRandom16(self):
        self.assertTrue(TestChecker.test("""
 x: function auto () {
 if (true) 
 return true;
 else
 return 1;
 }
 main: function void () {} 
 """, "Type mismatch in statement: ReturnStmt(IntegerLit(1))", 507))

    def testRandom17(self):
        self.assertTrue(TestChecker.test("""
 x: function auto (a: auto, b: auto) {
 while(true)
 return true;
 return 1;
 }
 main: function void () {} 
 """, "Type mismatch in statement: ReturnStmt(IntegerLit(1))", 508))

    def testRandom18(self):
        self.assertTrue(TestChecker.test("""
 x: function auto () {
 y("string", 4);
 }
 main: function void () {} 
 y: function auto (a: auto, b: integer) {
 x: integer = a + b;
 }
 """, "Type mismatch in expression: BinExpr(+, Id(a), Id(b))", 509))

    