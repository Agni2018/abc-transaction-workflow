import os
import csv
import json
import boto3
from decimal import Decimal
from datetime import datetime, timezone
from io import StringIO

BUCKET = os.environ["BUCKET"]
INPUT_KEY = os.environ["INPUT_KEY"]
OUTPUT_KEY = os.environ["OUTPUT_KEY"]

s3 = boto3.client("s3")


def main():
    response = s3.get_object(
        Bucket=BUCKET,
        Key=INPUT_KEY
    )

    content = response["Body"].read().decode("utf-8")
    reader = csv.DictReader(StringIO(content))

    total_transactions = 0
    successful_transactions = 0
    refund_transactions = 0

    successful_amount = Decimal("0.00")
    refund_amount = Decimal("0.00")

    for row in reader:
        total_transactions += 1

        amount = Decimal(row["amount"])

        if row["status"] == "success":
            successful_transactions += 1
            successful_amount += amount

        elif row["status"] == "refund":
            refund_transactions += 1
            refund_amount += amount

    report = {
        "total_transactions": total_transactions,
        "successful_transactions": successful_transactions,
        "refund_transactions": refund_transactions,
        "successful_amount": str(successful_amount),
        "refund_amount": str(refund_amount),
        "processed_at": datetime.now(timezone.utc).isoformat()
    }

    s3.put_object(
        Bucket=BUCKET,
        Key=OUTPUT_KEY,
        Body=json.dumps(report, indent=4),
        ContentType="application/json"
    )

    print("Transaction processing completed")
    print(json.dumps(report, indent=4))


if __name__ == "__main__":
    main()
