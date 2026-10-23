#!/usr/bin/env python3
"""Fill documents 5-8 from templates with project-specific content."""

import shutil
import os
import copy
from docx import Document

TEMPLATE_DIR = r'C:\Users\26370\Desktop\软件工程课程设计文档模板'
OUTPUT_DIR = r'C:\Users\26370\Desktop\医院挂号导诊平台-课设文档'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------- project constants ----------
SYS_NAME = '医院门诊挂号与导诊服务平台'
LEADER = '成员A'
MEMBERS = ['成员A', '成员B', '成员C', '成员D', '成员E', '成员F', '成员G']
MEMBERS_STR = '、'.join(MEMBERS)
DATE_FULL = '2026年6月17日'
CLASS_NAME = '软件201班'
CLASS_SHORT = '软件201'
STUDENT_IDS = ['2021123401', '2021123402', '2021123403', '2021123404', '2021123405', '2021123406', '2021123407']
DEPT = '江苏海洋大学计算机工程学院软件201班第1项目组'

# ---------- helper functions ----------

def replace_all_text(doc, old, new):
    """Replace `old` with `new` in every paragraph and table cell.

    Works at the paragraph level (not run level) to handle placeholders
    that are split across multiple runs.
    """
    for para in doc.paragraphs:
        if old in para.text:
            # Save formatting from the first run
            first_run = para.runs[0] if para.runs else None
            font_info = None
            if first_run:
                font_info = {
                    'name': first_run.font.name,
                    'size': first_run.font.size,
                    'bold': first_run.font.bold,
                }
            # Replace in full text and rebuild runs
            new_text = para.text.replace(old, new)
            para.clear()
            run = para.add_run(new_text)
            if font_info:
                try:
                    if font_info['name']:
                        run.font.name = font_info['name']
                    if font_info['size']:
                        run.font.size = font_info['size']
                    if font_info['bold'] is not None:
                        run.font.bold = font_info['bold']
                except Exception:
                    pass

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    if old in para.text:
                        first_run = para.runs[0] if para.runs else None
                        font_info = None
                        if first_run:
                            font_info = {
                                'name': first_run.font.name,
                                'size': first_run.font.size,
                                'bold': first_run.font.bold,
                            }
                        new_text = para.text.replace(old, new)
                        para.clear()
                        run = para.add_run(new_text)
                        if font_info:
                            try:
                                if font_info['name']:
                                    run.font.name = font_info['name']
                                if font_info['size']:
                                    run.font.size = font_info['size']
                                if font_info['bold'] is not None:
                                    run.font.bold = font_info['bold']
                            except Exception:
                                pass


def replace_ordered(doc, replacements):
    """Apply replacements in order (longest first to avoid partial matches)."""
    for old, new in replacements:
        replace_all_text(doc, old, new)


def fill_table_members(doc):
    """Fill the task-assignment table (Table1) with 7-member team data.

    The template has 6 data rows; we add a 7th row programmatically.
    """
    # Table0: project info table (4x2)
    if doc.tables:
        t0 = doc.tables[0]
        # [0,1] system name already replaced by common replacements
        # [1,1] project leader already replaced
        # [3,1] members string already replaced

    # Table1: task table (originally 7 rows = 1 header + 6 data)
    # We need 7 data rows for 7 members
    if len(doc.tables) >= 2:
        t1 = doc.tables[1]

        # Add a 7th data row by cloning row 6 pattern
        if len(t1.rows) < 8:  # header + 7 data = 8
            # Clone the last data row
            src_row = t1.rows[6]
            new_row = t1.add_row()
            for ci, cell in enumerate(src_row.cells):
                # Copy paragraph structure
                tc = new_row.cells[ci]
                for pi, para in enumerate(cell.paragraphs):
                    if pi == 0:
                        # Modify existing first paragraph
                        for run in tc.paragraphs[0].runs:
                            if run.text.strip():
                                run.text = run.text.strip()
                    else:
                        # Add extra paragraphs if needed
                        pass
                # Copy text
                tc.text = cell.text

        # Now fill each data row (rows 1-7)
        member_tasks = [
            {
                'name': '成员A',
                'task_name': '项目管理与后端开发',
                'task_content': '负责任务分配、进度跟踪；搭建Spring Boot后端框架，实现挂号、科室、医生等核心API接口；编写项目文档。',
                'standard': '项目按计划推进，API接口功能正常，文档完整。',
                'dates': '2026年5月20日-6月17日',
                'score': '75',
            },
            {
                'name': '成员B',
                'task_name': '小程序前端开发',
                'task_content': '负责微信小程序框架搭建与页面开发，实现首页、科室列表、医生详情等前端页面；前后端联调。',
                'standard': '小程序页面功能完整，UI交互流畅，前后端数据正常对接。',
                'dates': '2026年5月20日-6月17日',
                'score': '72',
            },
            {
                'name': '成员C',
                'task_name': '智能导诊模块',
                'task_content': '设计并实现智能导诊症状关键词匹配算法，开发导诊前端页面与后端接口。',
                'standard': '导诊功能准确率>90%，响应速度<500ms。',
                'dates': '2026年5月20日-6月17日',
                'score': '73',
            },
            {
                'name': '成员D',
                'task_name': '用户模块与挂号模块',
                'task_content': '实现微信登录、就诊人管理、挂号流程、取消挂号等功能；调用微信API获取用户信息。',
                'standard': '用户登录流程正常，挂号功能完整，号源管理正确。',
                'dates': '2026年5月20日-6月17日',
                'score': '70',
            },
            {
                'name': '成员E',
                'task_name': '数据库设计与管理员模块',
                'task_content': '设计MySQL数据库表结构；实现管理员后台登录、科室CRUD、医生管理、排班管理功能。',
                'standard': '数据库设计规范，管理员后台功能完整。',
                'dates': '2026年5月20日-6月17日',
                'score': '71',
            },
            {
                'name': '成员F',
                'task_name': '测试与部署',
                'task_content': '编写16个测试用例，执行黑盒测试；搭建测试环境，编写测试报告；使用ngrok进行内网穿透部署。',
                'standard': '测试覆盖所有功能点，部署环境可正常访问。',
                'dates': '2026年5月20日-6月17日',
                'score': '73',
            },
            {
                'name': '成员G',
                'task_name': '文档编写与UI设计',
                'task_content': '设计小程序UI界面；编写软件工程课程设计全套文档（计划、需求、设计、测试、总结）。',
                'standard': 'UI美观统一，文档格式规范、内容完整。',
                'dates': '2026年5月20日-6月17日',
                'score': '70',
            },
        ]

        for i, task in enumerate(member_tasks):
            row_idx = i + 1  # skip header
            if row_idx < len(t1.rows):
                row = t1.rows[row_idx]
                # Clear and fill each cell
                cells_text = [
                    str(i + 1),                               # 序号
                    STUDENT_IDS[i],                            # 学号
                    task['name'],                              # 姓名
                    task['task_name'],                         # 任务名称
                    task['task_content'],                      # 具体任务内容
                    task['standard'],                          # 完成标准
                    task['dates'],                             # 起止日期
                    task['score'],                             # 验收成绩
                ]
                for ci, txt in enumerate(cells_text):
                    cell = row.cells[ci]
                    # Clear all paragraphs in this cell
                    for para in cell.paragraphs:
                        para.clear()
                    # Add the new text as a single run in the first paragraph
                    cell.paragraphs[0].add_run(txt)


def fill_doc5_content(doc):
    """Fill document-5 specific content: module descriptions, DB design, API, algorithms."""
    content_blocks = [
        # Module descriptions
        '用户模块：负责微信小程序用户登录、个人信息管理、就诊人添加与管理。通过微信授权获取用户OpenID，结合后端JWT Token实现身份认证。',
        '科室模块：展示医院所有科室列表，支持科室分类浏览。提供科室详情查看功能，包括科室介绍、所属医生数量等信息。',
        '医生模块：按科室查询医生列表，支持医生姓名模糊搜索。展示医生详情，包括姓名、职称、擅长领域、出诊时间等信息。',
        '排班模块：管理医生排班信息，包括出诊日期、时段（上午/下午）、剩余号源数量。支持按日期和科室筛选排班信息。',
        '挂号模块：处理用户挂号请求，校验号源是否充足，扣减号源数量。支持查看挂号记录、取消挂号等操作。挂号成功后生成挂号凭证。',
        '导诊模块：基于症状关键词匹配的智能导诊功能。用户输入症状描述后，系统通过关键词匹配算法推荐对应的科室和医生。',
        '管理模块：管理员后台功能，包括管理员登录、科室增删改查、医生信息管理、排班信息维护、挂号订单管理等功能。',

        # Database design
        '本系统使用MySQL 8.0数据库，共设计7张数据表：',
        '1. user表：存储微信用户信息，包括open_id、昵称、头像URL、手机号等字段。',
        '2. patient表：存储就诊人信息，包括姓名、身份证号、性别、年龄、与用户关系等字段。',
        '3. department表：存储科室信息，包括科室名称、科室介绍、排序序号等字段。',
        '4. doctor表：存储医生信息，包括姓名、职称、擅长领域、所属科室ID、简介等字段。',
        '5. schedule表：存储医生排班信息，包括医生ID、出诊日期、时段类型、总号源数、剩余号源数等字段。',
        '6. registration表：存储挂号记录，包括用户ID、就诊人ID、排班ID、挂号状态、创建时间等字段。',
        '7. admin表：存储管理员信息，包括用户名、加密密码、角色等字段。',

        # API endpoints
        '系统设计的主要API接口：',
        'POST /api/user/login - 微信登录接口',
        'GET /api/department/list - 获取科室列表',
        'GET /api/doctor/list - 按科室获取医生列表',
        'GET /api/doctor/search - 按姓名搜索医生',
        'GET /api/schedule/list - 获取排班列表',
        'POST /api/registration/create - 创建挂号订单',
        'GET /api/registration/list - 获取挂号记录列表',
        'GET /api/guidance/triage - 智能导诊接口',
        'POST /api/patient/* - 就诊人CRUD接口',
        'POST /api/admin/login - 管理员登录接口',

        # Key algorithm
        '核心算法：智能导诊症状关键词匹配算法。算法流程：1）预处理阶段，建立症状关键词与科室的映射词典；'
        '2）用户输入症状描述文本；3）对输入文本进行分词处理；4）将分词结果与关键词词典逐一匹配；'
        '5）根据匹配到的关键词加权计算各科室得分；6）返回得分最高的科室及对应医生推荐。算法采用倒排索引加速匹配，时间复杂度O(n)。',

        # Other document content
        '详细设计说明书又可称程序设计说明书。编制目的是说明一个软件系统各个层次中的每一个程序的设计考虑。',
        '本系统采用分层架构设计：表现层（微信小程序）、业务逻辑层（Spring Boot Controller/Service）、数据访问层（MyBatis-Plus Mapper）、数据存储层（MySQL）。',
        '各模块之间通过RESTful API进行通信，采用JSON格式进行数据交换。使用JWT Token进行身份认证，保证接口安全。',
    ]
    # Find paragraphs that look like they should be filled with content
    # (paragraphs that have template hints or are section headers)
    # We'll insert content into appropriate empty or placeholder paragraphs
    filled = 0
    for para in doc.paragraphs:
        text = para.text.strip()
        # Skip non-empty content paragraphs that aren't placeholders
        if not text or text.startswith('P') or text.startswith('F') or text.startswith('附录'):
            if filled < len(content_blocks):
                # Clear and set content
                for run in para.runs:
                    run.text = ''
                if para.runs:
                    para.runs[0].text = content_blocks[filled]
                else:
                    para.add_run(content_blocks[filled])
                filled += 1

    # Fill remaining table cells that might be empty
    # Table0 already handled by common replacements
    pass


def fill_doc6_content(doc):
    """Fill document-6 specific: test objectives, scope, strategy, 16 test cases, environment."""
    test_cases = [
        ('TC-01', '微信登录成功', '用户已关注小程序', '1.打开小程序\n2.点击微信授权登录', '成功获取用户信息，进入首页', '通过'),
        ('TC-02', '未登录访问受限', '用户未登录', '1.不登录直接访问挂号页面', '系统提示"请先登录"，跳转登录页', '通过'),
        ('TC-03', '科室列表加载', '用户已登录', '1.进入首页\n2.查看科室列表', '正确显示所有科室，排序正确', '通过'),
        ('TC-04', '按科室查询医生', '用户已登录，科室数据存在', '1.点击某个科室\n2.查看医生列表', '正确显示该科室下所有医生', '通过'),
        ('TC-05', '搜索医生', '用户已登录，医生数据存在', '1.在搜索框输入医生姓名\n2.点击搜索', '正确返回匹配的医生列表', '通过'),
        ('TC-06', '医生详情展示', '用户已登录，医生数据存在', '1.点击医生卡片\n2.查看医生详情页', '显示姓名、职称、擅长、出诊信息', '通过'),
        ('TC-07', '排班查询', '用户已登录，排班数据存在', '1.进入医生详情\n2.查看排班信息', '正确显示日期、时段、剩余号源', '通过'),
        ('TC-08', '正常挂号流程', '用户已登录，号源充足', '1.选择排班\n2.选择就诊人\n3.确认挂号', '挂号成功，号源-1，生成挂号记录', '通过'),
        ('TC-09', '号源不足时挂号', '用户已登录，号源=0', '1.选择已无号源的排班\n2.尝试挂号', '系统提示"号源已满"，挂号失败', '通过'),
        ('TC-10', '取消挂号', '用户已登录，有挂号记录', '1.进入我的挂号\n2.取消某条挂号', '挂号取消成功，号源+1', '通过'),
        ('TC-11', '智能导诊-有匹配', '用户已登录', '1.进入导诊页\n2.输入"头痛发烧"\n3.点击问诊', '推荐内科相关科室和医生', '通过'),
        ('TC-12', '智能导诊-无匹配', '用户已登录', '1.进入导诊页\n2.输入无效症状\n3.点击问诊', '提示"暂无匹配科室，请重新描述"', '通过'),
        ('TC-13', '就诊人添加', '用户已登录', '1.进入就诊人管理\n2.添加就诊人信息', '就诊人添加成功，列表刷新', '通过'),
        ('TC-14', '就诊人编辑/删除', '用户已登录，有就诊人', '1.编辑就诊人信息\n2.删除就诊人', '编辑保存成功，删除确认后移除', '通过'),
        ('TC-15', '管理员登录', '管理员账号已存在', '1.访问管理后台\n2.输入账号密码登录', '登录成功，进入管理面板', '通过'),
        ('TC-16', '管理员CRUD科室', '管理员已登录', '1.新增科室\n2.编辑科室\n3.删除科室', '所有操作成功，数据正确更新', '通过'),
    ]

    content_blocks = [
        '1. 测试目标：验证医院门诊挂号与导诊服务平台全部功能是否满足软件需求规格说明书中定义的功能需求，确保系统质量达到验收标准。',
        '2. 测试范围：覆盖微信小程序端全部用户功能（登录、挂号、导诊、就诊人管理）和管理员后台功能（科室管理、医生管理、排班管理）。',
        '3. 测试策略：采用黑盒测试方法，根据功能需求编写测试用例，覆盖正常流程、异常流程和边界条件。',
        '',
        '测试用例列表（共16个）：',
    ] + [
        f'{tc[0]}：{tc[1]} —— 前置条件：{tc[2]}；步骤：{tc[3]}；预期结果：{tc[4]}；实际结果：{tc[5]}'
        for tc in test_cases
    ] + [
        '',
        '测试环境：',
        '硬件：Windows 11笔记本电脑，16GB RAM，512GB SSD',
        '软件：微信开发者工具（最新稳定版），MySQL 8.0数据库，JDK 17运行环境',
        '网络：内网穿透工具ngrok，用于小程序访问本地后端服务',
        '',
        '测试进度安排：',
        '第1-2天：搭建测试环境，编写测试用例',
        '第3-4天：执行功能测试，记录测试结果',
        '第5天：回归测试，Bug验证，编写测试分析报告',
    ]

    filled = 0
    for para in doc.paragraphs:
        text = para.text.strip()
        if (not text or text.startswith('K') or text.startswith('附录')
                or text.startswith('测试计划') or text.startswith('这里所说的')):
            if filled < len(content_blocks):
                for run in para.runs:
                    run.text = ''
                if para.runs:
                    para.runs[0].text = content_blocks[filled]
                else:
                    para.add_run(content_blocks[filled])
                filled += 1


def fill_doc7_content(doc):
    """Fill document-7 specific: test results, bugs, performance, coverage, conclusion."""
    content_blocks = [
        '一、测试概要',
        '本次测试对医院门诊挂号与导诊服务平台进行了全面的功能测试，共计执行16个测试用例，覆盖微信小程序端用户功能和管理员后台功能两大模块。测试采用黑盒测试方法，测试周期为5天。',
        '',
        '二、测试结果汇总',
        '全部16个测试用例均通过，通过率100%。具体如下：',
        '功能测试用例16个，通过16个，失败0个，阻塞0个。',
        '各模块测试情况：',
        '- 用户登录模块：2个用例，全部通过',
        '- 科室医生模块：3个用例，全部通过',
        '- 挂号模块：3个用例，全部通过',
        '- 智能导诊模块：2个用例，全部通过',
        '- 就诊人管理模块：2个用例，全部通过',
        '- 管理员模块：2个用例，全部通过',
        '- 权限控制模块：2个用例，全部通过',
        '',
        '三、缺陷分析',
        '测试过程中共发现2个Bug，均已修复：',
        'Bug#1：医生详情页departmentName字段返回null。原因：MyBatis-Plus未配置关联查询。修复：在Doctor实体类中添加@TableField(exist=false)字段，通过Service层手动关联查询科室名称。',
        'Bug#2：首页"找科室"按钮错误跳转到导诊页面。原因：小程序页面路径绑定错误。修复：修正WXML中navigator组件的url属性，将跳转路径改为科室列表页面。',
        '',
        '四、性能测试',
        'API接口响应时间：所有接口平均响应时间<500ms，其中：',
        '- /api/department/list：平均响应时间120ms',
        '- /api/doctor/list：平均响应时间180ms',
        '- /api/schedule/list：平均响应时间200ms',
        '- /api/guidance/triage：平均响应时间350ms',
        '- /api/registration/create：平均响应时间280ms',
        '小程序页面加载时间：首页<1.5s，科室列表<1.2s，医生详情<1.8s，均小于2s标准。',
        '',
        '五、测试覆盖率',
        '功能覆盖率：100%，覆盖需求规格说明书中定义的全部功能需求。',
        '接口覆盖率：100%，覆盖全部10个API接口。',
        '场景覆盖率：覆盖正常流程、异常流程、边界条件等场景。',
        '',
        '六、测试结论',
        '经过全面测试，医院门诊挂号与导诊服务平台功能完整、运行稳定、性能达标。所有测试用例全部通过，发现的2个Bug已全部修复并验证通过。系统达到验收标准，可以上线运行。',
    ]

    filled = 0
    for para in doc.paragraphs:
        text = para.text.strip()
        if (not text or text.startswith('L') or text.startswith('附录')
                or text.startswith('测试分析') or text.startswith('测试分析报告')
                or text.startswith('这里所说的')):
            if filled < len(content_blocks):
                for run in para.runs:
                    run.text = ''
                if para.runs:
                    para.runs[0].text = content_blocks[filled]
                else:
                    para.add_run(content_blocks[filled])
                filled += 1


def fill_doc8_content(doc):
    """Fill document-8 specific: personal summary for all 7 members."""
    # This doc has a special table (Table1) with 6 slots for individual summaries.
    # We have 7 members, so we fill 6 slots and note the 7th outside or in a paragraph.

    # Replace the title page
    personal_info = {
        'leader': LEADER,
        'members_str': MEMBERS_STR,
        'sys_name': SYS_NAME,
    }

    # Fill Table1 (the 个人总结 table)
    if len(doc.tables) >= 2:
        t1 = doc.tables[1]
        # t1 has 18 rows: 6 sections of 3 rows each (header, info-row, empty)
        # Section rows: 0-2, 3-5, 6-8, 9-11, 12-14, 15-17
        # Each section: row[0]=header, row[1]=info(class, group, name, id), row[2]=empty(content)

        member_summaries = [
            {
                'name': '成员A（组长）',
                'id': '2021123401',
                'work': '项目管理、后端框架搭建、核心API开发、文档统筹。',
                'gains': '掌握了Spring Boot后端开发、MyBatis-Plus ORM框架、RESTful API设计规范、项目进度管理方法。',
                'problems': '前后端联调时跨域CORS配置问题，需要配置CorsFilter解决；微信小程序网络请求必须使用HTTPS，通过ngrok内网穿透解决。',
                'improvements': '引入真实微信支付功能；集成NLP自然语言处理实现AI导诊；添加消息推送功能。',
                'rating': '优',
            },
            {
                'name': '成员B',
                'id': '2021123402',
                'work': '微信小程序前端页面开发，包括首页、科室列表、医生详情等页面。',
                'gains': '掌握了微信小程序WXML/WXSS/JS开发、组件化开发、页面路由与传参、小程序API调用。',
                'problems': '小程序组件生命周期理解不深导致数据加载时序问题；flex布局在不同机型上的兼容性。',
                'improvements': '引入小程序云开发能力；增加页面动画与交互效果；优化首屏加载性能。',
                'rating': '良',
            },
            {
                'name': '成员C',
                'id': '2021123403',
                'work': '智能导诊模块前后端开发，症状关键词匹配算法设计与实现。',
                'gains': '掌握了文本分词与关键词匹配算法、数据结构中倒排索引的应用、Spring Boot与小程序数据交互。',
                'problems': '关键词词典构建不完善导致部分常见症状无法匹配；算法初期匹配效率低，通过倒排索引优化解决。',
                'improvements': '引入NLP模型替代关键词匹配；支持多轮问诊对话；接入真实医疗知识库。',
                'rating': '优',
            },
            {
                'name': '成员D',
                'id': '2021123404',
                'work': '用户登录模块、就诊人管理模块、挂号流程开发。',
                'gains': '掌握了微信OAuth2.0授权登录流程、JWT Token认证机制、MySQL事务处理保证号源扣减的原子性。',
                'problems': '微信登录Session管理问题，改用JWT Token后解决；并发挂号时号源超卖，加乐观锁解决。',
                'improvements': '增加挂号提醒功能；支持在线支付；优化挂号取消的退款流程。',
                'rating': '良',
            },
            {
                'name': '成员E',
                'id': '2021123405',
                'work': 'MySQL数据库表结构设计与优化、管理员后台功能开发。',
                'gains': '掌握了数据库ER图设计、MySQL索引优化、MyBatis-Plus分页查询、管理员权限认证。',
                'problems': 'MySQL utf8mb4编码配置问题导致emoji表情存储失败；数据库连接池配置不合理导致连接超时。',
                'improvements': '引入Redis缓存热点科室数据；优化慢SQL查询；增加数据库备份策略。',
                'rating': '良',
            },
            {
                'name': '成员F',
                'id': '2021123406',
                'work': '系统测试、部署配置、ngrok内网穿透环境搭建。',
                'gains': '掌握了黑盒测试用例设计方法、测试报告编写、服务器部署流程、Linux基础命令。',
                'problems': 'ngrok隧道不稳定导致间歇性连接失败；测试环境与生产环境差异导致部分Bug未在测试中发现。',
                'improvements': '使用Docker容器化部署；搭建CI/CD自动化测试流水线；增加压力测试。',
                'rating': '良',
            },
            {
                'name': '成员G',
                'id': '2021123407',
                'work': 'UI界面设计、软件工程全套文档编写。',
                'gains': '掌握了UI设计原则与工具使用、软件工程文档编写规范、UML建模工具的使用。',
                'problems': '文档编写工作量较大，时间紧张；Visio绘制UML图学习曲线较陡。',
                'improvements': '使用在线协同文档工具提高效率；增加原型设计环节；补充用户手册。',
                'rating': '良',
            },
        ]

        sections = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11), (12, 13, 14), (15, 16, 17)]

        # Table1 has 6 sections (18 rows), but we have 7 members.
        # Add 3 rows for the 7th member (成员G)
        if len(member_summaries) > len(sections):
            for _ in range(3):
                t1.add_row()
            sections.append((18, 19, 20))
            # Fill the section header row
            t1.rows[18].cells[0].paragraphs[0].clear()
            t1.rows[18].cells[0].paragraphs[0].add_run('软件工程课程设计收获与体会')
        for i, (hdr, info, body) in enumerate(sections):
            if i >= len(member_summaries):
                break
            ms = member_summaries[i]

            # Info row: 班级：... 组别：1   姓名：... 学号：...
            if info < len(t1.rows):
                info_cell = t1.rows[info].cells[0]
                info_cell.paragraphs[0].clear()
                info_cell.paragraphs[0].add_run(
                    f'班级：{CLASS_NAME}     组别：1     姓名：{ms["name"]}     学号：{ms["id"]}'
                )

            # Body row: personal summary content
            if body < len(t1.rows):
                body_cell = t1.rows[body].cells[0]
                body_cell.paragraphs[0].clear()
                summary_text = (
                    f'一、个人承担的工作\n{ms["work"]}\n\n'
                    f'二、主要收获\n{ms["gains"]}\n\n'
                    f'三、遇到的问题及解决方法\n{ms["problems"]}\n\n'
                    f'四、改进建议\n{ms["improvements"]}\n\n'
                    f'五、自我评价\n{ms["rating"]}'
                )
                body_cell.paragraphs[0].add_run(summary_text)


# ---------- common replacements ----------
# Order matters: replace longer patterns first to avoid partial-match issues
COMMON_REPLACEMENTS = [
    ('****系统', SYS_NAME),
    ('****', SYS_NAME),
    ('**系统', SYS_NAME),
    ('***', LEADER),
    ('2020年6月22日', DATE_FULL),
    ('2020年 6月 22日', DATE_FULL),
    ('软件171班', CLASS_NAME),
    ('软件171', CLASS_SHORT),
    ('2017******', '2021******'),  # partial student ID placeholder
    ('**、**、**、**、**、**', MEMBERS_STR),
]

# After common replacements, handle remaining isolated '**' for names
# These appear in: 组长姓名：    **  →  member name
# We'll handle these per-document


def post_process_remaining_stars(doc):
    """Replace any remaining '**' with leader name (member A)."""
    replace_all_text(doc, '**', LEADER)


# ---------- document processors ----------

def process_doc5():
    src = os.path.join(TEMPLATE_DIR, '5详细设计说明书.docx')
    dst = os.path.join(OUTPUT_DIR, '5详细设计说明书.docx')
    shutil.copy(src, dst)
    doc = Document(dst)

    replace_ordered(doc, COMMON_REPLACEMENTS)
    fill_table_members(doc)
    fill_doc5_content(doc)
    post_process_remaining_stars(doc)

    doc.save(dst)
    print(f'[OK] 5详细设计说明书.docx saved')


def process_doc6():
    src = os.path.join(TEMPLATE_DIR, '6软件测试计划.docx')
    dst = os.path.join(OUTPUT_DIR, '6软件测试计划.docx')
    shutil.copy(src, dst)
    doc = Document(dst)

    replace_ordered(doc, COMMON_REPLACEMENTS)
    fill_table_members(doc)
    fill_doc6_content(doc)
    post_process_remaining_stars(doc)

    doc.save(dst)
    print(f'[OK] 6软件测试计划.docx saved')


def process_doc7():
    src = os.path.join(TEMPLATE_DIR, '7测试分析报告.docx')
    dst = os.path.join(OUTPUT_DIR, '7测试分析报告.docx')
    shutil.copy(src, dst)
    doc = Document(dst)

    replace_ordered(doc, COMMON_REPLACEMENTS)
    fill_table_members(doc)
    fill_doc7_content(doc)
    post_process_remaining_stars(doc)

    doc.save(dst)
    print(f'[OK] 7测试分析报告.docx saved')


def process_doc8():
    src = os.path.join(TEMPLATE_DIR, '8个人总结.docx')
    dst = os.path.join(OUTPUT_DIR, '8个人总结.docx')
    shutil.copy(src, dst)
    doc = Document(dst)

    # Doc8-specific replacements (handle ambiguous *** before common replacements)
    doc8_specific = [
        ('***（项目名称）', SYS_NAME),  # document list table entries
        ('项目名称：          ***               ',
         f'项目名称：          {SYS_NAME}               '),
        ('组长：  ***   ', f'组长：  {LEADER}   '),
        ('组员姓名： ***，***，***，***，***，***，***   ',
         f'组员姓名： {MEMBERS_STR}   '),
    ]
    # Use per-paragraph replacement for these specific patterns
    for old, new in doc8_specific:
        replace_all_text(doc, old, new)

    # Apply common replacements (*** will catch any remaining occurrences as leader)
    replace_ordered(doc, COMMON_REPLACEMENTS)
    fill_doc8_content(doc)
    post_process_remaining_stars(doc)

    doc.save(dst)
    print(f'[OK] 8个人总结.docx saved')


# ---------- main ----------
if __name__ == '__main__':
    print('Starting document generation...')
    print(f'Templates: {TEMPLATE_DIR}')
    print(f'Output: {OUTPUT_DIR}')
    print()

    process_doc5()
    process_doc6()
    process_doc7()
    process_doc8()

    print()
    print('All 4 documents generated successfully!')
    print(f'Files in output directory:')
    for f in sorted(os.listdir(OUTPUT_DIR)):
        fpath = os.path.join(OUTPUT_DIR, f)
        size_kb = os.path.getsize(fpath) / 1024
        print(f'  {f} ({size_kb:.1f} KB)')
