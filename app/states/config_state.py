import reflex as rx
import datetime
import logging
from currency_rate_bcv.currency import Currency


class ConfigState(rx.State):
    exchange_rate: float = 35.0
    last_updated: str = "No actualizado"
    use_manual_rate: bool = False
    manual_rate: float = 0.0
    is_loading_rate: bool = False

    @rx.var
    def active_rate(self) -> float:
        return (
            self.manual_rate
            if self.use_manual_rate and self.manual_rate > 0
            else self.exchange_rate
        )

    @rx.event(background=True)
    async def fetch_bcv_rate(self):
        async with self:
            self.is_loading_rate = True
        try:
            currency = Currency()
            rate_value = await currency.getDollar
            async with self:
                if rate_value:
                    if isinstance(rate_value, str):
                        rate_value = rate_value.replace(",", ".")
                    self.exchange_rate = float(rate_value)
                    self.last_updated = datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    rx.toast.success(f"Tasa BCV actualizada: {self.exchange_rate} Bs/$")
        except Exception as e:
            logging.exception(f"Error fetching BCV rate: {e}")
            async with self:
                rx.toast.error(
                    "Error al obtener tasa del BCV. Intentando usar valor en caché o manual."
                )
        finally:
            async with self:
                self.is_loading_rate = False

    @rx.event
    def toggle_manual_mode(self, value: bool):
        self.use_manual_rate = value

    @rx.event
    def set_manual_rate(self, value: str):
        if not value:
            return
        try:
            self.manual_rate = float(value)
        except ValueError as e:
            logging.exception(f"Error: {e}")