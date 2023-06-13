odoo.define('solse_vat_pos_pe.PartnerListScreen', function(require) {
	'use strict';

	const PartnerListScreen = require('point_of_sale.PartnerListScreen');
	const Registries = require('point_of_sale.Registries');
	const session = require('web.session');
	const core = require('web.core');
	const _t = core._t;
	const rpc = require('web.rpc');
	const QWeb = core.qweb;
	const { onMounted } = owl;

	const PartnerListScreenVat = (PartnerListScreen) =>
		class extends PartnerListScreen {
			setup() {
				super.setup();
			}
			constructor() {
				super(...arguments);
			}
			async updatePartnerList(event) {
				var self = this;
	            this.state.query = event.target.value;
	            this.render(true);
	            if (event.key === "Enter" || event.keyCode === 13) {
					let tipo = this.validarDocumento(this.state.query)
					let datos = this.partners
					if (datos.length == 0 && tipo) {
						let parametros = [tipo, this.state.query]
						let rpt1 = await rpc.query({
							model: 'res.partner',
							method: 'consulta_datos_externos',
							args: parametros,
						})
						if(rpt1) {
							if(datos) {
								await self.env.pos.load_new_partners();
                				self.state.selectedPartner = self.env.pos.db.get_partner_by_id(datos);
							} else {
								alert("No se pudo completar la operación")
							}
						}
					}
				}
	        }
	        validarDocumento(parametro) {
				if (typeof parametro === "number" || /^\d+$/.test(parametro)) {
					const parametroString = parametro.toString();
					if (parametroString.length === 11) {
						return "ruc";
					} else if (parametroString.length === 8) {
						return "dni";
					}
				}
				return false;
			}

		};

	Registries.Component.extend(PartnerListScreen, PartnerListScreenVat);

	return PartnerListScreen;
});
