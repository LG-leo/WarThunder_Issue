## 这个帖子仅表达相关网络连接问题，若遇到网络连接问题，请试图使用游戏加速器解决。
## 本次“测试”主要在 B*****城市 进行测试，其他地区网络情况没有考虑过。

---
# DATA数据区域

### MASQUE_via_udp（官方 WARP UDP模式）-now
*   **ASIA（亚洲）**：ping 500~699，平均 640；PL（丢包率）8~34，平均 22。[war thunder reconmand]
*   **EUROPE（欧洲）**：ping 569~704，平均 620；PL 2~47，平均 20。
*   **AMERICA（美洲）**：ping 593~653，平均 613；PL 4~33，平均 15。
*   **RUSSIA（俄罗斯）**：ping 597~642，平均 601；PL 4~30，平均 16。（备注：PL波动大）
*   **状态**：全部显示 `[war thunder reconmand]`（战雷推荐），且warp显示 `connect_successfully_stable`（连接成功且稳定）。

### MASQUE_via_udp（官方 WARP UDP模式）-9月份
*   **ASIA（亚洲）**：ping 270～320，平均 310；PL（丢包率）1~35，平均 10。[war thunder reconmand]
*   **EUROPE（欧洲）**：ping 310～340，平均 320左右；PL 0~30，平均 8。
*   **AMERICA（美洲）**：无数据no data
*   **RUSSIA（俄罗斯）**：无数据no data
*   **状态**：warp显示 `connect_successfully_stable`（连接成功且稳定）。

### MASQUE_via_https（官方 WARP HTTPS模式）
*   **ASIA（亚洲）**：ping 530~999，平均 703；PL 0~10，平均 1。（备注：ping波动大）[war thunder reconmand]
*   **EUROPE（欧洲）**：ping 547~623，平均 574；PL 1~48，平均 14。（备注：PL波动大）[war thunder reconmand]
*   **AMERICA（美洲）**：ping 620~999，平均 680；PL 0~8，平均 1。（备注：ping波动大）
*   **RUSSIA（俄罗斯）**：ping 590~730，平均 638；PL 8~35，平均 15。（备注：PL波动大）
*   **状态**：全部warp显示 `connect_successfully_stable`（连接成功且稳定）。

### MASQUE_via_tcp(tls)
*   **所有区域（亚洲/欧洲/美洲/俄罗斯）**：无数据。
*   **原因**：`no data caused by no able connect to warp`（无法连接到warp）。
*   **状态**：`warp:noable_to_connect_by_CF_DNS_LOOKUP_FAILURE`（因CF DNS解析失败导致无法连接）。

### directly_connect（直连）
*   **所有区域（亚洲/欧洲/美洲/俄罗斯）**：无数据。
*   **原因**：`no data caused by cannot connect to login_signup_severs and the war_thunder and war_thunder_launcher are being crushed by no sense-able problem`（无法连接到登录/注册服务器，战雷及启动器连环崩溃4次）。
*   **状态**：直连失败。

### clash_verge_rev(MASQUE-CF flow)（Clash Verge Rev接管）
*   **ASIA（亚洲）**：ping 380~480，平均 430；PL 1~10，平均 1。[war thunder reconmand]
*   **EUROPE/AMERICA/RUSSIA（欧洲/美洲/俄罗斯合并）**：ping 480~520，平均 640；PL 1~10，平均 1。
*   **状态**：`tcp+udp`（TCP+UDP模式，战雷推荐）。

### 释义（label）
*   `t`：连接类型（types of connect）。
*   `ave_PL`：平均丢包率（average PL）。
*   `[war thunder reconmand]`：表示战雷首选/推荐的服务器。
*   `-warp:connect_successfully_stable`：表示 WARP 数据流（设备->输出->Cloudflare 叠加 Cloudflare->输出->设备）延迟低于 220ms。

---
# 总结和推理过程

1. 首先第一点，warp的流量管道始终在测试过程中内的流量是处于 **ping200 pl20**以下的（`-warp:connect_successfully`），这就意味着 和warp本身没有关联。
2. 游戏客户端在游戏对局内使用UDP发包，意味着不需要进行3次握手
3. 用warp客户端连接，配置没变情况下，延迟暴增300ms~1000ms+
4. 在这个月，所有服务器（使用warp客户端），ping和PL基本一致（在同等模式下）
5. 意味着，其 “PL” 和**ping**增加主要集中在CF（cloudflare)边缘网络到gaijin服务器的一段路
6. 而这大概率是gaijin entertaiment的服务器防火墙的“QOS”规则造成
7. 而 clash verge rev只有380～500的ping，很有可能是发包频率不同造成

