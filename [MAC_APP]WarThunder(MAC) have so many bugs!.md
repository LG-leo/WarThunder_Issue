"Since the forum moderators suspended my account for 'Dismissive attitude' and 'Spam' before I could post this, here is the complete list of 18 critical Mac OS bugs. Enjoy the 'real investment'."

----

MAC problem[1]cloudflare Warp 不能进行单独的DNS解析

war thunder BUG[2]war thunder不能使用中文输入法

```
根源在于 Gaijin 的 Dagor 引擎极其粗暴地劫持了键盘输入（Raw Input）。

    在 Windows 上，游戏引擎会调用系统的 WM_IME 消息来接管输入法候选框。但战雷的引擎底层只认“物理按键”（WASD 是绝对优先级的）。

    到了 Mac 上，情况更加灾难。macOS 处理输入法用的是极其封闭的 NSTextInputClient 协议。

    如果你在游戏里按了 Option（或者 Control + Space）想切中文，战雷的底层代码首先拦截了 Option 键，判定为：“哦！玩家按下了自由视角键（Free Look）！”于是你的鼠标/视角被锁死了。

    同时，它根本没有实现让系统输入法（IME）呼出候选框的接口。系统的输入法进程发现游戏界面拒绝接收文字输入，就把候选框默默收回去了。
```

MAC problem[3]更新系统后，程序无法运行

MAC problem+war thunder BUG[4]war thunder不能使用第三方输入法

MAC problem+war thunder BUG[5]war thunder按到option会动不了视角

MAC problem+war thunder BUG[6]war thunder按到->|(tab)会动不了视角

MAC problem+war thunder BUG[7]war thunder按到“中/英”会动不了视角

MAC problem+war thunder BUG[8]war thunder按到option之后按1遍option还不会转动视角，必须按2遍解锁

MAC problem+war thunder BUG[9]war thunder按到control会动不了视角，且不能按option解锁视角，必须按2遍control

MAC problem+war thunder BUG[10]war thunder没有按到option会动不了视角

MAC problem[11]程序会莫名其妙的损坏，哪怕里面的文件压根没有损坏

war thunder BUG[12] 本地会话文件莫名其妙的损坏或不可写（cache) 

war thunder BUG[13] 启动器和客户端的会话会莫名其妙的不同步

war thunder BUG[14] 会出现打完一局 -> 登陆界面 -> 进入游戏 -> 连接服务器 -> 点击 “匹配” -> 连接服务器 -> 登陆 -> 进入对局 -> 打完一局

war thunder BUG[15] CAS在某些情况下，能够在上一场CAS没结束的情况下，在2S内启动开启新一轮CAS，且其他人无法使用战斗机护航/截击

MAC problem [16]表现形式：甚至我都是复制过来的文件，都能莫名其妙出现一份能运行，另一份不能，还有一份被拦 ；具体原因：Finder 复制：可能保留或继承扩展属性，也可能加上新的 quarantine 标记。
  - cp / rsync：默认行为不同，cp 可能不保留 xattr，rsync -E 才保留。
  - 下载/解压：从网络来的文件自动带 quarantine。
  - 移动硬盘/网络共享：有些文件系统不支持 xattr，复制过去 xattr 就丢了。
  - App bundle：里面包含符号链接、权限位、代码签名资源。复制方式不对，签名直接废掉，系统说“损坏”。
  - 公证/签名状态：Apple 的服务器会缓存信任状态，同一份 app 在不同路径、不同时间运行，可能得到不同判定。

MAC problem[17]:ASDW 这四个键位会不听我指挥

war thunder BUG[18]:当客户端无法连接登陆服务器的时候，将会直接自动退出且无法正常进行正常启动，启动器也会同时崩坏4次

war thunder BUG[19]:程序会莫名其妙的损坏，哪怕里面的文件压根没有损坏,只需要点击启动器“修复”下载0KB即可。
