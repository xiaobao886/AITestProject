/**
 * 待办事项应用 - 主逻辑
 * 功能：增删改查、优先级、编辑、本地存储持久化
 */

(function () {
    "use strict";

    // ==================== 常量 ====================
    var STORAGE_KEY = "todo_app_tasks";

    // ==================== DOM 引用 ====================
    var taskInput      = document.getElementById("taskInput");
    var prioritySelect = document.getElementById("prioritySelect");
    var btnAdd         = document.getElementById("btnAdd");
    var btnClear       = document.getElementById("btnClear");
    var btnClearAll    = document.getElementById("btnClearAll");
    var taskListEl     = document.getElementById("taskList");
    var totalCountEl   = document.getElementById("totalCount");
    var pendingCountEl = document.getElementById("pendingCount");
    var completedCountEl = document.getElementById("completedCount");
    var dateDisplayEl  = document.getElementById("dateDisplay");

    // 确认弹窗
    var confirmModal   = document.getElementById("confirmModal");
    var modalIcon      = document.getElementById("modalIcon");
    var modalTitle     = document.getElementById("modalTitle");
    var modalMessage   = document.getElementById("modalMessage");
    var modalCancel    = document.getElementById("modalCancel");
    var modalConfirm   = document.getElementById("modalConfirm");

    // 编辑弹窗
    var editModal      = document.getElementById("editModal");
    var editInput      = document.getElementById("editInput");
    var editPriority   = document.getElementById("editPriority");
    var editCancel     = document.getElementById("editCancel");
    var editConfirm    = document.getElementById("editConfirm");

    // 当前正在编辑的任务 ID
    var editingTaskId = null;

    // ==================== 数据管理 ====================

    /**
     * 从 localStorage 读取任务列表
     * @returns {Array}
     */
    function loadTasks() {
        try {
            var data = localStorage.getItem(STORAGE_KEY);
            return data ? JSON.parse(data) : [];
        } catch (e) {
            return [];
        }
    }

    /**
     * 将任务列表保存到 localStorage
     * @param {Array} tasks
     */
    function saveTasks(tasks) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
    }

    // ==================== 工具函数 ====================

    function generateId() {
        return "task_" + Date.now() + "_" + Math.random().toString(36).substr(2, 9);
    }

    // ==================== 优先级 ====================

    var PRIORITY_MAP = {
        high:   { label: "高", order: 0 },
        medium: { label: "中", order: 1 },
        low:    { label: "低", order: 2 }
    };

    function priorityOrder(p) {
        return (PRIORITY_MAP[p] || PRIORITY_MAP.medium).order;
    }

    function priorityLabel(p) {
        return (PRIORITY_MAP[p] || PRIORITY_MAP.medium).label;
    }

    // ==================== 渲染 ====================

    function createEmptyState() {
        var div = document.createElement("div");
        div.className = "empty-state";
        div.innerHTML = '<div class="icon">🌈</div>' +
                        '<p class="empty-title">暂无待办事项</p>' +
                        '<p class="empty-sub">在上方输入你的第一个任务吧！</p>';
        return div;
    }

    function createTaskElement(task) {
        var priority = task.priority || "medium";

        var item = document.createElement("div");
        item.className = "task-item" +
                         (task.completed ? " completed" : "") +
                         " priority-" + priority;
        item.dataset.id = task.id;

        // 复选框
        var label = document.createElement("label");
        label.className = "task-checkbox";

        var checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = task.completed;
        checkbox.addEventListener("change", function () {
            toggleTask(task.id);
        });

        var checkmark = document.createElement("span");
        checkmark.className = "checkmark";

        label.appendChild(checkbox);
        label.appendChild(checkmark);

        // 任务文本
        var textSpan = document.createElement("span");
        textSpan.className = "task-text";
        textSpan.textContent = task.text;

        // 优先级标签
        var badge = document.createElement("span");
        badge.className = "priority-badge " + priority;
        badge.textContent = priorityLabel(priority);

        // 操作按钮组
        var actions = document.createElement("div");
        actions.className = "task-actions";

        // 编辑按钮
        var editBtn = document.createElement("button");
        editBtn.className = "btn-edit";
        editBtn.title = "编辑";
        editBtn.textContent = "✏️";
        editBtn.addEventListener("click", function () {
            openEditModal(task.id);
        });

        // 删除按钮
        var deleteBtn = document.createElement("button");
        deleteBtn.className = "btn-delete";
        deleteBtn.title = "删除";
        deleteBtn.textContent = "✕";
        deleteBtn.addEventListener("click", function () {
            deleteTask(task.id);
        });

        actions.appendChild(editBtn);
        actions.appendChild(deleteBtn);

        item.appendChild(label);
        item.appendChild(textSpan);
        item.appendChild(badge);
        item.appendChild(actions);

        return item;
    }

    function renderTasks(newTaskId) {
        var tasks = loadTasks();

        taskListEl.innerHTML = "";

        if (tasks.length === 0) {
            taskListEl.appendChild(createEmptyState());
        } else {
            for (var i = 0; i < tasks.length; i++) {
                var item = createTaskElement(tasks[i]);
                if (tasks[i].id === newTaskId) {
                    item.classList.add("animate-in");
                }
                taskListEl.appendChild(item);
            }
        }

        updateStats(tasks);
    }

    function updateStats(tasks) {
        var total = tasks.length;
        var completed = 0;
        for (var i = 0; i < tasks.length; i++) {
            if (tasks[i].completed) completed++;
        }
        totalCountEl.textContent     = total;
        pendingCountEl.textContent   = total - completed;
        completedCountEl.textContent = completed;
    }

    // ==================== 弹窗 ====================

    function showConfirmModal(icon, title, message, onConfirm) {
        modalIcon.textContent    = icon;
        modalTitle.textContent   = title;
        modalMessage.textContent = message;
        confirmModal.classList.add("active");

        // 清除旧监听
        var newConfirm = modalConfirm.cloneNode(true);
        modalConfirm.parentNode.replaceChild(newConfirm, modalConfirm);
        modalConfirm = newConfirm;

        var newCancel = modalCancel.cloneNode(true);
        modalCancel.parentNode.replaceChild(newCancel, modalCancel);
        modalCancel = newCancel;

        modalConfirm.addEventListener("click", function () {
            confirmModal.classList.remove("active");
            onConfirm();
        });
        modalCancel.addEventListener("click", function () {
            confirmModal.classList.remove("active");
        });
    }

    function openEditModal(id) {
        var tasks = loadTasks();
        var task = null;
        for (var i = 0; i < tasks.length; i++) {
            if (tasks[i].id === id) { task = tasks[i]; break; }
        }
        if (!task) return;

        editingTaskId = id;
        editInput.value = task.text;
        editPriority.value = task.priority || "medium";
        editModal.classList.add("active");

        setTimeout(function () { editInput.focus(); editInput.select(); }, 100);
    }

    function closeEditModal() {
        editModal.classList.remove("active");
        editingTaskId = null;
    }

    function saveEdit() {
        if (!editingTaskId) return;
        var newText = editInput.value.trim();
        if (!newText) return;

        var tasks = loadTasks();
        for (var i = 0; i < tasks.length; i++) {
            if (tasks[i].id === editingTaskId) {
                tasks[i].text = newText;
                tasks[i].priority = editPriority.value;
                break;
            }
        }
        saveTasks(tasks);
        closeEditModal();
        renderTasks();
    }

    // ==================== 操作 ====================

    function addTask() {
        var text = taskInput.value.trim();
        if (!text) return;

        var tasks = loadTasks();
        var newTask = {
            id: generateId(),
            text: text,
            priority: prioritySelect.value,
            completed: false,
            createdAt: Date.now()
        };

        tasks.unshift(newTask);
        saveTasks(tasks);

        taskInput.value = "";
        prioritySelect.value = "medium";
        taskInput.focus();

        renderTasks(newTask.id);
    }

    function toggleTask(id) {
        var tasks = loadTasks();
        for (var i = 0; i < tasks.length; i++) {
            if (tasks[i].id === id) {
                tasks[i].completed = !tasks[i].completed;
                break;
            }
        }
        saveTasks(tasks);
        renderTasks();
    }

    function deleteTask(id) {
        var tasks = loadTasks();
        var remaining = [];
        for (var i = 0; i < tasks.length; i++) {
            if (tasks[i].id !== id) remaining.push(tasks[i]);
        }
        saveTasks(remaining);
        renderTasks();
    }

    function clearCompleted() {
        var tasks = loadTasks();
        var remaining = [];
        for (var i = 0; i < tasks.length; i++) {
            if (!tasks[i].completed) remaining.push(tasks[i]);
        }
        if (remaining.length === tasks.length) return;
        saveTasks(remaining);
        renderTasks();
    }

    function clearAll() {
        var tasks = loadTasks();
        if (tasks.length === 0) return;

        showConfirmModal(
            "⚠️",
            "确认全部清空",
            "此操作将删除所有 " + tasks.length + " 个任务，且无法恢复。确定要继续吗？",
            function () {
                saveTasks([]);
                renderTasks();
            }
        );
    }

    // ==================== 初始化 ====================

    function init() {
        // 显示当前日期
        var now = new Date();
        var weekdays = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
        var dateStr = now.getFullYear() + "年" +
                      (now.getMonth() + 1) + "月" +
                      now.getDate() + "日 " +
                      weekdays[now.getDay()];
        dateDisplayEl.textContent = dateStr;

        // 绑定事件
        btnAdd.addEventListener("click", addTask);
        btnClear.addEventListener("click", clearCompleted);
        btnClearAll.addEventListener("click", clearAll);

        editCancel.addEventListener("click", closeEditModal);
        editConfirm.addEventListener("click", saveEdit);

        // 点击弹窗遮罩关闭
        editModal.addEventListener("click", function (e) {
            if (e.target === editModal) closeEditModal();
        });
        confirmModal.addEventListener("click", function (e) {
            if (e.target === confirmModal) confirmModal.classList.remove("active");
        });

        // 编辑弹窗回车保存
        editInput.addEventListener("keydown", function (e) {
            if (e.key === "Enter") saveEdit();
        });

        // 添加任务回车
        taskInput.addEventListener("keydown", function (e) {
            if (e.key === "Enter") addTask();
        });

        renderTasks();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }

})();
