---
cssclasses:
  - home-page
  - hide-properties
---
## 🗓️ 任务看板 

>[!multi-column]
>
>> [!success] ☀️ 今日计划
>> ```tasks
>> not done
>> due today
>> # 隐藏多余的标记让界面更整洁
>> hide due date
>> hide task count
>> hide backlink
>> ```
>
>> [!warning] ⏳ 延期计划
>> ```tasks
>> not done
>> due before today
>> # 按过期天数排序，先解决拖延最久的
>> sort by due
>> hide task count
>> hide backlink
>> ```

---
## 🏅 任务复盘 (To-Do List)

> [!multi-column]
>
>> [!success] 🌟 本周完成任务
>> ```tasks
>> done this week
>> hide due date
>> hide backlink
>> hide task count
>> ```
>
>> [!info] 🏆 本月完成任务
>> ```tasks
>> done this month
>> hide due date
>> hide backlink
>> hide task count
>> ```

---
## DDL

> [!multi-column]
>
>> [!important] 🚨 DDL 
>> ```tasks
>> not done
>> has due date
>> path includes To do list
>> sort by due
>> hide backlink
>> ```
>
>> [!todo] 📥 To do
>> ```tasks
>> not done
>> no due date
>> no start date
>> no scheduled date
>> sort by priority
>> hide backlink
>> ```

---
## 🚀 项目全局 

>[!multi-column]
>> [!macro]  进行中
>> ```dataview
>> LIST 
>> WHERE type = "project" AND status = "Doing"
>> SORT file.mtime DESC
>> ```
  > 
>> [!todo]  未开始
>> ```dataview
>> LIST 
>> WHERE type = "project" AND status = "plan"
>> SORT file.mtime DESC
>> ```
>
>> [!done]  已完成
>> ```dataview
>> LIST 
>> WHERE type = "project" AND status = "Done"
>> SORT file.mtime DESC
>> ```
