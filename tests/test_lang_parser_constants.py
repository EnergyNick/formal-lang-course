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
12 [label="TERM: \\"TestGraph\\""];
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
26 [label=value];
26 -> 27;
27 [label="TERM: {"];
26 -> 28;
28 [label="TERM: 1"];
26 -> 29;
29 [label="TERM: .."];
26 -> 30;
30 [label="TERM: 15"];
26 -> 31;
31 [label="TERM: }"];
1 -> 32;
32 [label="TERM: ;"];
1 -> 33;
33 [label=statement];
33 -> 34;
34 [label=bind];
34 -> 35;
35 [label="TERM: var"];
34 -> 36;
36 [label=arg];
36 -> 37;
37 [label="TERM: inter"];
34 -> 38;
38 [label="TERM: ="];
34 -> 39;
39 [label=expr];
39 -> 40;
40 [label=expr];
40 -> 41;
41 [label=arg];
41 -> 42;
42 [label="TERM: upd1"];
39 -> 43;
43 [label="TERM: /\\"];
39 -> 44;
44 [label=expr];
44 -> 45;
45 [label=arg];
45 -> 46;
46 [label="TERM: initial"];
1 -> 47;
47 [label="TERM: ;"];
1 -> 48;
48 [label=statement];
48 -> 49;
49 [label=print];
49 -> 50;
50 [label="TERM: show"];
49 -> 51;
51 [label=expr];
51 -> 52;
52 [label="TERM: edges >>"];
51 -> 53;
53 [label=expr];
53 -> 54;
54 [label=arg];
54 -> 55;
55 [label="TERM: inter"];
1 -> 56;
56 [label="TERM: ;"];
1 -> 57;
57 [label=statement];
57 -> 58;
58 [label=bind];
58 -> 59;
59 [label="TERM: var"];
58 -> 60;
60 [label=arg];
60 -> 61;
61 [label="TERM: res"];
58 -> 62;
62 [label="TERM: ="];
58 -> 63;
63 [label=expr];
63 -> 64;
64 [label=lambda];
64 -> 65;
65 [label="TERM: ("];
64 -> 66;
66 [label=lambda];
66 -> 67;
67 [label=arg];
67 -> 68;
68 [label="TERM: x"];
66 -> 69;
69 [label="TERM: ->"];
66 -> 70;
70 [label=expr];
70 -> 71;
71 [label=expr];
71 -> 72;
72 [label="TERM: ("];
71 -> 73;
73 [label=expr];
73 -> 74;
74 [label="TERM: vertices >>"];
73 -> 75;
75 [label=expr];
75 -> 76;
76 [label=arg];
76 -> 77;
77 [label="TERM: x"];
71 -> 78;
78 [label="TERM: )"];
70 -> 79;
79 [label="TERM: ?>"];
70 -> 80;
80 [label=expr];
80 -> 81;
81 [label=value];
81 -> 82;
82 [label="TERM: 2"];
64 -> 83;
83 [label="TERM: )"];
63 -> 84;
84 [label="TERM: ?=>"];
63 -> 85;
85 [label=expr];
85 -> 86;
86 [label=value];
86 -> 87;
87 [label="TERM: {"];
86 -> 88;
88 [label=expr];
88 -> 89;
89 [label=arg];
89 -> 90;
90 [label="TERM: initial"];
86 -> 91;
91 [label="TERM: , "];
86 -> 92;
92 [label=expr];
92 -> 93;
93 [label=arg];
93 -> 94;
94 [label="TERM: upd1"];
86 -> 95;
95 [label="TERM: , "];
86 -> 96;
96 [label=expr];
96 -> 97;
97 [label=arg];
97 -> 98;
98 [label="TERM: inter"];
86 -> 99;
99 [label="TERM: }"];
1 -> 100;
100 [label="TERM: ;"];
1 -> 101;
101 [label="TERM: <EOF>"];
}
"""
