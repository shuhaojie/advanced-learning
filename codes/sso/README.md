## SSO流程

app1登录

1. 用户访问(app1或者app2)根目录请求
2. 根目录根据请求中的cookie来拿到sessionId 
3. 如果验证通过, 读出session中的username，返回登录成功页面
4. 如果拿不到sessionId，用户未登录。或者拿到的sessionId，但是验证未通过，用户也未通过。
5. 如果未通过验证，需要跳转到sso判断是否其他系统已登录，如果其他系统已登录，跳转到登录成功页面。如果其他系统未登录，跳转到/login。
6. 用户输入用户名、密码，sso来判断用户名密码是否正确
7. 如果正确，sso将登录状态写入到session，并写入到sso的cookie，并携带service ticket跳转到app1的/confirm请求
8. app1的/confirm，发送请求到sso，来判断service ticket是否有效
9. 如果有效，confirm中写入session，写入cookie，并跳转到根目录

app2登录

1. 用户访问(app1或者app2)根目录请求
2. 此时session为空，用户没有登录
3. 跳转到sso登录页面，sso根据cookie来判断用户已登录，并携带service ticket跳转到app2的/confirm请求
4. app2的/confirm，发送请求到sso，来判断service ticket是否有效
5. 如果有效，confirm中写入session，写入cookie，并跳转到根目录

app1退出

1. 用户在登录状态时，会有退出按钮
2. 用户点击退出登录，先删除自己的cookie和session，然后跳转到sso的退出页面
3. sso删除cookie，session，并跳转到app1的首页

app2退出