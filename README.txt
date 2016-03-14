pymovoice README


Current format in db
---------------------
{
  "_id": ObjectId("55c646f6bb3357da4d730b31"),
  "address": "Hans Muster\nMusterstrasse 99",
  "invoice_number": "RG-2015-0099",
  "invoice_date": new Date("2015-12-12T01:00:00+0100"),
  "customer_id": "AG-00004",
  "salutation": "Sehr geehrte Damen und Herren",
  "invoice_pre_text": "Dolor lorem ipsum",
  "amount": 999,
  "invoice_items": [
    {
      "description": "bla bla",
      "quantity": 6,
      "unitprice": 20.0,
      "price_of_position": 120.0
    },
    {
      "description": "blub blub",
      "quantity": 10,
      "unitprice": 50.0,
      "price_of_position": 500.0
    }
  ]
}
