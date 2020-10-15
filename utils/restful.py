# restful 它指的就是 接口的风格
#http 或者 https 协议
#http://api.qfedu.com/users
#http://www.qfedu.com/api/users

#返回值  json  不使用xml


# url 链接中 只能有名词 不能出现动词 复数 + s
#比如获取文章列表
#http://api.qfedu.com/articles
# http://api.qfedu.com/get_article  动词 不被允许

# 请求方法  数据库增删改查
# GET  相当于从数据库中查数据 从服务器获取资源
#POST                  添加   创建一个资源
#PUT      全量             修改   更新资源如果你有10个字段 修改其中两个 你也要把这个10个字段全部提交过来
#PATCH    增量           修改  如果你有10个字段 修改其中两个 只需要把这两个提交过来即可
#DELETE                 删除   从服务器删除数据

# GET  /users/  获取所有的用户
# GET  /user/id/   根据id获取指定的用户
#POST  /user/    添加一个用户
#PUT   /user/id  更新某个id用户的信息 提供所有的信息
#PATCH  /user/id  更新某个id用户的信息 提供需要更新的信息
#DELETE /user/id  删除制定的用户



#状态码

# 200 ok
# 301  永久重定向
#302 临时重定向

# 4 开头的肯定是客户端问题
# 400 参数错误 导致服务器并没有根据需求执行相关的操作
# 401 用户没有权限
# 403 因为某些原因进制访问
# 405 请求方法不被允许
# 404  发送请求的url 不存在

# 5  开头的肯定是 服务器的问题
# 500 肯定你的代码有问题 大部分语法问题
# 502 上线的时候遇到这样的问题 两个服务都需要启动 如果某一个没有启动 那么会报502的错误

"""
{"code":400,"message":"","data":""}

"""
from django.http import JsonResponse
class HttpCode(object):
    success = 200
    paramserror = 400
    unauth = 401
    methoderror = 405
    servererror = 500

# 根据不同的状态码返回不同的内容  这些方法定义一个统一的返回模板

def result(code=HttpCode.success,message='',data=None,kwargs=None):
    json_dict = {'code':code,'message':message,'data':data}

    if kwargs and isinstance(kwargs,dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict)

def success():
    return result()

def params_error(message='',data=None): #这个message等于空 是为了在不同的视图函数中 手动指定返回内容
    return result(code=HttpCode.paramserror,message=message,data=data)

def unauth(message='',data=None): #这个message等于空 是为了在不同的视图函数中 手动指定返回内容
    return result(code=HttpCode.unauth,message=message,data=data)
def method_error(message='',data=None): #这个message等于空 是为了在不同的视图函数中 手动指定返回内容
    return result(code=HttpCode.methoderror,message=message,data=data)

def server_error(message='',data=None): #这个message等于空 是为了在不同的视图函数中 手动指定返回内容
    return result(code=HttpCode.servererror,message=message,data=data)
