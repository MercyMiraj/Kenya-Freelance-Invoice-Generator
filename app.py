from datetime import datetime, timedelta
import random
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
  if request.method == "POST":
    business_name = request.form.get("business_name", "").strip()
    business_email = request.form.get("business_email", "").strip()
    business_phone = request.form.get("business_phone", "").strip()
    kra_pin = request.form.get("kra_pin", "").strip()

    client_name = request.form.get("client_name", "").strip()
    client_email = request.form.get("client_email", "").strip()

    payment_method = request.form.get("payment_method", "M-Pesa Paybill")
    payment_account = request.form.get("payment_account", "").strip()
    account_name = request.form.get("account_name", "").strip()

    tax_type = request.form.get("tax_type", "none")
    notes = request.form.get("notes", "").strip()

    descriptions = request.form.getlist("description[]")
    quantities = request.form.getlist("quantity[]")
    prices = request.form.getlist("price[]")

    items = []
    subtotal = 0.0
    for desc, qty, price in zip(descriptions, quantities, prices):
      if desc.strip():
        q = float(qty or 1)
        p = float(price or 0)
        line_total = q * p
        subtotal += line_total
        items.append(
            {"description": desc.strip(), "quantity": q, "price": p, "total": line_total}
        )

    tax_amount = 0.0
    tax_label = ""
    if tax_type == "vat":
      tax_amount = subtotal * 0.16
      tax_label = "VAT (16%)"
      grand_total = subtotal + tax_amount
    elif tax_type == "wht":
      tax_amount = subtotal * 0.05
      tax_label = "Less Withholding Tax (5%)"
      grand_total = subtotal - tax_amount
    else:
      grand_total = subtotal

    invoice_number = f"INV-{datetime.now().strftime('%Y%m')}-{random.randint(100, 999)}"
    issue_date = datetime.now().strftime("%d %b %Y")
    due_date = (datetime.now() + timedelta(days=7)).strftime("%d %b %Y")

    return render_template(
        "invoice.html",
        business_name=business_name,
        business_email=business_email,
        business_phone=business_phone,
        kra_pin=kra_pin,
        client_name=client_name,
        client_email=client_email,
        payment_method=payment_method,
        payment_account=payment_account,
        account_name=account_name,
        items=items,
        subtotal=subtotal,
        tax_type=tax_type,
        tax_label=tax_label,
        tax_amount=tax_amount,
        grand_total=grand_total,
        invoice_number=invoice_number,
        issue_date=issue_date,
        due_date=due_date,
        notes=notes,
    )

  return render_template("index.html")


if __name__ == "__main__":
  app.run(debug=True)
