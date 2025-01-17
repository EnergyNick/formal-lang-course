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
28 [label=setBody];
28 -> 29;
29 [label="TERM: 1"];
28 -> 30;
30 [label="TERM: .."];
28 -> 31;
31 [label="TERM: 15"];
26 -> 32;
32 [label="TERM: }"];
1 -> 33;
33 [label="TERM: ;"];
1 -> 34;
34 [label=statement];
34 -> 35;
35 [label=bind];
35 -> 36;
36 [label="TERM: var"];
35 -> 37;
37 [label=arg];
37 -> 38;
38 [label="TERM: inter"];
35 -> 39;
39 [label="TERM: ="];
35 -> 40;
40 [label=expr];
40 -> 41;
41 [label=expr];
41 -> 42;
42 [label=arg];
42 -> 43;
43 [label="TERM: upd1"];
40 -> 44;
44 [label="TERM: /\\"];
40 -> 45;
45 [label=expr];
45 -> 46;
46 [label=arg];
46 -> 47;
47 [label="TERM: initial"];
1 -> 48;
48 [label="TERM: ;"];
1 -> 49;
49 [label=statement];
49 -> 50;
50 [label=print];
50 -> 51;
51 [label="TERM: show"];
50 -> 52;
52 [label=expr];
52 -> 53;
53 [label="TERM: edges >>"];
52 -> 54;
54 [label=expr];
54 -> 55;
55 [label=arg];
55 -> 56;
56 [label="TERM: inter"];
1 -> 57;
57 [label="TERM: ;"];
1 -> 58;
58 [label=statement];
58 -> 59;
59 [label=bind];
59 -> 60;
60 [label="TERM: var"];
59 -> 61;
61 [label=arg];
61 -> 62;
62 [label="TERM: res"];
59 -> 63;
63 [label="TERM: ="];
59 -> 64;
64 [label=expr];
64 -> 65;
65 [label=lambda];
65 -> 66;
66 [label="TERM: ("];
65 -> 67;
67 [label=lambda];
67 -> 68;
68 [label=arg];
68 -> 69;
69 [label="TERM: x"];
67 -> 70;
70 [label="TERM: ->"];
67 -> 71;
71 [label=expr];
71 -> 72;
72 [label=expr];
72 -> 73;
73 [label="TERM: ("];
72 -> 74;
74 [label=expr];
74 -> 75;
75 [label="TERM: vertices >>"];
74 -> 76;
76 [label=expr];
76 -> 77;
77 [label=arg];
77 -> 78;
78 [label="TERM: x"];
72 -> 79;
79 [label="TERM: )"];
71 -> 80;
80 [label="TERM: ?>"];
71 -> 81;
81 [label=expr];
81 -> 82;
82 [label=value];
82 -> 83;
83 [label="TERM: 2"];
65 -> 84;
84 [label="TERM: )"];
64 -> 85;
85 [label="TERM: ?=>"];
64 -> 86;
86 [label=expr];
86 -> 87;
87 [label=value];
87 -> 88;
88 [label="TERM: {"];
87 -> 89;
89 [label=setBody];
89 -> 90;
90 [label=expr];
90 -> 91;
91 [label=arg];
91 -> 92;
92 [label="TERM: initial"];
89 -> 93;
93 [label="TERM: , "];
89 -> 94;
94 [label=expr];
94 -> 95;
95 [label=arg];
95 -> 96;
96 [label="TERM: upd1"];
89 -> 97;
97 [label="TERM: , "];
89 -> 98;
98 [label=expr];
98 -> 99;
99 [label=arg];
99 -> 100;
100 [label="TERM: inter"];
87 -> 101;
101 [label="TERM: }"];
1 -> 102;
102 [label="TERM: ;"];
1 -> 103;
103 [label="TERM: <EOF>"];
}
"""
