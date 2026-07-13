# Agnes 项目结构说明

## 项目概述
Agnes 是一个基于 iOS 平台的 Swift 应用，采用 Clean Architecture with MVVM-C 架构模式，使用 RxSwift 进行响应式编程。

## 代码规范
https://alexcode2.gitbook.io/ios-development-guidelines/swiftbian-ma-gui-fan

## 开发注意事项
- 图片资源推荐通过命名空间方式引用，保持统一的 `Assets.SomeImage` 访问入口，避免硬编码字符串
- 图片素材默认使用 PDF 矢量格式，便于适配不同分辨率和深色模式
- 新功能优先选择 `UICollectionView` 构建列表或瀑布流布局，减少 `UITableView` 的使用，保持交互一致性


## 项目根目录结构

```
Agnes/
├── Agnes.xcodeproj/          # Xcode 项目文件
├── Agnes/                    # 主应用代码目录
├── fastlane/                # 自动化构建和部署配置
├── build/                   # 构建输出目录
└── *.md                     # 文档文件
```

## 主应用目录结构 (Agnes/)

### 📁 Application/
应用程序入口和基础配置
- `AppDelegate.swift` - 应用程序生命周期管理
- `SceneDelegate.swift` - 场景生命周期管理
- `Application.swift` - 应用程序配置
- `Navigator.swift` - 导航管理器

### 📁 Models/
数据模型层
- `Account.swift` - 账户模型
- `Conversation.swift` - 对话模型
- `UserInfo.swift` - 用户信息模型
- `Token.swift` - 令牌模型
- `Home.swift` - 首页数据模型
- 其他业务相关模型...

### 📁 Modules/
功能模块层 (MVVM 架构)
每个模块包含 View、ViewController、ViewModel 三层

#### 🏠 Home/
首页模块
- `HomeView.swift` - 首页视图
- `HomeViewController.swift` - 首页控制器
- `HomeViewModel.swift` - 首页视图模型
- `WaterfallLayout.swift` - 瀑布流布局

#### 💬 Conversation/
对话模块
- `ConversationView.swift` - 对话视图
- `ConversationViewController.swift` - 对话控制器
- `ConversationViewModel.swift` - 对话视图模型
- `ConversationMessageParser/` - 消息解析器
- `Markdown/` - Markdown 渲染相关组件

#### 📝 ConversationInput/
对话输入模块
- `ConversationInputController.swift` - 输入控制器
- `ConversationInputView.swift` - 输入视图
- `ConversationInputViewModel.swift` - 输入视图模型

#### 👤 Account/
账户管理模块
- `AccountView.swift` - 账户视图
- `AccountViewController.swift` - 账户控制器
- `AccountViewModel.swift` - 账户视图模型
- `LanguageView.swift` - 语言设置视图
- `AccountAlert/` - 账户相关弹窗
- `ChangeUsername/` - 用户名修改功能

#### 🔐 SignIn/SignUp/
登录注册模块
- `SignInView.swift` - 登录视图
- `SignInViewController.swift` - 登录控制器
- `SignInViewModel.swift` - 登录视图模型
- `SignInStrategy/` - 登录策略模式实现
  - `AppleSignInStrategy.swift` - Apple 登录策略
  - `GoogleSignInStrategy.swift` - Google 登录策略
- `OtherSignIn/` - 其他登录方式

#### 🔄 ResetPassword/
密码重置模块
- `ResetPasswordView.swift` - 重置密码视图
- `ResetPasswordViewController.swift` - 重置密码控制器
- `ResetPasswordViewModel.swift` - 重置密码视图模型
- `ResetPasswordConfirm/` - 密码重置确认

#### 🔍 Search/
搜索模块
- `SearchView.swift` - 搜索视图
- `SearchViewController.swift` - 搜索控制器
- `SearchViewModel.swift` - 搜索视图模型

#### 📱 SideMenu/
侧边菜单模块
- `SideMenuView.swift` - 侧边菜单视图
- `SideMenuViewController.swift` - 侧边菜单控制器
- `SideMenuViewModel.swift` - 侧边菜单视图模型

#### 🐛 Debug/
调试模块
- `DebugView.swift` - 调试视图
- `DebugViewController.swift` - 调试控制器
- `DebugViewModel.swift` - 调试视图模型
- `Log/` - 日志相关功能

#### 其他模块
- `NewProject/` - 新建项目
- `ConversationWeb/` - Web 对话
- `Publish/` - 发布功能

### 📁 Common/
通用 UI 组件库
- `Button.swift` - 自定义按钮组件
- `Label.swift` - 自定义标签组件
- `View.swift` - 基础视图组件
- `ViewController.swift` - 基础控制器
- `NavigationController.swift` - 自定义导航控制器
- `TableView.swift` - 自定义表格视图
- `CollectionView.swift` - 自定义集合视图
- `LoadingHUD.swift` - 加载指示器
- `ToastMessage.swift` - 消息提示
- 其他通用 UI 组件...

### 📁 Extensions/
扩展类
- `String+AIProject.swift` - String 扩展
- `UIView/` - UIView 相关扩展
- `UIColor/` - UIColor 相关扩展
- `RxSwift/` - RxSwift 相关扩展
- 其他类型扩展...

### 📁 Networking/
网络层
- `Api.swift` - API 接口定义
- `Rest/` - REST API 实现
  - `Networking.swift` - 网络请求封装
  - `RestApi.swift` - REST API 具体实现
  - `***API.swift` - 角色相关 API
  - `StreamNetworking.swift` - 流式网络请求
  - `ErrorResponse.swift` - 错误响应处理

### 📁 Managers/
管理器类
- `AuthManager.swift` - 认证管理器
- `ThemeManager.swift` - 主题管理器
- `LogManager.swift` - 日志管理器
- `ToastManager.swift` - 消息提示管理器
- `TimerManager.swift` - 定时器管理器
- `Reachability.swift` - 网络状态监控

### 📁 Utils/
工具类
- `SSEClient.swift` - Server-Sent Events 客户端
- `SSEParser.swift` - SSE 解析器
- `MarkdownParser.swift` - Markdown 解析器
- `ContextMenuHelper.swift` - 上下文菜单助手

### 📁 Resources/
资源文件
- `Assets.xcassets/` - 图片资源
- `*.lproj/` - 多语言支持文件
  - `en.lproj/` - 英文
  - `zh-Hans.lproj/` - 简体中文
  - `vi.lproj/` - 越南语
  - `th.lproj/` - 泰语
  - 其他语言...
- `animation/` - 动画文件
- `*.json` - 配置文件
- `LaunchScreen.storyboard` - 启动屏
- `Main.storyboard` - 主故事板

### 📁 Configs/
配置文件
- `Configs.swift` - 应用配置

### 📁 Third Party/
第三方代码
- `RxActivityIndicator/` - RxSwift 活动指示器
- `RxErrorTracker/` - RxSwift 错误跟踪器
- `RxImagePicker/` - RxSwift 图片选择器

## 主要技术栈

### 核心框架
- **Swift** - 主要开发语言
- **UIKit** - UI 框架
- **RxSwift** - 响应式编程框架

### 网络通信
- **Moya** - 网络抽象层
- **Alamofire** - HTTP 网络库

### UI 组件
- **SnapKit** - 自动布局
- **Kingfisher** - 图片加载和缓存
- **Toast-Swift** - 消息提示
- **MJRefresh** - 下拉刷新
- **SideMenu** - 侧边菜单
- **Lottie** - 动画框架

### 工具库
- **SwiftyJSON** - JSON 解析
- **SwifterSwift** - Swift 扩展集合
- **DateToolsSwift** - 日期处理
- **KeychainAccess** - 钥匙串访问
- **DeviceKit** - 设备信息

### 开发工具
- **SwiftLint** - 代码规范检查
- **SwiftyBeaver** - 日志框架
- **LookinServer** - UI 调试工具

### 第三方登录
- **GoogleSignIn** - Google 登录
- **FirebaseAuth** - Firebase 认证

## 架构特点

1. **MVVM 架构模式** - 清晰的数据流和职责分离
2. **响应式编程** - 使用 RxSwift 处理异步操作和数据绑定
3. **模块化设计** - 每个功能模块独立，便于维护和扩展
4. **多语言支持** - 支持多种语言本地化
5. **策略模式** - 登录功能使用策略模式支持多种登录方式
6. **依赖管理** - 使用 Swift Package Manager(SPM) 管理第三方依赖

## 开发和构建

- **依赖管理**: Swift Package Manager(SPM)
- **最低支持**: iOS 16.0
- **自动化**: Fastlane 用于构建和部署
- **代码质量**: SwiftLint 保证代码规范
