exampleFromLang = """
var initial = import "TestGraph";
var extended = import "ExtendedTestGraph";

var upd1 = initial starts =+ {1..15};
var upd2 = upd1 finals =+ 0;

// Test
var upd3 = upd2 starts =# extended;

var cnct = (upd3) ++ upd2;
var inter = upd2 /\ initial;

show cnct ?> 0;

show edges >> inter;

var res = (x -> (vertices >> x) ?> 2) ?=> {cnct, upd1, upd2};
"""

exampleShorted = """
var initial = import "TestGraph";

var upd1 = initial starts =+ {1..15};
var inter = upd1 /\ initial;

show edges >> inter;
var res = (x -> (vertices >> x) ?> 2) ?=> {initial, upd1, inter};
"""

exampleDotFileContent = """digraph tree {
1 [label=program];
1 -> 2;
2 [label=statement];
2 -> 3;
3 [label=bind];
3 -> 4;
4 [label="TERM: var"];
3 -> 5;
5 [label=arg];
5 -> 6;
6 [label="TERM: initial"];
3 -> 7;
7 [label="TERM: ="];
3 -> 8;
8 [label=expr];
8 -> 9;
9 [label="TERM: import"];
8 -> 10;
10 [label=expr];
10 -> 11;
11 [label=value];
11 -> 12;
12 [label="TERM: \\\"TestGraph\\\""];
1 -> 13;
13 [label="TERM: ;"];
1 -> 14;
14 [label=statement];
14 -> 15;
15 [label=bind];
15 -> 16;
16 [label="TERM: var"];
15 -> 17;
17 [label=arg];
17 -> 18;
18 [label="TERM: upd1"];
15 -> 19;
19 [label="TERM: ="];
15 -> 20;
20 [label=expr];
20 -> 21;
21 [label=expr];
21 -> 22;
22 [label=arg];
22 -> 23;
23 [label="TERM: initial"];
20 -> 24;
24 [label="TERM: starts =+"];
20 -> 25;
25 [label=expr];
25 -> 26;
26 [label="TERM: {"];
25 -> 27;
27 [label="TERM: 1"];
25 -> 28;
28 [label="TERM: .."];
25 -> 29;
29 [label="TERM: 15"];
25 -> 30;
30 [label="TERM: }"];
1 -> 31;
31 [label="TERM: ;"];
1 -> 32;
32 [label=statement];
32 -> 33;
33 [label=bind];
33 -> 34;
34 [label="TERM: var"];
33 -> 35;
35 [label=arg];
35 -> 36;
36 [label="TERM: inter"];
33 -> 37;
37 [label="TERM: ="];
33 -> 38;
38 [label=expr];
38 -> 39;
39 [label=expr];
39 -> 40;
40 [label=arg];
40 -> 41;
41 [label="TERM: upd1"];
38 -> 42;
42 [label="TERM: /\\\"];
38 -> 43;
43 [label=expr];
43 -> 44;
44 [label=arg];
44 -> 45;
45 [label="TERM: initial"];
1 -> 46;
46 [label="TERM: ;"];
1 -> 47;
47 [label=statement];
47 -> 48;
48 [label=print];
48 -> 49;
49 [label="TERM: show"];
48 -> 50;
50 [label=expr];
50 -> 51;
51 [label="TERM: edges >>"];
50 -> 52;
52 [label=expr];
52 -> 53;
53 [label=arg];
53 -> 54;
54 [label="TERM: inter"];
1 -> 55;
55 [label="TERM: ;"];
1 -> 56;
56 [label=statement];
56 -> 57;
57 [label=bind];
57 -> 58;
58 [label="TERM: var"];
57 -> 59;
59 [label=arg];
59 -> 60;
60 [label="TERM: res"];
57 -> 61;
61 [label="TERM: ="];
57 -> 62;
62 [label=expr];
62 -> 63;
63 [label=lambda];
63 -> 64;
64 [label="TERM: ("];
63 -> 65;
65 [label=lambda];
65 -> 66;
66 [label=arg];
66 -> 67;
67 [label="TERM: x"];
65 -> 68;
68 [label="TERM: ->"];
65 -> 69;
69 [label=expr];
69 -> 70;
70 [label=expr];
70 -> 71;
71 [label="TERM: ("];
70 -> 72;
72 [label=expr];
72 -> 73;
73 [label="TERM: vertices >>"];
72 -> 74;
74 [label=expr];
74 -> 75;
75 [label=arg];
75 -> 76;
76 [label="TERM: x"];
70 -> 77;
77 [label="TERM: )"];
69 -> 78;
78 [label="TERM: ?>"];
69 -> 79;
79 [label=expr];
79 -> 80;
80 [label=value];
80 -> 81;
81 [label="TERM: 2"];
63 -> 82;
82 [label="TERM: )"];
62 -> 83;
83 [label="TERM: ?=>"];
62 -> 84;
84 [label=expr];
84 -> 85;
85 [label="TERM: {"];
84 -> 86;
86 [label=expr];
86 -> 87;
87 [label=arg];
87 -> 88;
88 [label="TERM: initial"];
84 -> 89;
89 [label="TERM: , "];
84 -> 90;
90 [label=expr];
90 -> 91;
91 [label=arg];
91 -> 92;
92 [label="TERM: upd1"];
84 -> 93;
93 [label="TERM: , "];
84 -> 94;
94 [label=expr];
94 -> 95;
95 [label=arg];
95 -> 96;
96 [label="TERM: inter"];
84 -> 97;
97 [label="TERM: }"];
1 -> 98;
98 [label="TERM: ;"];
1 -> 99;
99 [label="TERM: <EOF>"];
}
"""