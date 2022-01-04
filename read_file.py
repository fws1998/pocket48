import json
import psycopg2
import os


def photo_audio_video(timestamp, body, type, room):
    url = body["file"]["url"]
    custom = json.loads(body["custom"])
    userId = custom["user"]["userId"]
    name = custom["user"]["nickName"]
    if type == "audio":
        url = body["file"]["mp3Url"]
    sql = "INSERT INTO " + type + " VALUES (" + "to_timestamp(" + str(timestamp) + "), \'" + url + "\'," + str(
        userId) + ",\'" + name + "\'," + room + ")"
    try:
        # print(sql)
        cur.execute(sql)
        conn.commit()
    except psycopg2.errors.UniqueViolation as error:
        conn.rollback()


def normal_text_msg(time, body, room):
    if body["messageType"] != "DELETE" and body["messageType"] != "DISABLE_SPEAK":
        userId = body["user"]["userId"]
        name = body["user"]["nickName"]

        # body = json.loads(body)
        if userId in list:
            sql = ""
            if "replyName" in body:
                msg = body["text"]
                reply_to = body["replyName"]
                reply_text = body["replyText"]
                sql = "INSERT INTO reply VALUES (" + "to_timestamp(" + str(time) + "), \'" + msg + "\'," + str(
                    userId) + ",\'" + name + "\'," + room + ", \'" + reply_to + "\', \'" + reply_text + "\')"

            elif "liveCover" in body:
                title = body["liveTitle"]
                id = body["liveId"]
                path = body["shortPath"]

                sql = "INSERT INTO live VALUES (" + "to_timestamp(" + str(time) + "), \'" + title + "\'," + str(
                    userId) + ",\'" + name + "\'," + id + ", \'" + path + "\')"

            elif "giftInfo" in body:
                '''gift = body["giftInfo"]["giftName"]
                price = body["giftInfo"]["money"]
                accecpId = body["giftInfo"]["acceptUserId"]
                acceptName= body["giftInfo"]["acceptUserName"]'''

                # sql = "INSERT INTO idol_msg VALUES (" + "to_timestamp(" + str(time) + "), \'" + gift + "\',
                # " + userId + ",\'" + name + "\'," + room + ")"

            elif body["messageType"] == "EXPRESSIMAGE":
                msg = body["emotionRemote"]
                sql = "INSERT INTO idol_msg VALUES (" + "to_timestamp(" + str(time) + "), \'" + msg + "\'," + str(
                    userId) + ",\'" + name + "\'," + room + ")"

            else:
                msg = body["text"]
                sql = "INSERT INTO idol_msg VALUES (" + "to_timestamp(" + str(time) + "), \'" + msg + "\'," + str(
                    userId) + ",\'" + name + "\'," + room + ")"

            try:
                if sql != "":
                    # print(sql)
                    cur.execute(sql)
                    conn.commit()
            except psycopg2.errors.UniqueViolation as error:
                conn.rollback()


def flipcard(time, body):
    question = body["question"]
    reply = body["answer"]
    userId = body["user"]["userId"]
    name = body["user"]["nickName"]
    if "url" in reply:
        reply = json.loads(reply)
        reply = reply["url"]
        # print(reply)
    sql = "INSERT INTO flipcard VALUES (" + "to_timestamp(" + str(
        time) + "), \'" + question + "\', \'" + reply + "\'," + str(
        userId) + ",\'" + name + "\'" + ")"
    try:
        # print(sql)
        cur.execute(sql)
        conn.commit()
    except psycopg2.errors.UniqueViolation as error:
        conn.rollback()


if __name__ == '__main__':
    list = [1, 4, 5, 6, 8, 9, 11, 12, 17, 18, 19, 20, 21, 24, 25, 27, 28, 33, 34, 35, 36, 38, 39, 40, 46, 47, 49, 63,
            68, 2508, 5562, 5564, 5566, 5574, 5973, 6429, 6431, 6734, 6735, 6737, 6738, 6739, 6742, 6743, 6744, 6745,
            6746, 9073, 49003, 49005, 63548, 63554, 63555, 63558, 63559, 63560, 63561, 63562, 63564, 63566, 63567,
            63571, 63572, 63573, 63574, 63576, 63577, 63580, 63581, 63582, 286973, 286976, 286977, 286979, 286983,
            327558, 327560, 327561, 327563, 327566, 327567, 327568, 327569, 327571, 327572, 327574, 327575, 327577,
            327579, 327580, 327581, 327587, 327594, 327595, 327596, 327597, 327598, 327601, 327602, 327682, 327683,
            399631, 399652, 399654, 399662, 399667, 399669, 399672, 399674, 407106, 407108, 407110, 407121, 407126,
            407127, 407130, 417311, 417320, 417321, 417324, 417325, 417326, 417329, 417330, 417331, 417336, 419966,
            458335, 459989, 459991, 459997, 459999, 460004, 460005, 460933, 480675, 480680, 526172, 528329, 528335,
            528336, 528337, 528340, 529287, 530383, 530385, 530388, 530390, 530431, 530433, 530439, 530440, 530447,
            530452, 538697, 538735, 593820, 594002, 594003, 601302, 607507, 607511, 607513, 607515, 607521, 607523,
            607524, 607591, 609002, 610042, 614528, 614727, 614728, 614731, 614733, 614734, 614735, 614739, 614741,
            614742, 614750, 614753, 614755, 614756, 614761, 614773, 614776, 618319, 623828, 624121, 654707, 677395,
            677397, 677398, 677400, 677403, 677404, 679448, 679455, 679462, 679464, 679466, 707365, 707369, 707371,
            707372, 707374, 711726, 711732, 711735, 711741, 711746, 722778, 722780, 722781, 722784, 825969, 831078,
            844544, 844552, 846528, 867888, 867891, 867892, 867895, 867896, 868351, 868352, 869171, 874497, 874500,
            874505, 874508, 874512, 874693, 874696, 874701, 874723, 881190, 39911921, 39911923, 42402741, 42402769,
            42402792, 42402830, 42402868, 42402886, 42402897, 42402908, 42402920, 45285669, 45285672, 45285674,
            45285677, 45285682, 45285685, 45285691, 45285698, 45285702, 52494482, 52494487, 52494490, 54526093,
            54526095, 54526097, 54526098, 54526100, 54526102, 57737429, 57737430, 57737478, 58785983, 64422010,
            64422016, 64487703, 64487705, 64487708, 4344250371, 4344250372, 4344250373, 4344250374, 4528799751,
            4998561802, 5384437777, 5602541574, 6827278356, 6827278357, 6827278358, 7984906291, 8957984817, 8957984818,
            8957984819, 9276751976, 9276751977, 9276751978, 34306]
    room_list = ['67313770', '67313820', '67265391', '67207828', '67322480', '67313805', '67246085', '67313812',
                 '67256337', '67284386', '67333101', '67303256', '67217577', '67217583', '67236607', '67284410',
                 '67313730', '67199574', '67189770', '67313807', '67275458', '67199568', '67217571', '67352247',
                 '67352253', '67390892', '67217584', '67236601', '67207827', '67265436', '67246064', '67207810',
                 '67236636', '67217613', '67207881', '67313732', '67207851', '67265437', '67275459', '67275431',
                 '67352254', '67199596', '67390943', '67207831', '67333093', '67333066', '67265403', '67236685',
                 '67362239', '67265421', '67246060', '67333062', '67265467', '67313743', '67362289', '67284424',
                 '67333084', '67284411', '67199572', '67322491', '67265451', '67313745', '67370548', '67256348',
                 '67303260', '67352300', '67293879', '67246084', '67313837', '67303248', '67284398', '67265468',
                 '67390920', '67313734', '67199599', '67217562', '67236638', '67370538', '67189785', '67199579',
                 '67342026', '67246058', '67217596', '67333045', '67189767', '67380527', '67256340', '67380556',
                 '67275416', '67236634', '67236584', '67293874', '67313825', '67293899', '67342074', '67362271',
                 '67246081', '67207817', '67199580', '67207875', '67380600', '67265389', '67352304', '67275445',
                 '67342039', '67236589', '67275447', '67313798', '67313751', '67333041', '67313801', '67303252',
                 '67303246', '67217598', '67380550', '67370544', '67370540', '67390893', '67313737', '67293873',
                 '67199602', '67217582', '67352296', '67390950', '67342057', '67265449', '67370547', '67207862',
                 '67275488', '67189812', '67303271', '67189813', '67390969', '67275492', '67189818', '67265495',
                 '114030785', '67256375', '67303279', '67265498', '67207870', '67275503', '67207877', '67333146',
                 '67246100', '67189830', '67189834', '67362328', '67303296', '67380603', '67362340', '67313885',
                 '67303290', '67265514', '67293956', '67370575', '67207898', '67236667', '67380608', '67199629',
                 '67313899', '67333149', '67313897', '67390990', '67370588', '67236669', '67342126', '67352339',
                 '67342150', '67293973', '67275528', '67362351', '67390996', '67333166', '67246114', '67333162',
                 '67342133', '67342135', '67380616', '67236674', '67390997', '67236680', '67303313', '67256384',
                 '67199643', '67256391', '67390993', '67284477', '67275536', '67390999', '67333170', '67391008',
                 '67199656', '67189874', '67284484', '67370606', '67275553', '67293986', '67370603', '67303319',
                 '67275543', '67265535', '67380647', '67391014', '67265540', '67352359', '345764122', '67189871',
                 '67207923', '67275548', '67275547', '67207922', '67265541', '67284489', '67342180', '67352360',
                 '67303325', '67275559', '67303327', '67189881', '67293999', '67256412', '67322562', '67275562',
                 '67236697', '67189884', '67380657', '67284493', '67199663', '67342194', '67284494', '67352370',
                 '67207933', '147264238', '67362378', '67380660', '67391027', '67391028', '67256413', '224665866',
                 '224670690', '248619173', '248621211', '248610452', '248613346', '248602943', '248604670', '370409322',
                 '248619104', '248621117', '261502235', '261490803', '261489758', '261495713', '261502245', '261498409',
                 '261507061', '261489779', '261504207', '381012316', '387989946', '387989957', '377992915', '377987247',
                 '377982661', '377979685', '377983628', '377988067', '396390530', '396394228', '396399552', '402672067',
                 '442998267', '442997428', '443004994', '442998283', '443003991', '147283635', '147269132', '170000713',
                 '144655472', '143189214', '154058194', '157010991', '159822189', '155345469', '155333671', '155329896',
                 '180129550', '181393187', '181380525', '181396030', '187441914', '187441935', '187430892']
    conn = psycopg2.connect(database="postgres", user="postgres", password="fws7609922", host="localhost", port="5432")
    print("Opened database successfully")

    cur = conn.cursor()
    for i in room_list:
        with os.popen("node c:\\nim-node-main\\src\\bin\\hist.js " + i) as p:
            r = p.read()
        try:
            with open("test.json", 'r', encoding='UTF-8') as file:
                msg_info = json.load(file)
            for i in msg_info:
                room = i["chatroomId"]
                time_stamp = i["time"] / 1000
                msg_type = i["type"]
                body = json.loads(i["custom"])
                # print(body)
                if msg_type == "image" or msg_type == "video" or msg_type == "audio":
                    photo_audio_video(time_stamp, i, msg_type, room)
                elif msg_type == "text" and i["text"] == "偶像翻牌":
                    flipcard(time_stamp, body)
                else:
                    normal_text_msg(time_stamp, body, room)
        except FileNotFoundError as error:
            print(error)

    conn.close()
