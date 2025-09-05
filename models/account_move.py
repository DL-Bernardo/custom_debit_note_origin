from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    origin_invoice_id = fields.Many2one(
        'account.move',
        string='Fatura de Origem',
        domain="[('move_type', '=', 'out_invoice'), ('partner_id', '=', partner_id), ('state', '=', 'posted')]",
        readonly=True,
        states={'draft': [('readonly', False)]},
        help="Selecione a fatura de origem associada ao cliente."
    )

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """Limpa o campo origin_invoice_id quando o cliente muda."""
        self.origin_invoice_id = False

    @api.onchange('journal_id')
    def _onchange_journal_id(self):
        """Mostra o campo origin_invoice_id apenas para o diário ND Nota de Débito."""
        if self.journal_id and self.journal_id.name == 'ND Nota de Débito':
            self.origin_invoice_id = False  # Limpa o campo ao mudar para este diário
        else:
            self.origin_invoice_id = False  # Garante que o campo seja limpo se o diário for diferente

    @api.constrains('journal_id', 'origin_invoice_id')
    def _check_origin_invoice_required(self):
        """Validação para garantir que o campo Fatura de Origem seja preenchido com o diário ND."""
        for record in self:
            if record.journal_id and record.journal_id.name == 'ND Nota de Débito' and not record.origin_invoice_id:
                raise ValidationError("Erro de Validação! Com o diário 'ND Nota de Débito' selecionado, o campo 'Fatura de Origem' na nota de débito deve ser preenchido.")

    def action_post(self):
        """Sobrescreve a validação de postagem para incluir a lógica personalizada."""
        for move in self:
            if move.journal_id and move.journal_id.name == 'ND Nota de Débito' and not move.origin_invoice_id:
                raise ValidationError("Erro de Validação! Com o diário 'ND Nota de Débito' selecionado, o campo 'Fatura de Origem' na nota de débito deve ser preenchido.")
        return super(AccountMove, self).action_post()