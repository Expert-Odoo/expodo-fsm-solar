from odoo import models, fields, api


class FsmOrder(models.Model):
    _inherit = "expodo.fsm.order"

    # Array / installation
    installation_type = fields.Selection(
        [
            ("residential_roof", "Residential rooftop"),
            ("commercial_roof", "Commercial rooftop"),
            ("ground_mount", "Ground-mounted"),
            ("carport", "Solar carport"),
            ("agrivoltaic", "Agrivoltaic"),
            ("floating", "Floating PV"),
            ("off_grid", "Off-grid system"),
            ("other", "Other"),
        ],
        string="Installation Type",
    )
    mounting_type = fields.Selection(
        [
            ("on_roof", "On-roof (rails)"),
            ("in_roof", "In-roof (integrated)"),
            ("flat_ballast", "Flat roof / ballast"),
            ("ground_screw", "Ground screw"),
            ("concrete", "Concrete footing"),
            ("tracker", "Tracker"),
            ("other", "Other"),
        ],
        string="Mounting",
    )
    panel_brand = fields.Char(string="Panel Brand")
    panel_model = fields.Char(string="Panel Model")
    panel_count = fields.Integer(string="Number of Panels")
    panel_wattage = fields.Integer(
        string="Panel Power (Wp)", help="Rated power of a single module, in watts-peak"
    )
    array_power_kwp = fields.Float(
        string="Array Power (kWp)",
        compute="_compute_array_power_kwp",
        store=True,
        help="Total installed peak power (panels x panel power)",
    )
    roof_azimuth = fields.Integer(
        string="Azimuth (deg)", help="Orientation of the array, degrees from south"
    )
    roof_tilt = fields.Integer(string="Tilt (deg)", help="Tilt angle of the modules")
    commissioning_date = fields.Date(string="Commissioning Date")

    # Inverter, storage and grid
    inverter_brand = fields.Char(string="Inverter Brand")
    inverter_model = fields.Char(string="Inverter Model")
    inverter_type = fields.Selection(
        [
            ("string", "String inverter"),
            ("micro", "Microinverters"),
            ("hybrid", "Hybrid inverter"),
            ("central", "Central inverter"),
            ("optimizer", "String + optimizers"),
        ],
        string="Inverter Type",
    )
    string_count = fields.Integer(string="Number of Strings")
    serial_number = fields.Char(string="Inverter Serial", index=True)
    battery_storage = fields.Boolean(string="Battery Storage")
    battery_capacity_kwh = fields.Float(string="Battery Capacity (kWh)")
    grid_connection = fields.Selection(
        [
            ("self_consumption", "Self-consumption"),
            ("surplus", "Self-consumption + surplus sale"),
            ("full_injection", "Full injection / sale"),
            ("off_grid", "Off-grid"),
        ],
        string="Grid Connection",
    )

    # Performance and electrical safety
    expected_yield_kwh = fields.Float(
        string="Expected Yield (kWh/yr)", help="Estimated annual production"
    )
    measured_power_kw = fields.Float(
        string="Measured Output (kW)", help="Measured AC power at the inverter during the job"
    )
    insulation_test_done = fields.Boolean(string="Insulation Test Passed")
    earthing_check_done = fields.Boolean(string="Earthing / Bonding Checked")
    string_test_done = fields.Boolean(string="String I-V Test Done")

    @api.depends("panel_count", "panel_wattage")
    def _compute_array_power_kwp(self):
        for rec in self:
            rec.array_power_kwp = (rec.panel_count or 0) * (rec.panel_wattage or 0) / 1000.0
