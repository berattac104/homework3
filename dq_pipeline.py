import sys
import pandas as pd
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError, field_validator

CSV_PATH = "data/amazon_orders.csv"


class AmazonOrder(BaseModel):
    order_id: str = Field(min_length=1)
    qty: int = Field(ge=0)
    amount: float = Field(ge=0)
    currency: str
    ship_country: str
    date: str

    @field_validator("currency")
    @classmethod
    def currency_must_be_inr(cls, v):
        if v != "INR":
            raise ValueError("currency must be INR")
        return v

    @field_validator("ship_country")
    @classmethod
    def country_must_be_in(cls, v):
        if v != "IN":
            raise ValueError("ship_country must be IN")
        return v

    @field_validator("date")
    @classmethod
    def date_format_check(cls, v):
        datetime.strptime(v, "%m-%d-%y")
        return v


def main():
    df = pd.read_csv(CSV_PATH, low_memory=False)

    valid_count = 0
    invalid_count = 0

    for _, row in df.iterrows():
        try:
            AmazonOrder(
                order_id=row.get("Order ID"),
                qty=row.get("Qty"),
                amount=row.get("Amount"),
                currency=row.get("currency"),
                ship_country=row.get("ship-country"),
                date=row.get("Date"),
            )
            valid_count += 1
        except ValidationError:
            invalid_count += 1

    print("========== DATA QUALITY SUMMARY ==========")
    print(f"Total Rows: {len(df)}")
    print(f"Valid Rows: {valid_count}")
    print(f"Invalid Rows: {invalid_count}")
    print("==========================================")

    if invalid_count > 0:
        print("❌ Data validation failed.")
        sys.exit(1)
    else:
        print("✅ Data validation passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
