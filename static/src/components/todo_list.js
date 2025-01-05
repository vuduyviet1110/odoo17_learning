/** @odoo-module **/

import { registry } from "@web/core/registry";
const { Component, useState, onWillStart, useRef } = owl;
import { useService } from "@web/core/utils/hooks";
export class TodoList extends Component {
  setup() {
    this.state = useState({
      task: { name: "", color: "#FF0000", completed: false },
      taskList: [],
      isEdit: false,
      activeId: false,
    });

    this.orm = useService("orm");
    this.searchInput = useRef("searchInput");
    this.model = "education.student.todolist";

    onWillStart(async () => {
      await this.getAllTaskList();
    });
  }
  async getAllTaskList() {
    this.state.taskList = await this.orm.searchRead(this.model, [], ["name", "color", "completed"]);
  }

  addTask() {
    this.resetForm();
    this.state.activeId = false;
    this.state.isEdit = false;
  }
  editTask(task) {
    this.state.isEdit = true;
    this.state.activeId = task.id;
    this.state.task = { name: task.name, color: task.color, completed: task.completed };
  }
  async saveTask() {
    if (!this.state.isEdit) {
      await this.orm.create(this.model, [
        { name: this.state.task.name, color: this.state.task.color, completed: this.state.task.completed },
      ]);
    } else {
      await this.orm.write(this.model, [this.state.activeId], this.state.task);
    }
    await this.getAllTaskList();
  }
  resetForm() {
    this.state.task = { name: "", color: "#FF0000", completed: false };
  }

  async deleteTask(task) {
    await this.orm.unlink(this.model, [task.id]);
    await this.getAllTaskList();
  }
  async searchTasks() {
    const text = this.searchInput.el.value;
    this.state.taskList = await this.orm.searchRead(
      this.model,
      [["name", "ilike", text]],
      ["name", "color", "completed"]
    );
  }
  async toggleTask(e, task) {
    await this.orm.write(this.model, [task.id], { completed: e.target.checked });
    await this.getAllTaskList();
  }
  async updateColor(e, task) {
    await this.orm.write(this.model, [task.id], { color: e.target.val });
    await this.getAllTaskList();
  }
}

TodoList.template = "v_education.VtodoList";

// Đăng ký vào registry actions
registry.category("actions").add("v_education.action_owl_student_todolist_js", TodoList);
