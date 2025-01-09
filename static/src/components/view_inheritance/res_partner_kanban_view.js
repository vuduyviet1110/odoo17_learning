/** @odoo-module **/

import { registry } from "@web/core/registry";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { KanbanController } from "@web/views/kanban/kanban_controller";
import { useService } from "@web/core/utils/hooks";

const { onWillStart } = owl;

class ResPartnerKanbanController extends KanbanController {
  setup() {
    super.setup();
    this.action = useService("action");
    this.orm = useService("orm");

    onWillStart(async () => {
      this.customerLocations = await this.orm.readGroup("res.partner", [], ["state_id"], ["state_id"]);
      console.log("Customer Locations:", this.customerLocations);
    });
  }

  openSaleView() {
    return this.action.doAction({
      type: "ir.actions.act_window",
      name: "Customer Sale",
      res_model: "sale.order",
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }
}

// Định nghĩa view mới kế thừa từ kanbanView
export const resPartnerKanbanView = {
  ...kanbanView,
  Controller: ResPartnerKanbanController,
  buttonTemplate: "v_education.ResPartnerKanbanView.Buttons",
};

// Đăng ký view mới
registry.category("views").add("res_partner_kanban", resPartnerKanbanView);
