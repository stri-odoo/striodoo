// window.onload = function() {
// 	document.getElementsByClassName("js_invoice").click();
// }
document.getElementsByClassName("pay").onclick = function(){alert('TEST')}

/* odoo.define('pos_receipt_discount.PaymentScreen', function(require) {
	'use strict';
	console.log("Ento en el archivo")
	
	const PaymentScreen = require('point_of_sale.PaymentScreenWidget');
	const Registries = require('point_of_sale.Registries');


	const InvoiceButtonPaymentScreen = (PaymentScreen) =>
		class extends PaymentScreen {
		constructor() {
			super(...arguments);
			this.toggleIsToInvoice();
		}
	}

	Registries.Component.extend(PaymentScreen, InvoiceButtonPaymentScreen);
	return InvoiceButtonPaymentScreen;
}); */