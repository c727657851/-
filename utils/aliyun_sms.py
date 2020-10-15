from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
client = AcsClient('LTAI4GCuTM6zEebNqbCwkcX2', '3ZaY0vC6qki6o8Sif3FJ0FXUMrpyOv', 'cn-hangzhou')


def send_sms(phone, code):
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')


    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone)
    request.add_query_param('SignName', "xfz项目")
    request.add_query_param('TemplateCode', "SMS_197895383")
    request.add_query_param('TemplateParam', "{\"code\":\"%s\"}" % code)

    response = client.do_action(request)
    print(str(response, encoding='utf-8'))
