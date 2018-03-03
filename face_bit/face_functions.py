# -*- coding: utf-8 -*-
import requests
from .models import face_info, user_info
import json

api_key = "3v-2xdVkQWyx3QhxjjHUtvf8MTl1z14D"
api_secret = "7z4dP7AKOzaiRxAeq5r5Y2Y9BUTPHefO"


def face_detect(up_file):
    payload = {
        'api_key': api_key,
        'api_secret': api_secret,
        'return_attributes': 'gender,age'
    }
    files = {'image_file': up_file}
    r = requests.post("https://api-cn.faceplusplus.com/facepp/v3/detect", params=payload, files=files)
    # print(up_file.name)
    # result = r.json()
    # print(json.dumps(result, ensure_ascii=False))
    # faces = result.get("faces")
    # face_token = ""
    # face_rectangle = ""
    # if faces is not None:
    #     for face in faces:
    #         face_token += (str(face.get("face_token")) + ",")
    #         face_rectangle += (str(face.get("face_rectangle").get("left")) + "," +
    #                            str(face.get("face_rectangle").get("top")) + "," +
    #                            str(face.get("face_rectangle").get("width")) + "," +
    #                            str(face.get("face_rectangle").get("height")) + "/")
    # all_info = json.dumps(result, ensure_ascii=False)
    # face = face_info.objects.create(filename=up_file.name, face_token=face_token,
    #                                 face_rectangle=face_rectangle, remark=str(all_info))
    # face.save()
    # return r.json()
    info = {}
    if r is not None:
        print(up_file.name)
        result = r.json()
        print(json.dumps(result, ensure_ascii=False))
        faces = result.get("faces")
        face_token = ""
        face_rectangle = ""
        if faces is not None:
            for face in faces:
                face_token += (str(face.get("face_token")) + ",")
                face_rectangle += (str(face.get("face_rectangle").get("left")) + "," +
                                   str(face.get("face_rectangle").get("top")) + "," +
                                   str(face.get("face_rectangle").get("width")) + "," +
                                   str(face.get("face_rectangle").get("height")) + "/")
        all_info = json.dumps(result, ensure_ascii=False)
        face = face_info.objects.create(filename=up_file.name, face_token=face_token,
                                        face_rectangle=face_rectangle, remark=str(all_info))
        face.save()
        return r.json()
    else:
        info['status'] = 'failed'
        info['error_message'] = '超过并发量'
        return json.dumps(info)


def face_create(username, user_tag):
    payload = {
        'api_key': api_key,
        'api_secret': api_secret,
        'display_name': username,
        'outer_id': username,
        'tags': user_tag
    }
    r = requests.post("https://api-cn.faceplusplus.com/facepp/v3/faceset/create", params=payload)
    info = {}
    if r is not None:
        result = r.json()
        print(json.dumps(result, ensure_ascii=False))
        error_message = result.get("error_message")
        if error_message is None:
            faceset_token = result.get("faceset_token")
            user = user_info.objects.get(username=username)
            user.faceset_token = faceset_token
            user.save()
            info['status'] = 'success'
        else:
            info['status'] = 'failed'
        return info
    else:
        info['status'] = 'failed'
        info['error_message'] = '超过并发量'
        return info


def face_add(username, face_token, label):
    payload1 = {
        'api_key': api_key,
        'api_secret': api_secret,
        'user_id': label,
        'face_token': face_token
    }
    r1 = requests.post("https://api-cn.faceplusplus.com/facepp/v3/face/setuserid", params=payload1)
    info = {}
    if r1 is not None:
        result1 = r1.json()
        print(json.dumps(result1, ensure_ascii=False))
        error_message1 = result1.get("error_message")
        if error_message1 is None:
            payload = {
                'api_key': api_key,
                'api_secret': api_secret,
                'outer_id': username,
                'face_tokens': face_token
            }
            r = requests.post("https://api-cn.faceplusplus.com/facepp/v3/faceset/addface", params=payload)
            result = r.json()
            print(json.dumps(result, ensure_ascii=False))
            error_message = result.get("error_message")
            if error_message is None:
                info['status'] = 'success'
            else:
                info['status'] = 'failed'
                info['error_message'] = error_message
        return info
    else:
        info['status'] = 'failed'
        info['error_message'] = '超过并发量'
        return info


def delete_face(outer_id, delete_face_token):
    payload = {
        'api_key': api_key,
        'api_secret': api_secret,
        'outer_id': outer_id,
        'face_tokens': delete_face_token
    }
    r = requests.post("https://api-cn.faceplusplus.com/facepp/v3/faceset/removeface", params=payload)
    result = r.json()
    print(json.dumps(result, ensure_ascii=False))


def face_serach(username, face_token):
    payload = {
        'api_key': api_key,
        'api_secret': api_secret,
        'outer_id': username,
        'face_token': face_token
    }
    r = requests.post("https://api-cn.faceplusplus.com/facepp/v3/search", params=payload)
    info = {}
    if r is not None:
        result = r.json()
        print(json.dumps(result, ensure_ascii=False))
        error_message = result.get("error_message")
        if error_message is None:
            results = result.get("results")
            name = ""
            confidence = 0
            for res in results:
                if res.get("confidence") > confidence:
                    confidence = res.get("confidence")
                    name = res.get("user_id")
            if confidence > 80:
                info['name'] = name
            else:
                info['name'] = "unknow"
            info['status'] = 'success'
        else:
            info['status'] = 'failed'
            info['error_message'] = error_message
        return info
    else:
        info['status'] = 'failed'
        info['error_message'] = '超过并发量'
        return info




