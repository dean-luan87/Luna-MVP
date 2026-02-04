# JavaScript 代码规范

本文档定义了项目中 JavaScript 代码的编码规范，旨在避免语法错误并提高代码质量。

## 1. 异步代码规范

### 规则
- **必须在 `async` 函数或 ES 模块顶层才可使用 `await`**
- **否则应使用 `.then()/.catch()` 链式处理**
- 尽可能统一异步操作的写法，避免混合不同风格

### 示例

✅ **正确**：
```javascript
// 方式1：使用 async/await
async function fetchData() {
    const response = await fetch('/api/data');
    const data = await response.json();
    return data;
}

// 方式2：使用 Promise 链（非 async 函数中）
function fetchData() {
    return fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            return data;
        })
        .catch(err => {
            console.error('错误:', err);
        });
}
```

❌ **错误**：
```javascript
// 在非 async 函数中使用 await
function fetchData() {
    const response = await fetch('/api/data'); // ❌ 语法错误
    return response.json();
}
```

## 2. 字符串和注释规范

### 规则
- **单引号或双引号字符串不可跨行**
- **任何中文说明或文档文字必须置于注释中（以 `//` 或 `/* */` 开头）**
- **避免使用全角符号（：、（、）等）作为代码元素**
- **长文本应使用模板字符串（反引号 `` ` ``）**

### 示例

✅ **正确**：
```javascript
// 使用模板字符串（推荐）
showError(`⚠️ Safari 浏览器需要 HTTPS 才能访问摄像头。

解决方案：
1. 使用"选择图片"功能代替摄像头
2. 或配置 HTTPS 访问`);

// 单行字符串
showError('简单的错误消息');

// 注释中的中文
// 优化：提高检测频率
const FRAME_SKIP = 3;
```

❌ **错误**：
```javascript
// 单引号字符串跨行（语法错误）
showError('⚠️ Safari浏览器需要HTTPS才能访问摄像头。\\n\\n解决方案：\\n1.
使用"选择图片"功能代替摄像头\\n2. 或配置HTTPS访问'); // ❌

// 裸露的中文文本（语法错误）
优化：提高检测频率 // ❌
const FRAME_SKIP = 3;

// 全角符号在代码中
const errorMsg = '错误：无法访问'; // ❌ 应使用半角 :
```

## 3. 函数暴露规范

### 规则
- **需要在 HTML 中通过 `onclick` 调用的函数，应在文件顶层定义并显式赋值给 `window` 对象**

### 示例

✅ **正确**：
```javascript
function startProductMode() {
    // 函数实现
    console.log('启动产品模式');
}

// 显式暴露到全局作用域
window.startProductMode = startProductMode;

// 或者在函数内部暴露
function switchTab(tabName, event) {
    window.switchTab = switchTab; // 确保暴露
    // 函数实现
}
```

❌ **错误**：
```javascript
// 未暴露到 window，HTML 中的 onclick 无法访问
function startProductMode() {
    // 函数实现
}
// ❌ onclick="startProductMode()" 会报错：startProductMode is not defined
```

## 4. 检查工具和校验

### 规则
- 在保存并部署代码前使用 ESLint/Prettier 等工具检查格式和语法错误
- 利用 Node 的 `--check` 选项检查语法
- 使用浏览器开发者工具的"跳转到源码"功能定位错误

### 检查清单
- [ ] 括号匹配：`{ }`、`( )`、`[ ]`
- [ ] 模板字符串匹配：反引号数量为偶数
- [ ] 所有 `await` 都在 `async` 函数中
- [ ] 所有需要全局访问的函数都暴露到 `window`
- [ ] 没有裸露的中文文本（不在注释或字符串中）
- [ ] 没有全角符号在代码中（注释除外）

## 5. 统一错误消息处理

### 规则
- 为不同场景定义统一的错误提示函数
- 集中放置所有提示文本，便于后期维护和国际化
- 使用字符串模板或数组拼接方式生成多语言内容

### 示例

✅ **推荐**：
```javascript
// 定义错误消息常量
const ERROR_MESSAGES = {
    SAFARI_HTTPS_CAMERA: `⚠️ Safari 浏览器需要 HTTPS 才能访问摄像头。

解决方案：
1. 使用"选择图片"功能代替摄像头
2. 或配置 HTTPS 访问`,
    
    SAFARI_HTTPS_MIC: `⚠️ Safari 浏览器需要 HTTPS 才能访问麦克风。

当前功能受限，建议使用桌面浏览器测试。`
};

// 使用
showError(ERROR_MESSAGES.SAFARI_HTTPS_CAMERA);
```

## 6. 代码审查检查点

在提交代码前，请检查：

1. ✅ 所有异步操作是否正确处理（`async/await` 或 `.then()/.catch()`）
2. ✅ 所有字符串是否正确闭合（单引号、双引号、模板字符串）
3. ✅ 所有中文文本是否在注释或字符串中
4. ✅ 所有需要全局访问的函数是否暴露到 `window`
5. ✅ 没有全角符号在代码中（注释中的全角符号应统一格式）
6. ✅ 括号、引号、模板字符串是否匹配
7. ✅ 长文本是否使用模板字符串

## 7. 常见错误和修复

### 错误1：await 不在 async 函数中
```javascript
// ❌ 错误
function fetchData() {
    const data = await fetch('/api/data');
}

// ✅ 修复
function fetchData() {
    return fetch('/api/data')
        .then(response => response.json());
}
```

### 错误2：字符串跨行
```javascript
// ❌ 错误
showError('⚠️ Safari浏览器需要HTTPS才能访问摄像头。\\n\\n解决方案：\\n1.
使用"选择图片"功能代替摄像头\\n2. 或配置HTTPS访问');

// ✅ 修复
showError(`⚠️ Safari 浏览器需要 HTTPS 才能访问摄像头。

解决方案：
1. 使用"选择图片"功能代替摄像头
2. 或配置 HTTPS 访问`);
```

### 错误3：裸露的中文文本
```javascript
// ❌ 错误
优化：提高检测频率
const FRAME_SKIP = 3;

// ✅ 修复
// 优化：提高检测频率
const FRAME_SKIP = 3;
```

### 错误4：函数未暴露
```javascript
// ❌ 错误
function startProductMode() {
    // 实现
}
// HTML: <button onclick="startProductMode()"> 会报错

// ✅ 修复
function startProductMode() {
    window.startProductMode = startProductMode;
    // 实现
}
```

---

**最后更新**: 2024-11-14
**维护者**: 开发团队


