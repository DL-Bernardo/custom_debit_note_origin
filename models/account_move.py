from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    origin_invoice_id = fields.Many2one(
        'account.move',
        string='Fatura de Origem',
        domain="[('move_type', '=', 'out_invoice'), ('partner_id', '=', partner_id), ('state', '=', 'posted')]",
        help="Selecione a fatura de origem associada ao cliente."
    )

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """Limpa o campo origin_invoice_id quando o cliente muda."""
        self.origin_invoice_id = False

    @api.constrains('journal_id', 'origin_invoice_id')
    def _check_origin_invoice_required(self):
        """Validação para garantir que o campo Fatura de Origem seja preenchido com o diário ND."""
        for record in self:
            if record.journal_id and record.journal_id.code == 'ND' and not record.origin_invoice_id:
                raise ValidationError("Com o diário 'ND Nota de Débito' selecionado, o campo 'Fatura de Origem' na nota de débito deve ser preenchido.")