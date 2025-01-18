/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

const { Component, useState, onWillStart } = owl;

export class StudentForm extends Component {
  setup() {
    this.state = useState({ count: 0 });
  }

  increment() {
    this.state.count++;
  }

  decrement() {
    this.state.count--;
  }
}

StudentForm.template = "v_education.owl_api_student_view";

registry.category("actions").add("v_education.StudentForm", StudentForm);
