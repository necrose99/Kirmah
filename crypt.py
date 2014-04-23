#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#  kirmah/crypt.py
#  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#  software  : Kirmah    <http://kirmah.sourceforge.net/>
#  version   : 2.18
#  date      : 2013
#  licence   : GPLv3.0   <http://www.gnu.org/licenses/>
#  author    : a-Sansara <[a-sansara]at[clochardprod]dot[net]>
#  copyright : pluie.org <http://www.pluie.org/>
#
#  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#  This file is part of Kirmah.
#
#  Kirmah is free software (free as in speech) : you can redistribute it
#  and/or modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the License,
#  or (at your option) any later version.
#
#  Kirmah is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Kirmah.  If not, see <http://www.gnu.org/licenses/>.
#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ module crypt ~~

from base64             import urlsafe_b64encode, b64decode
from binascii           import b2a_base64, a2b_base64
from hashlib            import sha256, md5
from math               import log, floor, ceil
from random             import choice
from os                 import urandom
from re                 import sub
from mmap               import mmap
from ast                import literal_eval
from psr.sys            import Sys, Io, Const
from psr.log            import Log
from psr.mproc          import Manager

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ methods ~~

@Log(Const.LOG_ALL)
def hash_sha256(data):
    """Get a sha256 hash of str `data`
    :Returns: `str`
    """
    return str(sha256(bytes(data,'utf-8')).hexdigest())


@Log(Const.LOG_ALL)
def hash_sha256_file(path):
    """Get a sha256 hash of str `data`
    :Returns: `str`
    """
    return sha256(open(path, mode='rb').read()).hexdigest()


@Log()
def hash_md5_file(path):
    """Get a md5 hash of file from path
    :Returns: `str`
    """
    return md5(open(path, mode='rb').read()).hexdigest()


@Log(Const.LOG_ALL)
def randomFrom(val, sval=0):
    """Get a random number from range `sval=0` to `val`
    :Returns: `int`
    """
    lst = list(range(sval,val))
    return choice(lst)


@Log(Const.LOG_NEVER)
def represents_int(s):
    """"""
    try:
        if s is None : return False
        int(s)
        return True
    except ValueError:
        return False


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ class KeyGen ~~

class KeyGen :

    CHSET         = [33, 35, 36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739, 740, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754, 755, 756, 757, 758, 759, 760, 761, 762, 763, 764, 765, 766, 767, 768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 880, 881, 882, 883, 884, 885, 886, 887, 891, 892, 893, 894, 901, 902, 903, 904, 905, 906, 911, 912, 913, 914, 915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 928, 929, 932, 933, 934, 935, 936, 937, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 949, 950, 951, 952, 953, 954, 955, 956, 957, 958, 959, 960, 961, 962, 963, 964, 965, 966, 967, 968, 969, 970, 971, 972, 973, 974, 975, 976, 977, 978, 979, 980, 981, 982, 983, 984, 985, 986, 987, 988, 989, 990, 991, 992, 993, 994, 995, 996, 997, 998, 999, 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074, 1075, 1076, 1077, 1078, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095, 1096, 1097, 1098, 1099, 1100, 1101, 1102, 1103, 1104, 1105, 1106, 1107, 1108, 1109, 1110, 1111, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121, 1122, 1123, 1124, 1125, 1126, 1127, 1128, 1129, 1130, 1131, 1132, 1133, 1134, 1135, 1136, 1137, 1138, 1139, 1140, 1141, 1142, 1143, 1144, 1145, 1146, 1147, 1148, 1149, 1150, 1151, 1152, 1153, 1154, 1155, 1156, 1157, 1158, 1159, 1160, 1161, 1162, 1163, 1164, 1165, 1166, 1167, 1168, 1169, 1170, 1171, 1172, 1173, 1174, 1175, 1176, 1177, 1178, 1179, 1180, 1181, 1182, 1183, 1184, 1185, 1186, 1187, 1188, 1189, 1190, 1191, 1192, 1193, 1194, 1195, 1196, 1197, 1198, 1199, 1200, 1201, 1202, 1203, 1204, 1205, 1206, 1207, 1208, 1209, 1210, 1211, 1212, 1213, 1214, 1215, 1216, 1217, 1218, 1219, 1220, 1221, 1222, 1223, 1224, 1225, 1226, 1227, 1228, 1229, 1230, 1231, 1232, 1233, 1234, 1235, 1236, 1237, 1238, 1239, 1240, 1241, 1242, 1243, 1244, 1245, 1246, 1247, 1248, 1249, 1250, 1251, 1252, 1253, 1254, 1255, 1256, 1257, 1258, 1259, 1260, 1261, 1262, 1263, 1264, 1265, 1266, 1267, 1268, 1269, 1270, 1271, 1272, 1273, 1274, 1275, 1276, 1277, 1278, 1279, 1280, 1281, 1282, 1283, 1284, 1285, 1286, 1287, 1288, 1289, 1290, 1291, 1292, 1293, 1294, 1295, 1296, 1297, 1298, 1299, 1300, 1301, 1302, 1303, 1304, 1305, 1306, 1307, 1308, 1309, 3871, 3872, 3873, 3874, 3875, 3876, 3877, 3878, 3879, 3880, 3881, 3882, 3883, 3884, 3885, 3886, 3887, 3888, 3889, 3890, 3891, 3892, 3893, 3894, 3895, 2349, 2350, 2351, 2352, 2353, 2354, 2355, 2356, 2357, 2358, 2359, 2360, 2361, 2362, 2363, 2364, 2365, 2366, 2367, 2368, 2369, 2370, 2371, 2372, 2373, 2374, 2375, 2376, 2377, 2378, 2379, 2380, 2381, 2382, 2383, 2384, 2385, 2386, 2387, 2388, 2389, 2390, 2391, 2392, 2393, 2394, 2395, 2396, 2397, 2398, 2399, 2400, 2401, 2402, 2403, 2404, 2405, 2406, 2407, 2408, 2409, 2410, 2411, 2412, 2413, 2414, 2415, 2416, 2417, 2418, 2419, 2420, 2421, 2422, 2423, 4305, 4306, 4307, 4308, 4309, 4310, 4311, 4312, 4313, 4314, 4315, 4316, 4317, 4318, 4319, 4320, 4321, 4322, 4323, 4324, 4325, 4326, 4327, 4328, 4329, 4330, 4331, 4332, 4333, 4334, 4335, 4336, 4337, 4338, 4339, 4340, 4341, 4342, 4343, 4344, 4345, 4346, 4347, 4348, 4352, 4353, 4354, 4355, 4356, 4357, 4358, 4359, 4360, 4361, 4362, 4363, 4364, 4365, 4366, 4367, 4368, 4369, 4370, 4371, 4372, 4373, 4374, 4375, 4376, 4377, 4378, 4379, 4380, 4381, 4382, 4383, 4384, 4385, 4386, 4387, 4388, 4389, 4390, 4391, 4392, 4393, 4394, 4395, 4396, 4397, 4398, 4399, 4400, 4401, 4402, 4403, 4404, 4405, 4406, 4407, 4408, 4409, 4410, 4411, 4412, 4413, 4414, 4415, 4416, 4417, 4418, 4419, 4420, 4421, 4422, 4423, 4424, 4425, 4426, 4427, 4428, 4429, 4430, 4431, 4432, 4433, 4434, 4435, 4436, 4437, 4438, 4439, 4440, 4441, 4640, 4641, 4642, 4643, 4644, 4645, 4646, 4647, 4648, 4649, 4650, 4651, 4652, 4653, 4654, 4655, 4656, 4657, 4658, 4659, 4660, 4661, 4662, 4663, 4664, 4665, 4666, 4667, 4668, 4669, 4670, 4671, 4672, 4673, 4674, 4675, 4676, 4677, 4678, 4705, 4706, 4707, 4708, 4709, 4710, 4711, 4712, 4713, 4714, 4715, 4716, 4717, 4718, 4719, 4720, 4721, 4722, 4723, 4724, 4725, 4726, 4727, 4728, 4729, 4730, 4731, 4732, 4733, 4734, 4735, 4736, 4737, 4738, 4739, 4740, 4741, 4742, 4753, 4754, 4755, 4756, 4757, 4758, 4759, 4760, 4761, 4762, 4763, 4764, 4765, 4766, 4767, 4768, 4769, 4770, 4771, 4772, 4773, 4774, 4775, 4776, 4777, 4778, 4779, 4780, 4781, 4782, 4825, 4826, 4827, 4828, 4829, 4830, 4831, 4832, 4833, 4834, 4835, 4836, 4837, 4838, 4839, 4840, 4841, 4842, 4843, 4844, 4845, 4846, 4847, 4848, 4849, 4850, 4851, 4852, 4853, 4854, 4855, 4856, 4857, 4858, 4859, 4860, 4861, 4862, 4863, 4864, 4865, 4866, 4867, 4868] #, 4869, 4870, 4871, 4872, 4873, 4874, 4875, 4876, 4877, 4878, 5025, 5026, 5027, 5028, 5029, 5030, 5031, 5032, 5033, 5034, 5035, 5036, 5037, 5038, 5039, 5040, 5041, 5042, 5043, 5044, 5045, 5046, 5047, 5048, 5049, 5050, 5051, 5052, 5053, 5054, 5055, 5056, 5057, 5058, 5059, 5060, 5061, 5062, 5063, 5064, 5065, 5066, 5067, 5068, 5069, 5070, 5071, 5072, 5073, 5074, 5075, 5076, 5077, 5078, 5079, 5080, 5081, 5082, 5083, 5084, 5085, 5086, 5087, 5088, 5089, 5090, 5091, 5092, 5093, 5094, 5095, 5096, 5097, 5098, 5099, 5100, 5101, 5102, 5103, 5104, 5105, 5106, 5107, 5196, 5197, 5198, 5199, 5200, 5201, 5202, 5203, 5204, 5205, 5206, 5207, 5208, 5209, 5210, 5211, 5212, 5213, 5214, 5215, 5216, 5217, 5218, 5219, 5220, 5221, 5222, 5223, 5224, 5225, 5226, 5227, 5228, 5229, 5230, 5231, 5232, 5233, 5234, 5235, 5236, 5237, 5238, 5239, 5240, 5241, 5242, 5243, 5244, 5245, 5246, 5247, 5248, 5249, 5250, 5251, 5252, 5253, 5254, 5255, 5256, 5257, 5258, 5259, 5260, 5261, 5262, 5263, 5264, 5265, 5266, 5267, 5268, 5269, 5270, 5271, 5272, 5273, 5274, 5275, 5276, 5277, 5278, 5279, 5280, 5281, 5282, 5283, 5284, 5285, 5286, 5287, 5288, 5289, 5290, 5291, 5292, 5293, 5294, 5295, 5296, 5297, 5298, 5299, 5300, 5301, 5302, 5303, 5304, 5305, 5306, 5307, 5308, 5309, 5310, 5311, 5312, 5313, 5314, 5315, 5316, 5317, 5318, 5319, 5320, 5321, 5322, 5323, 5324, 5325, 5326, 5327, 5328, 5329, 5330, 5331, 5332, 5333, 5334, 5335, 5336, 5337, 5338, 5339, 5340, 5341, 5342, 5343, 5344, 5345, 5346, 5347, 5348, 5349, 5350, 5351, 5352, 5353, 5354, 5355, 5356, 5357, 5358, 5359, 5360, 5361, 5362, 5363, 5364, 5365, 5366, 5367, 5368, 5369, 5370, 5371, 5372, 5373, 5374, 5375, 5376, 5377, 5378, 5379, 5380, 5381, 5382, 5383, 5384, 5385, 5386, 5387, 5388, 5389, 5390, 5391, 5392, 5393, 5394, 5395, 5396, 5397, 5398, 5399, 5400, 5401, 5402, 5403, 5404, 5405, 5406, 5407, 5408, 5409, 5410, 5411, 5412, 5413, 5414, 5415, 5416, 5417, 5418, 5419, 5420, 5421, 5422, 5423, 5424, 5425, 5426, 5427, 5428, 5429, 5430, 5431, 5432, 5433, 5434, 5435, 5436, 5437, 5438, 5439, 5440, 5441, 5442, 5443, 5444, 5445, 5446, 5447, 5448, 5449, 5450, 5451, 5452, 5453, 5454, 5455, 5456, 5457, 5458, 5459, 5460, 5461, 5462, 5463, 5464, 5465, 5466, 5467, 5468, 5469, 5470, 5471, 5472, 5473, 5474, 5475, 5476, 5477, 5478, 5479, 5480, 5481, 5482, 5483, 5484, 5485, 5486, 5487, 5488, 5489, 5490, 5491, 5492, 5493, 5494, 5495, 5496, 5497, 5498, 5499, 5500, 5501, 5502, 5503, 5504, 5505, 5506, 5507, 5508, 5509, 5510, 5511, 5512, 5513, 5514, 5515, 5516, 5517, 5518, 5519, 5520, 5521, 5522, 5523, 5524, 5525, 5526, 5527, 5528, 5529, 5530, 5531, 5532, 5533, 5534, 5535, 5536, 5537, 5538, 5539, 5540, 5541, 5542, 5543, 5544, 5545, 5546, 5547, 5548, 5549, 5550, 5551, 5556, 5557, 5558, 5559, 5560, 5561, 5562, 5563, 5564, 5565, 5566, 5567, 5568, 5569, 5570, 5571, 5572, 5573, 5574, 5575, 5576, 5577, 5578, 5579, 5580, 5581, 5582, 5583, 5584, 5585, 5586, 5587, 5588, 5589, 5590, 5591, 5592, 5593, 5594, 5595, 5596, 5597, 5598, 5599, 5600, 5601, 5602, 5603, 5604, 5605, 5606, 5607, 5608, 5609, 5610, 5611, 5612, 5613, 5614, 5615, 5616, 5617, 5618, 5619, 5620, 5621, 5622, 5623, 5624, 5625, 5626, 5627, 5628, 5629, 5630, 5631, 5632, 5633, 5634, 5635, 5636, 5637, 5638, 5639, 5640, 5641, 5642, 5643, 5644, 5645, 5646, 5647, 5648, 5649, 5650, 5651, 5652, 5653, 5654, 5655, 5656, 5657, 5658, 5659, 5660, 5661, 5662, 5663, 5664, 5665, 5666, 5667, 5668, 5669, 5670, 5671, 5672, 5673, 5674, 5675, 5676, 5677, 5678, 5679, 5680, 5681, 5682, 5683, 5684, 5685, 5686, 5687, 5688, 5689, 5690, 5691, 5692, 5693, 5694, 5695, 5696, 5697, 5698, 5699, 5700, 5701, 5702, 5703, 5704, 5705, 5706, 5707, 5708, 5709, 5710, 5711, 5712, 5713, 5714, 5715, 5716, 5717, 5718, 5719, 5720, 5721, 5722, 5723, 5724, 5725, 5726, 5727, 5728, 5729, 5730, 5731, 5732, 5733, 5734, 5735, 5736, 5737, 5738, 5739, 5740, 5741, 5742, 5743, 5744, 5745, 5746, 5747, 5748, 5749, 5750, 5751, 5752, 5753, 5754, 5755, 5756, 5757, 5758, 5759, 5793, 5794, 5795, 5796, 5797, 5798, 5799, 5800, 5801, 5802, 5803, 5804, 5805, 5806, 5807, 5808, 5809, 5810, 5811, 5812, 5813, 5814, 5815, 5816, 5817, 5818, 5819, 5820, 5821, 5822, 5823, 5824, 5825, 5826, 5827, 5828, 5829, 5830, 5831, 5832, 5833, 5834, 5835, 5836, 5837, 5838, 5839, 5840, 5841, 5842, 5843, 5844, 5845, 5846, 5847, 5848, 5849, 5850, 5851, 5852, 5853, 5854, 5855, 5856, 5857, 5858, 5859, 5860, 5861, 5862, 5863, 5864, 5865, 5866, 5867, 5868, 5869, 5870, 5871, 5872, 7425, 7426, 7427, 7428, 7429, 7430, 7431, 7432, 7433, 7434, 7435, 7436, 7437, 7438, 7439, 7440, 7441, 7442, 7443, 7444, 7445, 7446, 7447, 7448, 7449, 7450, 7451, 7452, 7453, 7454, 7455, 7456, 7457, 7458, 7459, 7460, 7461, 7462, 7463, 7464, 7465, 7466, 7467, 7468, 7469, 7470, 7471, 7472, 7473, 7474, 7475, 7476, 7477, 7478, 7479, 7480, 7481, 7482, 7483, 7484, 7485, 7486, 7487, 7488, 7489, 7490, 7491, 7492, 7493, 7494, 7495, 7496, 7497, 7498, 7499, 7500, 7501, 7502, 7503, 7504, 7505, 7506, 7507, 7508, 7509, 7510, 7511, 7512, 7513, 7514, 7515, 7516, 7517, 7518, 7519, 7520, 7521, 7522, 7523, 7524, 7525, 7526, 7527, 7528, 7529, 7530, 7531, 7532, 7533, 7534, 7535, 7536, 7537, 7538, 7539, 7540, 7541, 7542, 7543, 7544, 7545, 7546, 7547, 7548, 7549, 7550, 7551, 7552, 7553, 7554, 7555, 7556, 7557, 7558, 7559, 7560, 7561, 7562, 7563, 7564, 7565, 7566, 7567, 7568, 7569, 7570, 7571, 7572, 7573, 7574, 7575, 7576, 7577, 7578, 7579, 7580, 7581, 7582, 7583, 7584, 7585, 7586, 7587, 7588, 7589, 7590, 7591, 7592, 7593, 7594, 7595, 7596, 7597, 7598, 7599, 7600, 7601, 7602, 7603, 7604, 7605, 7606, 7607, 7608, 7609, 7610, 7611, 7612, 7613, 7614, 7681, 7682, 7683, 7684, 7685, 7686, 7687, 7688, 7689, 7690, 7691, 7692, 7693, 7694, 7695, 7696, 7697, 7698, 7699, 7700, 7701, 7702, 7703, 7704, 7705, 7706, 7707, 7708, 7709, 7710, 7711, 7712, 7713, 7714, 7715, 7716, 7717, 7718, 7719, 7720, 7721, 7722, 7723, 7724, 7725, 7726, 7727, 7728, 7729, 7730, 7731, 7732, 7733, 7734, 7735, 7736, 7737, 7738, 7739, 7740, 7741, 7742, 7743, 7744, 7745, 7746, 7747, 7748, 7749, 7750, 7751, 7752, 7753, 7754, 7755, 7756, 7757, 7758, 7759, 7760, 7761, 7762, 7763, 7764, 7765, 7766, 7767, 7768, 7769, 7770, 7771, 7772, 7773, 7774, 7775, 7776, 7777, 7778, 7779, 7780, 7781, 7782, 7783, 7784, 7785, 7786, 7787, 7788, 7789, 7790, 7791, 7792, 7793, 7794, 7795, 7796, 7797, 7798, 7799, 7800, 7801, 7802, 7803, 7804, 7805, 7806, 7807, 7808, 7809, 7810, 7811, 7812, 7813, 7814, 7815, 7816, 7817, 7818, 7819, 7820, 7821, 7822, 7823, 7824, 7825, 7826, 7827, 7828, 7829, 7830, 7831, 7832, 7833, 7834, 7835, 7836, 7837, 7838, 7839, 7840, 7841, 7842, 7843, 7844, 7845, 7846, 7847, 7848, 7849, 7850, 7851, 7852, 7853, 7854, 7855, 7856, 7857, 7858, 7859, 7860, 7861, 7862, 7863, 7864, 7865, 7866, 7867, 7868, 7869, 7870, 7871, 7872, 7873, 7874, 7875, 7876, 7877, 7878, 7879, 7880, 7881, 7882, 7883, 7884, 7885, 7886, 7887, 7888, 7889, 7890, 7891, 7892, 7893, 7894, 7895, 7896, 7897, 7898, 7899, 7900, 7901, 7902, 7903, 7904, 7905, 7906, 7907, 7908, 7909, 7910, 7911, 7912, 7913, 7914, 7915, 7916, 7917, 7918, 7919, 7920, 7921, 7922, 7923, 7924, 7925, 7926, 7927, 7928, 7929, 7930, 7931, 7932, 7933, 7934, 7935, 7936, 7937, 7938, 7939, 7940, 7941, 7942, 7943, 7944, 7945, 7946, 7947, 7948, 7949, 7950, 7951, 7952, 7953, 7954, 7955, 7956, 7957, 8032, 8033, 8034, 8035, 8036, 8037, 8038, 8039, 8040, 8041, 8042, 8043, 8044, 8045, 8046, 8047, 8048, 8049, 8050, 8051, 8052, 8053, 8054, 8055, 8056, 8057, 8058, 8059, 8060, 8061, 4305, 8065, 8066, 8067, 8068, 8069, 8070, 8071, 8072, 8073, 8074, 8075, 8076, 8077, 8078, 8079, 8080, 8081, 8082, 8083, 8084, 8085, 8086, 8087, 8088, 8089, 8090, 8091, 8092, 8093, 8094, 8095, 8096, 8097, 8098, 8099, 8100, 8101, 8102, 8103, 8104, 8105, 8106, 8107, 8108, 8109, 8110, 8111, 8112, 8113, 8114, 8115, 8116, 8449, 8450, 8451, 8452, 8453, 8454, 8455, 8456, 8457, 8458, 8459, 8460, 8461, 8462, 8463, 8464, 8465, 8466, 8467, 8468, 8469, 8470, 8471, 8472, 8473, 8474, 8475, 8476, 8477, 8478, 8479, 8480, 8481, 8482, 8483, 8484, 8485, 8486, 8487, 8488, 8489, 8490, 8491, 8751, 8752, 8753, 8754, 8755, 8756, 8757, 8758, 8759, 8760, 8761, 8762, 8763, 8764, 8765, 8766, 8767, 8768, 8769, 8770, 8771, 8772, 8773, 8774, 8775, 8776, 8777, 8778, 8779, 8780, 8781, 8782, 8783, 8784, 8785, 8786, 8787, 8788, 8789, 8790, 8791, 8792, 8793, 8794, 8795, 8796, 8797, 8798, 8799, 8800, 8801, 8802, 8803, 8804, 8805, 8806, 8807, 8808, 4306, 4307, 4308, 4309, 4310, 4311, 4312, 4313, 4314, 4315, 4316, 4317, 4318, 4319, 4320, 4321, 4322, 4323, 4324, 4325, 4326, 4327, 4328, 4329, 4330, 4331, 4332, 4333, 4334, 4335, 4336, 4337, 4338, 4339, 4340, 4341, 4342, 4343, 4344, 4345, 4346, 4347, 1310, 1311, 1312, 1313, 1314, 1315, 1316, 1317, 1318, 1319, 1330, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1341, 1342, 1343, 1344, 1345, 1346, 1347, 1348, 1349, 1350, 1351, 1352, 1353, 1354, 1355, 1356, 1357, 1358, 1359, 1360, 1361, 1362, 1363, 1364, 1365, 1366, 1370, 1371, 1372, 1373, 1374, 1375, 1378, 1379, 1380, 1381, 1382, 1383, 1384, 1385, 1386, 1387, 1388, 1389, 1390, 1391, 1392, 1393, 1394, 1395, 1396, 1397, 1398, 1399, 1400, 1401, 1402, 1403, 1404, 1405, 1406, 1407, 1408, 1409, 1410, 1497, 1498, 1499, 1500, 1501, 1502, 1503, 1504, 1505, 1506, 1507, 1508, 1509, 1510, 1511, 1512, 1513, 1514, 1521, 1522, 1523, 1524, 1567, 1568, 1569, 1570, 1571, 1572, 1573, 1574, 1575, 1576, 1577, 1578, 1579, 1580, 1581, 1582, 1583, 1584, 1585, 1586, 1587, 1588, 1589, 1590, 1591, 1592, 1593, 1594, 1595, 1596, 1597, 1598, 1599, 1600, 1601, 1602, 1603, 1604, 1605, 1606, 1607, 1608, 1609, 1610, 1611, 1612, 1613, 1614, 1615, 1616, 1617, 1618, 1619, 1620, 1632, 1633, 1634, 1635, 1636, 1637, 1638, 1639, 1640, 1641, 1642, 1643, 1644, 1645, 1646, 1647, 1648, 1649, 1650, 1651, 1652, 1653, 1654, 1655, 1656, 1657, 1658, 1659, 1660, 1661, 1662, 1663, 1664, 1665, 1666, 1667, 1668, 1669, 1670, 1671, 1672, 1673, 1674, 1675, 1676, 1677, 1678, 1679, 1680, 1681, 1682, 1683, 1684, 1685, 1686, 1687, 1688, 1689, 1690, 1691, 1692, 1693, 1694, 1695, 1696, 1697, 1698, 1699, 1700, 1701, 1702, 1703, 1704, 1705, 1706, 1707, 1708, 1709, 1710, 1711, 1712, 1713, 1714, 1715, 1716, 1717, 1718, 1719, 1720, 1721, 1722, 1723, 1724, 1725, 1726, 1727, 1728, 1729, 1730, 1731, 1732, 1733, 1734, 1735, 1736, 1737, 1738, 1739, 1740, 1741, 1742, 1743, 1744, 1745, 1746, 1747, 1748, 1774, 1775, 1776, 1777, 1778, 1779, 1780, 1781, 1782, 1783, 1784, 1785, 1786, 1787, 1788, 1789, 1790, 1791, 1792, 1793, 1794, 1795, 1796, 1797, 1798, 1799, 1800, 1801, 1802, 1803, 1804, 1805, 1810, 1811, 1812, 1813, 1814, 1815, 1816, 1817, 1818, 1819, 1820, 1821, 1822, 1823, 1824, 1825, 1826, 1827, 1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838, 1839, 1840, 1841, 1842, 1843, 1844, 1845, 1846, 1847, 1848, 1849, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956]
    """"""
    LEN_FOOTPRINT = 24
    """"""
    SALT          = '-¤-Kirmah-¤-'
    """"""

    @Log(Const.LOG_BUILD)
    def __init__(self, length, salt=None):
        """"""
        self.new(length, salt)


    @Log(Const.LOG_PRIVATE)
    def _build(self,l):
        """"""
        r = Randomiz(len(self.CHSET),self.CHSET)
        self.key = ksin = kfoo = ''
        dic = {}
        for i in range(l):
            self.key += chr(r.get(False))
            if not self.key[i] in dic: dic[self.key[i]] = 1
        for c in dic: ksin += c
        for c in ksin[::-5]:
            if len(kfoo)>=self.LEN_FOOTPRINT: break
            kfoo += c
        self.mark = hash_sha256(self.salt+kfoo)


    @Log(Const.LOG_DEBUG)
    def getMark(self, key=None):
        """"""
        dic  = {}
        ksin = kfoo = ''
        if key is None :
            key = self.key
        for i in range(len(key)):
            if not key[i] in dic: dic[key[i]] = 1
        for c in dic: ksin += c
        for c in sorted(ksin)[::-5]:
            if len(kfoo)>=self.LEN_FOOTPRINT: break
            kfoo += c
        return hash_sha256(self.salt+kfoo)


    @Log(Const.LOG_DEBUG)
    def new(self, length, salt=None):
        """"""
        if salt == None : self.salt = self.SALT
        else : self.salt = salt
        self._build(length)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ class ConfigKey ~~

class ConfigKey:

    @Log(Const.LOG_BUILD)
    def __init__(self, key=None, salt=None, psize=19710000):
        """"""
        self.key  = bytes(key,'utf-8') if key is not None else self._build()
        self.salt = str(self.key[::-10]) if salt is None else salt
        self.psize  = psize
        self.noiser = Noiser(self.key)
        self.rdmz   = Randomiz(1)


    @staticmethod
    @Log(Const.LOG_ALL)
    def sumNumber(s,count):
        """"""
        return sum([ int(c) for j,c in enumerate(s) if represents_int(c)][0:count])


    @Log(Const.LOG_DEBUG)
    def getHashList(self,name,count,noSorted=False):
        """"""
        self.rdmz.new(count)
        dic, lst, hroot = {}, [], hash_sha256(self.salt+name)

        srdl = Kirmah.getRandomListFromKey(self.key, count)
        #~ srdl = getRandomListFromKey(self.key, count)
        for i in range(count) :
            self.noiser.build(i,ConfigKey.sumNumber(hash_sha256(str(i)+self.salt+name),1 if i%2 else 2))
            d     = str(i).rjust(2,'0')
            # part n°, hash, lns, lne, pos
            hpart = hash_sha256(self.salt+name+'.part'+d)[:-3]+str(ord(hroot[i])).rjust(3,'0')
            lst.append((i, hpart, self.noiser.lns, self.noiser.lne, self.rdmz.get(), srdl[i]))
        dic['head'] = [name,count,hroot,self.getKey()]
        if not noSorted :
            lst = sorted(lst, key=lambda lst: lst[4])
        dic['data'] = lst
        return dic


    @Log(Const.LOG_PRIVATE)
    def _build(self,l=48):
        """"""
        kg = KeyGen(l)
        k  = urlsafe_b64encode(bytes(kg.key,'utf-8'))
        return k


    @Log(Const.LOG_DEBUG)
    def getKey(self):
        """"""
        return str(self.key,'utf-8')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ class Kirmah ~~

class KirmahHeader:

    COMP_NONE        = 0
    COMP_ALL         = 1
    COMP_END         = 2

    POS_VERS         = 5
    POS_COMP         = 7
    POS_RAND         = 12
    POS_MIX          = 15
    POS_SEC          = 18
    POS_END          = 22

    ID               = b'\x05\xd9\x83MH'
    MODE_COMP        = b'Z'
    MODE_RAND        = b'R'
    MODE_MIX         = b'M'
    MODE_SEC         = b'S'

    """
         
    ex : كMH02Z2499R42M26S0055
          
    5o :  كMH    - File type id (FIXED)


    2o :  02     - Version (majeur number)
                   version.rjust(2,'0')

    5o :  Z??    - Compression Mode
                  '?' ord(chr mark pos)%2==0
                       ? compression ON
                       : compression OFF
                  '?' ord(chr mark pos)%2==0
                       ? compression all
                       : compression end

    3o :  R?     - Random Mode
                  '?' ord(chr mark pos)%2==0
                       ? random ON
                       : randon OFF

    3o :  M?     - Mix Mode
                  '?' ord(chr mark pos)%2==0
                       ? mix ON
                       : mix OFF

    3o :  S???   - Secure Mode
                  '?' mark[dlen%len(mark)].rjust(3,'0')

    """

    @Log(Const.LOG_BUILD)
    def __init__(self, version, mark, cmode=1, rmode=True, mmode=True):
        """"""
        self.version = bytes(str(int(float(version))).rjust(2,'0'),'utf-8')
        self.mark    = mark
        self.cmode   = cmode
        self.rmode   = rmode
        self.mmode   = mmode


    @Log(Const.LOG_DEBUG)
    def getPositionnalChar(self, sindex, test=True):
        """"""
        pc = None
        for i, c in enumerate(self.mark[sindex:]) :
            if c % 2 == 0 and test or not test and c % 2 != 0 :
                pc = i+sindex
                break
        return pc


    @Log(Const.LOG_DEBUG)
    def checkPositionnalChar(self, pc):
        """"""
        return ord(self.mark[pc:pc+1])%2==0


    @Log()
    def buildHeader(self, dlen, cmode=None, rmode=None, mmode=None):
        """"""
        if cmode is None : cmode = self.cmode
        if rmode is None : rmode = self.rmode
        if mmode is None : mmode = self.mmode
        nocomp = cmode is self.COMP_NONE
        cmpc1  = self.getPositionnalChar(1, not nocomp)
        cmpc2  = self.getPositionnalChar(cmpc1+5, cmode is self.COMP_ALL)
        rmpc   = self.getPositionnalChar(cmpc2+5, rmode)
        mmpc   = self.getPositionnalChar(rmpc+5, mmode)
        smpc   = self.mark[dlen%len(self.mark)]
        head   = [self.ID, self.version, self.MODE_COMP, Io.bytes(str(cmpc1).rjust(2,'0')), Io.bytes(str(cmpc2).rjust(2,'0')), self.MODE_RAND, Io.bytes(str(rmpc).rjust(2,'0')), self.MODE_MIX, Io.bytes(str(mmpc).rjust(2,'0')), self.MODE_SEC, Io.bytes(str(smpc).rjust(3,'0'))]
        return b''.join(head)


    @Log()
    def readHeader(self, header):
        """"""

        isKmh, vers, cmode, rmode, mmode, smode, pc1, badKmh = header[:self.POS_VERS] == self.ID, None, None , None, None, None, None, False
        if isKmh :
            vers  = int(header[self.POS_VERS:self.POS_VERS+2])
            if header[self.POS_COMP:self.POS_COMP+1] == self.MODE_COMP :
                if self.checkPositionnalChar(int(header[self.POS_COMP+1:self.POS_COMP+3])) :
                    cmode = self.COMP_ALL if self.checkPositionnalChar(int(header[self.POS_COMP+3:self.POS_COMP+5])) else self.COMP_END
                else :
                    cmode = self.COMP_NONE
            else :
                badKmh = True

            if header[self.POS_RAND:self.POS_RAND+1] == self.MODE_RAND :
                rmode = self.checkPositionnalChar(int(header[self.POS_RAND+1:self.POS_RAND+3]))
            else :
                badKmh = True

            if header[self.POS_MIX:self.POS_MIX+1] == self.MODE_MIX :
                mmode = self.checkPositionnalChar(int(header[self.POS_MIX+1:self.POS_MIX+3]))
            else :
                badKmh = True

            if header[self.POS_SEC:self.POS_SEC+1] == self.MODE_SEC :
                smode = chr(int(header[self.POS_SEC+1:self.POS_SEC+4]))
            else : badKmh = True

        return { 'version':vers, 'cmode':cmode, 'rmode':rmode, 'mmode':mmode,'smode':smode} if isKmh and not badKmh else {}



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ class Kirmah ~~

class Kirmah:

    VERSION    = '2.1'
    EXT        = '.kmh'
    EXT_TARK   = '.tark'
    DIR_OUTBOX = ''
    DIR_INBOX  = ''
    DIR_DEPLOY = ''
    DIR_TEMP   = ''
    KMP_FILE   = '.kmp'


    @Log(Const.LOG_BUILD)
    def __init__(self, key, mark=None, headcompress=2, headrandom=True, headmix=True):
        """"""
        self.key   = Io.bytes(key)
        self.mark  = KeyGen(len(key)).getMark(key) if mark is None else mark
        self.mark2 = hash_sha256(self.mark) + self.mark[::-1]
        self.ck    = ConfigKey(self.mark2)
        self.kh    = KirmahHeader(Kirmah.VERSION, Io.bytes(self.mark), headcompress, headrandom, headmix)


    @Log()
    def compress_start(self, fromPath, toPath, compress=True, lvl=9, emit=True):
        """"""
        if not Sys.is_cli_cancel():
            with Io.rfile(fromPath) as fi :
                with Io.wfile(toPath) as fo :
                    data = fi.read() if not compress else Io.gzcompress(fi.read(), lvl)
                    fo.write(b2a_base64(data))


    @Log()
    def uncompress_start(self, fromPath, toPath, decompress=True, emit=True):
        """"""
        if not Sys.is_cli_cancel():
            with Io.rfile(fromPath) as fi :
                with Io.wfile(toPath) as fo :
                    data = a2b_base64(fi.read())
                    fo.write(data if not decompress else Io.gzdecompress(data))


    @Log()
    def compress_end(self, fromPath, toPath, compress=True, lvl=9, emit=True):
        """"""
        if not Sys.is_cli_cancel():
            with Io.rfile(fromPath) as fi :
                with Io.wfile(toPath) as fo :
                    data   = fi.read()
                    if compress : data = Io.gzcompress(data, lvl)
                    header = self.kh.buildHeader(len(data))
                    fo.write(header)
                    fo.write(data)


    @Log()
    def uncompress_end(self, fromPath, toPath, decompress=True, emit=True):
        """"""
        if not Sys.is_cli_cancel():
            with Io.rfile(fromPath) as fi :
                with Io.wfile(toPath) as fo :
                    fi.seek(self.kh.POS_END)
                    fo.write(fi.read() if not decompress else Io.gzdecompress(fi.read()))

    @Log(Const.LOG_ALL)
    def encryptStr(self, data, emit=True):
        """"""
        if not Sys.is_cli_cancel():
            s, lk, i = [], len(self.key), 0
            for c in data:
                if lk-i <= 0:
                    i = 0
                    if Sys.is_cli_cancel(): break
                s.append(chr(c + i//4 + (self.key[i] if c + self.key[i] + i//4 < 11000 else -self.key[i])))
                i += 1
            return Io.bytes(''.join(s))


    @Log()
    def encryptToFile(self, fromPath, toPath, i=0, event=None, emit=True):
        """"""
        if not Sys.is_cli_cancel():
            with Io.ufile(fromPath) as fi :
                with Io.wfile(toPath, False) as fo :
                    s, lk = [], len(self.key)
                    for c in Io.read_utf8_chr(fi):
                        if i >= lk:
                            i = 0
                            if Sys.is_cli_cancel(event) :
                                Sys.pwarn((('terminating child process ',(str(Sys.getpid()),Sys.CLZ_WARN_PARAM), ' !'),), False)
                                break
                        fo.write(chr(ord(c) + i//4 + (self.key[i] if ord(c) + self.key[i] + i//4 < 11000 else -self.key[i])))
                        i += 1


    @Log()
    def decryptToFile(self, fromPath, toPath, i=0, event=None, emit=True):
        """"""
        if not Sys.is_cli_cancel():
            with Io.ufile(fromPath) as fi :
                with Io.rfile(fromPath) as fi2 :
                    s = fi2.read()
                with Io.wfile(toPath, False) as fo :
                    s, lk = [], len(self.key)

                    for c in Io.read_utf8_chr(fi):
                        if i >= lk:
                            i = 0
                            if Sys.is_cli_cancel(event) :
                                Sys.pwarn((('terminating child process ',(str(Sys.getpid()),Sys.CLZ_WARN_PARAM), ' !'),), False)
                                break
                        try :
                            fo.write(chr(ord(c)- i//4 + (-self.key[i] if ord(c) + self.key[i] +i//4 < 110000 else self.key[i])))
                        except Exception as e :
                            Sys.pwarn((('decryptToFile : ',(str(e),Sys.CLZ_ERROR_PARAM), ' !'),
                                       ('ord c : ',(str(ord(c)),Sys.CLZ_ERROR_PARAM), ' - self.key[',(str(i),Sys.CLZ_ERROR_PARAM), '] : ',(str(self.key[i]),Sys.CLZ_ERROR_PARAM)),
                            ), True)
                            raise e
                        i += 1


    @Log()
    def randomFileContent(self, fromPath, toPath, emit=True):
        """"""
        d = Sys.datetime.now()
        c = not Sys.is_cli_cancel()
        if c:
            with Io.rfile(fromPath) as fi :
                with Io.wfile(toPath) as fo :
                    fsize, chsize, size = Kirmah.getSizes(fromPath)
                    lst, rest, data     = Kirmah.getRandomListFromKey(self.ck.key, size), chsize - fsize%chsize, ['b']*size
                    if rest == chsize : rest = 0
                    for piece, i in Io.read_in_chunks(fi, chsize):
                        fo.seek(lst[i]*chsize-(rest if lst[i] > lst[size-1] else 0))
                        fo.write(piece[::-1])
        if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
        Sys.pstep('Random mode', d, c)


    @Log()
    def unRandomFileContent(self, fromPath, toPath, emit=True):
        """"""
        d = Sys.datetime.now()
        c = not Sys.is_cli_cancel()
        if c:
            with Io.rfile(fromPath) as fi :
                with Io.wfile(toPath) as fo :
                    fsize, chsize, size    = Kirmah.getSizes(fromPath)
                    lst, rest, piece, data = Kirmah.getRandomListFromKey(self.ck.key, size), chsize - fsize%chsize, b'', []
                    if rest == chsize : rest = 0
                    for i, pos in enumerate(lst):
                        dp = pos*chsize-(rest if pos >= lst[size-1] and pos!=0 else 0)
                        if dp >= 0 : fi.seek(dp)
                        piece = fi.read(chsize)
                        if i == size-1 and rest > 0 :
                            piece = piece[:-rest] if lst[i]==0 else piece[rest:]
                        fo.write(piece[::-1])
        if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
        Sys.pstep('Random mode - inv', d, c)


    @Log()
    def mixdata(self, fromPath, toPath, encryptNoise=False, label='kirmah', cpart=22, emit=True):
        """"""
        d = Sys.datetime.now()
        c = not Sys.is_cli_cancel()
        if c:
            hlst         = self.ck.getHashList(label, cpart, False)
            hlst['data'] = sorted(hlst['data'], key=lambda hlst: hlst[0])
            size         = Sys.getsize(fromPath)
            psize        = ceil(size/cpart)
            cp           = 0
            rsz          = 0
            for row in hlst['data']: rsz += row[2]+row[3]
            with Io.rfile(fromPath) as fi:
                with Io.wfile(toPath) as fo :
                    bdata, adata = '', ''
                    for row in hlst['data']:
                        bdata, adata = self.ck.noiser.getNoise(row[2]), self.ck.noiser.getNoise(row[3])
                        if encryptNoise :
                            bdata, adata = self.encryptStr(bdata)[:row[2]], self.encryptStr(adata)[:row[3]]
                        fi.seek(psize*row[5])
                        fo.write(bdata[:row[2]] + fi.read(psize) + adata[:row[3]])
                        cp      += 1
        if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
        Sys.pstep('Mix mode', d, c)


    @Log(Const.LOG_DEBUG)
    def getNoiseLenBeforeIndex(self, hlst, psize, rest, size):
        """"""
        if not Sys.is_cli_cancel():
            lst, l, df, sou, f = [], 0, psize, False, 0
            lst.append(l)
            mxp = size // psize
            if size % psize == 0 : mxp -= 1
            for row in hlst:
                if row[5] == mxp :
                    df = rest
                elif row[5] > mxp :
                    df = 0
                else : df = psize
                l += row[2]+ row[3] + df
                lst.append(l)
            return lst


    @Log()
    def unmixdata(self, fromPath, toPath, label='kirmah', cpart=22, emit=True):
        """"""
        d = Sys.datetime.now()
        c = not Sys.is_cli_cancel()
        if c:
            rsz, cp, hlst = 0, 0, self.ck.getHashList(label, cpart, True)
            for row in hlst['data']:
                rsz += row[2]+row[3]
            size         = Sys.getsize(fromPath)-rsz
            psize        = ceil(size/cpart)
            rest         = size % psize
            if rest == 0 : rest = psize
            lbi          = self.getNoiseLenBeforeIndex(hlst['data'],psize,rest, size)
            hlst['data'] = sorted(hlst['data'], key=lambda hlst: hlst[5])
            mxp = size // psize
            if size % psize == 0 : mxp -= 1
            with Io.rfile(fromPath) as fi :
                with Io.wfile(toPath) as fo :
                    header = fi.read(self.kh.POS_END)
                    fi.seek(0,Io.SEEK_CUR)
                    for row in hlst['data']:
                        fi.seek(lbi[row[0]]+row[2])
                        dp = fi.read(psize if row[5] <= mxp else (rest if rest!=psize or (psize*cpart==size) else 0))
                        cp += 1
                        if fo.tell() + len(dp) > size :
                            fo.write(dp[:rest])
                            break
                        fo.write(dp)
        if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
        Sys.pstep('Mix mode - inv', d, c)


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # SPLIT # #

    @Log()
    def splitFile(self, fromPath, hlst, nproc=1):
        """"""
        if not Sys.is_cli_cancel():
            d = Sys.datetime.now()
            Sys.cli_emit_progress(2)
            self.split(fromPath, hlst)
            Sys.cli_emit_progress(70)
            if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
            Sys.pstep('Splitting file', d, True)
            return self.kcfEnc(hlst)


    @Log()
    def kcfEnc(self, hlst, nproc=1):
        if not Sys.is_cli_cancel():
            d = Sys.datetime.now()
            theStr  = {'name': hlst['head'][0], 'count': hlst['head'][1] }
            Io.set_data(self.DIR_DEPLOY+hlst['head'][2]+'.tmp', str(theStr))
            self.encrypt(self.DIR_DEPLOY+hlst['head'][2]+'.tmp', self.DIR_DEPLOY+hlst['head'][2]+'.kcf', nproc, KirmahHeader(self.VERSION, Io.bytes(self.mark), KirmahHeader.COMP_NONE, True, True), False)
            Sys.removeFile(self.DIR_DEPLOY+hlst['head'][2]+'.tmp')
            if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
            Sys.pstep('Encrypting Kirmah configuration file', d, True)
            Sys.cli_emit_progress(75)
            return self.DIR_DEPLOY+hlst['head'][2]+'.kcf'


    @Log()
    def split(self, fromPath, hlst):
        """"""
        if not Sys.is_cli_cancel():
            self.DIR_OUTBOX = ''
            f               = open(fromPath, 'rb+')
            m, p, rsz       = mmap(f.fileno(), 0), 0, 0
            fsize           = Sys.getsize(fromPath)
            Sys.cli_emit_progress(3)
            for row in hlst['data']: rsz += row[2]+row[3]
            # ensure correct order
            hlst['data']    = sorted(hlst['data'], key=lambda lst: lst[0])

            self.splheader  = self.kh.buildHeader(fsize)
            psize  = ceil(fsize/hlst['head'][1])
            Sys.cli_emit_progress(4)
            perc = 5
            frav = 1.40
            while m.tell() < m.size():
                perc += frav
                Sys.cli_emit_progress(perc)
                self.splitPart(m, psize, hlst['data'][p])
                perc += frav
                Sys.cli_emit_progress(perc)
                p += 1
            m.close()

            # ensure random order
            hlst['data'] = sorted(hlst['data'], key=lambda lst: lst[4])
            hlst['head'].append(psize)
            return hlst


    @Log()
    def splitPart(self, mmap, size, phlst):
        """"""
        if not Sys.is_cli_cancel():
            with Io.wfile(self.DIR_OUTBOX+phlst[1]+self.EXT) as fo :
                bdata, adata, part = self.ck.noiser.getNoise(phlst[2], False)[len(self.splheader):], self.ck.noiser.getNoise(phlst[3], False), int(phlst[0])
                zd  = Io.gzcompress(bdata+mmap.read(size)+adata)
                hz  = Io.bytes(self.offuscate(zd[:self.kh.POS_END], part))
                lhz = Io.bytes(str(part + len(hz)).rjust(3,'0'))
                fo.write(self.splheader+lhz+hz+zd[self.kh.POS_END:])


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # MERGE # #

    @Log()
    def mergeFile(self, fromPath, toPath=None, uid=''):
        """"""
        if not Sys.is_cli_cancel():
            Sys.cli_emit_progress(2)
            self.decrypt(fromPath, '.cfg')
            Sys.cli_emit_progress(5)
            data  = Io.get_data('.cfg')
            clist = literal_eval(data)
            Sys.removeFile('.cfg')
            theList = self.ck.getHashList(clist['name'], clist['count'], True)
            ext     = ''
            if toPath is None :
                toPath = clist['name']
            elif Sys.isdir(toPath) :
                toPath += clist['name']
            toPath, ext = Sys.getFileExt(toPath)
            dirs    = (Sys.dirname(Sys.realpath(toPath)) if toPath is not None else Sys.dirname(Sys.realpath(fromPath)))+Sys.sep
            Sys.cli_emit_progress(10)
            toPath  = self.merge(theList, toPath, ext, uid, dirs)
            Sys.removeFile(fromPath)
            Sys.cli_emit_progress(90)
            return toPath


    @Log()
    def merge(self, hlst, fileName, ext='', uid='', dirs=None, fake=False):
        """"""
        if not Sys.is_cli_cancel():
            p = 0
            # ensure correct order
            hlst['data'] = sorted(hlst['data'], key=lambda lst: lst[0])
            #~ print(hlst['head'])
            #~ for row in hlst['data']:
                #~ print(row)
            #~ if dirs is not None and dirs!='none' :
                #~ dirPath = Sys.join(self.DIR_DEPLOY,dirs)+Sys.sep
                #~ Sys.mkdir_p(dirPath)
            #~ else: dirPath = self.DIR_DEPLOY
            #~ print('dirPath')
            #~ print(dirPath)
            #~ filePath = dirPath+fileName
            filePath = fileName
            if Io.file_exists(filePath+ext):
                filePath += '-'+str(uid)
            filePath += ext
            depDir   = dirs
            perc     = 10
            frav     = 2.7
            with Io.wfile(filePath) as fo :
                while p < hlst['head'][1] :
                    perc += 0.5
                    Sys.cli_emit_progress(perc)
                    try:
                        self.mergePart(fo, hlst['data'][p], depDir)
                    except Exception as e:
                        Sys.pwarn((('merge : ',(str(e),Sys.CLZ_WARN_PARAM), ' !'),), True)
                        raise e
                    perc += frav
                    Sys.cli_emit_progress(perc)
                    p += 1
            return filePath


    @Log()
    def mergePart(self, fo, phlst, depDir):
        """"""
        if not Sys.is_cli_cancel():
            with Io.rfile(depDir+phlst[1]+self.EXT) as fi:
                part, head = int(phlst[0]), fi.read(self.kh.POS_END)
                fo.write(Io.gzdecompress(self.deoffuscate(Io.str(fi.read(int(fi.read(3))-part)), part) + fi.read())[phlst[2]-self.kh.POS_END:-phlst[3]])
            Sys.removeFile(depDir+phlst[1]+self.EXT)


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # ENCRYPT # #

    @Log()
    def mpMergeFiles(self,hlstPaths, toPath, noRemove=False, emit=True):
        """"""
        if not Sys.is_cli_cancel():
            with Io.wfile(toPath) as fo:
                for fromPath in hlstPaths :
                    with Io.rfile(fromPath) as fi :
                        fo.write(fi.read())
                    if not noRemove : Sys.removeFile(fromPath)
        #~ if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
        #~ Sys.pstep('Encrypt Data (multiprocessing)', d, c)


    @Log()
    def encrypt_sp_start(self, fromPath, toPath, header=None, emit=True):
        """"""
        if not Sys.is_cli_cancel():
            if header is not None :
                self.kh = header
            fsize = Sys.getsize(fromPath)
            if fsize > 0 :
                strh = self.kh.buildHeader(fsize)
                decHeader = self.kh.readHeader(strh)
                self.tmpPath1  = self.DIR_TEMP + Sys.basename(fromPath) + '.tmp'
                self.tmpPath2  = self.DIR_TEMP + Sys.basename(fromPath) + '.tmp2'
                compend, compstart = not decHeader['cmode']== KirmahHeader.COMP_NONE, decHeader['cmode']== KirmahHeader.COMP_ALL
                fp, tp             = fromPath, self.tmpPath1
                if emit : Sys.cli_emit_progress(2)
                d = Sys.datetime.now()
                if compstart :
                    if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
                    Sys.ptask('Compressing data')
                self.compress_start(fp, tp, compstart, emit=emit)
                if compstart :
                    if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
                    Sys.pstep('Compression mode', d, True)
                fp, tp = tp, self.tmpPath2 if tp == self.tmpPath1 else self.tmpPath1
                if emit : Sys.cli_emit_progress(5)
                return fp, tp, decHeader['rmode'], decHeader['mmode'], compend


    @Log()
    def encrypt_sp_end(self, fp, tp, toPath, rmode, mmode, compend, emit=True):
        """"""
        if not Sys.is_cli_cancel():
            if rmode :
                #~ self.mpRandomFileContent(fp, tp, 4)
                if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
                Sys.ptask('Randomizing data')
                self.randomFileContent(fp, tp, emit=emit)
                fp, tp = tp, self.tmpPath2 if tp == self.tmpPath1 else self.tmpPath1
            if emit : Sys.cli_emit_progress(75)

            if mmode :
                if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
                Sys.ptask('Mixing data')
                self.mixdata(fp, tp, True, emit=emit)

                fp, tp = tp, self.tmpPath2 if tp == self.tmpPath1 else self.tmpPath1
            if emit : Sys.cli_emit_progress(85)

            if compend :
                d = Sys.datetime.now()
                if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
                Sys.ptask('Compressing data')
            self.compress_end(fp, toPath, compend, emit=emit)
            if emit : Sys.cli_emit_progress(95)

            if compend :
                if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
                Sys.pstep('Compression mode', d, True)

            # clean tmp files
            if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
            Sys.ptask('Cleaning')

            try :
                Sys.removeFile(self.tmpPath1)
                Sys.removeFile(self.tmpPath2)
            except:
                pass
            if emit : Sys.cli_emit_progress(97)


    @Log()
    def prepare_mproc_encode(self, fp, nproc):
        """"""
        if not Sys.is_cli_cancel():
            self.mproc_fsize = []
            fsize  = Sys.getsize(fp)
            chsize = (fsize//nproc)+1
            if fsize % chsize == 0 : chsize -= 1

            hlstPaths = []
            with Io.rfile(fp) as fi :
                for pdata, part in Io.read_in_chunks(fi, chsize):
                    self.mproc_fsize.append(len(pdata))
                    Io.set_data(self.KMP_FILE+'_'+str(Sys.getpid())+'_'+str(part), pdata, True)
                    hlstPaths.append(self.KMP_FILE+'enc_'+str(Sys.getpid())+'_'+str(part))
            return hlstPaths


    @Log()
    def mproc_encode_part(self, id, event=None, emit=True):
        """"""
        if not Sys.is_cli_cancel():
            mpfile, mpfilenc = self.KMP_FILE+'_'+str(Sys.g.MAIN_PROC)+'_'+str(id), self.KMP_FILE+'enc_'+str(Sys.g.MAIN_PROC)+'_'+str(id)
            self.encryptToFile(mpfile, mpfilenc, self.getSubStartIndice(id), event, emit=emit)
            Sys.removeFile(mpfile)


    @Log()
    def encrypt_mproc(self, fp, tp, nproc=1, emit=True):
        """"""
        if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
        Sys.ptask('Encrypting data')
        d = Sys.datetime.now()
        c = not Sys.is_cli_cancel()
        if c:
            if nproc == 1 :
                self.encryptToFile(fp, tp)
                if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
                Sys.pstep('Encrypt data', d, c)
            else :
                hlstPaths = self.prepare_mproc_encode(fp, nproc)
                mg        = Manager(self.mproc_encode_part, nproc, None, Sys.g.MPEVENT)
                mg.run()
                self.mpMergeFiles(hlstPaths, tp, emit=emit)
                if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
                Sys.pstep('Encrypt data (multiproc)', d, c)
            if emit : Sys.cli_emit_progress(70)


    @Log()
    def encrypt(self, fromPath, toPath, nproc=1, header=None, emit=True):
        """"""
        if emit : Sys.cli_emit_progress(0)
        if not Sys.is_cli_cancel():
            fp, tp, rmode, mmode, compend = self.encrypt_sp_start(fromPath, toPath, header, emit=True)
            self.encrypt_mproc(fp, tp, nproc, emit=True)
            fp, tp = tp, self.tmpPath2 if tp == self.tmpPath1 else self.tmpPath1
            self.encrypt_sp_end(fp, tp, toPath, rmode, mmode, compend, emit=True)
        if emit : Sys.cli_emit_progress(100)


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # DECRYPT # #

    @Log()
    def decrypt_sp_start(self, fromPath, toPath, emit=True):
        """"""
        if not Sys.is_cli_cancel():
            if Sys.getsize(fromPath) > 0 :
                self.tmpPath1 = self.DIR_TEMP + Sys.basename(fromPath) + '.tmp'
                self.tmpPath2 = self.DIR_TEMP + Sys.basename(fromPath) + '.tmp2'
                fsize = Sys.getsize(fromPath)
                fsize -= self.kh.POS_END
                with Io.rfile(fromPath) as f :
                    d = Sys.datetime.now()
                    if emit : Sys.cli_emit_progress(1)
                    decHeader = self.kh.readHeader(f.read(self.kh.POS_END))
                    if emit : Sys.cli_emit_progress(2)
                    #~ print(decHeader)
                    if len(decHeader) > 0 :
                        if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
                        if decHeader['smode'] == self.mark[fsize%len(self.mark)] :
                            Sys.pstep('Reading Header', d, True)
                        else :
                            Sys.pstep('Reading Header', d, False, False, False)
                            raise BadKeyException('wrong key')

                    compend, compstart = not decHeader['cmode']== KirmahHeader.COMP_NONE, decHeader['cmode']== KirmahHeader.COMP_ALL
                    fp, tp             = fromPath, self.tmpPath1

                    if emit : Sys.cli_emit_progress(3)
                    if compend :
                        d = Sys.datetime.now()
                        if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
                        Sys.ptask('Uncompressing data')
                    self.uncompress_end(fp, tp, compend, emit=emit)
                    if emit : Sys.cli_emit_progress(10)
                    if compend :
                        if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
                        Sys.pstep('Compression mode', d, True)
                    fp, tp = tp, self.tmpPath2 if tp == self.tmpPath1 else self.tmpPath1


                    if decHeader['mmode'] :
                        d = Sys.datetime.now()
                        if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
                        Sys.ptask('Sorting data')
                        self.unmixdata(fp, tp, emit=emit)
                        fp, tp = tp, self.tmpPath2 if tp == self.tmpPath1 else self.tmpPath1
                    if emit : Sys.cli_emit_progress(20)
                    if decHeader['rmode'] :
                        d = Sys.datetime.now()
                        if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
                        Sys.ptask('Reordering data')
                        self.unRandomFileContent(fp, tp, emit=emit)
                        fp, tp = tp, self.tmpPath2 if tp == self.tmpPath1 else self.tmpPath1
                    if emit : Sys.cli_emit_progress(25)
                    return fp, tp, compstart


    @Log()
    def decrypt_sp_end(self, fromPath, toPath, compstart, emit=True):
        """"""
        if not Sys.is_cli_cancel():
            d = Sys.datetime.now()
            if emit : Sys.cli_emit_progress(80)
            if compstart :
                if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
                Sys.ptask('Uncompressing data')
            self.uncompress_start(fromPath, toPath, compstart, emit=emit)
            if emit : Sys.cli_emit_progress(90)
            if compstart:
                if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
                Sys.pstep('Compression mode', d, True)

            if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
            Sys.ptask('Cleaning')
            if emit : Sys.cli_emit_progress(95)
            try :
                Sys.removeFile(self.tmpPath1)
                Sys.removeFile(self.tmpPath2)
            except:
                pass
            if emit : Sys.cli_emit_progress(97)


    @Log()
    def decrypt_mproc(self, fromPath, toPath, nproc=1, emit=True):
        """"""
        if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
        Sys.ptask('Decrypting data')
        d = Sys.datetime.now()
        c = not Sys.is_cli_cancel()
        if c:
            if emit : Sys.cli_emit_progress(30)
            if nproc == 1 :
                self.decryptToFile(fromPath, toPath)
                if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
                Sys.pstep('Decrypt data', d, True)
            else :
                hlstPaths = self.prepare_mproc_decode(fromPath, nproc)
                mg        = Manager(self.mproc_decode_part, nproc, None, Sys.g.MPEVENT, emit=True)
                mg.run()
                self.mpMergeFiles(hlstPaths, toPath, emit=emit)
                if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
                Sys.pstep('Decrypt data (multiproc)', d, True)



    @Log()
    def prepare_mproc_decode(self, fp, nproc):
        """"""
        if not Sys.is_cli_cancel():
            self.mproc_fsize = []
            fsize  = Sys.getsize(fp)
            chsize = (fsize//nproc)+1
            if fsize % chsize == 0 : chsize -= 1

            hlstPaths = []
            with Io.rfile(fp) as fi :
                content = ''
                for pdata, part in Io.read_in_chunks(fi, chsize, True):
                    content = Io.str(pdata)
                    self.mproc_fsize.append(len(content))
                    Io.set_data(self.KMP_FILE+'_'+str(Sys.getpid())+'_'+str(part), content)
                    hlstPaths.append(self.KMP_FILE+'dec_'+str(Sys.getpid())+'_'+str(part))

            return hlstPaths


    @Log()
    def mproc_decode_part(self, id, event=None, emit=True):
        """"""
        if emit : Sys.cli_emit_progress(-1)
        if not Sys.is_cli_cancel():
            mpfile, mpfiledec = self.KMP_FILE+'_'+str(Sys.g.MAIN_PROC)+'_'+str(id), self.KMP_FILE+'dec_'+str(Sys.g.MAIN_PROC)+'_'+str(id)
            self.decryptToFile(mpfile, mpfiledec, self.getSubStartIndice(id), event, emit=emit)
            Sys.removeFile(mpfile)


    @Log()
    def decrypt(self, fromPath, toPath, nproc=1, emit=True):
        """"""
        Sys.cli_emit_progress(0)
        if not Sys.is_cli_cancel():
            fp, tp, compstart = self.decrypt_sp_start(fromPath, toPath, emit=emit)
            self.decrypt_mproc(fp, tp, nproc, emit=emit)
            self.decrypt_sp_end(tp, toPath, compstart, emit=emit)

        Sys.cli_emit_progress(100)



    @Log(Const.LOG_DEBUG)
    def offuscate(self, data, index):
        """"""
        if not Sys.is_cli_cancel():
            adata, lim = [], len(data)
            for i, c in enumerate((self.mark2)[index:]) :
                if i >= lim : break
                d = ord(c) + data[i]
                adata.append(chr(d))
            return ''.join(adata)


    @Log(Const.LOG_DEBUG)
    def deoffuscate(self, adata, index):
        """"""
        if not Sys.is_cli_cancel():
            data, lim = [], len(adata)
            for i, c in enumerate((self.mark2)[index:]) :
                if i >= lim : break
                d = ord(adata[i]) - ord(c)
                data.append(d)
            return bytes(bytearray(data))


    @staticmethod
    @Log(Const.LOG_DEBUG)
    def getSizes(fromPath):
        #~ if not Sys.is_cli_cancel():
        fsize  = Sys.getsize(fromPath)
        s      = (22,44,122,444,1222,14444,52222,244444,522222,1444444)
        a      = (2,3,7,9,21,33,87,151,427)
        m, g   = 4000, 3
        chsize = None
        if fsize <= 22 :
            chsize = ceil(fsize/4)+1
        else :
            for i, v in enumerate(s[:-1]) :
                if fsize >= v and fsize < s[i+1]:
                    chsize = ceil(fsize/v)+a[i]
                    break
            if chsize is None :
                chsize = ceil(fsize/1444444)+739
        if chsize == 0 : chsize = 1
        while ceil(fsize/chsize) > 4000 :
            chsize *= 3
        return fsize, chsize, ceil(fsize/chsize)


    @staticmethod
    @Log()
    def getRandomListFromKey(key, size):
        """"""
        #~ if not Sys.is_cli_cancel():
        j, ok, lk, r, ho, hr, lv, hv, rev = 0, False, len(key), None, [], [], 0, size-1, False
        for i in range(size) :
            if j >= lk : j = 0
            r  = key[j]
            ok = r < size and not r in ho
            if not ok:
                r = hv if not rev else lv
                while r in ho :
                    r = r - 1 if not rev else r + 1
                    if r > size-1 : r = 0
                    elif r < 0 : r = size - 1
                if not rev : hv = r
                else : lv = r
                ok = not r in ho
            if ok : ho.append(r)
            j += 1
            rev = not rev
        return Kirmah.getSimulRandomList(ho, Kirmah.getSimulNumber(key, size//5 if not size//5==0 else size*2, size//10 if not size//10 ==0 else size))


    @staticmethod
    @Log(Const.LOG_DEBUG)
    def getSimulRandomList(lst, chsize):
        """"""
        #~ if not Sys.is_cli_cancel():
        return Kirmah._getSimulRandomList(list(reversed(Kirmah._getSimulRandomList(Kirmah._getSimulRandomList(lst, chsize), 4))),4)


    @staticmethod
    @Log(Const.LOG_PRIVATE)
    def _getSimulRandomList(lst, chsize):
        """"""
        #~ if not Sys.is_cli_cancel():
        size, rlst, pos = len(lst), [], 0
        if chsize > 0 :
            for i in range(chsize+1):
                for j in range(ceil(size/chsize)+1):
                    pos = j*chsize+i
                    if pos in lst and not lst[pos] in rlst:
                        rlst.append(lst[pos])
        else : rlst = lst
        return rlst


    @staticmethod
    @Log(Const.LOG_DEBUG)
    def getSimulNumber(key, lim, delta=12):
        """"""
        #~ if not Sys.is_cli_cancel():
        s = 0
        for c in key[::-1] :
            if represents_int(chr(c)): c = int(chr(c))
            if c > 2 and (lim-delta > c + s or c + s < lim + delta ) :
                s += c
        return s


    @Log(Const.LOG_DEBUG)
    def getSubStartIndice(self, idx):
        """"""
        return sum([ s for j, s in enumerate(self.mproc_fsize) if j < idx ])%len(self.key)



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ class Randomiz ~~

class Randomiz:
    """"""

    @Log(Const.LOG_BUILD)
    def __init__(self,count,chl=None):
        """"""
        if chl ==None : self.lst = list(range(0,count))
        else: self.lst = chl
        self.count = len(self.lst)


    @Log(Const.LOG_DEBUG)
    def new(self,count=None, chl=None):
        """"""
        if count : self.count = count
        self.__init__(self.count,chl)


    @Log(Const.LOG_NEVER)
    def get(self,single=True):
        """"""
        pos = choice(self.lst)
        if single: del self.lst[self.lst.index(pos)]
        return pos



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ class Noiser ~~

class Noiser:

    @Log(Const.LOG_BUILD)
    def __init__(self, key, part=0):
        """"""
        self.key  = key
        self.build(part)

    @Log(Const.LOG_DEBUG)
    def build(self, part, vord=22):
        """"""
        if not part < len(self.key)-1 : raise Exception('part exceed limit')
        else :
            self.part, v = part, vord
            v  = int(ceil((self.key[vord]+v)/4.20583))
            self.lns = abs(int(ceil(v/2))-self.key[self.part]+self.key[7])
            self.lne = abs(int(v-self.lns-self.key[self.part+2]-self.key[44]/2.1934))
            if self.lns < 24 : self.lns += 24
            if self.lne < 10 : self.lne += 10

    @Log(Const.LOG_DEBUG)
    def getNoise(self, l, b64encode=True, noBytes=False):
        """"""
        n = urandom(l)
        if b64encode : n = urlsafe_b64encode(n)
        if noBytes:
            n = str(n,'utf-8')
        return n[:l]



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ class BadKeyException ~~

class BadKeyException(BaseException):
    """"""
