<%*
let d = moment(tp.file.title, "YYYY-MM-DD");
let q = "Q" + (Math.floor(d.month() / 3) + 1);
let w = d.isoWeek().toString().padStart(2, '0');
-%>
---
week: '[[<% d.format("YYYY") %>-W<% w %>]]'
date: '<% tp.file.title %>'
cssclasses:
  - hide-properties
  - daily
  <% "- " + moment(tp.file.title, "YYYY-MM-DD").locale("en").format("dddd").toLowerCase() %>
---

## [[<% d.format("YYYY")%>]] / [[<%d.format("YYYY")%>-<% q %>|<% q %>]] / [[<% d.format("YYYY-MM") %>|<% d.format("MMMM") %>]] / [[<% d.format("YYYY") %>-W<% w %>|Week <% d.isoWeek() %>]]
# DAILY NOTE
##### ❮ [[<% d.clone().subtract(1, 'days').format("YYYY-MM-DD") %>]] | <% tp.file.title %> | [[<% d.clone().add(1, 'days').format("YYYY-MM-DD") %>]] ❯
---
### 📕Freewrite




---
### ⚛️Items

#### Daily Tasks


#### Habits
- 🔠 \[english:: ]
- 🪥 \[teeth::]

#### 🥦Health
- 🥬\[vegetable::]

#### 💪Body
- 🏃‍♀‍➡\[workout::]

#### End-of-Day Checklist
