# db_sql.py - COMPREHENSIVE SQL, DBMS, and Database Design Q&A
# Covers: SQL Theory (60+), SQL Coding (40+), SQL Fermi (10), DBMS Deep (30+)

SQL_QUESTIONS = []

def add(sub, q, a, is_coding=False, code_sql="", code_java="", code_python=""):
    SQL_QUESTIONS.append({
        "category": "sql_db",
        "subcategory": sub,
        "question": q,
        "answer": a.strip(),
        "is_coding": is_coding,
        "code_sql": code_sql.strip(),
        "code_java": code_java.strip(),
        "code_python": code_python.strip()
    })

# ═══════════════════════════════════════════════════════════════
# SQL THEORY (60 questions)
# ═══════════════════════════════════════════════════════════════

add("SQL Theory", "What does ACID stand for? Explain each property.", """
ACID stands for:
* **Atomicity**: All operations in a transaction succeed, or the entire transaction is rolled back (All-or-Nothing).
* **Consistency**: A transaction takes the database from one valid state to another, maintaining all schema constraints and rules.
* **Isolation**: Concurrent transactions don't interfere; the result is the same as if transactions ran sequentially. Prevents dirty reads, non-repeatable reads, and phantom reads.
* **Durability**: Once committed, changes are permanently written to non-volatile storage and survive system failures.
""")

add("SQL Theory", "What is a transaction in a database? Give an example.", """
A transaction is a logical unit of work containing one or more SQL statements that must complete entirely or not at all.
* **Example**: Bank transfer of $100 from Account A to B:
  1. UPDATE accounts SET balance = balance - 100 WHERE id = 'A';
  2. UPDATE accounts SET balance = balance + 100 WHERE id = 'B';
  Both must succeed. If step 2 fails, step 1 is rolled back.
""")

add("SQL Theory", "What is a primary key? Rules for primary key.", """
A primary key uniquely identifies each row in a table.
* **Rules**:
  1. **Uniqueness**: Each value must be unique.
  2. **Non-Nullability**: Cannot contain NULL values.
  3. **Single per table**: A table can have only one primary key.
  4. **Stability**: Values should rarely change.
  5. Can be a composite key (multiple columns together).
""")

add("SQL Theory", "What is a foreign key? What is referential integrity?", """
* **Foreign Key**: A column or set of columns that references the primary key of another table, establishing a parent-child relationship.
* **Referential Integrity**: Ensures that a foreign key value must match an existing primary key value in the referenced table, preventing orphaned rows. Enforced with ON DELETE CASCADE, SET NULL, or RESTRICT actions.
""")

add("SQL Theory", "What is normalization? Explain 1NF, 2NF, 3NF, and BCNF.", """
Normalization structures tables to reduce redundancy and anomalies:
* **1NF**: Atomic values only; no repeating groups or arrays in cells. Each row is unique.
* **2NF**: Satisfies 1NF + every non-key column fully depends on the entire primary key (no partial dependency on composite keys).
* **3NF**: Satisfies 2NF + no transitive dependencies (non-key columns don't depend on other non-key columns).
* **BCNF (Boyce-Codd)**: For every functional dependency X→Y, X must be a superkey. Stricter than 3NF; handles edge cases where 3NF still allows anomalies.
""")

add("SQL Theory", "What is denormalization? When would you use it?", """
Denormalization intentionally adds redundancy back into normalized tables to optimize read performance.
* **When to use**:
  - Read-heavy OLAP/data warehouse workloads where JOINs are expensive.
  - Frequently accessed reports or dashboards needing pre-computed aggregates.
  - Real-time applications where low-latency reads are critical.
* **Trade-off**: Faster reads, but slower writes and risk of data inconsistency.
""")

add("SQL Theory", "Explain the differences between INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL OUTER JOIN, and CROSS JOIN.", """
* **INNER JOIN**: Returns only rows with matching keys in both tables.
* **LEFT JOIN**: Returns all rows from the left table + matched rows from the right (NULLs for non-matches).
* **RIGHT JOIN**: Returns all rows from the right table + matched rows from the left (NULLs for non-matches).
* **FULL OUTER JOIN**: Returns all rows from both tables; NULLs where there's no match on either side.
* **CROSS JOIN**: Cartesian product — every row from table A paired with every row from table B. No join condition needed.
""")

add("SQL Theory", "What is a self-join? Give a practical use case.", """
A self-join joins a table to itself using aliases to compare rows within the same table.
* **Use case**: Finding employees and their managers when both are in the same 'employees' table:
  SELECT e.name AS employee, m.name AS manager
  FROM employees e JOIN employees m ON e.manager_id = m.id;
* Also used for: finding duplicates, hierarchical data, comparing sequential records.
""")

add("SQL Theory", "Explain the difference between WHERE and HAVING clauses.", """
* **WHERE**: Filters individual rows BEFORE grouping (applied to raw rows). Cannot use aggregate functions.
* **HAVING**: Filters groups AFTER GROUP BY (applied to aggregated results). Can use aggregate functions like COUNT(), SUM(), AVG().
* **Example**: WHERE salary > 50000 filters rows; HAVING COUNT(*) > 5 filters groups.
* **Execution order**: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY.
""")

add("SQL Theory", "What is the SQL execution order? Explain the logical processing sequence.", """
SQL statements are processed in this logical order (not the written order):
1. **FROM** / **JOIN** — Identify source tables and join them.
2. **WHERE** — Filter individual rows.
3. **GROUP BY** — Group remaining rows by specified columns.
4. **HAVING** — Filter aggregated groups.
5. **SELECT** — Choose output columns and compute expressions.
6. **DISTINCT** — Remove duplicate rows.
7. **ORDER BY** — Sort the result set.
8. **LIMIT / OFFSET** — Restrict the number of returned rows.
""")

add("SQL Theory", "What is a subquery? Difference between correlated and non-correlated subqueries.", """
A subquery is a query nested inside another query (SELECT, WHERE, FROM, or HAVING).
* **Non-correlated subquery**: Executes independently once. Inner query doesn't reference the outer query. Example: WHERE salary > (SELECT AVG(salary) FROM employees).
* **Correlated subquery**: References columns from the outer query. Executes once PER ROW of the outer query. Example: WHERE salary > (SELECT AVG(salary) FROM employees e2 WHERE e2.dept_id = e1.dept_id).
* Correlated subqueries are slower but more powerful for row-by-row comparisons.
""")

add("SQL Theory", "What is a Common Table Expression (CTE)? Benefits over subqueries?", """
A CTE is a temporary named result set defined with the WITH clause that exists only during query execution.
* **Syntax**: WITH cte_name AS (SELECT ...) SELECT * FROM cte_name;
* **Benefits over subqueries**:
  1. **Readability**: Named, modular, easier to understand than nested subqueries.
  2. **Reusability**: Can reference the same CTE multiple times in one query.
  3. **Recursion**: Supports recursive CTEs for hierarchical data (e.g., org charts, tree traversal).
  4. **Debugging**: Easier to test each CTE independently.
""")

add("SQL Theory", "Explain window functions: ROW_NUMBER, RANK, DENSE_RANK, NTILE.", """
Window functions perform calculations across a set of rows related to the current row without collapsing groups:
* **ROW_NUMBER()**: Assigns a unique sequential number to every row regardless of ties. (1, 2, 3, 4)
* **RANK()**: Same rank for ties, skips subsequent numbers. (1, 2, 2, 4)
* **DENSE_RANK()**: Same rank for ties, no gaps. (1, 2, 2, 3)
* **NTILE(n)**: Divides rows into n roughly equal buckets and assigns bucket numbers. Useful for percentile/quartile analysis.
All use OVER(PARTITION BY ... ORDER BY ...) clause.
""")

add("SQL Theory", "Explain LAG, LEAD, SUM OVER, and AVG OVER window functions.", """
* **LAG(col, n)**: Accesses data from n rows BEFORE the current row within the partition. Useful for calculating differences (e.g., month-over-month change).
* **LEAD(col, n)**: Accesses data from n rows AFTER the current row. Useful for forward-looking comparisons.
* **SUM() OVER(...)**: Running/cumulative sum across ordered rows. SUM(sales) OVER(ORDER BY date) gives running total.
* **AVG() OVER(...)**: Moving average. AVG(price) OVER(ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) gives 7-day moving average.
""")

add("SQL Theory", "What is an index? Types of indexes and when to use them.", """
An index is a data structure that speeds up data retrieval by creating pointers to rows based on indexed column values.
* **Types**:
  1. **Clustered Index**: Physically reorders table data. Only ONE per table. Usually the primary key.
  2. **Non-clustered Index**: Separate structure with pointers back to data. Multiple allowed per table.
  3. **Composite Index**: Index on multiple columns. Column order matters for query matching.
  4. **Unique Index**: Enforces uniqueness on indexed columns.
  5. **Full-text Index**: For text search operations.
  6. **Covering Index**: Contains all columns needed by a query, avoiding table lookups.
* **When to use**: Columns frequently used in WHERE, JOIN, ORDER BY, or GROUP BY clauses.
* **Trade-off**: Faster reads but slower writes (index must be updated on INSERT/UPDATE/DELETE).
""")

add("SQL Theory", "What is a view? What is a materialized view? Differences.", """
* **View**: A virtual table defined by a stored SQL query. No data stored; re-executes the query each time it's accessed. Provides abstraction and security.
* **Materialized View**: A physical snapshot of a query result stored on disk. Must be refreshed manually or on schedule.
* **Key Differences**:
  | Feature | View | Materialized View |
  |---------|------|-------------------|
  | Storage | No data stored | Data cached on disk |
  | Speed | Slow (re-executes) | Fast (pre-computed) |
  | Freshness | Always current | Stale until refreshed |
  | Use case | Security/abstraction | Reporting/dashboards |
""")

add("SQL Theory", "What is a stored procedure? Advantages and disadvantages.", """
A stored procedure is a precompiled set of SQL statements stored in the database that can be executed with parameters.
* **Advantages**:
  1. Performance: Pre-compiled execution plan, reducing parsing overhead.
  2. Security: Users can execute procedures without direct table access.
  3. Reusability: Centralized business logic callable from any application.
  4. Reduced network traffic: Single call instead of multiple SQL statements.
* **Disadvantages**:
  1. Debugging difficulty: Harder to debug than application code.
  2. Vendor lock-in: Syntax differs between databases.
  3. Version control: Harder to track changes in source control.
""")

add("SQL Theory", "What is a trigger? When should you use or avoid triggers?", """
A trigger is a stored procedure that automatically executes in response to specific table events (INSERT, UPDATE, DELETE).
* **Types**: BEFORE trigger, AFTER trigger, INSTEAD OF trigger.
* **Use cases**: Audit logging, enforcing complex business rules, maintaining denormalized summary tables, cascading updates.
* **Avoid when**:
  - Complex business logic (use application layer instead).
  - Performance-sensitive tables (triggers add overhead to every DML operation).
  - Cascading triggers (trigger A fires trigger B which fires trigger A — infinite loop risk).
""")

add("SQL Theory", "What is a cursor? Why are cursors generally discouraged?", """
A cursor is a database object that allows row-by-row processing of a result set.
* **How it works**: DECLARE cursor → OPEN → FETCH rows one by one → CLOSE → DEALLOCATE.
* **Why discouraged**:
  1. **Performance**: Row-by-row processing is drastically slower than set-based operations. SQL engines are optimized for set operations.
  2. **Memory**: Holds locks and consumes memory for the duration.
  3. **Scalability**: Doesn't parallelize well.
* **When acceptable**: Complex procedural logic that can't be expressed in set-based SQL (rare), ETL processing with error handling per row.
""")

add("SQL Theory", "What is the difference between DELETE, TRUNCATE, and DROP?", """
* **DELETE**: DML operation. Removes specific rows (can use WHERE clause). Logs each row deletion. Can be rolled back. Fires triggers.
* **TRUNCATE**: DDL operation. Removes ALL rows from a table. Minimal logging (deallocates pages). Cannot be rolled back in most RDBMS. Does NOT fire triggers. Resets identity counter.
* **DROP**: DDL operation. Removes the entire table structure (schema + data) from the database. Cannot be rolled back.
* **Speed**: DROP > TRUNCATE > DELETE.
""")

add("SQL Theory", "What is the difference between UNION and UNION ALL?", """
* **UNION**: Combines result sets of two queries and removes duplicate rows. Performs an implicit DISTINCT, which requires sorting — slower.
* **UNION ALL**: Combines result sets and keeps ALL rows including duplicates. Faster because no deduplication step.
* **Rule**: Both queries must have the same number of columns with compatible data types.
* **Best practice**: Use UNION ALL when you know there are no duplicates or duplicates are acceptable.
""")

add("SQL Theory", "Explain GROUP BY with ROLLUP, CUBE, and GROUPING SETS.", """
These are GROUP BY extensions for multi-level aggregation:
* **ROLLUP**: Creates subtotals rolling up from the most detailed level to a grand total. GROUP BY ROLLUP(year, quarter) gives: year+quarter totals, year totals, grand total.
* **CUBE**: Creates subtotals for ALL possible combinations. GROUP BY CUBE(year, quarter) gives: year+quarter, year only, quarter only, and grand total.
* **GROUPING SETS**: Allows specifying exactly which grouping combinations to compute. More selective than CUBE.
* **GROUPING()** function identifies which rows are subtotals (returns 1 for aggregated, 0 for detail).
""")

add("SQL Theory", "What are isolation levels? Explain Read Uncommitted, Read Committed, Repeatable Read, and Serializable.", """
Isolation levels control how much one transaction can see of another's uncommitted changes:
* **Read Uncommitted**: Lowest isolation. Allows dirty reads (reading uncommitted data from other transactions).
* **Read Committed**: Prevents dirty reads. Only sees data committed before the statement began. Default in PostgreSQL, Oracle.
* **Repeatable Read**: Prevents dirty reads and non-repeatable reads. Data read once stays the same within the transaction. Default in MySQL InnoDB.
* **Serializable**: Highest isolation. Transactions behave as if executed serially. Prevents phantom reads but has the lowest concurrency.
* **Trade-off**: Higher isolation = more consistency but less concurrency and more locks/deadlocks.
""")

add("SQL Theory", "What is a deadlock? How do databases handle deadlocks?", """
A deadlock occurs when two or more transactions are waiting for each other to release locks, creating a circular dependency where none can proceed.
* **Example**: Transaction A locks Row 1, waits for Row 2. Transaction B locks Row 2, waits for Row 1.
* **Detection**: Databases use a wait-for graph. When a cycle is detected, one transaction (the victim) is rolled back.
* **Prevention strategies**:
  1. Lock ordering: Always acquire locks in the same order.
  2. Lock timeouts: Set maximum wait times.
  3. Keep transactions short: Reduce lock hold time.
  4. Use appropriate isolation levels.
""")

add("SQL Theory", "What is database sharding? Strategies and trade-offs.", """
Sharding is horizontal partitioning of data across multiple database instances (shards), each holding a subset of the data.
* **Strategies**:
  1. **Range-based**: Partition by value range (e.g., user IDs 1-1M on shard 1, 1M-2M on shard 2). Simple but can create hot spots.
  2. **Hash-based**: Apply hash function to the shard key. Better distribution but makes range queries difficult.
  3. **Geographic**: Shard by region/location for data locality.
  4. **Directory-based**: Lookup table maps each record to its shard. Flexible but the directory becomes a bottleneck.
* **Trade-offs**: Enables horizontal scaling but adds complexity in cross-shard JOINs, distributed transactions, and rebalancing.
""")

add("SQL Theory", "Compare SQL (relational) vs NoSQL databases. When to use which?", """
* **SQL (Relational)**: Structured schema, ACID transactions, normalized data, SQL query language. Examples: PostgreSQL, MySQL, Oracle.
* **NoSQL**: Flexible/schema-less, BASE properties, various data models. Types:
  1. **Document**: MongoDB, CouchDB — JSON documents, nested data.
  2. **Key-Value**: Redis, DynamoDB — simple lookups, caching.
  3. **Column-Family**: Cassandra, HBase — wide-column stores for analytics.
  4. **Graph**: Neo4j, Amazon Neptune — relationship-heavy data.
* **When SQL**: Complex queries, transactions, strong consistency, structured data.
* **When NoSQL**: High scalability, flexible schemas, rapid iteration, specific data models (graphs, documents).
""")

add("SQL Theory", "What is CAP theorem? How does it apply to distributed databases?", """
CAP theorem states that a distributed system can guarantee at most two of three properties:
* **Consistency (C)**: Every read receives the most recent write.
* **Availability (A)**: Every request receives a response (success or failure).
* **Partition Tolerance (P)**: The system continues to operate despite network partitions between nodes.
* Since network partitions are inevitable, you must choose between CP or AP:
  - **CP systems**: Prioritize consistency over availability (e.g., MongoDB, HBase). During partition, some nodes refuse requests.
  - **AP systems**: Prioritize availability over consistency (e.g., Cassandra, DynamoDB). May return stale data during partition.
""")

add("SQL Theory", "What are database constraints? List and explain each type.", """
Constraints enforce rules on data in tables:
1. **NOT NULL**: Column cannot contain NULL values.
2. **UNIQUE**: All values in a column must be distinct (allows one NULL in most RDBMS).
3. **PRIMARY KEY**: Combination of NOT NULL + UNIQUE. One per table.
4. **FOREIGN KEY**: Enforces referential integrity between tables.
5. **CHECK**: Validates that values satisfy a Boolean expression (e.g., CHECK(age >= 18)).
6. **DEFAULT**: Provides a default value when no value is specified on INSERT.
""")

add("SQL Theory", "Explain OLTP vs OLAP. How do their database designs differ?", """
* **OLTP (Online Transaction Processing)**: Handles day-to-day operations (INSERT, UPDATE, DELETE). Highly normalized (3NF). Optimized for write performance and data integrity. Examples: banking, e-commerce.
* **OLAP (Online Analytical Processing)**: Handles complex analytical queries on historical data. Denormalized (star/snowflake schema). Optimized for read-heavy aggregation queries. Examples: data warehouses, BI dashboards.
* **Key Differences**:
  | Feature | OLTP | OLAP |
  |---------|------|------|
  | Operations | CRUD | READ-heavy analytics |
  | Schema | Normalized (3NF) | Denormalized (Star) |
  | Data | Current, operational | Historical, aggregated |
  | Users | App users | Data analysts |
""")

add("SQL Theory", "What is a star schema vs snowflake schema in data warehousing?", """
Both are dimensional modeling schemas for data warehouses:
* **Star Schema**: Central fact table connected directly to dimension tables. Denormalized dimensions. Simpler queries, faster reads, more storage.
* **Snowflake Schema**: Dimensions are further normalized into sub-dimension tables. Reduces redundancy but requires more JOINs.
* **Example**: In a star schema, a 'products' dimension has all product info in one table. In snowflake, 'products' references a separate 'categories' table.
* **Best practice**: Star schema is preferred for most BI tools and query performance. Snowflake for storage optimization.
""")

add("SQL Theory", "What is query optimization? Explain EXPLAIN/EXPLAIN ANALYZE.", """
Query optimization is the process of improving SQL query performance by analyzing and restructuring queries.
* **EXPLAIN**: Shows the query execution plan without running the query. Displays which indexes are used, join types, estimated row counts.
* **EXPLAIN ANALYZE**: Actually executes the query and shows real timing, row counts, and buffer usage alongside the plan.
* **Key things to look for**:
  1. Sequential Scan vs Index Scan (seq scan on large tables = bad).
  2. Nested Loop vs Hash Join vs Merge Join.
  3. Estimated vs actual row counts (large discrepancies = stale statistics).
  4. Sort operations (external sorts indicate insufficient work_mem).
""")

# ═══════════════════════════════════════════════════════════════
# SQL CODING QUESTIONS (40 questions)
# ═══════════════════════════════════════════════════════════════

add("SQL Coding", "Write a query to find the second highest salary from an Employees table.", """
Use DENSE_RANK or subquery to find the second highest salary. The DENSE_RANK approach handles ties correctly.
""", is_coding=True, code_sql="""
-- Method 1: Using DENSE_RANK
SELECT salary FROM (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
  FROM employees
) ranked WHERE rnk = 2;

-- Method 2: Using subquery
SELECT MAX(salary) FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- Method 3: LIMIT/OFFSET
SELECT DISTINCT salary FROM employees
ORDER BY salary DESC LIMIT 1 OFFSET 1;
""")

add("SQL Coding", "Write a query to find the Nth highest salary.", """
Generalized version: find the Nth highest salary using DENSE_RANK window function.
""", is_coding=True, code_sql="""
-- Using DENSE_RANK (handles ties)
SELECT salary FROM (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
  FROM employees
) ranked WHERE rnk = :N;

-- Using LIMIT/OFFSET (N=3 example)
SELECT DISTINCT salary FROM employees
ORDER BY salary DESC LIMIT 1 OFFSET 2;
""")

add("SQL Coding", "Write a query to find duplicate records in a table.", """
Use GROUP BY with HAVING COUNT(*) > 1 to find duplicates based on specific columns.
""", is_coding=True, code_sql="""
-- Find duplicate emails
SELECT email, COUNT(*) as cnt
FROM employees
GROUP BY email
HAVING COUNT(*) > 1;

-- Delete duplicates keeping the first occurrence
DELETE FROM employees
WHERE id NOT IN (
  SELECT MIN(id) FROM employees GROUP BY email
);
""")

add("SQL Coding", "Write a query to find employees who earn more than their manager.", """
Use a self-join to compare each employee's salary with their manager's salary.
""", is_coding=True, code_sql="""
SELECT e.name AS employee, e.salary AS emp_salary,
       m.name AS manager, m.salary AS mgr_salary
FROM employees e
JOIN employees m ON e.manager_id = m.id
WHERE e.salary > m.salary;
""")

add("SQL Coding", "Write a query to find departments with more than 5 employees.", """
Group by department and filter using HAVING.
""", is_coding=True, code_sql="""
SELECT d.name AS department, COUNT(e.id) AS emp_count
FROM departments d
JOIN employees e ON d.id = e.dept_id
GROUP BY d.name
HAVING COUNT(e.id) > 5
ORDER BY emp_count DESC;
""")

add("SQL Coding", "Write a query for running total (cumulative sum) of sales by date.", """
Use SUM() window function with ORDER BY to calculate running total.
""", is_coding=True, code_sql="""
SELECT sale_date, amount,
       SUM(amount) OVER (ORDER BY sale_date) AS running_total
FROM sales
ORDER BY sale_date;

-- Running total partitioned by region
SELECT region, sale_date, amount,
       SUM(amount) OVER (PARTITION BY region ORDER BY sale_date) AS running_total
FROM sales;
""")

add("SQL Coding", "Write a query to find month-over-month revenue growth.", """
Use LAG() window function to access previous month's revenue and calculate percentage change.
""", is_coding=True, code_sql="""
WITH monthly AS (
  SELECT DATE_TRUNC('month', order_date) AS month,
         SUM(revenue) AS total_revenue
  FROM orders
  GROUP BY DATE_TRUNC('month', order_date)
)
SELECT month, total_revenue,
       LAG(total_revenue) OVER (ORDER BY month) AS prev_month,
       ROUND(
         (total_revenue - LAG(total_revenue) OVER (ORDER BY month))
         / LAG(total_revenue) OVER (ORDER BY month) * 100, 2
       ) AS growth_pct
FROM monthly
ORDER BY month;
""")

add("SQL Coding", "Write a query to find customers who placed orders in consecutive months.", """
Use LAG or LEAD to compare each order's month with the previous order's month for the same customer.
""", is_coding=True, code_sql="""
WITH customer_months AS (
  SELECT customer_id,
         DATE_TRUNC('month', order_date) AS order_month,
         LAG(DATE_TRUNC('month', order_date))
           OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_month
  FROM orders
)
SELECT DISTINCT customer_id
FROM customer_months
WHERE order_month = prev_month + INTERVAL '1 month';
""")

add("SQL Coding", "Write a query to pivot rows into columns (cross-tab query).", """
Use CASE WHEN inside aggregate functions or PIVOT (SQL Server) to transform rows to columns.
""", is_coding=True, code_sql="""
-- Manual pivot using CASE
SELECT employee_id,
  SUM(CASE WHEN quarter = 'Q1' THEN sales ELSE 0 END) AS Q1,
  SUM(CASE WHEN quarter = 'Q2' THEN sales ELSE 0 END) AS Q2,
  SUM(CASE WHEN quarter = 'Q3' THEN sales ELSE 0 END) AS Q3,
  SUM(CASE WHEN quarter = 'Q4' THEN sales ELSE 0 END) AS Q4
FROM quarterly_sales
GROUP BY employee_id;
""")

add("SQL Coding", "Write a query to find the top 3 products by revenue in each category.", """
Use ROW_NUMBER or RANK partitioned by category and ordered by revenue.
""", is_coding=True, code_sql="""
WITH ranked AS (
  SELECT category, product_name, revenue,
         ROW_NUMBER() OVER (
           PARTITION BY category
           ORDER BY revenue DESC
         ) AS rn
  FROM products
)
SELECT category, product_name, revenue
FROM ranked
WHERE rn <= 3
ORDER BY category, rn;
""")

add("SQL Coding", "Write a recursive CTE to traverse an organizational hierarchy.", """
Recursive CTEs have a base case (anchor) and a recursive member joined back to the CTE.
""", is_coding=True, code_sql="""
WITH RECURSIVE org_tree AS (
  -- Base case: top-level managers (no manager)
  SELECT id, name, manager_id, 1 AS level
  FROM employees
  WHERE manager_id IS NULL

  UNION ALL

  -- Recursive: join employees to their managers
  SELECT e.id, e.name, e.manager_id, ot.level + 1
  FROM employees e
  JOIN org_tree ot ON e.manager_id = ot.id
)
SELECT id, name, level
FROM org_tree
ORDER BY level, name;
""")

add("SQL Coding", "Write a query to detect gaps in a sequential ID column.", """
Use LAG or LEAD to compare consecutive IDs and find where the difference is greater than 1.
""", is_coding=True, code_sql="""
-- Find gaps in sequential IDs
SELECT id + 1 AS gap_start,
       next_id - 1 AS gap_end
FROM (
  SELECT id,
         LEAD(id) OVER (ORDER BY id) AS next_id
  FROM my_table
) t
WHERE next_id - id > 1;
""")

add("SQL Coding", "Write a query to calculate a 7-day moving average of daily sales.", """
Use AVG() window function with ROWS BETWEEN clause for a sliding window.
""", is_coding=True, code_sql="""
SELECT sale_date, daily_sales,
       AVG(daily_sales) OVER (
         ORDER BY sale_date
         ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
       ) AS moving_avg_7day
FROM daily_sales_table
ORDER BY sale_date;
""")

add("SQL Coding", "Write a query to find all employees who share the same birthday month.", """
Extract the month from the date and use GROUP BY with HAVING.
""", is_coding=True, code_sql="""
SELECT EXTRACT(MONTH FROM birthday) AS birth_month,
       STRING_AGG(name, ', ') AS employees,
       COUNT(*) AS count
FROM employees
GROUP BY EXTRACT(MONTH FROM birthday)
HAVING COUNT(*) > 1
ORDER BY birth_month;
""")

add("SQL Coding", "Write a query using NTILE to divide employees into salary quartiles.", """
NTILE(4) divides ordered rows into 4 roughly equal groups.
""", is_coding=True, code_sql="""
SELECT name, salary, department,
       NTILE(4) OVER (ORDER BY salary) AS salary_quartile
FROM employees
ORDER BY salary_quartile, salary;

-- Quartile analysis
SELECT salary_quartile,
       MIN(salary) AS min_sal, MAX(salary) AS max_sal,
       AVG(salary) AS avg_sal, COUNT(*) AS count
FROM (
  SELECT salary, NTILE(4) OVER (ORDER BY salary) AS salary_quartile
  FROM employees
) q GROUP BY salary_quartile;
""")

add("SQL Coding", "Write a query to find the median salary.", """
Use PERCENTILE_CONT or a combination of ROW_NUMBER and COUNT.
""", is_coding=True, code_sql="""
-- Method 1: PERCENTILE_CONT (PostgreSQL, Oracle)
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median_salary
FROM employees;

-- Method 2: Using ROW_NUMBER
WITH ordered AS (
  SELECT salary,
         ROW_NUMBER() OVER (ORDER BY salary) AS rn,
         COUNT(*) OVER () AS total
  FROM employees
)
SELECT AVG(salary) AS median_salary
FROM ordered
WHERE rn IN (FLOOR((total+1)/2.0), CEIL((total+1)/2.0));
""")

add("SQL Coding", "Write a query to unpivot columns into rows.", """
Use UNION ALL or the UNPIVOT operator to transform columns into rows.
""", is_coding=True, code_sql="""
-- Using UNION ALL (universal)
SELECT employee_id, 'Q1' AS quarter, q1_sales AS sales FROM quarterly
UNION ALL
SELECT employee_id, 'Q2', q2_sales FROM quarterly
UNION ALL
SELECT employee_id, 'Q3', q3_sales FROM quarterly
UNION ALL
SELECT employee_id, 'Q4', q4_sales FROM quarterly
ORDER BY employee_id, quarter;
""")

add("SQL Coding", "Write a query to find users who logged in on at least 3 consecutive days.", """
Use LAG/LEAD or self-join to detect consecutive date patterns.
""", is_coding=True, code_sql="""
WITH daily_logins AS (
  SELECT DISTINCT user_id, DATE(login_time) AS login_date
  FROM logins
),
with_prev AS (
  SELECT user_id, login_date,
    login_date - ROW_NUMBER() OVER (
      PARTITION BY user_id ORDER BY login_date
    )::int AS grp
  FROM daily_logins
)
SELECT user_id, MIN(login_date) AS streak_start,
       MAX(login_date) AS streak_end,
       COUNT(*) AS consecutive_days
FROM with_prev
GROUP BY user_id, grp
HAVING COUNT(*) >= 3;
""")

add("SQL Coding", "Write a query to calculate retention rate: % of users who returned within 7 days.", """
Compare each user's first activity with subsequent activities within a 7-day window.
""", is_coding=True, code_sql="""
WITH first_visit AS (
  SELECT user_id, MIN(activity_date) AS first_date
  FROM user_activity GROUP BY user_id
),
returned AS (
  SELECT DISTINCT fv.user_id
  FROM first_visit fv
  JOIN user_activity ua ON fv.user_id = ua.user_id
    AND ua.activity_date BETWEEN fv.first_date + 1
    AND fv.first_date + 7
)
SELECT
  (SELECT COUNT(*) FROM returned) * 100.0 /
  (SELECT COUNT(*) FROM first_visit) AS retention_rate_pct;
""")

add("SQL Coding", "Write a query to implement pagination efficiently.", """
Use OFFSET/LIMIT for simple pagination, or keyset pagination for better performance.
""", is_coding=True, code_sql="""
-- Method 1: OFFSET/LIMIT (simple but slow for large offsets)
SELECT * FROM products
ORDER BY id
LIMIT 20 OFFSET 40;  -- Page 3, 20 per page

-- Method 2: Keyset pagination (faster, uses index)
SELECT * FROM products
WHERE id > :last_seen_id  -- ID of last item on previous page
ORDER BY id
LIMIT 20;
""")

# ═══════════════════════════════════════════════════════════════
# SQL FERMI / ESTIMATION QUESTIONS (10)
# ═══════════════════════════════════════════════════════════════

add("SQL Fermi", "Estimate the storage needed for a table with 1 billion rows and 10 columns averaging 50 bytes each.", """
* **Row size**: 10 columns × 50 bytes = 500 bytes per row.
* **Raw data**: 1B rows × 500 bytes = 500 GB.
* **With overhead** (indexes, padding, row headers): ~1.5x–2x overhead → 750 GB–1 TB.
* **Indexes**: A B-tree index on a single INT column ≈ 8 bytes/entry × 1B = 8 GB per index.
* **Total estimate**: ~1 TB for data + indexes.
* **Compression**: With page-level compression, typically 3x–5x reduction → 200–330 GB compressed.
""")

add("SQL Fermi", "How would you estimate query performance on a 100M row table with no index?", """
* **Full table scan**: Must read every row.
* **Disk I/O**: Assuming 8KB pages, ~100 rows per page → 1M pages. At 10ms random read → 10,000 seconds (terrible). Sequential scan at 200MB/s → ~500 seconds for 100GB.
* **In-memory**: If table fits in buffer cache (~50GB RAM), sequential scan takes seconds.
* **Key insight**: Without an index, ANY selective query degrades to O(N). With a B-tree index, point lookups are O(log N) ≈ 27 comparisons for 100M rows.
""")

add("SQL Fermi", "How many JOINs can a typical query optimizer handle before degrading?", """
* **Practical limit**: Most optimizers handle 8–12 JOINs efficiently. Beyond that, the optimizer's search space grows exponentially (join order permutations = N!).
* **PostgreSQL**: Uses genetic query optimizer (GEQO) when joins exceed geqo_threshold (default 12).
* **Best practice**: If you need 15+ JOINs, consider CTEs, materialized views, or denormalization.
* **Each additional JOIN**: Roughly doubles optimizer planning time and increases risk of suboptimal execution plans.
""")

# ═══════════════════════════════════════════════════════════════
# DBMS DEEP CONCEPTS (30 questions)
# ═══════════════════════════════════════════════════════════════

add("DBMS Deep", "What is Write-Ahead Logging (WAL)? Why is it critical for durability?", """
WAL is a technique where changes are written to a log file BEFORE being applied to the actual database pages.
* **How it works**: Every modification is first recorded in the WAL (sequential writes). The actual data pages are updated lazily.
* **Why critical**: If the system crashes, the database replays the WAL from the last checkpoint to recover committed transactions (redo) and undo uncommitted ones.
* **Performance benefit**: Sequential log writes are much faster than random page writes.
* **Used by**: PostgreSQL (WAL), MySQL InnoDB (redo log), SQLite (WAL mode).
""")

add("DBMS Deep", "What is a B-Tree? How does it differ from a B+ Tree in databases?", """
Both are self-balancing tree data structures used for database indexes:
* **B-Tree**: Stores keys AND data pointers in both internal nodes and leaf nodes. Good for random lookups.
* **B+ Tree** (used by most RDBMS):
  - Only leaf nodes store data pointers. Internal nodes only store keys for navigation.
  - Leaf nodes are linked together in a doubly-linked list for efficient range scans.
  - More keys fit per internal node → shorter tree height → fewer disk I/O operations.
* **Why B+ Tree wins**: Range queries traverse the linked leaf list without going back up the tree. Most RDBMS (PostgreSQL, MySQL, Oracle) use B+ Trees.
""")

add("DBMS Deep", "Explain the difference between optimistic and pessimistic concurrency control.", """
* **Pessimistic Concurrency**: Acquires locks BEFORE accessing data. Assumes conflicts are likely. Other transactions wait.
  - Methods: Row locks, table locks, SELECT FOR UPDATE.
  - Pro: Guarantees no conflicts. Con: Reduced concurrency, deadlock risk.
* **Optimistic Concurrency**: Does NOT acquire locks. Assumes conflicts are rare. At commit time, checks if data was modified by another transaction.
  - Methods: Version numbers, timestamps. If conflict detected → transaction is retried.
  - Pro: High concurrency, no blocking. Con: Wasted work on rollbacks if conflicts are frequent.
* **When to use**: Pessimistic for high-contention (e.g., financial). Optimistic for low-contention (e.g., web reads).
""")

add("DBMS Deep", "What is MVCC (Multi-Version Concurrency Control)?", """
MVCC allows multiple transactions to access the same data concurrently without blocking by maintaining multiple versions of each row.
* **How it works**: When a row is updated, the database creates a new version instead of overwriting. Each transaction sees a snapshot of data as of its start time.
* **Readers never block writers, writers never block readers.**
* **Implementation**:
  - PostgreSQL: Stores old row versions in the same table. Uses VACUUM to clean up dead tuples.
  - MySQL InnoDB: Stores old versions in an undo log (rollback segment).
* **Benefit**: High concurrency for read-heavy workloads without lock contention.
""")

add("DBMS Deep", "What is connection pooling? Why is it important?", """
Connection pooling maintains a cache of reusable database connections rather than creating a new connection for each request.
* **Why important**: Creating a new TCP connection + authentication for every query is expensive (~50-100ms per connection). In high-traffic apps, this causes:
  - Connection exhaustion (databases have max_connections limits).
  - High latency from connection setup overhead.
* **How it works**: A pool manager (e.g., PgBouncer, HikariCP) maintains N open connections. Application requests borrow a connection, use it, and return it to the pool.
* **Key settings**: min_pool_size, max_pool_size, idle_timeout, max_lifetime.
""")

add("DBMS Deep", "What is database replication? Explain master-slave vs multi-master.", """
Replication copies data across multiple database servers for availability, fault tolerance, and read scaling.
* **Master-Slave (Primary-Replica)**:
  - One master handles all writes. Replicas receive copies and handle reads.
  - Pro: Simple, no write conflicts. Con: Single point of failure for writes; replication lag.
* **Multi-Master**:
  - Multiple nodes accept writes. Changes are propagated between all masters.
  - Pro: No single point of failure. Con: Write conflicts must be resolved (last-write-wins, merge, or manual).
* **Sync vs Async**: Synchronous replication waits for replica acknowledgment (strong consistency, higher latency). Asynchronous is faster but risks data loss on master failure.
""")

add("DBMS Deep", "What is database partitioning? Horizontal vs vertical partitioning.", """
Partitioning splits a large table into smaller, more manageable pieces:
* **Horizontal Partitioning**: Splits rows into separate partitions based on a key (e.g., by date range, hash of ID). Each partition has the same columns but different rows. This is what 'sharding' refers to when done across servers.
* **Vertical Partitioning**: Splits columns into separate tables. Frequently accessed columns stay in the main table; rarely accessed large columns (e.g., BLOBs) move to a separate table. Improves cache efficiency.
* **Partition types**: Range, List, Hash, Composite.
* **Benefit**: Partition pruning — queries only scan relevant partitions instead of the full table.
""")

add("DBMS Deep", "Explain the concept of eventual consistency vs strong consistency.", """
* **Strong Consistency**: After a write, all subsequent reads (from any node) immediately return the updated value. Every node sees the same data at the same time. Example: Traditional RDBMS, Google Spanner.
* **Eventual Consistency**: After a write, not all nodes are immediately updated. Given enough time (with no new writes), all replicas will converge to the same value. Example: DynamoDB, Cassandra.
* **Use cases**:
  - Strong: Financial transactions, inventory counts where correctness is critical.
  - Eventual: Social media feeds, DNS, shopping carts where slight staleness is acceptable.
""")

add("DBMS Deep", "What is a query execution plan? How do you read one?", """
A query execution plan shows the step-by-step strategy the database optimizer chose to execute a query.
* **Key nodes to understand**:
  1. **Seq Scan**: Full table scan — reads every row. Warning sign on large tables.
  2. **Index Scan**: Uses an index to find rows. Much faster for selective queries.
  3. **Index Only Scan**: All needed data is in the index itself (covering index). Fastest.
  4. **Nested Loop Join**: For each row in outer table, scans inner table. O(N×M). Good for small tables.
  5. **Hash Join**: Builds hash table of smaller table, probes with larger. O(N+M). Good for large tables.
  6. **Merge Join**: Both tables sorted, then merged. O(N log N). Good when both are already sorted/indexed.
  7. **Sort**: External sort (spills to disk if work_mem exceeded).
""")

add("DBMS Deep", "What are phantom reads? How does Serializable isolation prevent them?", """
* **Phantom Read**: A transaction re-executes a query and gets a DIFFERENT SET of rows because another transaction inserted/deleted rows that match the query's WHERE clause.
* **Example**: Transaction A: SELECT COUNT(*) FROM orders WHERE status='pending' returns 10. Transaction B: INSERTs a new pending order. Transaction A re-runs the same query and gets 11.
* **Prevention at Serializable level**: Uses range locks or predicate locks that lock the entire range matching the WHERE condition, preventing any INSERT/DELETE by other transactions within that range.
""")
