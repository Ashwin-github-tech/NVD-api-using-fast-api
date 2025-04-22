# NVD CPE Data Viewer

This project displays the results of an XML file with NVD (National Vulnerability Database) CPE (Common Platform Enumeration) data in an HTML page using a FastAPI backend and a Flask-powered frontend.

---

## Features

- Convert NVD XML files to CSV for easier preprocessing
- Clean and load data into a SQLite database
- Expose paginated and filtered APIs using FastAPI
- Display results in a web-based frontend using Flask
- Allows filtering, pagination, and dynamic limit control

---

## 1. Data Collection, Processing, and Storing

### a. XML to CSV Conversion
Convert the raw NVD XML file to a CSV file for easier processing.

**Script:** `convert.py`

**Usage:**
```bash
python convert.py <xml_file_path>
# or
python3 convert.py <xml_file_path>
```

### b. Load CSV Data into SQLite Database
The cleaned CSV data is loaded into a SQLite database called `cpes.db`.

**Script:** `load_data_to_db.py`

**Database Table:** `cpes`

**Schema (defined in `schema.py`)**
```text
id: integer
cpe_title: string
cpe_22_uri: string
cpe_23_uri: string
reference_links: List[string]
cpe_22_deprecation_date: Optional[date]
cpe_23_deprecation_date: Optional[date]
```

**ORM Model (defined in `models.py`)**
```python
id = Column(Integer, primary_key=True, index=True)
cpe_title = Column(String, nullable=False)
cpe_22_uri = Column(String)
cpe_23_uri = Column(String)
reference_links = Column(String)
cpe_22_deprecation_date = Column(Date, nullable=True)
cpe_23_deprecation_date = Column(Date, nullable=True)
```

**Usage:**
```bash
python load_data_to_db.py <csv_file_path>
# or
python3 load_data_to_db.py <csv_file_path>
```

**Database Connection (`database.py`)**
Creates the SQLAlchemy engine and session to connect the ORM model to the database.

---

## 2. Backend API (FastAPI)

### Endpoint: `/api/cpes`
Returns paginated results from the database.

**Query Parameters:**
- `page`: int (default = 1)
- `limit`: int (default = 10)

**Response Structure:**
```json
{
  "page": 1,
  "limit": 10,
  "total": 100,
  "data": [
    {
      "id": 1,
      "cpe_title": "...",
      "cpe_22_uri": "...",
      "cpe_23_uri": "...",
      "reference_links": ["..."],
      "cpe_22_deprecation_date": "YYYY-MM-DD",
      "cpe_23_deprecation_date": "YYYY-MM-DD"
    }
  ]
}
```

### Endpoint: `/api/cpes/search`
Supports filtering by:
- `cpe_title`
- `cpe_22_uri`
- `cpe_23_uri`
- `deprecation_date`

Includes pagination with `page` and `limit`.

---

## 3. Frontend (Flask)

**Flask App:** `app.py`

### Features:
- Filters can be applied using input fields.
- Pagination using hidden fields to retain filter state.
- JavaScript used to dynamically submit pagination requests with filter data hidden from the URL (except for `page` and `limit`).
- Replaced dropdown with numeric input for records per page (min=15, max=50).

### Example HTML Code Snippet for Limit Input
```html
<label for="limitInput">Records per page:</label>
<input type="number" id="limitInput" name="limit" class="form-control" min="15" max="50" value="{{ limit }}">
```

---

## 4. Installation

Install dependencies from `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## 5. Running the App

**Start FastAPI Server:**
```bash
uvicorn main:app --reload
```

**Start Flask Frontend:**
```bash
python app.py
```

---

## 6. File Overview
| File | Description |
|------|-------------|
| `convert.py` | Converts XML to CSV |
| `load_data_to_db.py` | Loads CSV into SQLite database |
| `models.py` | SQLAlchemy ORM Models |
| `database.py` | DB engine/session configuration |
| `schema.py` | Data schema for API responses |
| `main.py` | FastAPI application |
| `app.py` | Flask frontend application |
| `templates/index.html` | HTML UI |
| `requirements.txt` | Python package dependencies |

---

## 7. Example

```
http://localhost:5000/?page=2&limit=50
```
Applies filters in the background while only showing `page` and `limit` in the URL.

---

## Author
Ashwin Karthik

