from django.contrib.auth import authenticate
class UserShell:
    def __init__(self,sys_argv):
        self.sys_argv=sys_argv
        self.user=None

    def auth(self):
        count=0
        while count <3:
            username=input('username:').strip()
            password=input('password:').strip()
            user=authenticate(username=username,password=password)
            #None 代表认证不成功
            #user object  ,认证对象 ,user.name取名称
            if not user:
                count+=1
                print('Invalid username or password false!')
            else:
                self.user=user
                return True
        else:
            print("too many attempts.")

    def start(self):

        if self.auth():
            while True:
                host_groups=self.user.account.host_groups.all()
                for index,group in enumerate(host_groups):
                    print("%s.\t%s[%s]"%(index,group,group.host_user_binds.count()))
                print("%s.\t未分组的主机[%s]"%(len(host_groups),self.user.account.host_user_binds.count()))
                choice=input('select group >>:').strip()
                if choice.isdigit():
                    choice=int(choice)
                    host_bind_list=None
                    if choice>=0 and choice<len(host_groups):
                        selected_group=host_groups[choice]
                        host_bind_list=selected_group.host_user_bind.all()
                    elif choice==len(host_groups):
                        host_bind_list=self.user.account.host_user_binds.all()
                    if host_bind_list:
                        while True:
                            for index,host in enumerate(host_bind_list):
                                print("%s.\t%s"%(index,host))
                            choice2=input('select host >>:').strip()
                            if choice2.isdigit():
                                choice2=int(choice2)
                                if choice2>=0and choice2<len(host_bind_list):
                                    selected_host=host_bind_list[choice2]
                                    print("selected_host is %s"%selected_host)
                            elif choice2 == "b":
                                break









