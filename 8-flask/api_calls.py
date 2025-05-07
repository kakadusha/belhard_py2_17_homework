"""
API calls to a FastAPI application (backend)

{"openapi":"3.1.0","info":{"title":"FastAPI","version":"0.1.0"},"paths":{"/api":{"get":{"tags":["api"],"summary":"Index","operationId":"index_api_get","responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}}}}},"/":{"get":{"tags":["api"],"summary":"Index","operationId":"index__get","responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}}}}},"/api/users":{"get":{"tags":["Пользователи"],"summary":"Get Users","operationId":"get_users_api_users_get","responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"type":"array","items":{"$ref":"#/components/schemas/DataClassUserGet"},"title":"Response Get Users Api Users Get"}}}}}},"post":{"tags":["Пользователи"],"summary":"Post User","operationId":"post_user_api_users_post","parameters":[{"name":"name","in":"query","required":true,"schema":{"type":"string","title":"Name"}},{"name":"age","in":"query","required":true,"schema":{"type":"integer","title":"Age"}},{"name":"phone","in":"query","required":false,"schema":{"anyOf":[{"type":"string"},{"type":"null"}],"title":"Phone"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/DataClassUserId"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/users/{id}":{"get":{"tags":["Пользователи"],"summary":"Get User","operationId":"get_user_api_users__id__get","parameters":[{"name":"id","in":"path","required":true,"schema":{"title":"Id"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/DataClassUserGet"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/gallery":{"get":{"tags":["Галерея"],"summary":"Get Galleries","operationId":"get_galleries_api_gallery_get","responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"type":"array","items":{"$ref":"#/components/schemas/DataClassGalleryList"},"title":"Response Get Galleries Api Gallery Get"}}}}}},"post":{"tags":["Галерея"],"summary":"Post Gallery","operationId":"post_gallery_api_gallery_post","parameters":[{"name":"name","in":"query","required":true,"schema":{"type":"string","title":"Name"}},{"name":"user_id","in":"query","required":true,"schema":{"type":"integer","title":"User Id"}},{"name":"desc","in":"query","required":false,"schema":{"anyOf":[{"type":"string"},{"type":"null"}],"title":"Desc"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/DataClassGalleryGet"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/gallery/{gallery_id}":{"get":{"tags":["Галерея"],"summary":"Get Gallery","operationId":"get_gallery_api_gallery__gallery_id__get","parameters":[{"name":"gallery_id","in":"path","required":true,"schema":{"type":"integer","title":"Gallery Id"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}},"delete":{"tags":["Галерея"],"summary":"Delete Gallery","operationId":"delete_gallery_api_gallery__gallery_id__delete","parameters":[{"name":"gallery_id","in":"path","required":true,"schema":{"type":"integer","title":"Gallery Id"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/gallery/{gallery_id}/paintings":{"get":{"tags":["Галерея"],"summary":"Get Gallery With Paintings","operationId":"get_gallery_with_paintings_api_gallery__gallery_id__paintings_get","parameters":[{"name":"gallery_id","in":"path","required":true,"schema":{"type":"integer","title":"Gallery Id"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/gallery/{gallery_id}/painting/{painting_id}":{"put":{"tags":["Галерея"],"summary":"Put Gallery Painting","operationId":"put_gallery_painting_api_gallery__gallery_id__painting__painting_id__put","parameters":[{"name":"gallery_id","in":"path","required":true,"schema":{"type":"integer","title":"Gallery Id"}},{"name":"painting_id","in":"path","required":true,"schema":{"type":"integer","title":"Painting Id"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/painting":{"get":{"tags":["Картина"],"summary":"Get Paintings","operationId":"get_paintings_api_painting_get","responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"type":"array","items":{"$ref":"#/components/schemas/DataClassPaintingGet"},"title":"Response Get Paintings Api Painting Get"}}}}}},"post":{"tags":["Картина"],"summary":"Add Painting","operationId":"add_painting_api_painting_post","parameters":[{"name":"name","in":"query","required":true,"schema":{"type":"string","title":"Name"}},{"name":"image","in":"query","required":true,"schema":{"type":"string","title":"Image"}},{"name":"size","in":"query","required":true,"schema":{"type":"string","title":"Size"}},{"name":"material","in":"query","required":true,"schema":{"type":"string","title":"Material"}},{"name":"technique","in":"query","required":true,"schema":{"type":"string","title":"Technique"}},{"name":"desc","in":"query","required":true,"schema":{"type":"string","title":"Desc"}},{"name":"price","in":"query","required":true,"schema":{"type":"string","title":"Price"}},{"name":"status","in":"query","required":false,"schema":{"anyOf":[{"type":"string"},{"type":"null"}],"title":"Status"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/DataClassPaintingGet"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/painting/{id}":{"get":{"tags":["Картина"],"summary":"Get Painting","operationId":"get_painting_api_painting__id__get","parameters":[{"name":"id","in":"path","required":true,"schema":{"title":"Id"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/DataClassPaintingGet"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}},"delete":{"tags":["Картина"],"summary":"Delete Painting","operationId":"delete_painting_api_painting__id__delete","parameters":[{"name":"id","in":"path","required":true,"schema":{"type":"integer","title":"Id"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}}},"components":{"schemas":{"DataClassGalleryGet":{"properties":{"name":{"type":"string","title":"Name"},"user_id":{"type":"integer","title":"User Id"},"desc":{"anyOf":[{"type":"string"},{"type":"null"}],"title":"Desc"},"id":{"type":"integer","title":"Id"},"paintings":{"anyOf":[{"items":{"type":"integer"},"type":"array"},{"type":"null"}],"title":"Paintings"}},"type":"object","required":["name","user_id","id"],"title":"DataClassGalleryGet"},"DataClassGalleryList":{"properties":{"name":{"type":"string","title":"Name"},"user_id":{"type":"integer","title":"User Id"},"desc":{"anyOf":[{"type":"string"},{"type":"null"}],"title":"Desc"},"id":{"type":"integer","title":"Id"}},"type":"object","required":["name","user_id","id"],"title":"DataClassGalleryList"},"DataClassPaintingGet":{"properties":{"name":{"type":"string","title":"Name"},"image":{"type":"string","title":"Image"},"size":{"type":"string","title":"Size"},"material":{"type":"string","title":"Material"},"technique":{"type":"string","title":"Technique"},"desc":{"type":"string","title":"Desc"},"price":{"type":"string","title":"Price"},"status":{"anyOf":[{"type":"string"},{"type":"null"}],"title":"Status"},"id":{"type":"integer","title":"Id"}},"type":"object","required":["name","image","size","material","technique","desc","price","id"],"title":"DataClassPaintingGet"},"DataClassUserGet":{"properties":{"name":{"type":"string","title":"Name"},"age":{"type":"integer","title":"Age"},"phone":{"anyOf":[{"type":"string"},{"type":"null"}],"title":"Phone"},"id":{"type":"integer","title":"Id"}},"type":"object","required":["name","age","id"],"title":"DataClassUserGet"},"DataClassUserId":{"properties":{"id":{"type":"integer","title":"Id"}},"type":"object","required":["id"],"title":"DataClassUserId"},"HTTPValidationError":{"properties":{"detail":{"items":{"$ref":"#/components/schemas/ValidationError"},"type":"array","title":"Detail"}},"type":"object","title":"HTTPValidationError"},"ValidationError":{"properties":{"loc":{"items":{"anyOf":[{"type":"string"},{"type":"integer"}]},"type":"array","title":"Location"},"msg":{"type":"string","title":"Message"},"type":{"type":"string","title":"Error Type"}},"type":"object","required":["loc","msg","type"],"title":"ValidationError"}}}}
"""

import requests


API_URL = "http://localhost:8200/api"


def api_get_gallery(gallery_id):
    response = requests.get(f"{API_URL}/gallery/{gallery_id}")
    if response.status_code == 200:
        return response.json()
    return None


def api_get_all_galleries():
    response = requests.get(f"{API_URL}/gallery")
    if response.status_code == 200:
        return response.json()
    return []


def api_add_gallery(name, user_id, desc=None):
    response = requests.post(
        f"{API_URL}/gallery",
        params={"name": name, "user_id": user_id, "desc": desc},
    )
    if response.status_code == 200:
        return response.json()
    return None


def api_delete_gallery(gallery_id):
    response = requests.delete(f"{API_URL}/gallery/{gallery_id}")
    if response.status_code == 200:
        return response.json()
    return None


def api_get_paintings_by_gallery_id(gallery_id):
    response = requests.get(f"{API_URL}/gallery/{gallery_id}/paintings")
    if response.status_code == 200:
        return response.json().get("paintings", [])
    return []


def api_add_painting(name, gallery_id, image, size, material, technique, desc, price):
    response = requests.post(
        f"{API_URL}/painting",
        params={
            "name": name,
            "gallery_id": gallery_id,
            "image": image,
            "size": size,
            "material": material,
            "technique": technique,
            "desc": desc,
            "price": price,
        },
    )
    if response.status_code == 200:
        return response.json()
    return None


def api_get_painting(id):
    response = requests.get(f"{API_URL}/painting/{id}")
    if response.status_code == 200:
        return response.json()
    return None


def api_delete_painting(id):
    response = requests.delete(f"{API_URL}/painting/{id}")
    if response.status_code == 200:
        return response.json()
    return None


def api_update_painting(id, name, image, size, material, technique, desc, price):
    response = requests.put(
        f"{API_URL}/painting/{id}",
        params={
            "name": name,
            "image": image,
            "size": size,
            "material": material,
            "technique": technique,
            "desc": desc,
            "price": price,
        },
    )
    if response.status_code == 200:
        return response.json()
    return None


def api_get_all_paintings():
    response = requests.get(f"{API_URL}/painting")
    if response.status_code == 200:
        return response.json()
    return []


def api_add_painting_to_gallery(gallery_id, painting_id):
    response = requests.put(f"{API_URL}/gallery/{gallery_id}/painting/{painting_id}")
    if response.status_code == 200:
        return response.json()
    return None


def api_delete_painting_from_gallery(gallery_id, painting_id):
    response = requests.delete(f"{API_URL}/gallery/{gallery_id}/painting/{painting_id}")
    if response.status_code == 200:
        return response.json()
    return None
