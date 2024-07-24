"""
Quick script to measure the FPS of the cameras when recording from their per frame JSON files.

marvel-fov-10_time_02_45_08_date_23_06_2024_ (1).json -> 8.2 FPS
marvel-fov-9_time_02_44_10_date_23_06_2024_ (1).json -> 7.84 FPS
marvel-fov-7_time_02_43_51_date_23_06_2024_.json -> 7.61 FPS


"""
import json
from datetime import datetime

# marvel-fov-10_time_02_45_08_date_23_06_2024_.json
# data = """
# {"timestamp": "2024-06-23 04:01:31,336", "level": "INFO", "message": "{'frame': 704}"}
# {"timestamp": "2024-06-23 04:01:31,456", "level": "INFO", "message": "{'frame': 705}"}
# {"timestamp": "2024-06-23 04:01:31,578", "level": "INFO", "message": "{'frame': 706}"}
# {"timestamp": "2024-06-23 04:01:31,701", "level": "INFO", "message": "{'frame': 707}"}
# {"timestamp": "2024-06-23 04:01:31,823", "level": "INFO", "message": "{'frame': 708}"}
# {"timestamp": "2024-06-23 04:01:31,943", "level": "INFO", "message": "{'frame': 709}"}
# {"timestamp": "2024-06-23 04:01:32,066", "level": "INFO", "message": "{'frame': 710}"}
# {"timestamp": "2024-06-23 04:01:32,190", "level": "INFO", "message": "{'frame': 711}"}
# {"timestamp": "2024-06-23 04:01:32,312", "level": "INFO", "message": "{'frame': 712}"}
# {"timestamp": "2024-06-23 04:01:32,431", "level": "INFO", "message": "{'frame': 713}"}
# {"timestamp": "2024-06-23 04:01:32,554", "level": "INFO", "message": "{'frame': 714}"}
# {"timestamp": "2024-06-23 04:01:32,676", "level": "INFO", "message": "{'frame': 715}"}
# {"timestamp": "2024-06-23 04:01:32,798", "level": "INFO", "message": "{'frame': 716}"}
# {"timestamp": "2024-06-23 04:01:32,919", "level": "INFO", "message": "{'frame': 717}"}
# {"timestamp": "2024-06-23 04:01:33,042", "level": "INFO", "message": "{'frame': 718}"}
# {"timestamp": "2024-06-23 04:01:33,165", "level": "INFO", "message": "{'frame': 719}"}
# {"timestamp": "2024-06-23 04:01:33,287", "level": "INFO", "message": "{'frame': 720}"}
# {"timestamp": "2024-06-23 04:01:33,408", "level": "INFO", "message": "{'frame': 721}"}
# {"timestamp": "2024-06-23 04:01:33,529", "level": "INFO", "message": "{'frame': 722}"}
# {"timestamp": "2024-06-23 04:01:33,652", "level": "INFO", "message": "{'frame': 723}"}
# {"timestamp": "2024-06-23 04:01:33,774", "level": "INFO", "message": "{'frame': 724}"}
# {"timestamp": "2024-06-23 04:01:33,896", "level": "INFO", "message": "{'frame': 725}"}
# {"timestamp": "2024-06-23 04:01:34,018", "level": "INFO", "message": "{'frame': 726}"}
# {"timestamp": "2024-06-23 04:01:34,142", "level": "INFO", "message": "{'frame': 727}"}
# {"timestamp": "2024-06-23 04:01:34,265", "level": "INFO", "message": "{'frame': 728}"}
# {"timestamp": "2024-06-23 04:01:34,386", "level": "INFO", "message": "{'frame': 729}"}
# {"timestamp": "2024-06-23 04:01:34,506", "level": "INFO", "message": "{'frame': 730}"}
# {"timestamp": "2024-06-23 04:01:34,629", "level": "INFO", "message": "{'frame': 731}"}
# {"timestamp": "2024-06-23 04:01:34,751", "level": "INFO", "message": "{'frame': 732}"}
# {"timestamp": "2024-06-23 04:01:34,872", "level": "INFO", "message": "{'frame': 733}"}
# {"timestamp": "2024-06-23 04:01:34,994", "level": "INFO", "message": "{'frame': 734}"}
# {"timestamp": "2024-06-23 04:01:35,118", "level": "INFO", "message": "{'frame': 735}"}
# {"timestamp": "2024-06-23 04:01:35,240", "level": "INFO", "message": "{'frame': 736}"}
# {"timestamp": "2024-06-23 04:01:35,361", "level": "INFO", "message": "{'frame': 737}"}
# {"timestamp": "2024-06-23 04:01:35,482", "level": "INFO", "message": "{'frame': 738}"}
# {"timestamp": "2024-06-23 04:01:35,604", "level": "INFO", "message": "{'frame': 739}"}
# {"timestamp": "2024-06-23 04:01:35,727", "level": "INFO", "message": "{'frame': 740}"}
# {"timestamp": "2024-06-23 04:01:35,848", "level": "INFO", "message": "{'frame': 741}"}
# {"timestamp": "2024-06-23 04:01:35,970", "level": "INFO", "message": "{'frame': 742}"}
# {"timestamp": "2024-06-23 04:01:36,093", "level": "INFO", "message": "{'frame': 743}"}
# {"timestamp": "2024-06-23 04:01:36,216", "level": "INFO", "message": "{'frame': 744}"}
# {"timestamp": "2024-06-23 04:01:36,337", "level": "INFO", "message": "{'frame': 745}"}
# {"timestamp": "2024-06-23 04:01:36,457", "level": "INFO", "message": "{'frame': 746}"}
# {"timestamp": "2024-06-23 04:01:36,580", "level": "INFO", "message": "{'frame': 747}"}
# {"timestamp": "2024-06-23 04:01:36,702", "level": "INFO", "message": "{'frame': 748}"}
# {"timestamp": "2024-06-23 04:01:36,824", "level": "INFO", "message": "{'frame': 749}"}
# {"timestamp": "2024-06-23 04:01:36,945", "level": "INFO", "message": "{'frame': 750}"}
# {"timestamp": "2024-06-23 04:01:37,068", "level": "INFO", "message": "{'frame': 751}"}
# {"timestamp": "2024-06-23 04:01:37,192", "level": "INFO", "message": "{'frame': 752}"}
# {"timestamp": "2024-06-23 04:01:37,313", "level": "INFO", "message": "{'frame': 753}"}
# {"timestamp": "2024-06-23 04:01:37,432", "level": "INFO", "message": "{'frame': 754}"}
# {"timestamp": "2024-06-23 04:01:37,555", "level": "INFO", "message": "{'frame': 755}"}
# {"timestamp": "2024-06-23 04:01:37,678", "level": "INFO", "message": "{'frame': 756}"}
# {"timestamp": "2024-06-23 04:01:37,799", "level": "INFO", "message": "{'frame': 757}"}
# {"timestamp": "2024-06-23 04:01:37,920", "level": "INFO", "message": "{'frame': 758}"}
# {"timestamp": "2024-06-23 04:01:38,043", "level": "INFO", "message": "{'frame': 759}"}
# {"timestamp": "2024-06-23 04:01:38,166", "level": "INFO", "message": "{'frame': 760}"}
# {"timestamp": "2024-06-23 04:01:38,288", "level": "INFO", "message": "{'frame': 761}"}
# {"timestamp": "2024-06-23 04:01:38,407", "level": "INFO", "message": "{'frame': 762}"}
# {"timestamp": "2024-06-23 04:01:38,529", "level": "INFO", "message": "{'frame': 763}"}
# {"timestamp": "2024-06-23 04:01:38,652", "level": "INFO", "message": "{'frame': 764}"}
# {"timestamp": "2024-06-23 04:01:38,774", "level": "INFO", "message": "{'frame': 765}"}
# {"timestamp": "2024-06-23 04:01:38,895", "level": "INFO", "message": "{'frame': 766}"}
# """
# marvel-fov-9_time_02_44_10_date_23_06_2024_.json
# data = """
# {"timestamp": "2024-06-23 04:04:57,724", "level": "INFO", "message": "{'frame': 2277}"}
# {"timestamp": "2024-06-23 04:04:57,850", "level": "INFO", "message": "{'frame': 2278}"}
# {"timestamp": "2024-06-23 04:04:57,975", "level": "INFO", "message": "{'frame': 2279}"}
# {"timestamp": "2024-06-23 04:04:58,101", "level": "INFO", "message": "{'frame': 2280}"}
# {"timestamp": "2024-06-23 04:04:58,227", "level": "INFO", "message": "{'frame': 2281}"}
# {"timestamp": "2024-06-23 04:04:58,352", "level": "INFO", "message": "{'frame': 2282}"}
# {"timestamp": "2024-06-23 04:04:58,478", "level": "INFO", "message": "{'frame': 2283}"}
# {"timestamp": "2024-06-23 04:04:58,604", "level": "INFO", "message": "{'frame': 2284}"}
# {"timestamp": "2024-06-23 04:04:58,729", "level": "INFO", "message": "{'frame': 2285}"}
# {"timestamp": "2024-06-23 04:04:58,855", "level": "INFO", "message": "{'frame': 2286}"}
# {"timestamp": "2024-06-23 04:04:58,980", "level": "INFO", "message": "{'frame': 2287}"}
# {"timestamp": "2024-06-23 04:04:59,106", "level": "INFO", "message": "{'frame': 2288}"}
# {"timestamp": "2024-06-23 04:04:59,232", "level": "INFO", "message": "{'frame': 2289}"}
# {"timestamp": "2024-06-23 04:04:59,358", "level": "INFO", "message": "{'frame': 2290}"}
# {"timestamp": "2024-06-23 04:04:59,483", "level": "INFO", "message": "{'frame': 2291}"}
# {"timestamp": "2024-06-23 04:04:59,609", "level": "INFO", "message": "{'frame': 2292}"}
# {"timestamp": "2024-06-23 04:04:59,734", "level": "INFO", "message": "{'frame': 2293}"}
# {"timestamp": "2024-06-23 04:04:59,860", "level": "INFO", "message": "{'frame': 2294}"}
# {"timestamp": "2024-06-23 04:04:59,986", "level": "INFO", "message": "{'frame': 2295}"}
# {"timestamp": "2024-06-23 04:05:00,112", "level": "INFO", "message": "{'frame': 2296}"}
# {"timestamp": "2024-06-23 04:05:00,238", "level": "INFO", "message": "{'frame': 2297}"}
# {"timestamp": "2024-06-23 04:05:00,363", "level": "INFO", "message": "{'frame': 2298}"}
# {"timestamp": "2024-06-23 04:05:00,489", "level": "INFO", "message": "{'frame': 2299}"}
# {"timestamp": "2024-06-23 04:05:00,615", "level": "INFO", "message": "{'frame': 2300}"}
# {"timestamp": "2024-06-23 04:05:00,740", "level": "INFO", "message": "{'frame': 2301}"}
# {"timestamp": "2024-06-23 04:05:00,866", "level": "INFO", "message": "{'frame': 2302}"}
# {"timestamp": "2024-06-23 04:05:00,992", "level": "INFO", "message": "{'frame': 2303}"}
# {"timestamp": "2024-06-23 04:05:01,117", "level": "INFO", "message": "{'frame': 2304}"}
# {"timestamp": "2024-06-23 04:05:01,382", "level": "INFO", "message": "{'frame': 2305}"}
# {"timestamp": "2024-06-23 04:05:01,507", "level": "INFO", "message": "{'frame': 2306}"}
# {"timestamp": "2024-06-23 04:05:01,633", "level": "INFO", "message": "{'frame': 2307}"}
# {"timestamp": "2024-06-23 04:05:01,759", "level": "INFO", "message": "{'frame': 2308}"}
# {"timestamp": "2024-06-23 04:05:01,884", "level": "INFO", "message": "{'frame': 2309}"}
# {"timestamp": "2024-06-23 04:05:02,010", "level": "INFO", "message": "{'frame': 2310}"}
# {"timestamp": "2024-06-23 04:05:02,136", "level": "INFO", "message": "{'frame': 2311}"}
# {"timestamp": "2024-06-23 04:05:02,261", "level": "INFO", "message": "{'frame': 2312}"}
# {"timestamp": "2024-06-23 04:05:02,387", "level": "INFO", "message": "{'frame': 2313}"}
# {"timestamp": "2024-06-23 04:05:02,513", "level": "INFO", "message": "{'frame': 2314}"}
# {"timestamp": "2024-06-23 04:05:02,639", "level": "INFO", "message": "{'frame': 2315}"}
# {"timestamp": "2024-06-23 04:05:02,764", "level": "INFO", "message": "{'frame': 2316}"}
# {"timestamp": "2024-06-23 04:05:02,890", "level": "INFO", "message": "{'frame': 2317}"}
# {"timestamp": "2024-06-23 04:05:03,016", "level": "INFO", "message": "{'frame': 2318}"}
# {"timestamp": "2024-06-23 04:05:03,141", "level": "INFO", "message": "{'frame': 2319}"}
# {"timestamp": "2024-06-23 04:05:03,267", "level": "INFO", "message": "{'frame': 2320}"}
# {"timestamp": "2024-06-23 04:05:03,392", "level": "INFO", "message": "{'frame': 2321}"}
# {"timestamp": "2024-06-23 04:05:03,518", "level": "INFO", "message": "{'frame': 2322}"}
# {"timestamp": "2024-06-23 04:05:03,644", "level": "INFO", "message": "{'frame': 2323}"}
# {"timestamp": "2024-06-23 04:05:03,770", "level": "INFO", "message": "{'frame': 2324}"}
# {"timestamp": "2024-06-23 04:05:03,895", "level": "INFO", "message": "{'frame': 2325}"}
# {"timestamp": "2024-06-23 04:05:04,021", "level": "INFO", "message": "{'frame': 2326}"}
# {"timestamp": "2024-06-23 04:05:04,146", "level": "INFO", "message": "{'frame': 2327}"}
# {"timestamp": "2024-06-23 04:05:04,272", "level": "INFO", "message": "{'frame': 2328}"}
# {"timestamp": "2024-06-23 04:05:04,398", "level": "INFO", "message": "{'frame': 2329}"}
# {"timestamp": "2024-06-23 04:05:04,523", "level": "INFO", "message": "{'frame': 2330}"}
# {"timestamp": "2024-06-23 04:05:04,649", "level": "INFO", "message": "{'frame': 2331}"}
# {"timestamp": "2024-06-23 04:05:04,775", "level": "INFO", "message": "{'frame': 2332}"}
# {"timestamp": "2024-06-23 04:05:04,900", "level": "INFO", "message": "{'frame': 2333}"}
# {"timestamp": "2024-06-23 04:05:05,027", "level": "INFO", "message": "{'frame': 2334}"}
# {"timestamp": "2024-06-23 04:05:05,152", "level": "INFO", "message": "{'frame': 2335}"}
# {"timestamp": "2024-06-23 04:05:05,278", "level": "INFO", "message": "{'frame': 2336}"}
# {"timestamp": "2024-06-23 04:05:05,403", "level": "INFO", "message": "{'frame': 2337}"}
# {"timestamp": "2024-06-23 04:05:05,529", "level": "INFO", "message": "{'frame': 2338}"}
# {"timestamp": "2024-06-23 04:05:05,654", "level": "INFO", "message": "{'frame': 2339}"}
# {"timestamp": "2024-06-23 04:05:05,780", "level": "INFO", "message": "{'frame': 2340}"}
# {"timestamp": "2024-06-23 04:05:05,906", "level": "INFO", "message": "{'frame': 2341}"}
# {"timestamp": "2024-06-23 04:05:06,031", "level": "INFO", "message": "{'frame': 2342}"}
# {"timestamp": "2024-06-23 04:05:06,157", "level": "INFO", "message": "{'frame': 2343}"}
# {"timestamp": "2024-06-23 04:05:06,283", "level": "INFO", "message": "{'frame': 2344}"}
# {"timestamp": "2024-06-23 04:05:06,409", "level": "INFO", "message": "{'frame': 2345}"}
# {"timestamp": "2024-06-23 04:05:06,534", "level": "INFO", "message": "{'frame': 2346}"}
# {"timestamp": "2024-06-23 04:05:06,660", "level": "INFO", "message": "{'frame': 2347}"}
# {"timestamp": "2024-06-23 04:05:06,785", "level": "INFO", "message": "{'frame': 2348}"}
# """

data = """
{"timestamp": "2024-06-23 04:02:31,015", "level": "INFO", "message": "{'frame': 1060}"}
{"timestamp": "2024-06-23 04:02:31,144", "level": "INFO", "message": "{'frame': 1061}"}
{"timestamp": "2024-06-23 04:02:31,274", "level": "INFO", "message": "{'frame': 1062}"}
{"timestamp": "2024-06-23 04:02:31,403", "level": "INFO", "message": "{'frame': 1063}"}
{"timestamp": "2024-06-23 04:02:31,532", "level": "INFO", "message": "{'frame': 1064}"}
{"timestamp": "2024-06-23 04:02:31,662", "level": "INFO", "message": "{'frame': 1065}"}
{"timestamp": "2024-06-23 04:02:31,791", "level": "INFO", "message": "{'frame': 1066}"}
{"timestamp": "2024-06-23 04:02:31,920", "level": "INFO", "message": "{'frame': 1067}"}
{"timestamp": "2024-06-23 04:02:32,050", "level": "INFO", "message": "{'frame': 1068}"}
{"timestamp": "2024-06-23 04:02:32,179", "level": "INFO", "message": "{'frame': 1069}"}
{"timestamp": "2024-06-23 04:02:32,308", "level": "INFO", "message": "{'frame': 1070}"}
{"timestamp": "2024-06-23 04:02:32,437", "level": "INFO", "message": "{'frame': 1071}"}
{"timestamp": "2024-06-23 04:02:32,567", "level": "INFO", "message": "{'frame': 1072}"}
{"timestamp": "2024-06-23 04:02:32,696", "level": "INFO", "message": "{'frame': 1073}"}
{"timestamp": "2024-06-23 04:02:32,825", "level": "INFO", "message": "{'frame': 1074}"}
{"timestamp": "2024-06-23 04:02:32,954", "level": "INFO", "message": "{'frame': 1075}"}
{"timestamp": "2024-06-23 04:02:33,084", "level": "INFO", "message": "{'frame': 1076}"}
{"timestamp": "2024-06-23 04:02:33,213", "level": "INFO", "message": "{'frame': 1077}"}
{"timestamp": "2024-06-23 04:02:33,343", "level": "INFO", "message": "{'frame': 1078}"}
{"timestamp": "2024-06-23 04:02:33,472", "level": "INFO", "message": "{'frame': 1079}"}
{"timestamp": "2024-06-23 04:02:33,602", "level": "INFO", "message": "{'frame': 1080}"}
{"timestamp": "2024-06-23 04:02:33,731", "level": "INFO", "message": "{'frame': 1081}"}
{"timestamp": "2024-06-23 04:02:33,860", "level": "INFO", "message": "{'frame': 1082}"}
{"timestamp": "2024-06-23 04:02:33,989", "level": "INFO", "message": "{'frame': 1083}"}
{"timestamp": "2024-06-23 04:02:34,118", "level": "INFO", "message": "{'frame': 1084}"}
{"timestamp": "2024-06-23 04:02:34,247", "level": "INFO", "message": "{'frame': 1085}"}
{"timestamp": "2024-06-23 04:02:34,377", "level": "INFO", "message": "{'frame': 1086}"}
{"timestamp": "2024-06-23 04:02:34,506", "level": "INFO", "message": "{'frame': 1087}"}
{"timestamp": "2024-06-23 04:02:34,635", "level": "INFO", "message": "{'frame': 1088}"}
{"timestamp": "2024-06-23 04:02:34,765", "level": "INFO", "message": "{'frame': 1089}"}
{"timestamp": "2024-06-23 04:02:34,894", "level": "INFO", "message": "{'frame': 1090}"}
{"timestamp": "2024-06-23 04:02:35,023", "level": "INFO", "message": "{'frame': 1091}"}
{"timestamp": "2024-06-23 04:02:35,152", "level": "INFO", "message": "{'frame': 1092}"}
{"timestamp": "2024-06-23 04:02:35,282", "level": "INFO", "message": "{'frame': 1093}"}
{"timestamp": "2024-06-23 04:02:35,411", "level": "INFO", "message": "{'frame': 1094}"}
{"timestamp": "2024-06-23 04:02:35,541", "level": "INFO", "message": "{'frame': 1095}"}
{"timestamp": "2024-06-23 04:02:35,671", "level": "INFO", "message": "{'frame': 1096}"}
{"timestamp": "2024-06-23 04:02:35,801", "level": "INFO", "message": "{'frame': 1097}"}
{"timestamp": "2024-06-23 04:02:35,931", "level": "INFO", "message": "{'frame': 1098}"}
{"timestamp": "2024-06-23 04:02:36,061", "level": "INFO", "message": "{'frame': 1099}"}
{"timestamp": "2024-06-23 04:02:36,190", "level": "INFO", "message": "{'frame': 1100}"}
{"timestamp": "2024-06-23 04:02:36,320", "level": "INFO", "message": "{'frame': 1101}"}
{"timestamp": "2024-06-23 04:02:36,450", "level": "INFO", "message": "{'frame': 1102}"}
{"timestamp": "2024-06-23 04:02:36,580", "level": "INFO", "message": "{'frame': 1103}"}
{"timestamp": "2024-06-23 04:02:36,710", "level": "INFO", "message": "{'frame': 1104}"}
{"timestamp": "2024-06-23 04:02:36,840", "level": "INFO", "message": "{'frame': 1105}"}
{"timestamp": "2024-06-23 04:02:36,969", "level": "INFO", "message": "{'frame': 1106}"}
{"timestamp": "2024-06-23 04:02:37,099", "level": "INFO", "message": "{'frame': 1107}"}
{"timestamp": "2024-06-23 04:02:37,229", "level": "INFO", "message": "{'frame': 1108}"}
{"timestamp": "2024-06-23 04:02:37,359", "level": "INFO", "message": "{'frame': 1109}"}
{"timestamp": "2024-06-23 04:02:37,489", "level": "INFO", "message": "{'frame': 1110}"}
{"timestamp": "2024-06-23 04:02:37,619", "level": "INFO", "message": "{'frame': 1111}"}
{"timestamp": "2024-06-23 04:02:37,748", "level": "INFO", "message": "{'frame': 1112}"}
{"timestamp": "2024-06-23 04:02:37,878", "level": "INFO", "message": "{'frame': 1113}"}
{"timestamp": "2024-06-23 04:02:38,008", "level": "INFO", "message": "{'frame': 1114}"}
{"timestamp": "2024-06-23 04:02:38,138", "level": "INFO", "message": "{'frame': 1115}"}
{"timestamp": "2024-06-23 04:02:38,268", "level": "INFO", "message": "{'frame': 1116}"}
{"timestamp": "2024-06-23 04:02:38,398", "level": "INFO", "message": "{'frame': 1117}"}
{"timestamp": "2024-06-23 04:02:38,527", "level": "INFO", "message": "{'frame': 1118}"}
{"timestamp": "2024-06-23 04:02:38,657", "level": "INFO", "message": "{'frame': 1119}"}
{"timestamp": "2024-06-23 04:02:38,787", "level": "INFO", "message": "{'frame': 1120}"}
{"timestamp": "2024-06-23 04:02:38,917", "level": "INFO", "message": "{'frame': 1121}"}
{"timestamp": "2024-06-23 04:02:39,047", "level": "INFO", "message": "{'frame': 1122}"}
{"timestamp": "2024-06-23 04:02:39,177", "level": "INFO", "message": "{'frame': 1123}"}
{"timestamp": "2024-06-23 04:02:39,306", "level": "INFO", "message": "{'frame': 1124}"}
{"timestamp": "2024-06-23 04:02:39,436", "level": "INFO", "message": "{'frame': 1125}"}
{"timestamp": "2024-06-23 04:02:39,566", "level": "INFO", "message": "{'frame': 1126}"}
{"timestamp": "2024-06-23 04:02:39,696", "level": "INFO", "message": "{'frame': 1127}"}
{"timestamp": "2024-06-23 04:02:39,827", "level": "INFO", "message": "{'frame': 1128}"}
{"timestamp": "2024-06-23 04:02:39,957", "level": "INFO", "message": "{'frame': 1129}"}
{"timestamp": "2024-06-23 04:02:40,086", "level": "INFO", "message": "{'frame': 1130}"}
{"timestamp": "2024-06-23 04:02:40,216", "level": "INFO", "message": "{'frame': 1131}"}
{"timestamp": "2024-06-23 04:02:40,346", "level": "INFO", "message": "{'frame': 1132}"}
{"timestamp": "2024-06-23 04:02:40,476", "level": "INFO", "message": "{'frame': 1133}"}
{"timestamp": "2024-06-23 04:02:40,606", "level": "INFO", "message": "{'frame': 1134}"}
{"timestamp": "2024-06-23 04:02:40,735", "level": "INFO", "message": "{'frame': 1135}"}
{"timestamp": "2024-06-23 04:02:41,004", "level": "INFO", "message": "{'frame': 1136}"}
{"timestamp": "2024-06-23 04:02:41,133", "level": "INFO", "message": "{'frame': 1137}"}
{"timestamp": "2024-06-23 04:02:41,263", "level": "INFO", "message": "{'frame': 1138}"}
{"timestamp": "2024-06-23 04:02:41,393", "level": "INFO", "message": "{'frame': 1139}"}
{"timestamp": "2024-06-23 04:02:41,523", "level": "INFO", "message": "{'frame': 1140}"}
{"timestamp": "2024-06-23 04:02:41,652", "level": "INFO", "message": "{'frame': 1141}"}
{"timestamp": "2024-06-23 04:02:41,782", "level": "INFO", "message": "{'frame': 1142}"}
{"timestamp": "2024-06-23 04:02:41,912", "level": "INFO", "message": "{'frame': 1143}"}
{"timestamp": "2024-06-23 04:02:42,041", "level": "INFO", "message": "{'frame': 1144}"}
{"timestamp": "2024-06-23 04:02:42,171", "level": "INFO", "message": "{'frame': 1145}"}
{"timestamp": "2024-06-23 04:02:42,301", "level": "INFO", "message": "{'frame': 1146}"}
{"timestamp": "2024-06-23 04:02:42,431", "level": "INFO", "message": "{'frame': 1147}"}
{"timestamp": "2024-06-23 04:02:42,561", "level": "INFO", "message": "{'frame': 1148}"}
{"timestamp": "2024-06-23 04:02:42,690", "level": "INFO", "message": "{'frame': 1149}"}
{"timestamp": "2024-06-23 04:02:42,820", "level": "INFO", "message": "{'frame': 1150}"}
{"timestamp": "2024-06-23 04:02:42,949", "level": "INFO", "message": "{'frame': 1151}"}
{"timestamp": "2024-06-23 04:02:43,079", "level": "INFO", "message": "{'frame': 1152}"}
{"timestamp": "2024-06-23 04:02:43,209", "level": "INFO", "message": "{'frame': 1153}"}
{"timestamp": "2024-06-23 04:02:43,339", "level": "INFO", "message": "{'frame': 1154}"}
{"timestamp": "2024-06-23 04:02:43,468", "level": "INFO", "message": "{'frame': 1155}"}
{"timestamp": "2024-06-23 04:02:43,598", "level": "INFO", "message": "{'frame': 1156}"}
{"timestamp": "2024-06-23 04:02:43,728", "level": "INFO", "message": "{'frame': 1157}"}
{"timestamp": "2024-06-23 04:02:43,858", "level": "INFO", "message": "{'frame': 1158}"}
{"timestamp": "2024-06-23 04:02:43,987", "level": "INFO", "message": "{'frame': 1159}"}
{"timestamp": "2024-06-23 04:02:44,117", "level": "INFO", "message": "{'frame': 1160}"}
{"timestamp": "2024-06-23 04:02:44,247", "level": "INFO", "message": "{'frame': 1161}"}
{"timestamp": "2024-06-23 04:02:44,376", "level": "INFO", "message": "{'frame': 1162}"}
{"timestamp": "2024-06-23 04:02:44,506", "level": "INFO", "message": "{'frame': 1163}"}
{"timestamp": "2024-06-23 04:02:44,636", "level": "INFO", "message": "{'frame': 1164}"}
{"timestamp": "2024-06-23 04:02:44,765", "level": "INFO", "message": "{'frame': 1165}"}
{"timestamp": "2024-06-23 04:02:44,895", "level": "INFO", "message": "{'frame': 1166}"}
{"timestamp": "2024-06-23 04:02:45,025", "level": "INFO", "message": "{'frame': 1167}"}
{"timestamp": "2024-06-23 04:02:45,154", "level": "INFO", "message": "{'frame': 1168}"}
{"timestamp": "2024-06-23 04:02:45,284", "level": "INFO", "message": "{'frame': 1169}"}
{"timestamp": "2024-06-23 04:02:45,414", "level": "INFO", "message": "{'frame': 1170}"}
{"timestamp": "2024-06-23 04:02:45,543", "level": "INFO", "message": "{'frame': 1171}"}
{"timestamp": "2024-06-23 04:02:45,673", "level": "INFO", "message": "{'frame': 1172}"}
{"timestamp": "2024-06-23 04:02:45,803", "level": "INFO", "message": "{'frame': 1173}"}
{"timestamp": "2024-06-23 04:02:46,073", "level": "INFO", "message": "{'frame': 1174}"}
{"timestamp": "2024-06-23 04:02:46,204", "level": "INFO", "message": "{'frame': 1175}"}
{"timestamp": "2024-06-23 04:02:46,333", "level": "INFO", "message": "{'frame': 1176}"}
{"timestamp": "2024-06-23 04:02:46,463", "level": "INFO", "message": "{'frame': 1177}"}
{"timestamp": "2024-06-23 04:02:46,593", "level": "INFO", "message": "{'frame': 1178}"}
{"timestamp": "2024-06-23 04:02:46,722", "level": "INFO", "message": "{'frame': 1179}"}
{"timestamp": "2024-06-23 04:02:46,852", "level": "INFO", "message": "{'frame': 1180}"}
{"timestamp": "2024-06-23 04:02:46,981", "level": "INFO", "message": "{'frame': 1181}"}
{"timestamp": "2024-06-23 04:02:47,111", "level": "INFO", "message": "{'frame': 1182}"}
{"timestamp": "2024-06-23 04:02:47,240", "level": "INFO", "message": "{'frame': 1183}"}
{"timestamp": "2024-06-23 04:02:47,370", "level": "INFO", "message": "{'frame': 1184}"}
{"timestamp": "2024-06-23 04:02:47,500", "level": "INFO", "message": "{'frame': 1185}"}
{"timestamp": "2024-06-23 04:02:47,629", "level": "INFO", "message": "{'frame': 1186}"}
{"timestamp": "2024-06-23 04:02:47,759", "level": "INFO", "message": "{'frame': 1187}"}
{"timestamp": "2024-06-23 04:02:47,888", "level": "INFO", "message": "{'frame': 1188}"}
{"timestamp": "2024-06-23 04:02:48,018", "level": "INFO", "message": "{'frame': 1189}"}
{"timestamp": "2024-06-23 04:02:48,148", "level": "INFO", "message": "{'frame': 1190}"}
{"timestamp": "2024-06-23 04:02:48,278", "level": "INFO", "message": "{'frame': 1191}"}
{"timestamp": "2024-06-23 04:02:48,407", "level": "INFO", "message": "{'frame': 1192}"}
{"timestamp": "2024-06-23 04:02:48,537", "level": "INFO", "message": "{'frame': 1193}"}
{"timestamp": "2024-06-23 04:02:48,666", "level": "INFO", "message": "{'frame': 1194}"}
{"timestamp": "2024-06-23 04:02:48,796", "level": "INFO", "message": "{'frame': 1195}"}
{"timestamp": "2024-06-23 04:02:48,925", "level": "INFO", "message": "{'frame': 1196}"}
{"timestamp": "2024-06-23 04:02:49,055", "level": "INFO", "message": "{'frame': 1197}"}
{"timestamp": "2024-06-23 04:02:49,185", "level": "INFO", "message": "{'frame': 1198}"}
{"timestamp": "2024-06-23 04:02:49,315", "level": "INFO", "message": "{'frame': 1199}"}
{"timestamp": "2024-06-23 04:02:49,444", "level": "INFO", "message": "{'frame': 1200}"}
{"timestamp": "2024-06-23 04:02:49,574", "level": "INFO", "message": "{'frame': 1201}"}
{"timestamp": "2024-06-23 04:02:49,703", "level": "INFO", "message": "{'frame': 1202}"}
{"timestamp": "2024-06-23 04:02:49,833", "level": "INFO", "message": "{'frame': 1203}"}
{"timestamp": "2024-06-23 04:02:49,962", "level": "INFO", "message": "{'frame': 1204}"}
{"timestamp": "2024-06-23 04:02:50,092", "level": "INFO", "message": "{'frame': 1205}"}
{"timestamp": "2024-06-23 04:02:50,222", "level": "INFO", "message": "{'frame': 1206}"}
{"timestamp": "2024-06-23 04:02:50,351", "level": "INFO", "message": "{'frame': 1207}"}
{"timestamp": "2024-06-23 04:02:50,481", "level": "INFO", "message": "{'frame': 1208}"}
{"timestamp": "2024-06-23 04:02:50,610", "level": "INFO", "message": "{'frame': 1209}"}
{"timestamp": "2024-06-23 04:02:50,740", "level": "INFO", "message": "{'frame': 1210}"}
{"timestamp": "2024-06-23 04:02:50,870", "level": "INFO", "message": "{'frame': 1211}"}
{"timestamp": "2024-06-23 04:02:50,999", "level": "INFO", "message": "{'frame': 1212}"}
"""


def calculate_fps(data):
    lines = data.strip().split('\n')
    timestamps = []

    for line in lines:
        try:
            entry = json.loads(line)
            timestamp = entry['timestamp']
            timestamps.append(datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S,%f"))
        except (json.JSONDecodeError, KeyError):
            print(f"Skipping invalid line: {line}")

    if len(timestamps) < 2:
        print("Not enough valid timestamps to calculate FPS.")
        return None

    total_time = (timestamps[-1] - timestamps[0]).total_seconds()
    total_frames = len(timestamps)

    fps = (total_frames - 1) / total_time
    return fps




fps = calculate_fps(data)
if fps is not None:
    print(f"Calculated FPS: {fps:.2f}")