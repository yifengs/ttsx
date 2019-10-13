from django.core.files.storage import Storage  # 导入storage工具类
from fdfs_client.client import Fdfs_client  # 客户端上传的类
from django.conf import settings  # 导入django配置

class FDFSStorage(Storage):  # 创建上传类继承Storage类
    '''fast dfs文件存储类'''
    def __init__(self, client_conf=None, base_url=None):
        if client_conf is None:
            self.client_conf = settings.FDFS_CLIENT_CONF
        if base_url is None:
            self.base_url = settings.FDFS_URL

    def _open(self, name, mode='rb'):  # 必须要有的方法
        '''打开文件时使用'''
        pass

    def _save(self, name, content):  # 必须要有的方法
        '''存储文件时使用'''
        # name: 你选择上传的文件的名字
        # content:参数必须为django.core.files.File或者File子类的实例 即：包含你上传文件内容的file类的对象

        # 创建一个Fdfd_client对象
        client = Fdfs_client(self.client_conf)
        # 上传文件到fast dfs系统中
        # upload_by_buffer() 根据文件内容上传文件
        res = client.upload_by_buffer(content.read())  # 返回的是一个字典格式
        # dict
        # {
        #     'Group name': group_name,
        #     'Remote file_id': remote_file_id,
        #     'Status': 'Upload successed.',
        #     'Local file name': '',
        #     'Uploaded size': upload_size,
        #     'Storage IP': storage_ip
        # }
        # print(res)
        if res.get('Status') != 'Upload successed.':  # res.get()获取字典里的内容
            # 上传失败 抛出异常
            raise Exception('上传文件到fdfs失败')
        # 获取文件id
        filename = res.get('Remote file_id')
        # 返回文件id
        return filename
    def exists(self, name):  # 调用_save()前会先调用exists()方法
        '''django判断文件名是否可用'''
        return False;  # False表示没有这个文件名 该文件名可用

    def url(self, name):  # 如果没有这个 在admin显示详情的时候会报url()的错
        '''返回文件url路径'''
        return self.base_url+name