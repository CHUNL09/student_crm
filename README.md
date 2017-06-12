1. django admin: admin/admin123
2. 使用admin用户登录后可以操作，系统中已经存在其他用户，密码统一为admin123
3. 如果要添加新用户，需要使用django admin portal添加好后才能在CRM portal添加，后续会改进。
4. 对于各个表的增，删，改，查基本实现，后续会进一步改进！
5. 增加Userprofile页面分页功能
6. 增加部分字段高亮显示
7. 增加Statics，提供更加具体每天课程查询当天学生学习记录的页面
8. 增加权限
角色以及权限如下：
admin,consultant以及teacher在group表中定义
管理员(admin) ---全portal---全部权限
顾问老师(consultant) -- 操作(不能删除)customer和consult 记录
讲师(teacher) -- 操作(不能删除)classlist,courserecords，studyrecord,和Statics

目前的粒度还不够细，后续会继续细分（比如某个讲师只能更改自己所有的记录。。）

