grammar GraphLang;

COMMENT: '//'~[\n]* -> skip;

IDENT: [a-zA-Z][0-9a-zA-Z]*;
INT: '-'? [1-9][0-9]* | '0';
STRING: '"' (~[\\"])* '"';
BOOL: 'true' | 'false';

arg: IDENT | '_' | ('('(arg ', ')* arg')');
value: INT | STRING | BOOL;

bind: 'var' arg '=' expr;
print: 'show' expr;

lambda: arg '->' expr | '(' lambda ')';

statement: bind | print;


expr:
  arg
  | value
  | '(' expr ')'
  | expr 'starts =#' expr               // Set
  | expr 'finals =#' expr               // Set
  | expr 'starts =+' expr               // Add
  | expr 'finals =+' expr               // Add
  | 'starts >>' expr                    // Get...
  | 'finals >>' expr
  | 'reachables >>' expr
  | 'vertices >>' expr
  | 'edges >>' expr
  | 'labels >>' expr                                 // ...Get
  | lambda '=>' expr                                 // Map
  | lambda '?=>' expr                                // Filter
  | 'import' expr                                    // Load
  | expr '/\\' expr                                  // Intersect
  | expr '++' expr                                   // Concat
  | expr '&' expr                                    // Union
  | expr '*'                                         // Star
  | expr '?>' expr                                   // Contains
  | '{' (((expr ', ')* expr)? | INT '..' INT) '}'    // Set
  | expr '==>' expr                                  // Единичный переход
  ;

program: (statement ';')* EOF;
