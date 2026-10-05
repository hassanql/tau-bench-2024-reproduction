# Five historical retail task examples

Static source inspection only; none is an observed trajectory. Complete task definitions, profiles, and associated starting orders are preserved in `evidence/task-examples.json`. Every episode begins with a fresh deep copy of the full shared database, not a task-specific reset patch.

## Task 0

Source: `tau_bench/envs/retail/tasks.py`, zero-based index 0.

**User goal and supplied knowledge (verbatim task instruction):**

You are Yusuf Rossi in 19122. You received your order #W2378156 and wish to exchange the mechanical keyboard for a similar one but with clicky switches and the smart thermostat for one compatible with Google Home instead of Apple HomeKit. If there is no keyboard that is clicky, RGB backlight, full size, you'd go for no backlight. You are detail-oriented and want to make sure everything is addressed in one go.

**Starting state:**

User `yusuf_rossi_9620`. Associated order statuses: `#W6247578` = pending, `#W9711842` = cancelled, `#W4776164` = pending, `#W6679257` = delivered, `#W2378156` = delivered. Full records are in the evidence JSON.

**Encoded gold action sequence:**

```json
[
  {
    "name": "find_user_id_by_name_zip",
    "arguments": {
      "first_name": "Yusuf",
      "last_name": "Rossi",
      "zip": "19122"
    }
  },
  {
    "name": "get_order_details",
    "arguments": {
      "order_id": "#W2378156"
    }
  },
  {
    "name": "get_product_details",
    "arguments": {
      "product_id": "1656367028"
    }
  },
  {
    "name": "get_product_details",
    "arguments": {
      "product_id": "4896585277"
    }
  },
  {
    "name": "exchange_delivered_order_items",
    "arguments": {
      "order_id": "#W2378156",
      "item_ids": [
        "1151293680",
        "4983901480"
      ],
      "new_item_ids": [
        "7706410293",
        "7747408585"
      ],
      "payment_method_id": "credit_card_9513926"
    }
  }
]
```

**Expected behavior:** Authenticate through the policy lookup, retrieve needed records, honor the instruction’s conditional preferences, and confirm consequential changes. This describes policy requirements; the evaluator does not verify all of them.

**Expected final response and success criteria:** No response substring constraints are encoded. There is no gold final sentence. Terminal reward requires the full database to equal the result of replaying the listed gold actions, plus any output constraints. Gold read actions do not themselves impose a required agent read sequence.

## Task 2

Source: `tau_bench/envs/retail/tasks.py`, zero-based index 2.

**User goal and supplied knowledge (verbatim task instruction):**

You are Yusuf Rossi in 19122. You want to know how many tshirt options are available in the online store right now. You want to also return the cleaner, headphone, and smart watch.

**Starting state:**

User `yusuf_rossi_9620`. Associated order statuses: `#W6247578` = pending, `#W9711842` = cancelled, `#W4776164` = pending, `#W6679257` = delivered, `#W2378156` = delivered. Full records are in the evidence JSON.

**Encoded gold action sequence:**

```json
[
  {
    "name": "find_user_id_by_name_zip",
    "arguments": {
      "first_name": "Yusuf",
      "last_name": "Rossi",
      "zip": "19122"
    }
  },
  {
    "name": "get_product_details",
    "arguments": {
      "product_id": "6086499569"
    }
  },
  {
    "name": "list_all_product_types",
    "arguments": {}
  },
  {
    "name": "get_product_details",
    "arguments": {
      "product_id": "9523456873"
    }
  },
  {
    "name": "get_user_details",
    "arguments": {
      "user_id": "yusuf_rossi_9620"
    }
  },
  {
    "name": "get_order_details",
    "arguments": {
      "order_id": "#W6247578"
    }
  },
  {
    "name": "get_order_details",
    "arguments": {
      "order_id": "#W9711842"
    }
  },
  {
    "name": "get_order_details",
    "arguments": {
      "order_id": "#W4776164"
    }
  },
  {
    "name": "get_order_details",
    "arguments": {
      "order_id": "#W6679257"
    }
  },
  {
    "name": "get_order_details",
    "arguments": {
      "order_id": "#W2378156"
    }
  },
  {
    "name": "get_product_details",
    "arguments": {
      "product_id": "9523456873"
    }
  },
  {
    "name": "return_delivered_order_items",
    "arguments": {
      "order_id": "#W2378156",
      "item_ids": [
        "4602305039",
        "4202497723",
        "9408160950"
      ],
      "payment_method_id": "credit_card_9513926"
    }
  }
]
```

**Expected behavior:** Authenticate through the policy lookup, retrieve needed records, honor the instruction’s conditional preferences, and confirm consequential changes. This describes policy requirements; the evaluator does not verify all of them.

**Expected final response and success criteria:** Agent speech must include every required substring: `10`. There is no gold final sentence. Terminal reward requires the full database to equal the result of replaying the listed gold actions, plus any output constraints. Gold read actions do not themselves impose a required agent read sequence.

## Task 16

Source: `tau_bench/envs/retail/tasks.py`, zero-based index 16.

**User goal and supplied knowledge (verbatim task instruction):**

You are Fatima Johnson in 78712. You want to cancel all pending orders and return the watch you have received (but nothing else), and you want to know the total amount you can get back. You are a private person that does not want to reveal much about yourself.

**Starting state:**

User `fatima_johnson_7581`. Associated order statuses: `#W5199551` = pending, `#W8665881` = pending, `#W9389413` = delivered. Full records are in the evidence JSON.

**Encoded gold action sequence:**

```json
[
  {
    "name": "find_user_id_by_name_zip",
    "arguments": {
      "first_name": "Fatima",
      "last_name": "Johnson",
      "zip": "78712"
    }
  },
  {
    "name": "get_user_details",
    "arguments": {
      "user_id": "fatima_johnson_7581"
    }
  },
  {
    "name": "get_order_details",
    "arguments": {
      "order_id": "#W5199551"
    }
  },
  {
    "name": "get_order_details",
    "arguments": {
      "order_id": "#W8665881"
    }
  },
  {
    "name": "get_order_details",
    "arguments": {
      "order_id": "#W9389413"
    }
  },
  {
    "name": "calculate",
    "arguments": {
      "expression": "3131.1 + 4777.75 + 367.38"
    }
  },
  {
    "name": "cancel_pending_order",
    "arguments": {
      "order_id": "#W5199551",
      "reason": "no longer needed"
    }
  },
  {
    "name": "cancel_pending_order",
    "arguments": {
      "order_id": "#W8665881",
      "reason": "no longer needed"
    }
  },
  {
    "name": "return_delivered_order_items",
    "arguments": {
      "order_id": "#W9389413",
      "item_ids": [
        "2554056026"
      ],
      "payment_method_id": "paypal_5364164"
    }
  }
]
```

**Expected behavior:** Authenticate through the policy lookup, retrieve needed records, honor the instruction’s conditional preferences, and confirm consequential changes. This describes policy requirements; the evaluator does not verify all of them.

**Expected final response and success criteria:** Agent speech must include every required substring: `8276.23`. There is no gold final sentence. Terminal reward requires the full database to equal the result of replaying the listed gold actions, plus any output constraints. Gold read actions do not themselves impose a required agent read sequence.

## Task 22

Source: `tau_bench/envs/retail/tasks.py`, zero-based index 22.

**User goal and supplied knowledge (verbatim task instruction):**

You are Ethan Garcia, and you live in Denver, 80280. You want to change your user address and all possible order addresses to be 101 Highway, New York, 10001. Then you regret and want to change the user address back to the original address. You are a mysterious person and do not want to reveal much about yourself.

**Starting state:**

User `ethan_garcia_1261`. Associated order statuses: `#W4967593` = processed, `#W9911714` = pending, `#W5733668` = processed. Full records are in the evidence JSON.

**Encoded gold action sequence:**

```json
[
  {
    "name": "find_user_id_by_name_zip",
    "arguments": {
      "first_name": "Ethan",
      "last_name": "Garcia",
      "zip": "80280"
    }
  },
  {
    "name": "modify_user_address",
    "arguments": {
      "user_id": "ethan_garcia_1261",
      "address1": "101 Highway",
      "address2": "",
      "city": "New York",
      "state": "NY",
      "country": "USA",
      "zip": "10001"
    }
  },
  {
    "name": "get_order_details",
    "arguments": {
      "order_id": "#W4967593"
    }
  },
  {
    "name": "get_order_details",
    "arguments": {
      "order_id": "#W9911714"
    }
  },
  {
    "name": "get_order_details",
    "arguments": {
      "order_id": "#W5733668"
    }
  },
  {
    "name": "modify_pending_order_address",
    "arguments": {
      "order_id": "#W9911714",
      "address1": "101 Highway",
      "address2": "",
      "city": "New York",
      "state": "NY",
      "country": "USA",
      "zip": "10001"
    }
  },
  {
    "name": "modify_user_address",
    "arguments": {
      "user_id": "ethan_garcia_1261",
      "address1": "667 Highland Drive",
      "address2": "Suite 865",
      "city": "Denver",
      "state": "CO",
      "country": "USA",
      "zip": "80280"
    }
  }
]
```

**Expected behavior:** Authenticate through the policy lookup, retrieve needed records, honor the instruction’s conditional preferences, and confirm consequential changes. This describes policy requirements; the evaluator does not verify all of them.

**Expected final response and success criteria:** No response substring constraints are encoded. There is no gold final sentence. Terminal reward requires the full database to equal the result of replaying the listed gold actions, plus any output constraints. Gold read actions do not themselves impose a required agent read sequence.

## Task 24

Source: `tau_bench/envs/retail/tasks.py`, zero-based index 24.

**User goal and supplied knowledge (verbatim task instruction):**

You are Sofia Hernandez, and you live in Seattle, WA, 98193. You want to cancel the grill, but if the agent asks you to confirm, you regret and want to keep it. You then want to ask which two t-shirts you have ordered in another order, and what materials are they. Make everything sound very natural and make up reasons.

**Starting state:**

User `sofia_hernandez_5364`. Associated order statuses: `#W3561391` = pending, `#W6876713` = delivered, `#W9609649` = processed, `#W3947049` = delivered. Full records are in the evidence JSON.

**Encoded gold action sequence:**

```json
[]
```

**Expected behavior:** Authenticate through the policy lookup, retrieve needed records, honor the instruction’s conditional preferences, and confirm consequential changes. This describes policy requirements; the evaluator does not verify all of them.

**Expected final response and success criteria:** Agent speech must include every required substring: `polyester`, `cotton`. There is no gold final sentence. Terminal reward requires the full database to equal the result of replaying the listed gold actions, plus any output constraints. Gold read actions do not themselves impose a required agent read sequence.
