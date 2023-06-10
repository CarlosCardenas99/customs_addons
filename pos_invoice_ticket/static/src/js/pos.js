odoo.define('pos_invoice_ticket', function (require) {
    "use strict";
    var core = require('web.core');
    var screens = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');
    var models = require('point_of_sale.models');

    PaymentScreenWidget.include({
        renderElement: function () {
            this._super();
            var self = this;
            this.$('.js_boleta').click(function () {
                self.order.set_type_document('b');
                self.$('.js_boleta').addClass('highlight');
                self.$('.js_factura').removeClass('highlight');
            });
            this.$('.js_factura').click(function () {
                self.order.set_type_document('f');
                self.$('.js_factura').addClass('highlight');
                self.$('.js_boleta').removeClass('highlight');
            });
        },
    });
});
