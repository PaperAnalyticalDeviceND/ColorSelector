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

The final coefficient file for the app has format,
```
albendazole	35.82806338	0.031822435	-0.039181285	0.020019181	0.027034675	-0.035567419	0.054637873	0.004979496	-0.031010949	0.020610039	-0.007867745	-0.017389889	0.021776773	-0.023660356	0.019349498	0.007511665	-0.016809353	-0.024489059	-0.001229793	0.008609973	0.005772966	0.024945759	-0.032852974	-0.001191432	0.018320014	-0.00173765	0.024033763	0.006463561	-0.004363606	0.002165523	-0.033510082	-0.009619594	-0.006305928	-0.016878183	-0.016744036	0.041549913	-0.04626389	-0.012044341	0.036626229	-0.022515844	-0.042256711	0.002166325	-0.014737067	0.014938875	-0.007133991	0.002990917	-0.012638158	-0.017789067	-0.006602562	0.003452018	-0.007095683	0.019243393	-0.013747189	-0.004443161	0.023151623	-0.015451585	-0.007875091	0.010201432	0.034632895	-0.015983333	-0.008213183	-0.0104807	0.002073945	0.038669539	0.003253116	0.028578852	0.024147726	-0.010325451	-0.006847081	-0.002065356	0.013831255	-0.009169261	-0.0217658	0.04471428	0.011347206	-0.00755688	-0.030551472	0.010871719	0.022427704	-0.034294712	-0.011432908	0.016322161	-0.014492851	-0.007283526	0.007912083	0.03375289	0.002925125	-0.01062919	0.077618011	-0.014240412	-0.053662048	-0.013569344	0.010554653	0.009010285	0.010770648	0.0105156	-0.00120695	-0.007771908	0.03741365	0.006358379	0.004549353	0.002802338	-0.022593615	-0.003712115	0.010595837	0.002401843	0.013760954	0.016269567	-0.043266662	0.018635	0.008041692	-0.055842883	0.034713685	0.00165631	-0.02583817	-0.021478899	0.01282946	0.024587344	-0.067979289	0.033035254	0.016049644	0.040302032	-0.043953179	0.014062885	0.011324077	-0.035181666	0.040035797	-0.005178185	-0.038629151	0.029324757	0.010486658	-0.03878451	0.015929831	0.017104243	-0.030590376	0.000637972	-0.019982047	-0.016327978	0.018787714	-0.010958142	0.006124015	0.01892771	-0.00948361	0.020017971	-0.003854675	0.025570965	-0.016387859	-0.037124976	0.046484607	0.012037033	-0.043040559	-0.000560505	0.02128052	-0.024368566	-0.016761618	0.012531954	0.012011054	-0.000116012	-0.010104579	0.005231854	0.023073212	-0.016507003	0.003318209	0.007305005	-0.013229437	0.02243237	-0.017365656	0.008203171	0.00340601	-0.007884716	0.007154161	0.008594108	-0.02383572	0.020673863	-0.007922055	0.008270235	0.001178185	-0.051008602	0.007635453	0.004869304	-0.039288611	0.034777683	-0.024741588	-0.009341188	0.03970481	0.02902189	-0.009133174	-0.013317885	0.030922013	-0.016054956	-0.038867052	0.041465967	-0.010623953	-0.023811571	0.040128955	-0.012626193	-0.004826284	-0.007994373	-0.001187722	0.020423551	-0.025820533	0.00868841	-0.003018852	-0.042867612	0.008192008	0.001852574	-0.021940512	0.00355663	-0.003463201	0.004473262	0.013120989	-0.084040185	0.035593358	-0.018472398	-0.101071772	0.050135173	-0.012290263	-0.09597406	0.02432384	0.010069365	-0.040413483	0.014061523	0.006368576	-0.04415976	-0.001052723	0.037552252	0.019433585	0.002052565	0.020443253	0.038513961	-0.020488825	-0.029030715	0.000290739	0.025305472	-0.025178063	-0.126787511	0.07105074	0.009977834	-0.059551564	0.020728771	0.017121276	0.001057772	0.03491181	-0.024716336	-0.012653247	0.026520263	-0.020475988	0.035763402	0.012023146	-0.017399027	-0.055382792	-0.014013308	0.034390845	-0.028072853	-0.01862309	0.03632117	0.01555795	-0.010489496	0.012360512	0.035321595	-0.038916457	0.030287941	0.044933957	-0.025938517	-0.019976253	0.007957713	-0.017352056	-0.0117102	0.076493301	-0.056128604	-0.056329574	0.034671124	-0.034408864	-0.024680438	0.03791424	-0.030615291	0.008323962	0.077927125	-0.047728839	-0.008530573	0.032482003	-0.048752319	0.010882726	0.047109456	-0.049082157	0.008729444	0.059980167	-0.078036813	0.027565069	0.079512397	-0.098488305	0.032144766	0.093714645	-0.083415516	0.0056181	0.030896029	-0.017129469	0.002208832	-0.032837017	0.014786949	0.042314548	-0.016583364	0.03388249	-0.00413757	-0.022091208	0.075730336	-0.059933492	-0.102131826	0.0412731	-6.40E-05	-0.037169084	0.049152345	-0.039713785	-0.015226858	0.063841102	-0.037800473	-0.035013019	0.059956638	-0.011611642	-0.020025126	0.020834382	-0.017815494	-0.005201009	0.003032578	-0.00071536	0.000166647	0.000643284	0.037454931	-0.002993156	-0.016155637	0.019348155	-0.00446804	0.019120578	0.014958945	-0.021876598	0.005516704	0.022421526	-0.006938735	0.008132118	0.029914729	0.007924937	0.006110888	0.008052754	0.008298738	-0.007115783	-0.0219726	0.02545615	0.007939063	-0.019491988	0.036404523	0.000529102	-0.033096702	0.025573505	0.01226118	-0.003722273	-0.019192156	-0.01433939	0.012315987	-0.041521537	-0.023459139	0.086173738
amoxicillin	4.779548433	0.026433264	-0.026093121	0.009506221	0.087847865	-0.031392152	0.025971171	0.014831884	-0.009673856	0.022700654	0.042672889	-0.00482494	-0.000159697	-0.005271874	0.003413058	0.000151236	0.011169896	-0.001473211	0.000605087	-0.001373347	0.001063884	-0.002458048	0.003656791	-0.00163838	-0.007943869	0.024984516	-0.00714644	-0.004251978	0.024228641	-0.010336609	0.001299824	-0.099531422	0.0726028	-0.028799956	-0.149778643	0.07187833	-0.01087923	-0.129046247	0.060211452	-0.023637776	-0.113732105	0.058525729	-0.026257722	-0.06332359	0.050824468	-0.006453688	-0.039900758	0.026366545	-0.01049369	-0.024623742	0.015256212	-0.005252048	0.004444953	0.007394314	-0.004371565	0.018935875	-0.004781595	-0.009404454	0.019459758	-0.004030813	-0.016477675	0.012453375	-0.012909002	-0.01454074	0.008225784	-0.010417157	0.017487409	-0.020086676	-0.022366778	0.006008084	-0.004460113	-0.013697628	0.016141736	-0.002133991	-0.023610808	-0.001555292	0.016380409	-0.013515632	-0.003367731	0.015344653	-0.000178079	-0.004711778	0.0053444	-0.000671594	-0.008133941	0.016367748	7.89E-05	-0.002575919	0.002302534	-0.003653032	0.000348806	0.001513685	-0.013043277	0.003579771	0.008446247	-0.021769256	0.032837168	0.000476944	-0.024655495	0.046385972	0.001861588	-0.026966015	0.047828057	0.009720978	-0.035148797	0.028722145	-0.003373995	-0.023042486	0.034849704	-0.004631373	-0.012688562	0.01539383	-0.000634356	0.006419692	-0.008577983	0.004092299	-0.001952278	-0.008952096	0.007624117	-0.002236359	-0.004348317	0.009693576	0.007138192	-0.000197816	0.002092294	0.03457179	-0.013181737	0.003506024	0.02730415	-0.040085173	-0.007888233	0.014469147	-0.041179714	0.002110259	0.013258432	-0.020845403	-0.00632566	0.006814387	-0.00232898	-0.008120752	0.013704422	0.008162621	0.003167996	-0.005552637	0.003383182	9.58E-05	0.000990594	0.013075437	0.009246331	0.0054396	0.013644944	-0.003741136	-0.013843382	0.012918258	0.01207775	-0.028106798	0.004606327	0.005722575	-0.023780055	0.002294634	0.016184168	-0.017378534	-0.003024027	-0.00244279	-0.002926263	0.015086777	0.010030754	-0.002111692	0.008856742	0.003210261	-0.00730842	-0.001677399	0.011271918	0.005051448	-0.005681851	0.011068232	-0.000302463	-0.006398399	9.43E-06	0.000845481	-0.00790424	0.018419789	-0.008165918	0.003351432	4.57E-05	-0.012870356	0.008046183	0.04143768	-0.002092939	-0.003446593	0.031849553	-0.003270247	-0.002462291	-0.007655202	-0.013682938	0.001532916	0.002516357	-0.003527625	0.014019775	0.020818907	0.002064548	-0.016884862	0.010859354	0.011254061	-0.00739159	-0.004389389	0.002609253	-0.003919398	-0.015247497	0.000466205	0.008560328	0.028348283	0.00762634	-0.007383842	0.002675899	-0.005176706	-0.002418223	0.012394797	-0.001337048	-0.008085958	0.022847623	-0.001819622	-0.005011686	-0.002745671	-0.006023566	0.006712766	0.000750404	0.001241517	0.003242957	-0.00046049	0.011902985	-0.00948182	-0.012113851	0.017729859	-0.015219421	0.017739828	0.007168133	-0.002661808	-0.008381267	0.011069276	-0.001634148	-0.009427417	0.012274654	0.00023168	0.000394953	0.007975493	-0.004872223	0.03142675	-0.017945001	-0.00444221	0.015927274	-0.016755092	-0.002078371	-0.015634802	0.016788332	0.00478395	0.000997937	-0.003754455	0.000855231	-0.007027652	-0.007488248	-0.00159605	-0.009767376	-4.62E-05	0.007225063	-0.021391443	0.008156946	0.012319885	-0.046023427	0.017755379	0.01777754	-0.005430796	0.019865849	-0.005668999	0.008803203	0.000491307	-0.005172082	-0.014740923	-0.007528051	0.006423621	-0.003345492	-0.002908992	0.001062927	-0.002269241	-0.002236352	-0.001349665	-0.001509892	-0.00235756	-0.00437571	-0.009013784	0.002191604	0.005430273	-0.006517625	0.006388442	0.000906324	0.005167609	-6.33E-05	-0.01046351	0.002459839	0.001342415	-0.008626933	0.02215484	-0.005718224	-0.016599545	0.004205791	-0.022657952	0.036436552	0.018963305	-0.051262676	0.031685567	0.081114412	-0.092674624	0.019154209	0.060847066	-0.063895235	0.031819575	0.066966506	-0.078394823	0.019552357	0.017528209	-0.019365325	0.005096289	-0.031883258	0.030064038	-0.018140324	-0.05615634	0.045700513	-0.011026196	-0.016912113	0.007702009	-0.000648314	0.012393695	-7.84E-05	-0.015693416	0.011608603	0.009150403	0.001863236	-0.01351607	-0.003178027	0.004864052	-0.007746554	-0.003013199	0.002428377	-0.006157445	-0.000213791	0.006988084	-0.001801528	0.001096995	0.005461754	-0.00117829	-0.006478585	-0.003254802	-0.002428638	-0.000339862	0.00469426	0.005650991	0.004718045	-0.008564	0.00515714	0.011240765	-0.010471925![image](https://user-images.githubusercontent.com/1945867/124943395-742e7b80-dfda-11eb-8865-814794c4132a.png)

```
where the first column is the drug label, the second the intercpt and the remaining columns correspond to the RGB intensities for the regions.

#### Files
1. ```regionRoutine.py```, the main python script.
1. ```intensityFind.py```, finds the most intense pixels in the defined region.
1. ```pixelProcessing.py```, takes an average of the selected pixel RGB values.
1. ```pls_generate_app_coeff_csv.py```, script to take the R PLS coefficients for each drug and create a single csv file.
