/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
const { Component, useState, onWillStart, useRef } = owl;

export class TodoList extends Component {
  setup() {
    this.state = useState({
      task: {
        name: "",
        color: "#FF0000",
        completed: false,
        description: "",
        category: "",
        student_id: null,
      },
      taskList: [],
      categories: ["work", "personal", "shopping", "others"],
      isEdit: false,
      activeId: false,
      filterCategory: "",
      studentFilter: "",
      sortBy: "name",
      sortDirection: "asc",
      currentPage: 1,
      itemsPerPage: 10,
      totalPages: 1,
      isLoading: false,
      students: [],
    });

    this.orm = useService("orm");
    this.searchInput = useRef("searchInput");
    this.model = "education.student.todolist";
    this.searchDebounceTimeout = null;

    onWillStart(async () => {
      await this.getAllTaskList();
      await this.getStudents();
    });
  }

  async filterTasks() {
    if (this.state.isLoading) return;

    const domain = [];
    if (this.state.filterCategory) {
      domain.push(["category", "=", this.state.filterCategory]);
    }
    await this.getAllTaskList(domain);
  }
  async studentFilter() {
    if (this.state.isLoading) return;

    const domain = [];
    if (this.state.studentFilter) {
      domain.push(["student_id.id", "=", this.state.studentFilter]);
    }
    console.log(domain);
    await this.getAllTaskList(domain);
  }

  // Tối ưu việc sắp xếp
  async sortTasks() {
    if (this.state.isLoading) return;

    const { sortBy, sortDirection } = this.state;
    const order = `${sortBy} ${sortDirection}`;
    await this.getAllTaskList([], order);
  }

  // Cập nhật trạng thái hoàn thành
  async toggleStatus(event, task) {
    const newCompletedStatus = event.target.checked;
    task.completed = newCompletedStatus;
    try {
      await this.orm.write(this.model, [task.id], { completed: newCompletedStatus });
    } catch (error) {
      console.error("Error updating task:", error);
    }
  }

  // Cập nhật màu sắc
  async updateColor(event, task) {
    const newColor = event.target.value;
    task.color = newColor;
    try {
      await this.orm.write(this.model, [task.id], { color: newColor });
    } catch (error) {
      console.error("Error updating color:", error);
    }
  }

  // Tối ưu hóa việc lấy dữ liệu
  async getAllTaskList(extraDomain = [], order = null) {
    if (this.state.isLoading) return;

    this.state.isLoading = true;
    const { currentPage, itemsPerPage } = this.state;
    const offset = (currentPage - 1) * itemsPerPage;

    try {
      const baseDomain = [];
      const domain = [...baseDomain, ...extraDomain]; // Combine baseDomain and filter conditions

      console.log("Final domain:", domain);

      const [tasks, totalTasks] = await Promise.all([
        this.orm.searchRead(
          this.model,
          domain,
          ["name", "color", "completed", "description", "category", "student_id"],
          {
            limit: itemsPerPage,
            offset: offset,
            order: order,
          }
        ),
        this.orm.searchCount(this.model, domain),
      ]);

      this.state.taskList = tasks || [];
      this.state.totalPages = Math.ceil(totalTasks / itemsPerPage);
    } catch (error) {
      console.error("Error fetching tasks:", error);
      this.state.taskList = [];
      this.state.totalPages = 1;
    } finally {
      this.state.isLoading = false;
    }
  }

  // Tối ưu việc tìm kiếm bằng debounce
  async searchTasks() {
    if (this.searchDebounceTimeout) {
      clearTimeout(this.searchDebounceTimeout);
    }

    this.searchDebounceTimeout = setTimeout(async () => {
      const searchText = this.searchInput.el.value;
      if (searchText.trim() === "") {
        await this.getAllTaskList();
        return;
      }

      const domain = [["name", "ilike", searchText]];
      await this.getAllTaskList(domain);
    }, 2000);
  }

  // Tối ưu việc xuất CSV
  async exportTasks() {
    if (this.state.isLoading) return;

    this.state.isLoading = true;
    try {
      const tasks = await this.orm.searchRead(
        this.model,
        [],
        ["name", "color", "completed", "description", "category"],
        { limit: 1000 }
      );

      if (!tasks.length) {
        alert("No tasks to export.");
        return;
      }

      const csvContent = this.generateCSV(tasks);
      this.downloadCSV(csvContent);
    } catch (error) {
      console.error("Error exporting tasks:", error);
      alert("Error exporting tasks");
    } finally {
      this.state.isLoading = false;
    }
  }

  generateCSV(tasks) {
    const headers = "No,Name,Description,Category,Completed\n";
    const rows = tasks
      .map(
        (task, index) =>
          `${index + 1},"${task.name || ""}","${task.description || ""}","${task.category || ""}",${
            task.completed || false
          }`
      )
      .join("\n");

    return "data:text/csv;charset=utf-8," + headers + rows;
  }

  downloadCSV(csvContent) {
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `tasks_${new Date().toISOString()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  async importTasks(file) {
    if (this.state.isLoading) return;

    this.state.isLoading = true;
    try {
      const tasks = await this.parseFile(file);

      if (tasks && tasks.length > 0) {
        await this.orm.create(this.model, tasks);
        await this.getAllTaskList();
      } else {
        alert("No tasks to import.");
      }
    } catch (error) {
      console.error("Error importing tasks:", error);
      alert("Error importing tasks");
    } finally {
      this.state.isLoading = false;
    }
  }

  parseFile(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const tasks = JSON.parse(reader.result);
        resolve(tasks);
      };
      reader.onerror = reject;
      reader.readAsText(file);
    });
  }

  // Các hàm CRUD cơ bản đã được tối ưu
  async saveTask() {
    if (this.state.isLoading || !this.state.task.name) return;

    this.state.isLoading = true;
    try {
      if (!this.state.isEdit) {
        await this.orm.create(this.model, [this.state.task]);
      } else {
        await this.orm.write(this.model, [this.state.activeId], this.state.task);
      }
      this.resetForm();
      await this.getAllTaskList();
    } catch (error) {
      console.error("Error saving task:", error);
      alert("Error saving task");
    } finally {
      this.state.isLoading = false;
    }
  }

  async deleteTask(task) {
    if (this.state.isLoading) return;

    if (!confirm("Are you sure you want to delete this task?")) return;

    this.state.isLoading = true;
    try {
      await this.orm.unlink(this.model, [task.id]);
      await this.getAllTaskList();
    } catch (error) {
      console.error("Error deleting task:", error);
      alert("Error deleting task");
    } finally {
      this.state.isLoading = false;
    }
  }

  // Lấy danh sách học sinh từ server
  async getStudents() {
    try {
      const students = await this.orm.searchRead("education.student", [], ["id", "name"]);
      this.state.students = students;
    } catch (error) {
      console.error("Error fetching students:", error);
    }
  }

  onStudentSelect(event) {
    const studentId = parseInt(event.target.value);
    const selectedStudent = this.state.students.find((student) => student.id === studentId);

    if (selectedStudent) {
      this.state.task.student_id = studentId;
      console.log("Selected student:", selectedStudent);
    } else {
      console.warn("Selected student not found!");
    }
  }

  // Các hàm helper
  resetForm() {
    this.state.task = {
      name: "",
      color: "#FF0000",
      completed: false,
      description: "",
      category: "",
    };
    this.state.isEdit = false;
    this.state.activeId = false;
  }

  addTask() {
    this.resetForm();
  }

  editTask(task) {
    this.state.isEdit = true;
    this.state.activeId = task.id;
    this.state.task = { ...task };
  }

  // Tối ưu việc chuyển trang
  async setPage(pageNumber) {
    if (this.state.isLoading) return;

    if (pageNumber >= 1 && pageNumber <= this.state.totalPages) {
      this.state.currentPage = pageNumber;
      await this.getAllTaskList();
    }
  }

  nextPage() {
    this.setPage(this.state.currentPage + 1);
  }

  prevPage() {
    this.setPage(this.state.currentPage - 1);
  }
}

TodoList.template = "v_education.VtodoList";

registry.category("actions").add("v_education.action_owl_student_todolist_js", TodoList);
