odoo.define('point_of_sale.CompanyLogo', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class CompanyLogo extends PosComponent {
        get company_name() {
            if (this.env.pos.company == null ) return 'Odoo';
            const name  = this.env.pos.company.name;
            console.log(name ? name : 'Odoo')
            return name ? name : 'Odoo';
        }
        get company_logo() {
            if (this.env.pos.company == null ) return '/web/binary/company_logo';
            const logo_b64 = this.env.pos.company_logo_base64;
            const logo = logo_b64 ? logo_b64 : '/web/binary/company_logo';
            return logo;
        }
    }
    CompanyLogo.template = 'CompanyLogo';

    Registries.Component.add(CompanyLogo);

    return CompanyLogo;
});
