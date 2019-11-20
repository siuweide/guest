from django.test import TestCase
from django.contrib.auth.models import User

from sign.models import Event,Guest

# Create your tests here.
class ModelTest(TestCase):

    def setUp(self):
        Event.objects.create(name='锤子发布会', limit=100, status=True,
                             address='shenzhen', start_time='2019-12-01 14:00:00')
        Guest.objects.create(event_id=4, realname='alen',
                             phone='18888888888',email='alen163.com',sign=False)

    def test_event_models(self):
        result = Event.objects.get(name='锤子发布会')
        self.assertEqual(result.address, 'shenzhen')
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(realname='alen')
        self.assertEqual(result.realname, 'alen')
        self.assertFalse(result.sign)


class LoginActionTest(TestCase):
    '''测试登录动作'''

    def setUp(self):
        User.objects.create(username='admin', password='admin123456', email='admin@163.com')

    def test_add_admin(self):
        '''测试添加的用户'''
        user = User.objects.get(username='admin')
        self.assertEqual(user.username,'admin')
        self.assertEqual(user.email,'admin@163.com')

    def test_login_action_username_password_null(self):
        '''用户名或密码为空'''
        test_data = {'username':'','password':''}
        response = self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username or password error!', response.content)

    def test_login_action_username_password_error(self):
        '''用户名或密码错误'''
        test_data = {'username':'admin','password':'123456'}
        response = self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username or password error!', response.content)

    def test_login_action_success(self):
        '''登录成功'''
        test_data = {'username':'admin','password':'admin123456'}
        response = self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code, 302)


class EventMangeTest(TestCase):
    ''' 发布会管理 '''

    def setUp(self):
        User.objects.create_user('admin', 'admin163.com', 'admin123456')
        Event.objects.create(name='xiaomi5',limit=100,address='shenzhen',status=1,start_time='2019-11-20 14:00:00')

        self.login_user = {'username':'admin','password':'admin123456'}

    def test_event_manage_success(self):
        ''' 测试发布会:xiaomi5  '''
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/project/event_manage/')
        response_content = response.content
        response_content = str(response_content,encoding='utf-8')  # 把bytes的格式转化为str
        print(type(response_content))
        # self.assertEqual(response.status_code, 200)
        response1 = Event.objects.get(name='xiaomi5')
        self.assertEqual('xiaomi5' ,response1.name)
        self.assertIn('shenzhen' ,response_content)

    def test_event_manage_sreach_success(self):
        ''' 测试发布会搜索 '''
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/project/search_event_name/',{'name':'xiaomi5'})
        response_content = str(response.content,encoding='utf-8')  # 把bytes的格式转化为str
        self.assertEqual(response.status_code, 200)
        self.assertIn('xiaomi5',response_content)
        self.assertIn('shenzhen',response_content)


class SignIndexActionTest(TestCase):
    ''' 发布会签到 '''

    def setUp(self):
        User.objects.create_user('admin', 'admin163.com', 'admin123456')
        Event.objects.create(id=1, name='xiaomi5',limit=100,address='shenzhen',status=1,start_time='2019-11-20 14:00:00')
        Event.objects.create(id=2, name='iphone12',limit=100,address='guangzhou',status=1,start_time='2019-11-20 14:00:00')

        Guest.objects.create(realname='huashao',phone=13888888810,email='huashao@163.com',sign=False,event_id=1)
        Guest.objects.create(realname='xiaoming',phone=13888888811,email='xiaoming@163.com',sign=True,event_id=2)

        self.login_user = {'username':'admin','password':'admin123456'}

    def test_sign_index_action_phone_null(self):
        ''' 手机号为空 '''
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/project/sign_index_action/1/', {'phone':''})
        response_content = str(response.content,encoding='utf-8')  # 把bytes的格式转化为str
        self.assertEqual(response.status_code, 200)
        self.assertIn('phone error',response_content)

    def test_sign_index_action_phone_or_event_id_error(self):
        ''' 手机号或发布会id错误 '''
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/project/sign_index_action/2/', {'phone':'13888888810'})
        response_content = str(response.content,encoding='utf-8')  # 把bytes的格式转化为str
        self.assertEqual(response.status_code, 200)
        self.assertIn('event_id or phone error',response_content)

    def test_sign_index_action_sign_is_exist(self):
        ''' 该手机号已签到 '''
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/project/sign_index_action/2/', {'phone':'13888888811'})
        response_content = str(response.content,encoding='utf-8')  # 把bytes的格式转化为str
        self.assertEqual(response.status_code, 200)
        self.assertIn('user has sign in',response_content)

    def test_sign_index_action_login_success(self):
        ''' 签到成功 '''
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/project/sign_index_action/1/', {'phone':'13888888810'})
        response_content = str(response.content,encoding='utf-8')  # 把bytes的格式转化为str
        self.assertEqual(response.status_code, 200)
        self.assertIn('sign in success',response_content)
