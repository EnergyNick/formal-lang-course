# Абстрактный синтаксис языка

```
prog = List<stmt>

stmt =
    bind of var * expr
  | print of expr

val =
    Bool of bool
  | String of string
  | Int of int

expr =
    Var of var                   // переменные
  | Val of val                   // константы
  | Set_start of Set<val> * expr // задать множество стартовых состояний
  | Set_final of Set<val> * expr // задать множество финальных состояний
  | Add_start of Set<val> * expr // добавить состояния в множество стартовых
  | Add_final of Set<val> * expr // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load of path                 // загрузка графа
  | Intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)
  | Smb of expr                  // единичный переход

lambda = Lambda of List<var> * expr

```

# Синтаксиса определенного языка

```

COMMENT: '//'[^\n]*

IDENT: [a-zA-Z] [0-9a-zA-Z]*
INT: '-'? [1-9][0-9]* | 0
STRING: '"' ([^\\"])* '"'
BOOL: 'true' | 'false'
ARG: IDENT | '_' | ('('(ARG ', ')* ARG')')

Value: INT | STRING | BOOL | Literals


Bind: 'var' ARG '=' Expr
Print: 'show' IDENT

Lambda: ARG '->' Expr

Statement: Bind | Print


Expr ->
    COMMENT
  | IDENT                                  
  | Value   
  | '(' expr ')'   
  | Expr 'starts =#' Expr               // Set
  | Expr 'finals =#' Expr               // Set
  | Expr 'starts =+' Expr               // Add
  | Expr 'finals =+' Expr               // Add
  | 'starts >>' Expr                    // Get...
  | 'finals >>' Expr            
  | 'reachables >>' Expr       
  | 'vertices >>' Expr         
  | 'edges >>' Expr            
  | 'labels >>' Expr                                 // ...Get
  | Lambda '=>' Expr                                 // Map
  | Lambda '?=>' Expr                                // Filter
  | 'import' Expr                                    // Load
  | Expr '/\' Expr                                   // Intersect
  | Expr '++' Expr                                   // Concat
  | Expr '&' Expr                                    // Union
  | Expr '*'                                         // Star
  | Expr '?>' Expr                                   // Contains
  | '{' (((Expr ', ')* Expr)? | INT '..' INT) '}'    // Set
  | Expr ==> Expr                                    // Единичный переход

Program: ((Statement ';' EOL)+ | COMMENT) Program | EOF

```

# Пример на языке

```
// Загрузка графа и установка стартовых и конечных вершин
var initial = import "TestGraph";
var extended = import "ExtendedTestGraph";

var upd1 = initial starts =+ {1..15}
var upd2 = upd1 finals =+ 0

// Перезапись вершин
var upd3 = upd2 starts =# extended

// Пересечение и комбинация графов
var cnct = (upd3) ++ upd2
var inter = upd2 /\ initial

show cnct ?> 0

show edges >> inter

// Фильтрация графов, у кого есть вершина 2
var res = (x -> (vertices >> x) ?> 2) ?=> {cnct, upd1, upd2}

```