grammar GraphLang;

COMMENT: '//'~[\n]* -> skip;

IDENT: [a-zA-Z][0-9a-zA-Z]*;
INT: '-'? [1-9][0-9]* | '0';
STRING: '"' (~[\\"])* '"';
BOOL: 'true' | 'false';

arg: IDENT   #nameArg
    | '_'    #emptyArg
    ;

setBody:
    ((expr ', ')* expr)?   #setBodyElements
    | INT '..' INT         #setBodyRange
    ;

value:
    INT                 #integerVal
    | STRING            #stringVal
    | BOOL              #booleanVal
    | '{' setBody '}'   #setVal
    ;

bind: 'var' arg '=' expr;
print: 'show' expr;

lambda:
    arg '->' expr     #lambdaBody
    | '(' lambda ')'  #lambdaBrackets
    ;

statement: bind | print;


expr:
  arg                               #varExp
  | value                           #valExp
  | '(' expr ')'                    #bracketExp
  | expr 'starts =#' expr           #setStartExp
  | expr 'finals =#' expr           #setFinalExp
  | expr 'starts =+' expr           #addStartExp
  | expr 'finals =+' expr           #addFinalExp
  | 'starts >>' expr                #getStartExp
  | 'finals >>' expr                #getFinalExp
  | 'reachables >>' expr            #reachExp
  | 'vertices >>' expr              #vertsExp
  | 'edges >>' expr                 #edgeExp
  | 'labels >>' expr                #labelExp
  | lambda '=>' expr                #mapExp
  | lambda '?=>' expr               #filterExp
  | 'import' expr                   #loadExp
  | expr '/\\' expr                 #interExp
  | expr '++' expr                  #concatExp
  | expr '&' expr                   #unionExp
  | expr '^'                        #starExp
  | expr '?>' expr                  #containExp
  | expr '*' expr                   #multExp
  | expr '+' expr                   #sumExp
  | expr '-' expr                   #subExp
  | expr '/' expr                   #divExp
  | expr '%' expr                   #modExp
  | expr '==' expr                  #equalExp
  ;

program: (statement ';')* EOF;
