# 医院门诊挂号与导诊服务平台

面向患者的门诊预约挂号系统：微信小程序端负责科室浏览、医生查询、排班预约、挂号单管理与智能导诊，Spring Boot 后端提供 REST 接口与管理员后台。

## 技术栈

| 层级 | 选型 |
|------|------|
| 小程序 | 微信原生框架（WXML / WXSS / JavaScript） |
| 后端 | Spring Boot 2.7、MyBatis-Plus 3.5 |
| 数据库 | MySQL 8.0 |
| 鉴权 | JWT（HS256）+ Spring Security Crypto（BCrypt） |
| 校验 | Bean Validation（javax.validation） |

## 功能

**患者端**

- 微信登录（演示环境用设备标识代替 openid，接口已按真实登录流程预留）
- 科室浏览、医生列表与搜索、医生详情
- 未来 7 天排班查看、按时段预约挂号
- 就诊人管理：新增、编辑、默认就诊人、删除（校验身份证与手机号）
- 挂号单管理：按状态筛选、分页加载、取消预约
- 智能导诊：症状描述 → 推荐科室（含急症提示）

**管理端**

- 账号密码登录，独立的管理员 token
- 科室维护：新增、编辑、删除（科室下有医生时禁止删除）
- 医生维护：所属科室、职称、挂号费、擅长领域
- 排班维护：按日期查看出诊安排，新增/删除排班，号源数量校验
- 挂号单查询：状态、就诊日期筛选，支持签到 / 完成 / 取消

## 目录结构

```
hospital-registration/
├── start.bat / stop.bat / status.bat  # 一键启动、停止、查看状态
├── scripts/                          # 上面三个脚本的 PowerShell 实现
├── database/init.sql                 # 建库建表 + 初始数据（科室、医生、排班）
├── backend/
│   ├── pom.xml
│   └── src/
│       ├── main/java/com/hospital/
│       │   ├── common/               # 统一响应、异常、分页、登录上下文
│       │   ├── config/               # 鉴权拦截器、CORS、MyBatis-Plus、启动初始化
│       │   ├── controller/           # 接口层
│       │   ├── dto/                  # 入参对象（含参数校验）
│       │   ├── entity/               # 数据库实体
│       │   ├── mapper/               # MyBatis-Plus Mapper
│       │   ├── service/              # 业务逻辑，含 TriageEngine 导诊引擎
│       │   ├── util/                 # JWT、身份证校验、时段映射
│       │   └── vo/                   # 出参对象
│       ├── main/resources/
│       │   ├── application.yml
│       │   └── mapper/RegistrationMapper.xml
│       └── test/java/                # TriageEngine、JwtUtil 单元测试
├── miniprogram/
│   ├── app.js / app.json / app.wxss  # 应用配置与设计系统
│   ├── assets/icons/                 # 由 tools/gen_icons.py 生成的图标
│   ├── components/                   # empty-state、admin-nav
│   ├── styles/admin.wxss             # 管理端共用样式
│   ├── utils/                        # api 请求层、登录态、日期与格式化
│   └── pages/                        # 18 个页面
├── tools/
│   ├── gen_icons.py                  # 生成 tabBar 与界面图标
│   └── check_miniprogram.py          # WXML 结构 / 事件函数 / 组件路径检查
└── README.md
```

## 快速开始

### 一键启动（推荐）

仓库根目录双击：

- `start.bat`：启动 MySQL 服务 → 后端 → ngrok 公网隧道；缺 jar 会自动编译，已在运行会跳过，最后打印本机与公网地址
- `stop.bat`：停止后端 + ngrok + MySQL；`stop.bat -KeepDatabase` 只停后端和隧道
- `status.bat`：查看数据库、后端、隧道与接口自检状态

日志在 `logs/backend.out.log` 与 `logs/ngrok.out.log`，也可以直接用 PowerShell 调用 `scripts/start.ps1`、`scripts/stop.ps1`、`scripts/status.ps1`。

可选参数：`start.bat -SkipTunnel` 只起后端、不开隧道；`stop.bat -KeepTunnel` 保留隧道。

> ngrok 的静态域名在 `scripts/common.ps1` 的 `$NgrokDomain` 中配置，换域名时这里和 `miniprogram/app.js` 的 `baseUrl` 要一起改。
>
> `stop.bat` 会停掉整个 MySQL 实例，同一实例上的其他数据库也会断开。

### 1. 数据库

```bash
mysql -u root -p < database/init.sql
```

脚本会重建 `hospital` 库，写入 13 个科室、19 位医生、未来 7 天的排班（约 300 条）以及一个演示用户与就诊人。

### 2. 后端

```bash
cd backend
mvn clean package
java -jar target/hospital-registration-1.0.0.jar
```

服务默认运行在 `http://localhost:8080`。数据库连接可用环境变量覆盖：

```bash
SPRING_DATASOURCE_URL=jdbc:mysql://localhost:3306/hospital?useUnicode=true&characterEncoding=utf-8&serverTimezone=Asia/Shanghai&useSSL=false
SPRING_DATASOURCE_USERNAME=root
SPRING_DATASOURCE_PASSWORD=123456
JWT_SECRET=请替换为长度不小于 32 位的随机字符串
```

### 3. 小程序

1. 微信开发者工具 → 导入项目 → 选择 `miniprogram/` 目录（也可直接导入仓库根目录，`miniprogramRoot` 已配置）。
2. AppID 使用测试号或自己的小程序 AppID。
3. 开发者工具「详情 → 本地设置」勾选 **不校验合法域名**（本地 `http://` 调试必需）。
4. 接口地址在 `miniprogram/app.js` 的 `globalData.baseUrl`，当前走 ngrok 内网穿透：`https://campsite-recount-floss.ngrok-free.dev/api`，真机、体验版和其他电脑都能访问；只在本机模拟器调试时可以改成 `http://127.0.0.1:8080/api` 或内网地址 `http://10.178.32.109:8080/api`。
5. 走 ngrok 时请求会自动带上 `ngrok-skip-browser-warning: true` 头（`utils/api.js` 里），否则免费版会把请求拦成提示页。

## 演示账号

| 角色 | 账号 | 密码 |
|------|------|------|
| 管理员 | `admin` | `123456` |
| 患者 | 小程序内点击「微信一键登录」 | — |

管理员初始密码在 `database/init.sql` 中以明文写入，后端首次启动时由 `DataInitializer` 自动替换为 BCrypt 密文；之后再改库不会影响登录。

## 接口

返回体统一为 `{ code, message, data }`，HTTP 状态码与 `code` 一致。鉴权方式为请求头 `Authorization: Bearer <token>`，token 中带 `role`（`USER` / `ADMIN`）。

| 方法 | 路径 | 权限 | 说明 |
|------|------|------|------|
| POST | `/api/user/login` | 公开 | 患者登录，返回 token |
| GET | `/api/user/me` | 患者 | 当前用户信息 |
| GET | `/api/department/list` | 公开 | 科室列表（含医生数量） |
| GET | `/api/department/detail` | 公开 | 科室详情 |
| POST/PUT/DELETE | `/api/department/*` | 管理员 | 科室增改删 |
| GET | `/api/doctor/list` | 公开 | 医生列表（可按科室过滤） |
| GET | `/api/doctor/search` | 公开 | 按姓名/科室/擅长搜索 |
| GET | `/api/doctor/detail` | 公开 | 医生详情 |
| POST/PUT/DELETE | `/api/doctor/*` | 管理员 | 医生增改删 |
| GET | `/api/schedule/list` | 公开 | 医生可约时段 |
| GET | `/api/schedule/dates` | 公开 | 可预约日期 |
| POST/PUT/DELETE | `/api/schedule/*` | 管理员 | 排班增改删 |
| POST | `/api/registration/create` | 患者 | 创建挂号 |
| GET | `/api/registration/list` | 患者 | 我的挂号（分页、状态筛选） |
| GET | `/api/registration/detail` | 患者 | 挂号详情 |
| POST | `/api/registration/cancel` | 患者 | 取消挂号 |
| GET/POST/PUT/DELETE | `/api/patient/*` | 患者 | 就诊人管理 |
| POST | `/api/guidance/triage` | 公开 | 智能导诊 |
| POST | `/api/admin/login` | 公开 | 管理员登录 |
| GET | `/api/admin/registration/list` | 管理员 | 挂号单查询（状态、日期、关键词） |
| PUT | `/api/admin/registration/status` | 管理员 | 更新挂号状态 |
| GET | `/api/admin/schedule/list` | 管理员 | 按日期查询排班 |

## 业务规则

- **号源扣减**使用 `UPDATE schedule SET remain_count = remain_count - 1 WHERE id = ? AND status = 1 AND remain_count > 0`，以影响行数判断成功，避免并发超卖。
- **挂号校验**：就诊人必须属于当前登录用户；排班必须正常出诊、未过期、未开诊且有余号；同一就诊人同一时段不可重复挂号；挂号费取自医生 `consultation_fee`。
- **取消规则**：仅「已预约」可取消，且需在就诊前 `app.booking.cancel-limit-hours`（默认 2 小时）之外；取消后号源自动恢复。
- **可约列表**：已过期、已停诊、余量为 0 以及当天已开诊的时段不会出现在患者端。
- **管理员操作**：科室下有医生时不能删除；医生、就诊人存在挂号记录时不能删除；排班有未完成挂号时不能删除；状态流转仅允许 已预约 → 已签到 → 已完成，或取消。

## 智能导诊

`TriageEngine` 维护「症状关键词 → 科室名称」的多对多映射（130 余条规则），一个关键词可指向多个科室（如「腰痛」同时命中骨科与泌尿外科），结果按命中关键词数量排序并给出置信度。

- 科室以名称引用，不再硬编码科室 ID，新增科室后无需改代码。
- 先剥离「不咳嗽」「没有发烧」这类否定描述，减少误判。
- 命中胸痛、呼吸困难、意识模糊等急症关键词时，结果中优先给出急诊科，并返回 `emergency = true` 与就医提示。

## 界面说明

小程序端采用医院导视系统式的克制排版：单一主色 `#0F6B5C`、细描边卡片、编号式信息层级，没有渐变色块与表情符号。图标由 `tools/gen_icons.py` 生成，避免引入图标字体。

- 颜色与排版变量集中在 `miniprogram/app.wxss`。
- `empty-state`、`admin-nav` 为复用组件；管理端四个页面共用 `styles/admin.wxss`。
- 页面间传参使用 `app.globalData.draft` 传递预约草稿，避免把中文拼进 URL。
- `docs/preview/` 下是按 WXSS 静态渲染的界面预览图，用于快速了解视觉风格，实际效果以微信开发者工具为准。

## 配置项

| 配置 | 默认值 | 说明 |
|------|--------|------|
| `app.jwt.secret` | 内置演示密钥 | 生产环境务必用 `JWT_SECRET` 覆盖 |
| `app.jwt.expire-hours` | 72 | token 有效期 |
| `app.booking.cancel-limit-hours` | 2 | 就诊前多少小时停止取消 |
| `app.booking.bookable-days` | 7 | 患者可预约天数 |

## 开发脚本

```bash
python tools/gen_icons.py        # 重新生成图标
python tools/check_miniprogram.py  # 检查 WXML 标签、事件函数、组件路径
```

## 已知限制

- 微信登录为演示实现：小程序用本机生成的设备标识充当 `code`，后端直接拼成 openid。接入生产环境需要补充 `appid/secret` 并调用 `jscode2session`。
- 未接入在线支付、短信通知与排队叫号。
- 身份证号用于校验身份，列表与订单中已做脱敏展示，但数据库仍为明文存储，生产环境需要加密与访问审计。
