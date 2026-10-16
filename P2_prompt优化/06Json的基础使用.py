import json

# 1.其他转Json

d = {
    "name":"王迪",
    "age":25,
    "gender":"女"
}

s = json.dumps(d, ensure_ascii=False)
#注意：json转换后的字符串是双引号，不是单引号

print(s)

l = [
    {
        "name":"王迪",
        "age":25,
        "gender":"女"
    },
    {
        "name":"任俊璋",
        "age":25,
        "gender":"男"
    },
    {
        "name":"XXX",
        "age":30,
        "gender":"未知"
    }
]

print(json.dumps(l, ensure_ascii=False))

# 2.Json转其他

Json_str = '{"name": "王迪", "age": 25, "gender": "女"}'
Json_array_str = '[{"name": "王迪", "age": 25, "gender": "女"}, {"name": "任俊璋", "age": 25, "gender": "男"}, {"name": "XXX", "age": 30, "gender": "未知"}]'

res_dict = json.loads(Json_str)
print(res_dict, type(res_dict))

res_list = json.loads(Json_array_str)
print(res_list, type(res_list))