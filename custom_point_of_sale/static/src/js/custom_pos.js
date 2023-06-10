odoo.define('custom_point_of_sale.custom_pos', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var gui = require('point_of_sale.gui');

    models.load_fields('res.partner', ['l10n_pe_district_id']);

    var ClientDetailsEditWidget = require('point_of_sale.screens').ClientDetailsEditWidget;
    ClientDetailsEditWidget.include({
        save_client_details: function() {
            var self = this;
            var res = this._super();

            if (this.editing_client) {
                var district = this.$('#district').val();
                this.editing_client.l10n_pe_district_id = district;
            }

            return res;
        },
    });

    gui.Gui.include({
        show_screen: function(screen_name, params, refresh, skip_close_popup) {
            if (screen_name === 'clientlist') {
                models.load_fields('res.partner', ['l10n_pe_district_id']);
            }

            return this._super(screen_name, params, refresh, skip_close_popup);
        },
    });
});
