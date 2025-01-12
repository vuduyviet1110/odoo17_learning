import { Component } from "@odoo/owl";

export class StudentForm extends Component {
  static template = "v_education.StudentFormTemplate";

  state = {
    name: "",
    student_code: "",
    gender: "male",
  };

  handleSubmit() {
    console.log("Submitted form data:", this.state);
  }
}
