from data_analyst import DataAnalyst
import pandas as pd 
import matplotlib.pyplot as plt
import pandas

analyst = DataAnalyst()

#The MAE for different Train_test splits
#results = {'Movies_count': {0: 100.0, 1: 100.0, 2: 100.0, 3: 100.0, 4: 300.0, 5: 300.0, 6: 300.0, 7: 300.0, 8: 500.0, 9: 500.0, 10: 500.0, 11: 500.0}, 'PC_calc_time': {0: 0.17899999999999999, 1: 0.25600000000000001, 2: 0.39200000000000002, 3: 0.65000000000000002, 4: 1.268, 5: 2.4380000000000002, 6: 3.476, 7: 4.6310000000000002, 8: 3.3460000000000001, 9: 6.7789999999999999, 10: 9.9529999999999994, 11: 13.676}, 'Throughput': {0: 1.0200438618860612, 1: 1.8454156798818935, 2: 2.3937761819269898, 3: 1.9199385619660172, 4: 2.5254385318784003, 5: 2.7301683603822231, 6: 2.0576484507621871, 7: 2.4135156878519712, 8: 2.498422870562957, 9: 2.0552731458010767, 10: 1.8423161598761963, 11: 2.2976357328309169}, 'Train_percentage': {0: 0.20000000000000001, 1: 0.40000000000000002, 2: 0.59999999999999998, 3: 0.80000000000000004, 4: 0.20000000000000001, 5: 0.40000000000000002, 6: 0.59999999999999998, 7: 0.80000000000000004, 8: 0.20000000000000001, 9: 0.40000000000000002, 10: 0.59999999999999998, 11: 0.80000000000000004}, 'Time_MAE': {0: 78.427999999999997, 1: 32.512999999999998, 2: 16.710000000000001, 3: 10.417, 4: 95.033000000000001, 5: 65.930000000000007, 6: 58.319000000000003, 7: 24.859999999999999, 8: 160.101, 9: 145.96600000000001, 10: 108.559, 11: 43.523000000000003}, 'K_neighbors': {0: 30.0, 1: 30.0, 2: 30.0, 3: 30.0, 4: 30.0, 5: 30.0, 6: 30.0, 7: 30.0, 8: 30.0, 9: 30.0, 10: 30.0, 11: 30.0}, 'MAE': {0: 2.1276463397663035, 1: 1.0018717427689214, 2: 1.0359768520350567, 3: 0.70920577936111728, 4: 1.3728308598853887, 5: 1.5136898693320273, 6: 1.4447391414746189, 7: 0.93281745526311066, 8: 1.3745858205163464, 9: 1.6892123946619295, 10: 1.3610415496239447, 11: 1.1146783817121961}}
#analyst.compare_train_percentage(pd.DataFrame.from_dict(results))


#One dump that fails:

failing_dump = {512: 1.0, 3075: 0.21320071635561047, 1030: 0.13713778525191897, 1034: 0.10468722436577495, 14: 0.56894588667580492, 528: 0.30508510792387578, 344: 0.12988413337573146, 2073: -0.091287092917527707, 3103: 0.61839732715891327, 544: 0.43685202833051895, 1573: 0.21278189801811079, 1063: 0.13363062095621217, 40: 0.86602540378443849, 1069: 0.18749999999999997, 46: 0.13711585057950956, 2106: 0.097205035351250135, 3646: -0.071176831125384504, 66: 0.46549615967252389, 1091: 0.42066404228707138, 3656: nan, 593: 0.036395863344879674, 2133: 0.19247252518624766, 602: nan, 1115: nan, 3164: nan, 1631: 0.0, 3168: 0.3378495543913993, 3171: 0.49999999999999994, 3857: -0.3100868364730211, 2664: 0.085519961210396372, 1641: -0.057506448321731587, 2155: 0.34511838512583037, 108: nan, 2669: 0.37139067635410372, 1650: 0.16666666666666663, 2163: 0.23638176004556163, 630: nan, 125: 0.38723550162550441, 639: 0.55737040171315366, 3712: 0.35273781075132926, 3202: nan, 2180: 0.0, 1815: nan, 2700: 0.22301333841295279, 3729: 0.13537500329959098, 2708: nan, 3223: 0.0, 1688: 0.38650387566186112, 3737: -0.49341743441788222, 1183: -0.34975090916913493, 1699: -0.066258915644907962, 2215: -1.0, 3242: nan, 2226: nan, 1722: 0.039523077558997061, 3190: 0.034736673714593741, 1226: 0.075139136222286088, 3276: nan, 3791: 0.57816592612348316, 3794: 0.67988969693620149, 291: -0.11750214770165525, 725: 0.43835700375960468, 2774: -0.84980784762166917, 215: -0.072739296745330792, 1240: 0.13815891165058272, 1241: 0.49230092688291266, 3802: 0.19612725279182538, 3291: nan, 2780: 0.20836838116105902, 3294: nan, 225: 0.27372445072567952, 2939: -0.51549131177645169, 1253: 0.081777892774356348, 2792: 0.15115826989487557, 2795: 0.20218293454472772, 749: nan, 2287: 0.096913967438263443, 2288: 0.32537869626565047, 3313: 0.5, 2802: 0.1490569540112277, 2803: 0.22214093694806542, 2293: -1.0, 297: 0.21483446221182986, 762: 0.65452670253389167, 3837: 0.090689938061449996, 3839: 0.1608263120241715, 3338: nan, 1805: 0.21414073881388376, 3855: -0.15617376188860607, 273: 0.21386943613450379, 2836: 0.55195721704268152, 1302: 0.12195151929358565, 2839: nan, 3546: -0.10213282622766345, 286: nan, 2336: -0.1923212843422388, 803: 0.2711630722733202, 3366: -0.011416200657059956, 1833: 0.11395744700716622, 989: nan, 308: -0.2931509849889643, 3388: 0.38315280371235633, 834: nan, 1349: 0.99999999999999989, 331: nan, 332: 0.5639810626529993, 2381: 0.43591020703449251, 3918: 0.4865553561149738, 1359: 0.0096812293812014276, 1361: -0.31048514985041553, 1874: nan, 2904: nan, 3419: 0.5, 3932: 0.085157035806185569, 3421: 0.20194075920585994, 1852: nan, 2410: 0.30131778228140399, 2411: 0.33337817270940645, 2413: 0.21270390223267358, 2416: 0.12961536913333052, 372: 0.21269001997231651, 379: 0.50467959604372492, 2428: 0.54096571113326852, 1422: 0.37900905881981906, 2339: -0.8703882797784892, 409: 0.15309310892394867, 2971: 0.26257802759355986, 1438: 0.2344007771032752, 3489: 0.20066604360171852, 930: -0.031200104832528316, 2981: nan, 422: 0.0, 2986: 0.33162710718686811, 2992: -0.41011244760386623, 434: 0.46119032953536215, 3510: 0.17454293492414438, 1466: 0.25354595405447922, 443: 0.5, 2492: 0.95346258924559235, 2521: -0.33094381626464864, 1990: 0.24906774069335891, 2977: 1.0, 3016: 0.43763716305025979, 969: -0.19522542027763629, 2509: nan, 1243: 0.21805922889798224, 473: 0.63995703367147894, 3034: 0.0114252409399597, 2523: 0.026261286571944521, 3037: -0.035695294242590166, 1502: nan, 3041: 0.053300179088902597, 483: -0.10369516947304253, 2028: 0.0087568937219038995, 3060: 0.18707716585350945, 2558: 0.51992464591217491, 3578: 0.095034047557785148, 3068: 0.29320824645568438, 2218: nan, 510: 0.62749501990055667}



