#!/usr/bin/env python
# -*- coding: utf-8 -*-

features = [[6, 9, 15, 18, 27, 31, 33, 35, 38, 46, 48, 50, 59, 62, 65, 70, 78, 79, 88, 91, 108, 114, 117, 118, 120, 121, 125, 145, 147, 148, 154, 157, 164, 166, 167, 178, 184, 185, 186, 187, 190, 191, 203, 206, 212, 217, 220, 221, 224, 225, 245, 252, 268, 269, 270, 271, 272, 285, 286, 291, 292, 296, 297, 299, 300, 303, 305, 319, 320, 329, 334, 336, 339, 341, 345, 352, 360, 371, 372, 378, 385, 387, 391, 393, 396, 398, 404, 405, 406, 407, 420, 426, 430, 433, 438, 439, 440, 441, 451, 452, 453, 454, 455, 459, 462, 465, 469, 472, 473, 479, 482, 493, 498, 499, 501, 502, 504, 507, 520, 526, 532, 535, 536, 537, 541, 542, 550, 556, 559, 566, 570, 571, 583, 585, 592, 593, 594, 597, 601, 608, 610, 611, 613, 614, 618, 619, 633, 638, 645, 651, 656, 658, 664, 666, 667, 672, 675, 684, 687, 688, 702, 706, 707, 709, 711, 712, 714, 716, 718, 730, 742, 744, 745, 750, 755, 766, 772, 774, 778, 779, 780, 783, 784, 785, 786, 787, 788, 792, 795, 800, 804, 807, 813, 822, 825, 856, 867, 871, 884, 886, 889, 892, 895, 899, 903, 916, 917, 919, 921, 922, 927, 931, 933, 937, 940, 946, 947, 948, 949, 953, 960, 964, 968, 973, 974, 981, 989, 993, 997, 1003, 1004, 1005, 1013, 1016, 1030, 1033, 1035, 1037, 1040, 1045, 1048, 1051, 1058, 1067, 1068, 1071, 1078, 1080, 1088, 1092, 1100, 1105, 1107, 1108, 1109, 1111, 1114, 1115, 1117, 1118, 1119, 1122, 1124, 1125, 1127, 1136, 1143, 1144, 1150, 1160, 1161, 1162, 1163, 1166, 1171, 1173, 1175, 1176, 1179, 1183, 1184, 1187, 1188, 1195, 1212, 1214, 1216, 1220, 1233, 1236, 1239, 1243, 1250, 1253, 1264, 1266, 1269, 1275, 1278, 1279, 1281, 1283, 1285, 1291, 1294, 1297, 1303, 1305, 1307, 1310, 1319, 1326, 1327, 1329, 1332, 1340, 1341, 1343, 1344, 1352, 1355, 1363, 1366, 1372, 1386, 1389, 1393, 1396, 1397, 1402, 1413, 1417, 1420, 1426, 1430, 1432, 1435, 1436, 1443, 1446, 1460, 1463, 1465, 1466, 1474, 1479, 1484, 1491, 1497, 1498],
            [10, 11, 18, 20, 23, 25, 28, 29, 33, 35, 42, 43, 47, 51, 52, 54, 57, 59, 63, 64, 77, 78, 82, 89, 98, 101, 103, 108, 109, 112, 114, 116, 118, 119, 130, 137, 140, 141, 144, 146, 147, 150, 154, 156, 157, 159, 173, 174, 189, 191, 193, 201, 214, 216, 222, 224, 227, 231, 233, 240, 243, 245, 248, 249, 256, 259, 262, 263, 264, 266, 267, 279, 285, 298, 300, 301, 309, 319, 321, 323, 324, 335, 336, 338, 344, 345, 346, 348, 349, 351, 356, 357, 359, 362, 376, 378, 382, 387, 390, 392, 395, 398, 417, 425, 430, 433, 438, 439, 442, 443, 450, 451, 454, 472, 478, 480, 488, 493, 501, 506, 512, 514, 517, 519, 520, 535, 539, 541, 550, 555, 557, 576, 577, 578, 579, 589, 591, 603, 609, 611, 614, 626, 633, 636, 639, 643, 667, 669, 670, 677, 683, 693, 704, 708, 709, 711, 714, 717, 722, 729, 737, 738, 739, 742, 749, 750, 755, 772, 773, 775, 776, 777, 778, 780, 785, 793, 795, 796, 804, 805, 809, 812, 813, 817, 819, 827, 830, 835, 845, 847, 851, 852, 853, 855, 858, 877, 886, 890, 892, 901, 910, 911, 915, 916, 919, 929, 935, 936, 937, 941, 956, 959, 960, 963, 965, 967, 968, 970, 972, 973, 984, 996, 997, 999, 1001, 1010, 1011, 1013, 1018, 1019, 1020, 1025, 1028, 1032, 1034, 1049, 1052, 1060, 1063, 1066, 1068, 1070, 1073, 1074, 1075, 1076, 1084, 1085, 1102, 1112, 1120, 1123, 1134, 1138, 1140, 1141, 1142, 1144, 1159, 1163, 1166, 1169, 1170, 1173, 1177, 1178, 1181, 1182, 1183, 1184, 1186, 1187, 1195, 1197, 1198, 1200, 1224, 1228, 1233, 1234, 1237, 1238, 1240, 1246, 1254, 1256, 1258, 1260, 1267, 1270, 1281, 1285, 1286, 1293, 1301, 1302, 1305, 1306, 1317, 1318, 1326, 1327, 1328, 1333, 1334, 1338, 1341, 1342, 1343, 1353, 1354, 1355, 1361, 1362, 1374, 1375, 1382, 1387, 1388, 1390, 1398, 1402, 1406, 1407, 1415, 1429, 1442, 1446, 1455, 1463, 1474, 1475, 1485, 1486, 1490, 1494, 1495, 1499, 1500, 1502, 1509, 1516, 1520, 1528, 1532, 1537, 1538, 1539, 1543, 1544],
            [5, 10, 12, 13, 18, 19, 20, 22, 28, 48, 50, 51, 53, 60, 61, 65, 68, 70, 76, 77, 83, 87, 100, 101, 104, 105, 110, 111, 119, 120, 124, 129, 130, 131, 139, 140, 143, 145, 154, 162, 164, 165, 169, 170, 172, 176, 189, 199, 209, 216, 229, 232, 252, 255, 257, 258, 260, 262, 265, 269, 275, 277, 279, 286, 288, 290, 300, 301, 307, 317, 322, 329, 332, 338, 355, 360, 369, 372, 374, 384, 388, 392, 395, 412, 413, 418, 426, 437, 441, 444, 445, 450, 456, 459, 464, 471, 475, 479, 480, 487, 489, 491, 497, 510, 512, 513, 518, 520, 522, 529, 536, 537, 538, 539, 540, 556, 560, 570, 572, 576, 578, 580, 585, 586, 587, 588, 589, 593, 597, 601, 602, 605, 607, 608, 611, 619, 621, 623, 625, 628, 630, 631, 633, 636, 643, 652, 657, 663, 672, 673, 675, 686, 688, 689, 691, 694, 696, 697, 700, 702, 704, 706, 708, 712, 728, 730, 731, 736, 738, 748, 749, 750, 757, 764, 772, 779, 780, 785, 790, 795, 806, 809, 812, 818, 819, 826, 833, 838, 839, 842, 848, 849, 856, 864, 869, 873, 879, 884, 887, 889, 897, 898, 902, 903, 904, 908, 910, 911, 914, 922, 924, 928, 933, 937, 939, 946, 951, 955, 958, 961, 984, 985, 986, 987, 988, 992, 993, 995, 1004, 1011, 1018, 1030, 1033, 1036, 1045, 1052, 1063, 1065, 1067, 1068, 1069, 1070, 1077, 1078, 1080, 1086, 1092, 1095, 1096, 1097, 1100, 1107, 1111, 1125, 1128, 1130, 1131, 1132, 1135, 1138, 1139, 1140, 1141, 1143, 1149, 1150, 1151, 1155, 1167, 1172, 1173, 1176, 1186, 1187, 1192, 1194, 1203, 1204, 1208, 1215, 1222, 1225, 1228, 1233, 1234, 1250, 1253, 1257, 1263, 1269, 1270, 1273, 1279, 1281, 1287, 1298, 1300, 1303, 1315, 1320, 1324, 1325, 1332, 1356, 1362, 1364, 1370, 1372, 1383, 1387, 1389, 1390, 1393, 1394, 1396, 1401, 1405, 1409, 1420, 1421, 1428, 1433, 1445, 1450, 1451, 1453, 1455, 1456, 1465, 1470, 1480, 1488, 1490, 1493, 1494, 1495, 1497, 1500, 1503, 1506, 1514, 1517, 1519, 1521, 1522, 1525, 1531, 1543, 1552, 1553], 
            [12, 22, 31, 35, 37, 45, 48, 49, 52, 58, 66, 75, 79, 80, 82, 83, 86, 94, 95, 103, 111, 114, 121, 126, 128, 131, 134, 135, 139, 140, 142, 146, 147, 148, 149, 153, 155, 156, 163, 167, 169, 171, 175, 177, 182, 203, 206, 211, 212, 219, 223, 228, 236, 238, 240, 241, 243, 246, 248, 249, 252, 254, 255, 258, 261, 274, 282, 286, 292, 299, 300, 302, 328, 330, 334, 336, 337, 340, 347, 348, 351, 354, 355, 356, 359, 361, 365, 372, 387, 394, 401, 404, 411, 414, 418, 419, 422, 424, 437, 440, 443, 445, 450, 453, 455, 459, 461, 462, 466, 469, 476, 479, 481, 488, 498, 505, 511, 514, 519, 528, 538, 539, 542, 549, 556, 557, 559, 561, 565, 572, 574, 575, 576, 586, 592, 599, 601, 602, 604, 608, 611, 616, 631, 632, 637, 639, 643, 644, 648, 649, 656, 668, 673, 696, 699, 706, 709, 714, 715, 717, 740, 741, 743, 746, 751, 752, 756, 757, 758, 763, 768, 773, 784, 785, 790, 793, 802, 807, 808, 809, 812, 817, 826, 829, 845, 846, 850, 851, 854, 857, 863, 870, 871, 873, 883, 886, 888, 889, 891, 900, 910, 918, 923, 925, 929, 938, 948, 954, 955, 956, 961, 964, 972, 973, 984, 985, 986, 987, 988, 990, 996, 1016, 1018, 1019, 1020, 1025, 1026, 1027, 1030, 1036, 1040, 1048, 1049, 1053, 1058, 1060, 1066, 1067, 1069, 1071, 1078, 1079, 1085, 1088, 1092, 1093, 1095, 1096, 1098, 1099, 1105, 1109, 1117, 1118, 1125, 1127, 1129, 1130, 1134, 1139, 1144, 1154, 1157, 1164, 1173, 1175, 1179, 1182, 1190, 1195, 1205, 1207, 1211, 1221, 1222, 1225, 1227, 1232, 1238, 1242, 1252, 1255, 1257, 1258, 1269, 1273, 1275, 1277, 1279, 1288, 1289, 1291, 1295, 1301, 1303, 1312, 1317, 1320, 1338, 1345, 1348, 1350, 1353, 1359, 1360, 1361, 1369, 1370, 1372, 1377, 1381, 1383, 1390, 1395, 1398, 1407, 1410, 1411, 1413, 1414, 1424, 1427, 1430, 1433, 1434, 1436, 1439, 1447, 1454, 1456, 1461, 1462, 1477, 1478, 1482, 1489, 1493, 1496, 1499, 1514, 1515, 1518, 1527, 1528, 1533, 1538, 1542, 1552, 1553, 1556],
            [3, 8, 13, 16, 19, 23, 35, 36, 41, 44, 45, 49, 68, 70, 71, 72, 84, 86, 88, 90, 91, 99, 105, 106, 108, 113, 119, 122, 131, 133, 135, 143, 150, 155, 156, 159, 161, 162, 163, 165, 167, 170, 176, 188, 190, 191, 192, 194, 201, 204, 206, 207, 224, 236, 241, 248, 252, 255, 257, 258, 259, 262, 263, 264, 269, 271, 272, 274, 275, 277, 281, 292, 294, 296, 297, 298, 305, 306, 307, 315, 323, 324, 325, 326, 329, 332, 333, 336, 338, 340, 342, 349, 358, 365, 368, 372, 378, 390, 394, 395, 402, 415, 426, 431, 434, 436, 442, 445, 452, 454, 459, 467, 472, 475, 480, 489, 493, 495, 499, 509, 514, 515, 519, 522, 526, 529, 536, 543, 547, 549, 550, 556, 557, 564, 568, 576, 580, 589, 598, 600, 601, 607, 629, 634, 645, 646, 651, 656, 658, 664, 665, 674, 681, 684, 687, 691, 696, 698, 703, 707, 709, 710, 712, 716, 725, 726, 729, 731, 735, 741, 742, 743, 747, 752, 753, 760, 768, 769, 772, 777, 779, 783, 789, 793, 796, 799, 807, 810, 816, 821, 823, 827, 839, 849, 850, 864, 868, 876, 882, 887, 889, 890, 896, 907, 911, 916, 919, 922, 931, 936, 953, 958, 960, 964, 970, 974, 979, 980, 983, 986, 987, 988, 994, 1000, 1003, 1004, 1007, 1012, 1014, 1016, 1017, 1022, 1024, 1031, 1054, 1060, 1061, 1063, 1067, 1068, 1069, 1074, 1089, 1091, 1105, 1107, 1111, 1118, 1119, 1120, 1122, 1126, 1128, 1129, 1131, 1132, 1138, 1139, 1143, 1145, 1147, 1149, 1150, 1156, 1157, 1161, 1165, 1176, 1180, 1182, 1183, 1189, 1196, 1202, 1203, 1206, 1216, 1217, 1220, 1221, 1230, 1237, 1242, 1243, 1250, 1251, 1254, 1266, 1273, 1283, 1295, 1307, 1310, 1313, 1314, 1316, 1323, 1325, 1327, 1331, 1333, 1336, 1339, 1344, 1352, 1354, 1359, 1364, 1365, 1369, 1380, 1384, 1385, 1391, 1394, 1395, 1400, 1406, 1414, 1429, 1435, 1444, 1446, 1459, 1462, 1466, 1468, 1472, 1479, 1481, 1482, 1485, 1489, 1490, 1496, 1497, 1500, 1503, 1506, 1511, 1516, 1523, 1526, 1527, 1529, 1533, 1541, 1546, 1548, 1554],
            [5, 6, 17, 18, 20, 25, 27, 28, 29, 30, 33, 51, 53, 54, 69, 78, 83, 84, 88, 92, 96, 98, 101, 108, 113, 126, 135, 142, 145, 146, 150, 151, 156, 160, 163, 164, 177, 178, 194, 200, 205, 209, 210, 225, 227, 228, 231, 233, 235, 243, 253, 256, 257, 265, 268, 272, 280, 290, 295, 296, 299, 311, 319, 323, 325, 326, 333, 340, 341, 344, 346, 347, 357, 358, 359, 360, 362, 363, 364, 368, 372, 373, 376, 379, 380, 384, 385, 390, 395, 397, 401, 408, 411, 413, 415, 419, 432, 437, 440, 442, 443, 444, 446, 462, 463, 464, 466, 472, 477, 481, 483, 485, 489, 495, 498, 501, 502, 503, 506, 511, 514, 515, 524, 526, 529, 533, 534, 545, 551, 557, 563, 567, 568, 569, 571, 577, 578, 581, 594, 596, 597, 605, 614, 617, 624, 630, 632, 646, 647, 661, 668, 672, 683, 706, 708, 709, 712, 714, 716, 719, 723, 730, 741, 747, 759, 763, 765, 767, 768, 771, 780, 782, 790, 791, 797, 801, 804, 806, 808, 809, 812, 813, 814, 816, 817, 823, 824, 826, 834, 843, 844, 848, 850, 856, 857, 859, 865, 871, 877, 886, 888, 889, 890, 904, 911, 915, 918, 920, 921, 926, 936, 942, 944, 957, 959, 961, 966, 967, 972, 975, 987, 994, 1007, 1008, 1013, 1015, 1027, 1028, 1032, 1033, 1043, 1047, 1049, 1050, 1054, 1057, 1058, 1060, 1068, 1069, 1077, 1078, 1080, 1094, 1095, 1112, 1127, 1130, 1134, 1136, 1139, 1145, 1150, 1151, 1154, 1155, 1159, 1160, 1164, 1167, 1175, 1178, 1179, 1180, 1191, 1192, 1196, 1200, 1202, 1206, 1207, 1211, 1214, 1215, 1220, 1224, 1228, 1233, 1239, 1254, 1259, 1260, 1261, 1263, 1264, 1271, 1282, 1287, 1289, 1290, 1292, 1296, 1305, 1307, 1309, 1319, 1325, 1328, 1333, 1338, 1339, 1340, 1342, 1343, 1359, 1360, 1374, 1376, 1377, 1379, 1380, 1383, 1385, 1390, 1396, 1399, 1402, 1405, 1417, 1421, 1429, 1439, 1444, 1446, 1459, 1466, 1467, 1469, 1470, 1480, 1488, 1489, 1492, 1497, 1504, 1506, 1508, 1515, 1516, 1517, 1523, 1524, 1528, 1533, 1543, 1547, 1551, 1552, 1555, 1557],
            [4, 8, 14, 28, 33, 40, 45, 47, 48, 50, 57, 69, 75, 78, 79, 80, 82, 85, 88, 89, 94, 98, 101, 110, 115, 118, 119, 122, 124, 127, 134, 146, 147, 156, 157, 169, 182, 185, 190, 191, 192, 194, 197, 198, 202, 203, 209, 218, 221, 228, 230, 237, 240, 242, 248, 264, 265, 269, 270, 274, 280, 286, 288, 290, 300, 302, 305, 309, 312, 320, 327, 328, 330, 332, 333, 341, 342, 343, 350, 353, 357, 362, 364, 367, 370, 382, 383, 389, 391, 392, 393, 395, 397, 402, 406, 413, 417, 420, 421, 422, 425, 429, 442, 449, 453, 456, 458, 459, 461, 462, 471, 473, 474, 477, 480, 481, 490, 491, 492, 496, 499, 508, 517, 520, 522, 528, 529, 536, 542, 572, 575, 585, 592, 598, 605, 606, 611, 613, 624, 625, 626, 628, 632, 633, 637, 638, 651, 653, 656, 661, 666, 674, 677, 679, 682, 687, 698, 700, 705, 707, 712, 723, 737, 738, 742, 776, 778, 784, 785, 786, 787, 793, 805, 809, 812, 817, 818, 820, 821, 828, 829, 831, 836, 839, 844, 848, 855, 863, 867, 868, 869, 870, 871, 873, 874, 883, 885, 889, 892, 900, 909, 920, 929, 930, 934, 935, 940, 945, 948, 957, 958, 959, 962, 968, 969, 975, 977, 983, 986, 994, 996, 998, 1010, 1015, 1023, 1024, 1027, 1034, 1035, 1038, 1040, 1042, 1051, 1053, 1057, 1061, 1068, 1071, 1074, 1076, 1080, 1083, 1084, 1087, 1088, 1090, 1091, 1096, 1103, 1108, 1109, 1111, 1112, 1115, 1119, 1130, 1132, 1135, 1146, 1148, 1155, 1157, 1164, 1165, 1167, 1169, 1172, 1181, 1182, 1189, 1201, 1204, 1205, 1214, 1219, 1221, 1232, 1238, 1240, 1241, 1243, 1258, 1264, 1273, 1274, 1275, 1281, 1289, 1290, 1294, 1296, 1301, 1302, 1307, 1311, 1319, 1321, 1325, 1332, 1334, 1337, 1343, 1347, 1353, 1355, 1361, 1369, 1371, 1375, 1378, 1379, 1381, 1382, 1386, 1398, 1400, 1409, 1417, 1418, 1419, 1430, 1440, 1442, 1445, 1450, 1459, 1464, 1467, 1468, 1473, 1477, 1481, 1482, 1484, 1487, 1495, 1496, 1497, 1498, 1501, 1502, 1505, 1513, 1515, 1519, 1523, 1534, 1541, 1543, 1551],
            [4, 5, 10, 16, 21, 22, 23, 26, 32, 33, 52, 61, 62, 63, 67, 69, 71, 73, 78, 88, 91, 93, 97, 101, 103, 107, 115, 120, 124, 126, 130, 135, 137, 138, 140, 154, 162, 164, 170, 185, 186, 187, 188, 202, 213, 217, 220, 225, 227, 235, 237, 238, 245, 247, 248, 249, 258, 261, 266, 273, 277, 289, 290, 298, 301, 302, 303, 314, 318, 319, 331, 336, 337, 339, 344, 345, 347, 348, 352, 355, 356, 360, 365, 366, 371, 378, 382, 394, 398, 403, 411, 414, 418, 421, 432, 441, 444, 448, 454, 455, 456, 460, 462, 474, 477, 479, 480, 482, 483, 487, 495, 506, 508, 509, 511, 515, 518, 524, 535, 536, 537, 542, 546, 550, 553, 557, 558, 562, 565, 579, 585, 587, 592, 596, 611, 615, 616, 620, 622, 635, 638, 640, 644, 656, 660, 666, 668, 670, 677, 688, 696, 698, 707, 714, 724, 725, 727, 736, 746, 747, 750, 752, 754, 756, 758, 759, 761, 764, 769, 777, 778, 782, 798, 799, 814, 816, 819, 820, 822, 823, 824, 826, 835, 836, 852, 853, 859, 862, 865, 868, 869, 870, 875, 886, 914, 922, 928, 935, 940, 948, 949, 953, 955, 958, 960, 963, 965, 966, 967, 968, 969, 980, 982, 985, 986, 991, 996, 1003, 1005, 1009, 1013, 1022, 1029, 1035, 1040, 1044, 1048, 1051, 1053, 1060, 1068, 1069, 1074, 1075, 1081, 1084, 1095, 1105, 1107, 1109, 1118, 1120, 1123, 1133, 1136, 1138, 1143, 1162, 1164, 1174, 1177, 1181, 1182, 1187, 1198, 1199, 1204, 1207, 1209, 1210, 1213, 1215, 1222, 1223, 1225, 1226, 1231, 1238, 1240, 1242, 1244, 1252, 1255, 1256, 1266, 1271, 1272, 1274, 1283, 1284, 1287, 1290, 1293, 1295, 1299, 1300, 1306, 1307, 1308, 1309, 1320, 1323, 1325, 1326, 1327, 1334, 1335, 1338, 1340, 1345, 1348, 1349, 1352, 1354, 1358, 1365, 1367, 1368, 1372, 1375, 1376, 1379, 1380, 1397, 1400, 1403, 1404, 1408, 1410, 1415, 1417, 1420, 1422, 1423, 1429, 1442, 1443, 1456, 1457, 1463, 1471, 1476, 1477, 1480, 1483, 1485, 1506, 1512, 1513, 1519, 1520, 1527, 1530, 1534, 1541, 1545, 1547, 1549, 1551, 1555],
            [16, 19, 20, 25, 26, 28, 31, 36, 37, 42, 43, 45, 55, 57, 60, 61, 74, 85, 92, 94, 98, 99, 101, 104, 107, 109, 115, 116, 131, 133, 134, 140, 143, 153, 154, 158, 166, 170, 184, 187, 189, 190, 191, 199, 200, 207, 210, 213, 226, 227, 229, 236, 241, 244, 245, 246, 248, 250, 254, 257, 258, 259, 261, 274, 275, 282, 295, 297, 298, 313, 331, 337, 345, 346, 349, 351, 353, 355, 359, 360, 361, 365, 366, 368, 369, 371, 373, 379, 383, 384, 385, 387, 389, 391, 396, 400, 409, 410, 416, 418, 419, 421, 426, 427, 429, 431, 432, 433, 439, 442, 448, 451, 452, 453, 457, 458, 466, 477, 482, 485, 487, 489, 490, 492, 493, 504, 509, 520, 523, 534, 546, 549, 550, 559, 560, 571, 572, 573, 575, 576, 583, 588, 597, 601, 604, 608, 609, 611, 614, 615, 617, 623, 628, 629, 632, 633, 641, 642, 643, 654, 658, 661, 672, 673, 675, 676, 677, 680, 688, 693, 696, 699, 702, 722, 723, 729, 732, 733, 734, 739, 741, 744, 762, 764, 775, 780, 782, 784, 787, 790, 792, 809, 817, 820, 826, 835, 837, 857, 858, 863, 869, 889, 892, 893, 898, 900, 904, 907, 908, 910, 911, 913, 916, 927, 941, 946, 947, 954, 965, 969, 971, 973, 978, 981, 985, 987, 989, 990, 991, 994, 1012, 1014, 1034, 1038, 1041, 1042, 1043, 1048, 1070, 1072, 1075, 1077, 1078, 1085, 1087, 1090, 1100, 1102, 1107, 1115, 1116, 1117, 1119, 1121, 1129, 1130, 1131, 1138, 1139, 1142, 1143, 1148, 1151, 1152, 1157, 1159, 1160, 1161, 1167, 1172, 1173, 1177, 1180, 1182, 1183, 1189, 1192, 1194, 1195, 1204, 1205, 1210, 1211, 1212, 1215, 1228, 1235, 1245, 1246, 1251, 1253, 1261, 1266, 1273, 1276, 1291, 1292, 1300, 1302, 1303, 1312, 1313, 1323, 1325, 1326, 1331, 1335, 1339, 1345, 1355, 1357, 1371, 1379, 1383, 1388, 1392, 1394, 1397, 1406, 1409, 1410, 1416, 1429, 1430, 1432, 1436, 1446, 1450, 1451, 1452, 1454, 1464, 1465, 1466, 1477, 1481, 1497, 1498, 1507, 1509, 1516, 1519, 1520, 1521, 1524, 1534, 1543, 1545, 1554, 1556],
            [10, 11, 14, 15, 18, 19, 21, 25, 39, 43, 44, 45, 47, 52, 59, 62, 63, 67, 68, 71, 80, 83, 87, 89, 93, 97, 98, 99, 101, 111, 113, 117, 124, 125, 131, 142, 157, 158, 160, 168, 170, 173, 174, 175, 177, 179, 193, 198, 214, 217, 218, 230, 234, 235, 237, 238, 245, 249, 252, 253, 255, 262, 276, 279, 284, 295, 297, 302, 315, 323, 326, 330, 336, 342, 344, 348, 355, 360, 361, 365, 366, 372, 374, 382, 388, 391, 393, 394, 397, 404, 408, 409, 419, 421, 428, 432, 434, 440, 451, 454, 457, 460, 473, 475, 477, 479, 480, 492, 495, 500, 511, 517, 519, 521, 525, 526, 531, 533, 539, 540, 543, 550, 563, 567, 569, 574, 576, 590, 606, 608, 611, 622, 627, 628, 631, 633, 644, 650, 651, 660, 665, 666, 675, 680, 692, 695, 697, 701, 702, 704, 707, 714, 716, 719, 720, 721, 725, 732, 736, 742, 743, 749, 754, 758, 760, 761, 770, 771, 772, 774, 778, 781, 782, 784, 794, 800, 804, 806, 811, 814, 817, 820, 822, 823, 824, 833, 834, 838, 843, 844, 850, 851, 852, 858, 862, 864, 866, 870, 872, 873, 880, 892, 895, 902, 904, 909, 929, 938, 940, 941, 942, 947, 958, 959, 967, 971, 973, 980, 981, 983, 986, 991, 997, 999, 1008, 1015, 1017, 1020, 1021, 1023, 1028, 1029, 1032, 1033, 1037, 1038, 1046, 1047, 1051, 1053, 1057, 1058, 1059, 1066, 1070, 1072, 1080, 1083, 1086, 1089, 1093, 1099, 1108, 1112, 1117, 1118, 1119, 1125, 1126, 1132, 1136, 1143, 1146, 1147, 1150, 1153, 1157, 1158, 1163, 1180, 1183, 1185, 1192, 1194, 1195, 1197, 1202, 1203, 1208, 1214, 1215, 1218, 1220, 1221, 1232, 1246, 1253, 1257, 1258, 1262, 1269, 1270, 1273, 1275, 1279, 1292, 1300, 1307, 1310, 1314, 1321, 1322, 1332, 1334, 1336, 1337, 1338, 1351, 1364, 1367, 1371, 1373, 1379, 1383, 1391, 1392, 1395, 1414, 1416, 1417, 1421, 1423, 1446, 1447, 1449, 1455, 1458, 1460, 1473, 1475, 1479, 1480, 1484, 1486, 1487, 1494, 1511, 1516, 1517, 1521, 1522, 1526, 1527, 1528, 1535, 1539, 1546, 1548, 1549, 1551]
           ]

def get_ads_features(id1, id2):
	ftrs_idx = (id1+id2) % 10
	return features[ftrs_idx]
 