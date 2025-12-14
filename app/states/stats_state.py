import reflex as rx
from typing import TypedDict
import datetime
import logging
from app.states.payment_state import PaymentState


class MonthlyStats(TypedDict):
    name: str
    usd: float
    bs: float


class DailyStats(TypedDict):
    date: str
    usd: float
    bs: float


class StatsState(rx.State):
    all_payments: list[dict] = []
    start_date: str = datetime.datetime.now().strftime("%Y-%m-%d")
    end_date: str = datetime.datetime.now().strftime("%Y-%m-%d")
    selected_method: str = "Todos"
    selected_currency: str = "Todos"

    @rx.var
    def today_metrics(self) -> dict:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        today_payments = [p for p in self.all_payments if p["date"] == today]
        return {
            "usd": sum(
                (p["amount"] for p in today_payments if p["currency"] == "USD ($)")
            ),
            "bs": sum(
                (
                    p["amount"]
                    for p in today_payments
                    if p["currency"] == "Bolívares (Bs)"
                )
            ),
            "count": len(today_payments),
        }

    @rx.var
    def monthly_revenue_data(self) -> list[MonthlyStats]:
        monthly_data = {}
        months = [
            "Ene",
            "Feb",
            "Mar",
            "Abr",
            "May",
            "Jun",
            "Jul",
            "Ago",
            "Sep",
            "Oct",
            "Nov",
            "Dic",
        ]
        current_year = datetime.datetime.now().year
        for m in months:
            monthly_data[m] = {"usd": 0.0, "bs": 0.0}
        for p in self.all_payments:
            try:
                p_date = datetime.datetime.strptime(p["date"], "%Y-%m-%d")
                if p_date.year == current_year:
                    month_idx = p_date.month - 1
                    month_name = months[month_idx]
                    if p["currency"] == "USD ($)":
                        monthly_data[month_name]["usd"] += p["amount"]
                    elif p["currency"] == "Bolívares (Bs)":
                        monthly_data[month_name]["bs"] += p["amount"]
            except Exception as e:
                logging.exception(f"Error processing payment for monthly stats: {e}")
        return [
            {"name": m, "usd": monthly_data[m]["usd"], "bs": monthly_data[m]["bs"]}
            for m in months
        ]

    @rx.var
    def filtered_payments(self) -> list[dict]:
        filtered = []
        for p in self.all_payments:
            if not self.start_date <= p["date"] <= self.end_date:
                continue
            if self.selected_method != "Todos" and p["method"] != self.selected_method:
                continue
            if (
                self.selected_currency != "Todos"
                and p["currency"] != self.selected_currency
            ):
                continue
            filtered.append(p)
        return filtered

    @rx.var
    def filtered_totals(self) -> dict:
        return {
            "usd": sum(
                (
                    p["amount"]
                    for p in self.filtered_payments
                    if p["currency"] == "USD ($)"
                )
            ),
            "bs": sum(
                (
                    p["amount"]
                    for p in self.filtered_payments
                    if p["currency"] == "Bolívares (Bs)"
                )
            ),
        }

    @rx.event
    async def load_data(self):
        payment_state = await self.get_state(PaymentState)
        self.all_payments = payment_state.payments

    @rx.event
    def set_start_date(self, date: str):
        self.start_date = date

    @rx.event
    def set_end_date(self, date: str):
        self.end_date = date

    @rx.event
    def set_method(self, method: str):
        self.selected_method = method

    @rx.event
    def set_currency(self, currency: str):
        self.selected_currency = currency