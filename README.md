## Natural Language to SQL Query
It is Database agonistic Natural Language to SQL query application created with FastAPI. It is specially designed to work with databases with large schema and tables. The schema being used here is from  [AdventureWorks2019](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure?view=sql-server-ver17&tabs=ssms) database. You can use replace the `db_schema.json` with schema information from your own database and use this application.
It makes the schema information manageable using a two step approach of identifying relevant schema & tables and then creating actual SQL query by using the specific table related information. 

There are multiple improvements that can be done, including Intent Classification, Ambiguity Resolution, Config related to database values etc. 


1.  **Create a Virtual Environment:**

   ```bash
   python3 -m venv .venv
   ```

2.  **Activate the Virtual Environment:**

   *   **Linux/macOS:**

   ```      
   source .venv/bin/activate
   ```

   *   **Windows:**

   ```bash
   .venv\Scripts\activate
   ```

3.  **Create a `.env` file:**

   *   **Copy from example (if available):**

   ```bash
   cp .env.example .env
   ```

   *   **Otherwise, create an empty file:**

   ```bash
   touch .env
   ```

4.  **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   *(Create `requirements.txt` first, if it doesn't exist.  Example: `touch requirements.txt`)*

5. Run `python3 test.py` to run sample test cases stored as list at test.py file. 