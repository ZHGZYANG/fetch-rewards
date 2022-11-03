## Fetch Rewards Coding Exercise - Backend Software Engineering



### Requirements

* Python 3.8+

### Setup

1. Install necessary packages

`pip3 install -r requirement.txt`

2. Run the server

`python3 main.py`





### API Reference

**Different status levels in response**

* 0: successful
* 1: logical error
* 2: field(s) missing
* 3: invalid input

#### 1. Add transaction

##### POST /add

* When attempted points is negative, the request will be denied if it makes balance negative. To enforce the request, add `force=true` in request body, then this payer’s balance will be 0.

**Request body: **

```
payer: string
points: integer
timestamp: string
force: optional
```

**Response body:**

```json
{"status": 0, "meta": {"count": 1}, "msg": "Adding transaction successful."}
```

```json
{"status": 1, "meta": {"count": 0}, "msg": "Action denied. Attempted points is negative and will make balance negative."}
```

```json
{"status": 2, "meta": {"count": 0}, "msg": "Error. Please fill in all required fields."}
```

```json
{"status": 3, "meta": {"count": 0}, "msg": "Error. Points inputted is invalid."}
```

```json
{"status": 3, "meta": {"count": 0}, "msg": "Error. Timestamp inputted is invalid."}
```



#### 2. Spend points

##### POST /spend

**Request body: **

```
points: integer
```

**Response body:**

```json
{"status": 0, "meta": {"count": 3}, "msg": [{"payer": "DANNON", "points": -100}, {"payer": "UNILEVER", "points": -200},
{"payer": "MILLER COORS", "points": -4700}]}
```

```json
{"status": 1, "meta": {"count": 0}, "msg": "Action denied. Attempted points is greater than current balance."}
```

```json
{"status": 2, "meta": {"count": 0}, "msg": "Error. Please fill in all required fields."}
```

```json
{"status": 3, "meta": {"count": 0}, "msg": "Error. Points inputted is invalid."}
```



#### 3. Get balances of all payers

##### GET /all

**Response body:**

```json
{"status": 0, "meta": {"count": 3}, "msg": {"DANNON": 1000, "UNILEVER": 0, "MILLER COORS": 5300}}
```



