# ColorSelector
Image segmentation for the FHI project. Works with this R project to generate PLSR coefficients https://github.com/sortijas/PAD .

The coefficients are used to predict the drug concentration and is also implemented in the Android app at https://github.com/PaperAnalyticalDeviceND/PADS_Lite .

#### Running the scripts
Running ```python3 regionRoutine.py``` generates a csv file contaning the RGB values for each region of each lane. 

Format
```
	Image	Contains	Drug %	PAD S#	A1-R	A1-G	A1-B	A2-R	A2-G	A2-B	A3-R	A3-G	A3-B	A4-R	A4-G	A4-B	A5-R	A5-G	A5-B	A6-R	A6-G	A6-B	A7-R	A7-G	A7-B	A8-R	A8-G	A8-B	A9-R	A9-G	A9-B	A10-R	A10-G	A10-B	B1-R	B1-G	B1-B	B2-R	B2-G	B2-B	B3-R	B3-G	B3-B	B4-R	B4-G	B4-B	B5-R	B5-G	B5-B	B6-R	B6-G	B6-B	B7-R	B7-G	B7-B	B8-R	B8-G	B8-B	B9-R	B9-G	B9-B	B10-R	B10-G	B10-B	C1-R	C1-G	C1-B	C2-R	C2-G	C2-B	C3-R	C3-G	C3-B	C4-R	C4-G	C4-B	C5-R	C5-G	C5-B	C6-R	C6-G	C6-B	C7-R	C7-G	C7-B	C8-R	C8-G	C8-B	C9-R	C9-G	C9-B	C10-R	C10-G	C10-B	D1-R	D1-G	D1-B	D2-R	D2-G	D2-B	D3-R	D3-G	D3-B	D4-R	D4-G	D4-B	D5-R	D5-G	D5-B	D6-R	D6-G	D6-B	D7-R	D7-G	D7-B	D8-R	D8-G	D8-B	D9-R	D9-G	D9-B	D10-R	D10-G	D10-B	E1-R	E1-G	E1-B	E2-R	E2-G	E2-B	E3-R	E3-G	E3-B	E4-R	E4-G	E4-B	E5-R	E5-G	E5-B	E6-R	E6-G	E6-B	E7-R	E7-G	E7-B	E8-R	E8-G	E8-B	E9-R	E9-G	E9-B	E10-R	E10-G	E10-B	F1-R	F1-G	F1-B	F2-R	F2-G	F2-B	F3-R	F3-G	F3-B	F4-R	F4-G	F4-B	F5-R	F5-G	F5-B	F6-R	F6-G	F6-B	F7-R	F7-G	F7-B	F8-R	F8-G	F8-B	F9-R	F9-G	F9-B	F10-R	F10-G	F10-B	G1-R	G1-G	G1-B	G2-R	G2-G	G2-B	G3-R	G3-G	G3-B	G4-R	G4-G	G4-B	G5-R	G5-G	G5-B	G6-R	G6-G	G6-B	G7-R	G7-G	G7-B	G8-R	G8-G	G8-B	G9-R	G9-G	G9-B	G10-R	G10-G	G10-B	H1-R	H1-G	H1-B	H2-R	H2-G	H2-B	H3-R	H3-G	H3-B	H4-R	H4-G	H4-B	H5-R	H5-G	H5-B	H6-R	H6-G	H6-B	H7-R	H7-G	H7-B	H8-R	H8-G	H8-B	H9-R	H9-G	H9-B	H10-R	H10-G	H10-B	I1-R	I1-G	I1-B	I2-R	I2-G	I2-B	I3-R	I3-G	I3-B	I4-R	I4-G	I4-B	I5-R	I5-G	I5-B	I6-R	I6-G	I6-B	I7-R	I7-G	I7-B	I8-R	I8-G	I8-B	I9-R	I9-G	I9-B	I10-R	I10-G	I10-B	J1-R	J1-G	J1-B	J2-R	J2-G	J2-B	J3-R	J3-G	J3-B	J4-R	J4-G	J4-B	J5-R	J5-G	J5-B	J6-R	J6-G	J6-B	J7-R	J7-G	J7-B	J8-R	J8-G	J8-B	J9-R	J9-G	J9-B	J10-R	J10-G	J10-B	K1-R	K1-G	K1-B	K2-R	K2-G	K2-B	K3-R	K3-G	K3-B	K4-R	K4-G	K4-B	K5-R	K5-G	K5-B	K6-R	K6-G	K6-B	K7-R	K7-G	K7-B	K8-R	K8-G	K8-B	K9-R	K9-G	K9-B	K10-R	K10-G	K10-B	L1-R	L1-G	L1-B	L2-R	L2-G	L2-B	L3-R	L3-G	L3-B	L4-R	L4-G	L4-B	L5-R	L5-G	L5-B	L6-R	L6-G	L6-B	L7-R	L7-G	L7-B	L8-R	L8-G	L8-B	L9-R	L9-G	L9-B	L10-R	L10-G	L10-B																																																																																																																																																																																																																																																																																																																																																																												
16895	16895	albendazole	20	53232	225	216	190	225	148	161	240	100	135	234	228	219	228	225	214	226	223	211	223	220	207	224	219	209	246	241	231	236	231	219	235	226	168	234	225	164	232	224	173	238	229	182	237	230	188	235	229	191	240	233	198	229	223	193	232	226	205	235	230	211	169	213	223	191	214	213	190	206	199	201	217	209	194	211	202	200	218	209	179	198	189	190	211	203	210	225	218	236	238	222	250	206	199	241	184	185	240	183	182	240	185	184	243	194	189	242	196	191	247	210	199	242	205	194	131	183	195	158	198	197	213	119	131	226	150	153	221	160	158	229	177	171	228	187	171	233	196	181	226	193	174	235	207	191	227	217	197	234	221	203	159	216	220	115	206	218	108	205	216	109	204	207	132	210	208	141	208	204	237	235	217	236	231	214	248	243	224	243	240	219	241	203	0	241	207	0	237	209	14	236	212	20	209	175	3	203	186	58	226	218	144	237	228	193	236	226	200	235	228	203	208	170	81	214	174	80	225	203	134	202	181	104	195	181	116	213	208	162	227	220	174	231	222	182	239	230	197	248	240	214	215	196	142	244	240	220	239	236	221	219	221	206	208	238	225	181	226	215	169	225	215	230	229	211	239	236	214	237	229	203	255	254	219	252	250	235	247	247	232	235	231	214	242	167	23	234	164	24	237	162	18	231	156	27	222	167	73	217	174	91	241	202	101	249	241	196	240	235	199	242	236	200	242	235	194	241	234	193	239	214	171	238	204	160	231	202	161	238	214	169	237	234	198	242	237	212	239	234	208	244	239	213	228	221	194	213	211	183	225	219	197	224	220	192	253	245	221	248	239	213																																																																																																																																																																																																																																																																																																																																																																												
```

It requires an input file (sample card-10.csv) that contains information on the cards to be processed. This is a dump from the pad.crc.nd.edu website with format,
```
16895,albendazole,,,,,,/images/padimages/email/processed/53232.processed.png,,,,,,,,,,53232,20
```

We can generate this with SQL,
```
SELECT * FROM `card` WHERE `category`='FHI2020'
```

#### Files
1. ```regionRoutine.py```, the main python script.
1. ```intensityFind.py```, finds the most intense pixels in the defined region.
1. ```pixelProcessing.py```, takes an average of the selected pixel RGB values.
1. ```pls_generate_app_coeff_csv.py```, script to take the R PLS coefficients for each drug and create a single csv file.
