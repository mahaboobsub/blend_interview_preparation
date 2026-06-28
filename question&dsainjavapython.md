# Interview Question Bank — Assessment Aligned

> Compiled with detailed answers. Duplicates removed.

---

## SQL, DB Design & DBMS Deep Concepts

### Q: What does ACID stand for? Explain each property.

**A:** ACID stands for:
* **Atomicity**: All operations in a transaction succeed, or the entire transaction is rolled back (All-or-Nothing).
* **Consistency**: A transaction takes the database from one valid state to another, maintaining all schema constraints and rules.
* **Isolation**: Concurrent transactions don't interfere; the result is the same as if transactions ran sequentially. Prevents dirty reads, non-repeatable reads, and phantom reads.
* **Durability**: Once committed, changes are permanently written to non-volatile storage and survive system failures.

---

### Q: What is a transaction in a database? Give an example.

**A:** A transaction is a logical unit of work containing one or more SQL statements that must complete entirely or not at all.
* **Example**: Bank transfer of $100 from Account A to B:
  1. UPDATE accounts SET balance = balance - 100 WHERE id = 'A';
  2. UPDATE accounts SET balance = balance + 100 WHERE id = 'B';
  Both must succeed. If step 2 fails, step 1 is rolled back.

---

### Q: What is a primary key? Rules for primary key.

**A:** A primary key uniquely identifies each row in a table.
* **Rules**:
  1. **Uniqueness**: Each value must be unique.
  2. **Non-Nullability**: Cannot contain NULL values.
  3. **Single per table**: A table can have only one primary key.
  4. **Stability**: Values should rarely change.
  5. Can be a composite key (multiple columns together).

---

### Q: What is a foreign key? What is referential integrity?

**A:** * **Foreign Key**: A column or set of columns that references the primary key of another table, establishing a parent-child relationship.
* **Referential Integrity**: Ensures that a foreign key value must match an existing primary key value in the referenced table, preventing orphaned rows. Enforced with ON DELETE CASCADE, SET NULL, or RESTRICT actions.

---

### Q: What is normalization? Explain 1NF, 2NF, 3NF, and BCNF.

**A:** Normalization structures tables to reduce redundancy and anomalies:
* **1NF**: Atomic values only; no repeating groups or arrays in cells. Each row is unique.
* **2NF**: Satisfies 1NF + every non-key column fully depends on the entire primary key (no partial dependency on composite keys).
* **3NF**: Satisfies 2NF + no transitive dependencies (non-key columns don't depend on other non-key columns).
* **BCNF (Boyce-Codd)**: For every functional dependency X→Y, X must be a superkey. Stricter than 3NF; handles edge cases where 3NF still allows anomalies.

---

### Q: What is denormalization? When would you use it?

**A:** Denormalization intentionally adds redundancy back into normalized tables to optimize read performance.
* **When to use**:
  - Read-heavy OLAP/data warehouse workloads where JOINs are expensive.
  - Frequently accessed reports or dashboards needing pre-computed aggregates.
  - Real-time applications where low-latency reads are critical.
* **Trade-off**: Faster reads, but slower writes and risk of data inconsistency.

---

### Q: Explain the differences between INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL OUTER JOIN, and CROSS JOIN.

**A:** * **INNER JOIN**: Returns only rows with matching keys in both tables.
* **LEFT JOIN**: Returns all rows from the left table + matched rows from the right (NULLs for non-matches).
* **RIGHT JOIN**: Returns all rows from the right table + matched rows from the left (NULLs for non-matches).
* **FULL OUTER JOIN**: Returns all rows from both tables; NULLs where there's no match on either side.
* **CROSS JOIN**: Cartesian product — every row from table A paired with every row from table B. No join condition needed.

---

### Q: What is a self-join? Give a practical use case.

**A:** A self-join joins a table to itself using aliases to compare rows within the same table.
* **Use case**: Finding employees and their managers when both are in the same 'employees' table:
  SELECT e.name AS employee, m.name AS manager
  FROM employees e JOIN employees m ON e.manager_id = m.id;
* Also used for: finding duplicates, hierarchical data, comparing sequential records.

---

### Q: Explain the difference between WHERE and HAVING clauses.

**A:** * **WHERE**: Filters individual rows BEFORE grouping (applied to raw rows). Cannot use aggregate functions.
* **HAVING**: Filters groups AFTER GROUP BY (applied to aggregated results). Can use aggregate functions like COUNT(), SUM(), AVG().
* **Example**: WHERE salary > 50000 filters rows; HAVING COUNT(*) > 5 filters groups.
* **Execution order**: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY.

---

### Q: What is the SQL execution order? Explain the logical processing sequence.

**A:** SQL statements are processed in this logical order (not the written order):
1. **FROM** / **JOIN** — Identify source tables and join them.
2. **WHERE** — Filter individual rows.
3. **GROUP BY** — Group remaining rows by specified columns.
4. **HAVING** — Filter aggregated groups.
5. **SELECT** — Choose output columns and compute expressions.
6. **DISTINCT** — Remove duplicate rows.
7. **ORDER BY** — Sort the result set.
8. **LIMIT / OFFSET** — Restrict the number of returned rows.

---

### Q: What is a subquery? Difference between correlated and non-correlated subqueries.

**A:** A subquery is a query nested inside another query (SELECT, WHERE, FROM, or HAVING).
* **Non-correlated subquery**: Executes independently once. Inner query doesn't reference the outer query. Example: WHERE salary > (SELECT AVG(salary) FROM employees).
* **Correlated subquery**: References columns from the outer query. Executes once PER ROW of the outer query. Example: WHERE salary > (SELECT AVG(salary) FROM employees e2 WHERE e2.dept_id = e1.dept_id).
* Correlated subqueries are slower but more powerful for row-by-row comparisons.

---

### Q: What is a Common Table Expression (CTE)? Benefits over subqueries?

**A:** A CTE is a temporary named result set defined with the WITH clause that exists only during query execution.
* **Syntax**: WITH cte_name AS (SELECT ...) SELECT * FROM cte_name;
* **Benefits over subqueries**:
  1. **Readability**: Named, modular, easier to understand than nested subqueries.
  2. **Reusability**: Can reference the same CTE multiple times in one query.
  3. **Recursion**: Supports recursive CTEs for hierarchical data (e.g., org charts, tree traversal).
  4. **Debugging**: Easier to test each CTE independently.

---

### Q: Explain window functions: ROW_NUMBER, RANK, DENSE_RANK, NTILE.

**A:** Window functions perform calculations across a set of rows related to the current row without collapsing groups:
* **ROW_NUMBER()**: Assigns a unique sequential number to every row regardless of ties. (1, 2, 3, 4)
* **RANK()**: Same rank for ties, skips subsequent numbers. (1, 2, 2, 4)
* **DENSE_RANK()**: Same rank for ties, no gaps. (1, 2, 2, 3)
* **NTILE(n)**: Divides rows into n roughly equal buckets and assigns bucket numbers. Useful for percentile/quartile analysis.
All use OVER(PARTITION BY ... ORDER BY ...) clause.

---

### Q: Explain LAG, LEAD, SUM OVER, and AVG OVER window functions.

**A:** * **LAG(col, n)**: Accesses data from n rows BEFORE the current row within the partition. Useful for calculating differences (e.g., month-over-month change).
* **LEAD(col, n)**: Accesses data from n rows AFTER the current row. Useful for forward-looking comparisons.
* **SUM() OVER(...)**: Running/cumulative sum across ordered rows. SUM(sales) OVER(ORDER BY date) gives running total.
* **AVG() OVER(...)**: Moving average. AVG(price) OVER(ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) gives 7-day moving average.

---

### Q: What is an index? Types of indexes and when to use them.

**A:** An index is a data structure that speeds up data retrieval by creating pointers to rows based on indexed column values.
* **Types**:
  1. **Clustered Index**: Physically reorders table data. Only ONE per table. Usually the primary key.
  2. **Non-clustered Index**: Separate structure with pointers back to data. Multiple allowed per table.
  3. **Composite Index**: Index on multiple columns. Column order matters for query matching.
  4. **Unique Index**: Enforces uniqueness on indexed columns.
  5. **Full-text Index**: For text search operations.
  6. **Covering Index**: Contains all columns needed by a query, avoiding table lookups.
* **When to use**: Columns frequently used in WHERE, JOIN, ORDER BY, or GROUP BY clauses.
* **Trade-off**: Faster reads but slower writes (index must be updated on INSERT/UPDATE/DELETE).

---

### Q: What is a view? What is a materialized view? Differences.

**A:** * **View**: A virtual table defined by a stored SQL query. No data stored; re-executes the query each time it's accessed. Provides abstraction and security.
* **Materialized View**: A physical snapshot of a query result stored on disk. Must be refreshed manually or on schedule.
* **Key Differences**:
  | Feature | View | Materialized View |
  |---------|------|-------------------|
  | Storage | No data stored | Data cached on disk |
  | Speed | Slow (re-executes) | Fast (pre-computed) |
  | Freshness | Always current | Stale until refreshed |
  | Use case | Security/abstraction | Reporting/dashboards |

---

### Q: What is a stored procedure? Advantages and disadvantages.

**A:** A stored procedure is a precompiled set of SQL statements stored in the database that can be executed with parameters.
* **Advantages**:
  1. Performance: Pre-compiled execution plan, reducing parsing overhead.
  2. Security: Users can execute procedures without direct table access.
  3. Reusability: Centralized business logic callable from any application.
  4. Reduced network traffic: Single call instead of multiple SQL statements.
* **Disadvantages**:
  1. Debugging difficulty: Harder to debug than application code.
  2. Vendor lock-in: Syntax differs between databases.
  3. Version control: Harder to track changes in source control.

---

### Q: What is a trigger? When should you use or avoid triggers?

**A:** A trigger is a stored procedure that automatically executes in response to specific table events (INSERT, UPDATE, DELETE).
* **Types**: BEFORE trigger, AFTER trigger, INSTEAD OF trigger.
* **Use cases**: Audit logging, enforcing complex business rules, maintaining denormalized summary tables, cascading updates.
* **Avoid when**:
  - Complex business logic (use application layer instead).
  - Performance-sensitive tables (triggers add overhead to every DML operation).
  - Cascading triggers (trigger A fires trigger B which fires trigger A — infinite loop risk).

---

### Q: What is a cursor? Why are cursors generally discouraged?

**A:** A cursor is a database object that allows row-by-row processing of a result set.
* **How it works**: DECLARE cursor → OPEN → FETCH rows one by one → CLOSE → DEALLOCATE.
* **Why discouraged**:
  1. **Performance**: Row-by-row processing is drastically slower than set-based operations. SQL engines are optimized for set operations.
  2. **Memory**: Holds locks and consumes memory for the duration.
  3. **Scalability**: Doesn't parallelize well.
* **When acceptable**: Complex procedural logic that can't be expressed in set-based SQL (rare), ETL processing with error handling per row.

---

### Q: What is the difference between DELETE, TRUNCATE, and DROP?

**A:** * **DELETE**: DML operation. Removes specific rows (can use WHERE clause). Logs each row deletion. Can be rolled back. Fires triggers.
* **TRUNCATE**: DDL operation. Removes ALL rows from a table. Minimal logging (deallocates pages). Cannot be rolled back in most RDBMS. Does NOT fire triggers. Resets identity counter.
* **DROP**: DDL operation. Removes the entire table structure (schema + data) from the database. Cannot be rolled back.
* **Speed**: DROP > TRUNCATE > DELETE.

---

### Q: What is the difference between UNION and UNION ALL?

**A:** * **UNION**: Combines result sets of two queries and removes duplicate rows. Performs an implicit DISTINCT, which requires sorting — slower.
* **UNION ALL**: Combines result sets and keeps ALL rows including duplicates. Faster because no deduplication step.
* **Rule**: Both queries must have the same number of columns with compatible data types.
* **Best practice**: Use UNION ALL when you know there are no duplicates or duplicates are acceptable.

---

### Q: Explain GROUP BY with ROLLUP, CUBE, and GROUPING SETS.

**A:** These are GROUP BY extensions for multi-level aggregation:
* **ROLLUP**: Creates subtotals rolling up from the most detailed level to a grand total. GROUP BY ROLLUP(year, quarter) gives: year+quarter totals, year totals, grand total.
* **CUBE**: Creates subtotals for ALL possible combinations. GROUP BY CUBE(year, quarter) gives: year+quarter, year only, quarter only, and grand total.
* **GROUPING SETS**: Allows specifying exactly which grouping combinations to compute. More selective than CUBE.
* **GROUPING()** function identifies which rows are subtotals (returns 1 for aggregated, 0 for detail).

---

### Q: What are isolation levels? Explain Read Uncommitted, Read Committed, Repeatable Read, and Serializable.

**A:** Isolation levels control how much one transaction can see of another's uncommitted changes:
* **Read Uncommitted**: Lowest isolation. Allows dirty reads (reading uncommitted data from other transactions).
* **Read Committed**: Prevents dirty reads. Only sees data committed before the statement began. Default in PostgreSQL, Oracle.
* **Repeatable Read**: Prevents dirty reads and non-repeatable reads. Data read once stays the same within the transaction. Default in MySQL InnoDB.
* **Serializable**: Highest isolation. Transactions behave as if executed serially. Prevents phantom reads but has the lowest concurrency.
* **Trade-off**: Higher isolation = more consistency but less concurrency and more locks/deadlocks.

---

### Q: What is a deadlock? How do databases handle deadlocks?

**A:** A deadlock occurs when two or more transactions are waiting for each other to release locks, creating a circular dependency where none can proceed.
* **Example**: Transaction A locks Row 1, waits for Row 2. Transaction B locks Row 2, waits for Row 1.
* **Detection**: Databases use a wait-for graph. When a cycle is detected, one transaction (the victim) is rolled back.
* **Prevention strategies**:
  1. Lock ordering: Always acquire locks in the same order.
  2. Lock timeouts: Set maximum wait times.
  3. Keep transactions short: Reduce lock hold time.
  4. Use appropriate isolation levels.

---

### Q: What is database sharding? Strategies and trade-offs.

**A:** Sharding is horizontal partitioning of data across multiple database instances (shards), each holding a subset of the data.
* **Strategies**:
  1. **Range-based**: Partition by value range (e.g., user IDs 1-1M on shard 1, 1M-2M on shard 2). Simple but can create hot spots.
  2. **Hash-based**: Apply hash function to the shard key. Better distribution but makes range queries difficult.
  3. **Geographic**: Shard by region/location for data locality.
  4. **Directory-based**: Lookup table maps each record to its shard. Flexible but the directory becomes a bottleneck.
* **Trade-offs**: Enables horizontal scaling but adds complexity in cross-shard JOINs, distributed transactions, and rebalancing.

---

### Q: Compare SQL (relational) vs NoSQL databases. When to use which?

**A:** * **SQL (Relational)**: Structured schema, ACID transactions, normalized data, SQL query language. Examples: PostgreSQL, MySQL, Oracle.
* **NoSQL**: Flexible/schema-less, BASE properties, various data models. Types:
  1. **Document**: MongoDB, CouchDB — JSON documents, nested data.
  2. **Key-Value**: Redis, DynamoDB — simple lookups, caching.
  3. **Column-Family**: Cassandra, HBase — wide-column stores for analytics.
  4. **Graph**: Neo4j, Amazon Neptune — relationship-heavy data.
* **When SQL**: Complex queries, transactions, strong consistency, structured data.
* **When NoSQL**: High scalability, flexible schemas, rapid iteration, specific data models (graphs, documents).

---

### Q: What is CAP theorem? How does it apply to distributed databases?

**A:** CAP theorem states that a distributed system can guarantee at most two of three properties:
* **Consistency (C)**: Every read receives the most recent write.
* **Availability (A)**: Every request receives a response (success or failure).
* **Partition Tolerance (P)**: The system continues to operate despite network partitions between nodes.
* Since network partitions are inevitable, you must choose between CP or AP:
  - **CP systems**: Prioritize consistency over availability (e.g., MongoDB, HBase). During partition, some nodes refuse requests.
  - **AP systems**: Prioritize availability over consistency (e.g., Cassandra, DynamoDB). May return stale data during partition.

---

### Q: What are database constraints? List and explain each type.

**A:** Constraints enforce rules on data in tables:
1. **NOT NULL**: Column cannot contain NULL values.
2. **UNIQUE**: All values in a column must be distinct (allows one NULL in most RDBMS).
3. **PRIMARY KEY**: Combination of NOT NULL + UNIQUE. One per table.
4. **FOREIGN KEY**: Enforces referential integrity between tables.
5. **CHECK**: Validates that values satisfy a Boolean expression (e.g., CHECK(age >= 18)).
6. **DEFAULT**: Provides a default value when no value is specified on INSERT.

---

### Q: Explain OLTP vs OLAP. How do their database designs differ?

**A:** * **OLTP (Online Transaction Processing)**: Handles day-to-day operations (INSERT, UPDATE, DELETE). Highly normalized (3NF). Optimized for write performance and data integrity. Examples: banking, e-commerce.
* **OLAP (Online Analytical Processing)**: Handles complex analytical queries on historical data. Denormalized (star/snowflake schema). Optimized for read-heavy aggregation queries. Examples: data warehouses, BI dashboards.
* **Key Differences**:
  | Feature | OLTP | OLAP |
  |---------|------|------|
  | Operations | CRUD | READ-heavy analytics |
  | Schema | Normalized (3NF) | Denormalized (Star) |
  | Data | Current, operational | Historical, aggregated |
  | Users | App users | Data analysts |

---

### Q: What is a star schema vs snowflake schema in data warehousing?

**A:** Both are dimensional modeling schemas for data warehouses:
* **Star Schema**: Central fact table connected directly to dimension tables. Denormalized dimensions. Simpler queries, faster reads, more storage.
* **Snowflake Schema**: Dimensions are further normalized into sub-dimension tables. Reduces redundancy but requires more JOINs.
* **Example**: In a star schema, a 'products' dimension has all product info in one table. In snowflake, 'products' references a separate 'categories' table.
* **Best practice**: Star schema is preferred for most BI tools and query performance. Snowflake for storage optimization.

---

### Q: What is query optimization? Explain EXPLAIN/EXPLAIN ANALYZE.

**A:** Query optimization is the process of improving SQL query performance by analyzing and restructuring queries.
* **EXPLAIN**: Shows the query execution plan without running the query. Displays which indexes are used, join types, estimated row counts.
* **EXPLAIN ANALYZE**: Actually executes the query and shows real timing, row counts, and buffer usage alongside the plan.
* **Key things to look for**:
  1. Sequential Scan vs Index Scan (seq scan on large tables = bad).
  2. Nested Loop vs Hash Join vs Merge Join.
  3. Estimated vs actual row counts (large discrepancies = stale statistics).
  4. Sort operations (external sorts indicate insufficient work_mem).

---

### Q: Write a query to find the second highest salary from an Employees table.

**A:** Use DENSE_RANK or subquery to find the second highest salary. The DENSE_RANK approach handles ties correctly.

```sql
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
```

---

### Q: Write a query to find the Nth highest salary.

**A:** Generalized version: find the Nth highest salary using DENSE_RANK window function.

```sql
-- Using DENSE_RANK (handles ties)
SELECT salary FROM (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
  FROM employees
) ranked WHERE rnk = :N;

-- Using LIMIT/OFFSET (N=3 example)
SELECT DISTINCT salary FROM employees
ORDER BY salary DESC LIMIT 1 OFFSET 2;
```

---

### Q: Write a query to find duplicate records in a table.

**A:** Use GROUP BY with HAVING COUNT(*) > 1 to find duplicates based on specific columns.

```sql
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
```

---

### Q: Write a query to find employees who earn more than their manager.

**A:** Use a self-join to compare each employee's salary with their manager's salary.

```sql
SELECT e.name AS employee, e.salary AS emp_salary,
       m.name AS manager, m.salary AS mgr_salary
FROM employees e
JOIN employees m ON e.manager_id = m.id
WHERE e.salary > m.salary;
```

---

### Q: Write a query to find departments with more than 5 employees.

**A:** Group by department and filter using HAVING.

```sql
SELECT d.name AS department, COUNT(e.id) AS emp_count
FROM departments d
JOIN employees e ON d.id = e.dept_id
GROUP BY d.name
HAVING COUNT(e.id) > 5
ORDER BY emp_count DESC;
```

---

### Q: Write a query for running total (cumulative sum) of sales by date.

**A:** Use SUM() window function with ORDER BY to calculate running total.

```sql
SELECT sale_date, amount,
       SUM(amount) OVER (ORDER BY sale_date) AS running_total
FROM sales
ORDER BY sale_date;

-- Running total partitioned by region
SELECT region, sale_date, amount,
       SUM(amount) OVER (PARTITION BY region ORDER BY sale_date) AS running_total
FROM sales;
```

---

### Q: Write a query to find month-over-month revenue growth.

**A:** Use LAG() window function to access previous month's revenue and calculate percentage change.

```sql
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
```

---

### Q: Write a query to find customers who placed orders in consecutive months.

**A:** Use LAG or LEAD to compare each order's month with the previous order's month for the same customer.

```sql
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
```

---

### Q: Write a query to pivot rows into columns (cross-tab query).

**A:** Use CASE WHEN inside aggregate functions or PIVOT (SQL Server) to transform rows to columns.

```sql
-- Manual pivot using CASE
SELECT employee_id,
  SUM(CASE WHEN quarter = 'Q1' THEN sales ELSE 0 END) AS Q1,
  SUM(CASE WHEN quarter = 'Q2' THEN sales ELSE 0 END) AS Q2,
  SUM(CASE WHEN quarter = 'Q3' THEN sales ELSE 0 END) AS Q3,
  SUM(CASE WHEN quarter = 'Q4' THEN sales ELSE 0 END) AS Q4
FROM quarterly_sales
GROUP BY employee_id;
```

---

### Q: Write a query to find the top 3 products by revenue in each category.

**A:** Use ROW_NUMBER or RANK partitioned by category and ordered by revenue.

```sql
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
```

---

### Q: Write a recursive CTE to traverse an organizational hierarchy.

**A:** Recursive CTEs have a base case (anchor) and a recursive member joined back to the CTE.

```sql
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
```

---

### Q: Write a query to detect gaps in a sequential ID column.

**A:** Use LAG or LEAD to compare consecutive IDs and find where the difference is greater than 1.

```sql
-- Find gaps in sequential IDs
SELECT id + 1 AS gap_start,
       next_id - 1 AS gap_end
FROM (
  SELECT id,
         LEAD(id) OVER (ORDER BY id) AS next_id
  FROM my_table
) t
WHERE next_id - id > 1;
```

---

### Q: Write a query to calculate a 7-day moving average of daily sales.

**A:** Use AVG() window function with ROWS BETWEEN clause for a sliding window.

```sql
SELECT sale_date, daily_sales,
       AVG(daily_sales) OVER (
         ORDER BY sale_date
         ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
       ) AS moving_avg_7day
FROM daily_sales_table
ORDER BY sale_date;
```

---

### Q: Write a query to find all employees who share the same birthday month.

**A:** Extract the month from the date and use GROUP BY with HAVING.

```sql
SELECT EXTRACT(MONTH FROM birthday) AS birth_month,
       STRING_AGG(name, ', ') AS employees,
       COUNT(*) AS count
FROM employees
GROUP BY EXTRACT(MONTH FROM birthday)
HAVING COUNT(*) > 1
ORDER BY birth_month;
```

---

### Q: Write a query using NTILE to divide employees into salary quartiles.

**A:** NTILE(4) divides ordered rows into 4 roughly equal groups.

```sql
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
```

---

### Q: Write a query to find the median salary.

**A:** Use PERCENTILE_CONT or a combination of ROW_NUMBER and COUNT.

```sql
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
```

---

### Q: Write a query to unpivot columns into rows.

**A:** Use UNION ALL or the UNPIVOT operator to transform columns into rows.

```sql
-- Using UNION ALL (universal)
SELECT employee_id, 'Q1' AS quarter, q1_sales AS sales FROM quarterly
UNION ALL
SELECT employee_id, 'Q2', q2_sales FROM quarterly
UNION ALL
SELECT employee_id, 'Q3', q3_sales FROM quarterly
UNION ALL
SELECT employee_id, 'Q4', q4_sales FROM quarterly
ORDER BY employee_id, quarter;
```

---

### Q: Write a query to find users who logged in on at least 3 consecutive days.

**A:** Use LAG/LEAD or self-join to detect consecutive date patterns.

```sql
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
```

---

### Q: Write a query to calculate retention rate: % of users who returned within 7 days.

**A:** Compare each user's first activity with subsequent activities within a 7-day window.

```sql
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
```

---

### Q: Write a query to implement pagination efficiently.

**A:** Use OFFSET/LIMIT for simple pagination, or keyset pagination for better performance.

```sql
-- Method 1: OFFSET/LIMIT (simple but slow for large offsets)
SELECT * FROM products
ORDER BY id
LIMIT 20 OFFSET 40;  -- Page 3, 20 per page

-- Method 2: Keyset pagination (faster, uses index)
SELECT * FROM products
WHERE id > :last_seen_id  -- ID of last item on previous page
ORDER BY id
LIMIT 20;
```

---

### Q: Estimate the storage needed for a table with 1 billion rows and 10 columns averaging 50 bytes each.

**A:** * **Row size**: 10 columns × 50 bytes = 500 bytes per row.
* **Raw data**: 1B rows × 500 bytes = 500 GB.
* **With overhead** (indexes, padding, row headers): ~1.5x–2x overhead → 750 GB–1 TB.
* **Indexes**: A B-tree index on a single INT column ≈ 8 bytes/entry × 1B = 8 GB per index.
* **Total estimate**: ~1 TB for data + indexes.
* **Compression**: With page-level compression, typically 3x–5x reduction → 200–330 GB compressed.

---

### Q: How would you estimate query performance on a 100M row table with no index?

**A:** * **Full table scan**: Must read every row.
* **Disk I/O**: Assuming 8KB pages, ~100 rows per page → 1M pages. At 10ms random read → 10,000 seconds (terrible). Sequential scan at 200MB/s → ~500 seconds for 100GB.
* **In-memory**: If table fits in buffer cache (~50GB RAM), sequential scan takes seconds.
* **Key insight**: Without an index, ANY selective query degrades to O(N). With a B-tree index, point lookups are O(log N) ≈ 27 comparisons for 100M rows.

---

### Q: How many JOINs can a typical query optimizer handle before degrading?

**A:** * **Practical limit**: Most optimizers handle 8–12 JOINs efficiently. Beyond that, the optimizer's search space grows exponentially (join order permutations = N!).
* **PostgreSQL**: Uses genetic query optimizer (GEQO) when joins exceed geqo_threshold (default 12).
* **Best practice**: If you need 15+ JOINs, consider CTEs, materialized views, or denormalization.
* **Each additional JOIN**: Roughly doubles optimizer planning time and increases risk of suboptimal execution plans.

---

### Q: What is Write-Ahead Logging (WAL)? Why is it critical for durability?

**A:** WAL is a technique where changes are written to a log file BEFORE being applied to the actual database pages.
* **How it works**: Every modification is first recorded in the WAL (sequential writes). The actual data pages are updated lazily.
* **Why critical**: If the system crashes, the database replays the WAL from the last checkpoint to recover committed transactions (redo) and undo uncommitted ones.
* **Performance benefit**: Sequential log writes are much faster than random page writes.
* **Used by**: PostgreSQL (WAL), MySQL InnoDB (redo log), SQLite (WAL mode).

---

### Q: What is a B-Tree? How does it differ from a B+ Tree in databases?

**A:** Both are self-balancing tree data structures used for database indexes:
* **B-Tree**: Stores keys AND data pointers in both internal nodes and leaf nodes. Good for random lookups.
* **B+ Tree** (used by most RDBMS):
  - Only leaf nodes store data pointers. Internal nodes only store keys for navigation.
  - Leaf nodes are linked together in a doubly-linked list for efficient range scans.
  - More keys fit per internal node → shorter tree height → fewer disk I/O operations.
* **Why B+ Tree wins**: Range queries traverse the linked leaf list without going back up the tree. Most RDBMS (PostgreSQL, MySQL, Oracle) use B+ Trees.

---

### Q: Explain the difference between optimistic and pessimistic concurrency control.

**A:** * **Pessimistic Concurrency**: Acquires locks BEFORE accessing data. Assumes conflicts are likely. Other transactions wait.
  - Methods: Row locks, table locks, SELECT FOR UPDATE.
  - Pro: Guarantees no conflicts. Con: Reduced concurrency, deadlock risk.
* **Optimistic Concurrency**: Does NOT acquire locks. Assumes conflicts are rare. At commit time, checks if data was modified by another transaction.
  - Methods: Version numbers, timestamps. If conflict detected → transaction is retried.
  - Pro: High concurrency, no blocking. Con: Wasted work on rollbacks if conflicts are frequent.
* **When to use**: Pessimistic for high-contention (e.g., financial). Optimistic for low-contention (e.g., web reads).

---

### Q: What is MVCC (Multi-Version Concurrency Control)?

**A:** MVCC allows multiple transactions to access the same data concurrently without blocking by maintaining multiple versions of each row.
* **How it works**: When a row is updated, the database creates a new version instead of overwriting. Each transaction sees a snapshot of data as of its start time.
* **Readers never block writers, writers never block readers.**
* **Implementation**:
  - PostgreSQL: Stores old row versions in the same table. Uses VACUUM to clean up dead tuples.
  - MySQL InnoDB: Stores old versions in an undo log (rollback segment).
* **Benefit**: High concurrency for read-heavy workloads without lock contention.

---

### Q: What is connection pooling? Why is it important?

**A:** Connection pooling maintains a cache of reusable database connections rather than creating a new connection for each request.
* **Why important**: Creating a new TCP connection + authentication for every query is expensive (~50-100ms per connection). In high-traffic apps, this causes:
  - Connection exhaustion (databases have max_connections limits).
  - High latency from connection setup overhead.
* **How it works**: A pool manager (e.g., PgBouncer, HikariCP) maintains N open connections. Application requests borrow a connection, use it, and return it to the pool.
* **Key settings**: min_pool_size, max_pool_size, idle_timeout, max_lifetime.

---

### Q: What is database replication? Explain master-slave vs multi-master.

**A:** Replication copies data across multiple database servers for availability, fault tolerance, and read scaling.
* **Master-Slave (Primary-Replica)**:
  - One master handles all writes. Replicas receive copies and handle reads.
  - Pro: Simple, no write conflicts. Con: Single point of failure for writes; replication lag.
* **Multi-Master**:
  - Multiple nodes accept writes. Changes are propagated between all masters.
  - Pro: No single point of failure. Con: Write conflicts must be resolved (last-write-wins, merge, or manual).
* **Sync vs Async**: Synchronous replication waits for replica acknowledgment (strong consistency, higher latency). Asynchronous is faster but risks data loss on master failure.

---

### Q: What is database partitioning? Horizontal vs vertical partitioning.

**A:** Partitioning splits a large table into smaller, more manageable pieces:
* **Horizontal Partitioning**: Splits rows into separate partitions based on a key (e.g., by date range, hash of ID). Each partition has the same columns but different rows. This is what 'sharding' refers to when done across servers.
* **Vertical Partitioning**: Splits columns into separate tables. Frequently accessed columns stay in the main table; rarely accessed large columns (e.g., BLOBs) move to a separate table. Improves cache efficiency.
* **Partition types**: Range, List, Hash, Composite.
* **Benefit**: Partition pruning — queries only scan relevant partitions instead of the full table.

---

### Q: Explain the concept of eventual consistency vs strong consistency.

**A:** * **Strong Consistency**: After a write, all subsequent reads (from any node) immediately return the updated value. Every node sees the same data at the same time. Example: Traditional RDBMS, Google Spanner.
* **Eventual Consistency**: After a write, not all nodes are immediately updated. Given enough time (with no new writes), all replicas will converge to the same value. Example: DynamoDB, Cassandra.
* **Use cases**:
  - Strong: Financial transactions, inventory counts where correctness is critical.
  - Eventual: Social media feeds, DNS, shopping carts where slight staleness is acceptable.

---

### Q: What is a query execution plan? How do you read one?

**A:** A query execution plan shows the step-by-step strategy the database optimizer chose to execute a query.
* **Key nodes to understand**:
  1. **Seq Scan**: Full table scan — reads every row. Warning sign on large tables.
  2. **Index Scan**: Uses an index to find rows. Much faster for selective queries.
  3. **Index Only Scan**: All needed data is in the index itself (covering index). Fastest.
  4. **Nested Loop Join**: For each row in outer table, scans inner table. O(N×M). Good for small tables.
  5. **Hash Join**: Builds hash table of smaller table, probes with larger. O(N+M). Good for large tables.
  6. **Merge Join**: Both tables sorted, then merged. O(N log N). Good when both are already sorted/indexed.
  7. **Sort**: External sort (spills to disk if work_mem exceeded).

---

### Q: What are phantom reads? How does Serializable isolation prevent them?

**A:** * **Phantom Read**: A transaction re-executes a query and gets a DIFFERENT SET of rows because another transaction inserted/deleted rows that match the query's WHERE clause.
* **Example**: Transaction A: SELECT COUNT(*) FROM orders WHERE status='pending' returns 10. Transaction B: INSERTs a new pending order. Transaction A re-runs the same query and gets 11.
* **Prevention at Serializable level**: Uses range locks or predicate locks that lock the entire range matching the WHERE condition, preventing any INSERT/DELETE by other transactions within that range.

---

## Data Structures & Algorithms (DSA)

### Q: Two Sum: Find two numbers that add up to a target.

**A:** Given an array of integers and a target, return indices of two numbers that add up to the target.
* **Approach**: Use a HashMap to store each number's complement (target - num) as you iterate. O(n) time, O(n) space.

```java
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (map.containsKey(complement))
            return new int[]{map.get(complement), i};
        map.put(nums[i], i);
    }
    return new int[]{};
}
```

```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

---

### Q: Best Time to Buy and Sell Stock: Maximum profit from one transaction.

**A:** Track the minimum price seen so far and calculate profit at each step.
* **Approach**: Single pass, O(n) time, O(1) space. Keep running min_price and max_profit.

```java
public int maxProfit(int[] prices) {
    int minPrice = Integer.MAX_VALUE, maxProfit = 0;
    for (int price : prices) {
        minPrice = Math.min(minPrice, price);
        maxProfit = Math.max(maxProfit, price - minPrice);
    }
    return maxProfit;
}
```

```python
def max_profit(prices):
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    return max_profit
```

---

### Q: Contains Duplicate: Check if any value appears at least twice.

**A:** Use a HashSet to track seen values. If a number is already in the set, return true.
* **Time**: O(n), **Space**: O(n).

```java
public boolean containsDuplicate(int[] nums) {
    Set<Integer> seen = new HashSet<>();
    for (int num : nums) {
        if (!seen.add(num)) return true;
    }
    return false;
}
```

```python
def contains_duplicate(nums):
    return len(nums) != len(set(nums))
```

---

### Q: Product of Array Except Self: Return array where each element is the product of all others.

**A:** Use prefix and suffix products without division.
* **Approach**: Two passes — first pass computes prefix products, second pass multiplies by suffix products. O(n) time, O(1) extra space (output array doesn't count).

```java
public int[] productExceptSelf(int[] nums) {
    int n = nums.length;
    int[] result = new int[n];
    result[0] = 1;
    for (int i = 1; i < n; i++)
        result[i] = result[i-1] * nums[i-1];  // prefix
    int suffix = 1;
    for (int i = n-1; i >= 0; i--) {
        result[i] *= suffix;
        suffix *= nums[i];
    }
    return result;
}
```

```python
def product_except_self(nums):
    n = len(nums)
    result = [1] * n
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n-1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
    return result
```

---

### Q: Maximum Subarray (Kadane's Algorithm): Find contiguous subarray with the largest sum.

**A:** Kadane's Algorithm: Track current_sum and max_sum. Reset current_sum to current element if it drops below.
* **Time**: O(n), **Space**: O(1).

```java
public int maxSubArray(int[] nums) {
    int maxSum = nums[0], curSum = nums[0];
    for (int i = 1; i < nums.length; i++) {
        curSum = Math.max(nums[i], curSum + nums[i]);
        maxSum = Math.max(maxSum, curSum);
    }
    return maxSum;
}
```

```python
def max_sub_array(nums):
    max_sum = cur_sum = nums[0]
    for num in nums[1:]:
        cur_sum = max(num, cur_sum + num)
        max_sum = max(max_sum, cur_sum)
    return max_sum
```

---

### Q: Merge Two Sorted Arrays in-place.

**A:** Start from the end of both arrays and fill the larger array from the back.
* **Time**: O(m+n), **Space**: O(1).

```java
public void merge(int[] nums1, int m, int[] nums2, int n) {
    int i = m - 1, j = n - 1, k = m + n - 1;
    while (j >= 0) {
        if (i >= 0 && nums1[i] > nums2[j])
            nums1[k--] = nums1[i--];
        else
            nums1[k--] = nums2[j--];
    }
}
```

```python
def merge(nums1, m, nums2, n):
    i, j, k = m - 1, n - 1, m + n - 1
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]; i -= 1
        else:
            nums1[k] = nums2[j]; j -= 1
        k -= 1
```

---

### Q: Move Zeroes: Move all 0s to end while maintaining order of non-zero elements.

**A:** Two-pointer approach: slow pointer tracks position for next non-zero, fast pointer scans array.
* **Time**: O(n), **Space**: O(1).

```java
public void moveZeroes(int[] nums) {
    int slow = 0;
    for (int fast = 0; fast < nums.length; fast++) {
        if (nums[fast] != 0) {
            int temp = nums[slow];
            nums[slow] = nums[fast];
            nums[fast] = temp;
            slow++;
        }
    }
}
```

```python
def move_zeroes(nums):
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
```

---

### Q: Find the missing number in array of 0 to n.

**A:** Use XOR or math (expected sum - actual sum). XOR cancels out pairs.
* **Time**: O(n), **Space**: O(1).

```java
public int missingNumber(int[] nums) {
    int n = nums.length;
    int expected = n * (n + 1) / 2;
    int actual = 0;
    for (int num : nums) actual += num;
    return expected - actual;
}
```

```python
def missing_number(nums):
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)
```

---

### Q: Rotate Array: Rotate array to the right by k steps.

**A:** Reverse the entire array, then reverse first k elements, then reverse the rest.
* **Time**: O(n), **Space**: O(1).

```java
public void rotate(int[] nums, int k) {
    k %= nums.length;
    reverse(nums, 0, nums.length - 1);
    reverse(nums, 0, k - 1);
    reverse(nums, k, nums.length - 1);
}
private void reverse(int[] nums, int l, int r) {
    while (l < r) {
        int tmp = nums[l]; nums[l] = nums[r]; nums[r] = tmp;
        l++; r--;
    }
}
```

```python
def rotate(nums, k):
    k %= len(nums)
    nums.reverse()
    nums[:k] = reversed(nums[:k])
    nums[k:] = reversed(nums[k:])
```

---

### Q: Container With Most Water: Find two lines that hold the most water.

**A:** Two-pointer approach: start from both ends, move the shorter line inward.
* **Time**: O(n), **Space**: O(1). Greedy — moving the shorter line is the only way to potentially find a larger area.

```java
public int maxArea(int[] height) {
    int left = 0, right = height.length - 1, maxWater = 0;
    while (left < right) {
        int area = Math.min(height[left], height[right]) * (right - left);
        maxWater = Math.max(maxWater, area);
        if (height[left] < height[right]) left++;
        else right--;
    }
    return maxWater;
}
```

```python
def max_area(height):
    left, right, max_water = 0, len(height) - 1, 0
    while left < right:
        area = min(height[left], height[right]) * (right - left)
        max_water = max(max_water, area)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return max_water
```

---

### Q: Three Sum: Find all unique triplets that sum to zero.

**A:** Sort the array, fix one element, use two pointers for the remaining two. Skip duplicates.
* **Time**: O(n²), **Space**: O(1) extra.

```java
public List<List<Integer>> threeSum(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> result = new ArrayList<>();
    for (int i = 0; i < nums.length - 2; i++) {
        if (i > 0 && nums[i] == nums[i-1]) continue;
        int lo = i + 1, hi = nums.length - 1;
        while (lo < hi) {
            int sum = nums[i] + nums[lo] + nums[hi];
            if (sum == 0) {
                result.add(Arrays.asList(nums[i], nums[lo], nums[hi]));
                while (lo < hi && nums[lo] == nums[lo+1]) lo++;
                while (lo < hi && nums[hi] == nums[hi-1]) hi--;
                lo++; hi--;
            } else if (sum < 0) lo++;
            else hi--;
        }
    }
    return result;
}
```

```python
def three_sum(nums):
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i-1]: continue
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s == 0:
                result.append([nums[i], nums[lo], nums[hi]])
                while lo < hi and nums[lo] == nums[lo+1]: lo += 1
                while lo < hi and nums[hi] == nums[hi-1]: hi -= 1
                lo += 1; hi -= 1
            elif s < 0: lo += 1
            else: hi -= 1
    return result
```

---

### Q: Majority Element: Find the element that appears more than n/2 times.

**A:** Boyer-Moore Voting Algorithm: maintain a candidate and count. O(n) time, O(1) space.

```java
public int majorityElement(int[] nums) {
    int candidate = nums[0], count = 1;
    for (int i = 1; i < nums.length; i++) {
        if (count == 0) { candidate = nums[i]; count = 1; }
        else if (nums[i] == candidate) count++;
        else count--;
    }
    return candidate;
}
```

```python
def majority_element(nums):
    candidate, count = nums[0], 1
    for num in nums[1:]:
        if count == 0:
            candidate, count = num, 1
        elif num == candidate:
            count += 1
        else:
            count -= 1
    return candidate
```

---

### Q: Reverse a String in-place.

**A:** Two-pointer swap from both ends. O(n) time, O(1) space.

```java
public void reverseString(char[] s) {
    int l = 0, r = s.length - 1;
    while (l < r) {
        char tmp = s[l]; s[l] = s[r]; s[r] = tmp;
        l++; r--;
    }
}
```

```python
def reverse_string(s):
    s.reverse()  # in-place
    # or: s[:] = s[::-1]
```

---

### Q: Valid Anagram: Check if two strings are anagrams.

**A:** Count character frequencies. If both strings have identical frequency counts, they are anagrams.
* **Time**: O(n), **Space**: O(1) since the character set is fixed (26 letters).

```java
public boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    int[] counts = new int[26];
    for (char c : s.toCharArray()) counts[c - 'a']++;
    for (char c : t.toCharArray()) counts[c - 'a']--;
    for (int c : counts) if (c != 0) return false;
    return true;
}
```

```python
from collections import Counter
def is_anagram(s, t):
    return Counter(s) == Counter(t)
```

---

### Q: Valid Palindrome: Check if a string reads the same forwards and backwards.

**A:** Two-pointer approach: compare characters from both ends, skipping non-alphanumeric characters.
* **Time**: O(n), **Space**: O(1).

```java
public boolean isPalindrome(String s) {
    int l = 0, r = s.length() - 1;
    while (l < r) {
        while (l < r && !Character.isLetterOrDigit(s.charAt(l))) l++;
        while (l < r && !Character.isLetterOrDigit(s.charAt(r))) r--;
        if (Character.toLowerCase(s.charAt(l)) != Character.toLowerCase(s.charAt(r)))
            return false;
        l++; r--;
    }
    return true;
}
```

```python
def is_palindrome(s):
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]
```

---

### Q: Longest Substring Without Repeating Characters (Sliding Window).

**A:** Use a sliding window with a HashSet. Expand right pointer, shrink left when duplicate found.
* **Time**: O(n), **Space**: O(min(n, alphabet_size)).

```java
public int lengthOfLongestSubstring(String s) {
    Set<Character> set = new HashSet<>();
    int left = 0, maxLen = 0;
    for (int right = 0; right < s.length(); right++) {
        while (set.contains(s.charAt(right)))
            set.remove(s.charAt(left++));
        set.add(s.charAt(right));
        maxLen = Math.max(maxLen, right - left + 1);
    }
    return maxLen;
}
```

```python
def length_of_longest_substring(s):
    seen = set()
    left = max_len = 0
    for right in range(len(s)):
        while s[right] in seen:
            seen.remove(s[left])
            left += 1
        seen.add(s[right])
        max_len = max(max_len, right - left + 1)
    return max_len
```

---

### Q: Longest Palindromic Substring: Find the longest palindrome in a string.

**A:** Expand around center approach: for each character (and each pair), expand outward while characters match.
* **Time**: O(n²), **Space**: O(1).

```java
public String longestPalindrome(String s) {
    int start = 0, maxLen = 0;
    for (int i = 0; i < s.length(); i++) {
        int len1 = expand(s, i, i);     // odd length
        int len2 = expand(s, i, i + 1); // even length
        int len = Math.max(len1, len2);
        if (len > maxLen) {
            maxLen = len;
            start = i - (len - 1) / 2;
        }
    }
    return s.substring(start, start + maxLen);
}
private int expand(String s, int l, int r) {
    while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) { l--; r++; }
    return r - l - 1;
}
```

```python
def longest_palindrome(s):
    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1; r += 1
        return s[l+1:r]
    result = ""
    for i in range(len(s)):
        odd = expand(i, i)
        even = expand(i, i + 1)
        result = max(result, odd, even, key=len)
    return result
```

---

### Q: Group Anagrams: Group strings that are anagrams of each other.

**A:** Sort each string to create a canonical key. Group by that key using a HashMap.
* **Time**: O(n × k log k) where k is max string length. **Space**: O(n × k).

```java
public List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> map = new HashMap<>();
    for (String s : strs) {
        char[] arr = s.toCharArray();
        Arrays.sort(arr);
        String key = new String(arr);
        map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
    }
    return new ArrayList<>(map.values());
}
```

```python
from collections import defaultdict
def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = ''.join(sorted(s))
        groups[key].append(s)
    return list(groups.values())
```

---

### Q: String to Integer (atoi): Implement string to integer conversion.

**A:** Handle whitespace, sign, digits, and overflow. Process character by character.
* **Edge cases**: Leading whitespace, +/- sign, non-digit characters, INT_MIN/INT_MAX overflow.

```java
public int myAtoi(String s) {
    int i = 0, sign = 1, result = 0;
    while (i < s.length() && s.charAt(i) == ' ') i++;
    if (i < s.length() && (s.charAt(i) == '+' || s.charAt(i) == '-'))
        sign = s.charAt(i++) == '-' ? -1 : 1;
    while (i < s.length() && Character.isDigit(s.charAt(i))) {
        int digit = s.charAt(i++) - '0';
        if (result > (Integer.MAX_VALUE - digit) / 10)
            return sign == 1 ? Integer.MAX_VALUE : Integer.MIN_VALUE;
        result = result * 10 + digit;
    }
    return result * sign;
}
```

```python
def my_atoi(s):
    s = s.lstrip()
    if not s: return 0
    sign = -1 if s[0] == '-' else 1
    i = 1 if s[0] in '+-' else 0
    result = 0
    while i < len(s) and s[i].isdigit():
        result = result * 10 + int(s[i])
        i += 1
    result *= sign
    return max(-(2**31), min(2**31 - 1, result))
```

---

### Q: Count and Say: Generate the nth term of the count-and-say sequence.

**A:** Iteratively build each term by reading off digits of the previous term.
* 1 → '1', 2 → '11' (one 1), 3 → '21' (two 1s), 4 → '1211' (one 2, one 1).

```java
public String countAndSay(int n) {
    String s = "1";
    for (int i = 2; i <= n; i++) {
        StringBuilder sb = new StringBuilder();
        int count = 1;
        for (int j = 1; j < s.length(); j++) {
            if (s.charAt(j) == s.charAt(j-1)) count++;
            else { sb.append(count).append(s.charAt(j-1)); count = 1; }
        }
        sb.append(count).append(s.charAt(s.length()-1));
        s = sb.toString();
    }
    return s;
}
```

```python
def count_and_say(n):
    s = "1"
    for _ in range(n - 1):
        result, i = "", 0
        while i < len(s):
            count = 1
            while i + count < len(s) and s[i + count] == s[i]:
                count += 1
            result += str(count) + s[i]
            i += count
        s = result
    return s
```

---

### Q: Reverse a Linked List iteratively and recursively.

**A:** Iterative: Use three pointers (prev, curr, next). Recursive: Reverse the rest, then fix pointers.
* **Time**: O(n), **Space**: O(1) iterative, O(n) recursive.

```java
// Iterative
public ListNode reverseList(ListNode head) {
    ListNode prev = null, curr = head;
    while (curr != null) {
        ListNode next = curr.next;
        curr.next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}
```

```python
# Iterative
def reverse_list(head):
    prev, curr = None, head
    while curr:
        curr.next, prev, curr = prev, curr, curr.next
    return prev
```

---

### Q: Detect a cycle in a linked list (Floyd's Algorithm).

**A:** Use slow (1 step) and fast (2 steps) pointers. If they meet, there's a cycle.
* **Time**: O(n), **Space**: O(1).

```java
public boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;
    }
    return false;
}
```

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

---

### Q: Merge Two Sorted Linked Lists.

**A:** Use a dummy node and compare heads of both lists, linking the smaller one.
* **Time**: O(n+m), **Space**: O(1).

```java
public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
    ListNode dummy = new ListNode(0), curr = dummy;
    while (l1 != null && l2 != null) {
        if (l1.val <= l2.val) { curr.next = l1; l1 = l1.next; }
        else { curr.next = l2; l2 = l2.next; }
        curr = curr.next;
    }
    curr.next = (l1 != null) ? l1 : l2;
    return dummy.next;
}
```

```python
def merge_two_lists(l1, l2):
    dummy = curr = ListNode(0)
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next, l1 = l1, l1.next
        else:
            curr.next, l2 = l2, l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next
```

---

### Q: Inorder, Preorder, Postorder Traversals of a Binary Tree.

**A:** * **Inorder** (Left, Root, Right): Gives sorted order for BST.
* **Preorder** (Root, Left, Right): Used for tree serialization.
* **Postorder** (Left, Right, Root): Used for deletion, expression evaluation.

```java
// Inorder traversal (iterative)
public List<Integer> inorderTraversal(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    Stack<TreeNode> stack = new Stack<>();
    TreeNode curr = root;
    while (curr != null || !stack.isEmpty()) {
        while (curr != null) { stack.push(curr); curr = curr.left; }
        curr = stack.pop();
        result.add(curr.val);
        curr = curr.right;
    }
    return result;
}
```

```python
# All three traversals (recursive)
def inorder(root):
    return inorder(root.left) + [root.val] + inorder(root.right) if root else []

def preorder(root):
    return [root.val] + preorder(root.left) + preorder(root.right) if root else []

def postorder(root):
    return postorder(root.left) + postorder(root.right) + [root.val] if root else []
```

---

### Q: Maximum Depth of a Binary Tree.

**A:** Recursively find max depth of left and right subtrees, return the larger + 1.
* **Time**: O(n), **Space**: O(h) where h is height.

```java
public int maxDepth(TreeNode root) {
    if (root == null) return 0;
    return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
}
```

```python
def max_depth(root):
    if not root: return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

---

### Q: Validate Binary Search Tree (BST).

**A:** Use inorder traversal (should produce sorted sequence) or pass valid range recursively.
* **Time**: O(n), **Space**: O(h).

```java
public boolean isValidBST(TreeNode root) {
    return validate(root, Long.MIN_VALUE, Long.MAX_VALUE);
}
private boolean validate(TreeNode node, long min, long max) {
    if (node == null) return true;
    if (node.val <= min || node.val >= max) return false;
    return validate(node.left, min, node.val) &&
           validate(node.right, node.val, max);
}
```

```python
def is_valid_bst(root, lo=float('-inf'), hi=float('inf')):
    if not root: return True
    if root.val <= lo or root.val >= hi: return False
    return (is_valid_bst(root.left, lo, root.val) and
            is_valid_bst(root.right, root.val, hi))
```

---

### Q: Implement Merge Sort.

**A:** Divide array in half, recursively sort each half, merge the two sorted halves.
* **Time**: O(n log n) always, **Space**: O(n). Stable sort.

```java
public void mergeSort(int[] arr, int l, int r) {
    if (l < r) {
        int m = (l + r) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}
private void merge(int[] arr, int l, int m, int r) {
    int[] left = Arrays.copyOfRange(arr, l, m + 1);
    int[] right = Arrays.copyOfRange(arr, m + 1, r + 1);
    int i = 0, j = 0, k = l;
    while (i < left.length && j < right.length)
        arr[k++] = left[i] <= right[j] ? left[i++] : right[j++];
    while (i < left.length) arr[k++] = left[i++];
    while (j < right.length) arr[k++] = right[j++];
}
```

```python
def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]
```

---

### Q: Implement Binary Search.

**A:** Divide search space in half each iteration. Array must be sorted.
* **Time**: O(log n), **Space**: O(1) iterative.

```java
public int binarySearch(int[] arr, int target) {
    int lo = 0, hi = arr.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
```

```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target: return mid
        elif arr[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return -1
```

---

## Machine Learning & Statistics

### Q: What is the difference between supervised, unsupervised, and reinforcement learning?

**A:** * **Supervised Learning**: Model learns from labeled data (input-output pairs). Types: Classification (discrete labels) and Regression (continuous values). Examples: spam detection, house price prediction.
* **Unsupervised Learning**: Model finds hidden patterns in unlabeled data. Types: Clustering (K-Means, DBSCAN), Dimensionality Reduction (PCA, t-SNE), Association Rules. Examples: customer segmentation.
* **Reinforcement Learning**: Agent learns by interacting with an environment, receiving rewards/penalties. Examples: game playing (AlphaGo), robotics, autonomous driving.

---

### Q: What is the Bias-Variance Trade-off?

**A:** * **Bias**: Error from overly simplistic model assumptions (underfitting). High bias = model can't capture data patterns.
* **Variance**: Error from sensitivity to training data fluctuations (overfitting). High variance = model memorizes noise.
* **Total Error** = Bias² + Variance + Irreducible Error.
* **Trade-off**: As model complexity increases, bias decreases but variance increases. The optimal model minimizes total error.
* **Solutions**: Regularization (L1/L2), cross-validation, ensemble methods, more training data.

---

### Q: Explain L1 (Lasso) vs L2 (Ridge) regularization.

**A:** * **L1 (Lasso)**: Adds |w| penalty. Drives unimportant weights to exactly zero → performs feature selection, creates sparse models.
* **L2 (Ridge)**: Adds w² penalty. Shrinks all weights toward zero but never exactly zero → keeps all features, prevents any single feature from dominating.
* **Elastic Net**: Combines L1 + L2 penalties. Best of both worlds.
* **When to use**:
  - L1: When you suspect many irrelevant features (sparse solution desired).
  - L2: When all features contribute but you want to prevent overfitting.

---

### Q: How do Decision Trees work? What are Gini Impurity and Information Gain?

**A:** Decision Trees recursively split data based on feature values to maximize class separation.
* **Gini Impurity**: Measures probability of misclassifying a randomly chosen element. Gini(p) = 1 - Σ(pᵢ²). Gini = 0 means pure node. Used by CART algorithm.
* **Entropy**: H(p) = -Σ(pᵢ log₂ pᵢ). Measures disorder/uncertainty.
* **Information Gain**: IG = Entropy(parent) - Σ(weighted × Entropy(child)). Higher IG = better split. Used by ID3/C4.5.
* **Stopping criteria**: Max depth, min samples per leaf, min information gain.

---

### Q: Explain Random Forest vs Gradient Boosting (XGBoost, LightGBM).

**A:** * **Random Forest (Bagging)**:
  - Trains many independent trees in parallel on bootstrap samples.
  - Each split considers random subset of features.
  - Aggregates predictions by averaging (regression) or majority vote (classification).
  - Reduces variance. Robust to overfitting.
* **Gradient Boosting (Boosting)**:
  - Trains trees sequentially; each corrects errors of the ensemble so far.
  - Each tree fits the residual errors (negative gradient of loss).
  - Reduces bias. More prone to overfitting → needs regularization.
* **XGBoost**: Adds L1/L2 regularization, handles missing values, parallel tree construction.
* **LightGBM**: Histogram-based splitting, leaf-wise growth (faster on large data).

---

### Q: What is cross-validation? Why is it important?

**A:** Cross-validation splits data into K folds, trains on K-1 folds and validates on the remaining fold, rotating K times.
* **K-Fold CV**: Standard approach. K=5 or K=10 most common.
* **Stratified K-Fold**: Maintains class distribution in each fold. Essential for imbalanced datasets.
* **Leave-One-Out (LOO)**: K = N. Computationally expensive but unbiased.
* **Why important**:
  1. More reliable performance estimate than a single train/test split.
  2. Detects overfitting.
  3. Uses all data for both training and validation.
  4. Critical for hyperparameter tuning.

---

### Q: How do you handle imbalanced datasets?

**A:** When classes are heavily skewed (e.g., 1% fraud), standard accuracy is misleading.
* **Data-level techniques**:
  1. **Oversampling minority**: SMOTE (Synthetic Minority Over-sampling) creates synthetic examples.
  2. **Undersampling majority**: Random removal or Tomek Links.
  3. **Combination**: SMOTE + Tomek Links.
* **Algorithm-level techniques**:
  1. **Class weights**: Assign higher penalty for misclassifying minority class.
  2. **Cost-sensitive learning**: Different misclassification costs.
  3. **Focal Loss**: Down-weights easy examples, focuses on hard ones.
* **Evaluation**: Use Precision, Recall, F1, PR-AUC instead of accuracy.

---

### Q: What is feature engineering? Common techniques.

**A:** Feature engineering transforms raw data into informative features that improve model performance.
* **Techniques**:
  1. **Encoding categoricals**: One-hot encoding, label encoding, target encoding.
  2. **Scaling numericals**: Min-Max normalization, Z-score standardization.
  3. **Binning**: Convert continuous to categorical (age groups).
  4. **Polynomial features**: Create interaction terms (x₁ × x₂) and powers (x²).
  5. **Log/Box-Cox transforms**: Handle skewed distributions.
  6. **Time features**: Extract day, month, day-of-week, is_weekend from timestamps.
  7. **Text features**: TF-IDF, word counts, n-grams.
  8. **Domain knowledge**: Ratios, aggregations, rolling statistics.

---

### Q: What is the Kernel Trick in SVMs?

**A:** Support Vector Machines find the optimal hyperplane that maximizes the margin between classes.
* **Kernel Trick**: When data is not linearly separable, the kernel function maps data into a higher-dimensional space where it becomes separable — WITHOUT explicitly computing the transformation.
* **Common kernels**:
  - Linear: K(x,y) = x·y
  - Polynomial: K(x,y) = (x·y + c)^d
  - RBF/Gaussian: K(x,y) = exp(-γ||x-y||²) — most popular, handles complex boundaries
  - Sigmoid: K(x,y) = tanh(αx·y + c)
* **Key insight**: Kernel functions compute dot products in high-dimensional space efficiently.

---

### Q: Explain PCA (Principal Component Analysis).

**A:** PCA is an unsupervised dimensionality reduction technique.
* **How it works**:
  1. Standardize the data (mean=0, std=1).
  2. Compute the covariance matrix.
  3. Calculate eigenvalues and eigenvectors.
  4. Sort eigenvectors by eigenvalue (descending).
  5. Select top-k eigenvectors (principal components).
  6. Project data onto these components.
* **Result**: Transforms features into orthogonal components that capture maximum variance.
* **Choosing k**: Use explained variance ratio. Keep components that explain ≥95% of total variance.
* **Limitations**: Linear only, loses interpretability, sensitive to scaling.

---

### Q: K-Means vs KNN: What's the difference?

**A:** Completely different algorithms despite similar names:
* **K-Means** (Unsupervised Clustering):
  - Groups unlabeled data into K clusters.
  - Minimizes within-cluster distance to centroids.
  - Training: O(I × K × N × D). Prediction: O(K × D).
  - Choose K: Elbow method, Silhouette score.
* **KNN** (Supervised Classification/Regression):
  - Classifies new points based on K nearest neighbors' labels.
  - Lazy learner — no training phase.
  - Prediction: O(N × D) per query (slow on large datasets).
  - Choose K: Cross-validation (use odd K to avoid ties).

---

### Q: What is Logistic Regression? Is it regression or classification?

**A:** Despite the name, Logistic Regression is a CLASSIFICATION algorithm.
* **How it works**: Applies sigmoid function σ(z) = 1/(1+e^(-z)) to a linear combination of features, outputting a probability between 0 and 1.
* **Decision boundary**: Threshold at 0.5 (or optimized threshold).
* **Loss function**: Binary Cross-Entropy (log loss): L = -[y·log(p) + (1-y)·log(1-p)].
* **Assumptions**: Linear decision boundary, features are independent, no multicollinearity.
* **Multiclass**: One-vs-Rest (OvR) or Softmax (multinomial).

---

### Q: What is Gradient Descent? Types and differences.

**A:** Gradient Descent is an optimization algorithm that minimizes the loss function by iteratively updating parameters in the direction of steepest descent.
* **Update rule**: θ = θ - α · ∇L(θ), where α is the learning rate.
* **Types**:
  1. **Batch GD**: Uses entire dataset per update. Stable but slow.
  2. **Stochastic GD (SGD)**: Uses one random sample per update. Fast but noisy.
  3. **Mini-Batch GD**: Uses a small batch (32, 64, 128). Best trade-off — most common.
* **Learning rate**: Too high → diverges. Too low → very slow convergence.
* **Advanced optimizers**: Adam (adaptive learning rates), RMSprop, Adagrad.

---

### Q: What is hyperparameter tuning? Common strategies.

**A:** Hyperparameters are settings configured before training (not learned from data). Tuning finds the best combination.
* **Strategies**:
  1. **Grid Search**: Exhaustive search over predefined parameter grid. Guaranteed to find best in grid but exponentially expensive.
  2. **Random Search**: Randomly samples parameter combinations. Often finds good results faster than grid search.
  3. **Bayesian Optimization**: Uses probabilistic model to intelligently choose next parameters. Efficient for expensive evaluations.
  4. **Optuna/Hyperopt**: Automated frameworks implementing Bayesian and TPE strategies.
* **Always use cross-validation** during tuning to avoid overfitting to the validation set.

---

### Q: What is overfitting? How do you detect and prevent it?

**A:** Overfitting: Model learns noise and patterns specific to training data, failing to generalize.
* **Detection**:
  - Training accuracy >> validation accuracy.
  - Large gap between training and validation loss curves.
  - Model performs poorly on unseen data.
* **Prevention**:
  1. More training data.
  2. Regularization (L1, L2, dropout).
  3. Cross-validation.
  4. Early stopping (stop training when validation loss starts increasing).
  5. Simpler model architecture.
  6. Data augmentation (for images).
  7. Feature selection (remove irrelevant features).
  8. Ensemble methods.

---

### Q: What is the curse of dimensionality?

**A:** As the number of features (dimensions) increases, the volume of the feature space grows exponentially, making data extremely sparse.
* **Effects**:
  1. Distance metrics become meaningless (all points are equally far apart).
  2. Models need exponentially more data to generalize.
  3. Overfitting risk increases dramatically.
  4. Computation time and storage increase.
* **Solutions**:
  1. Feature selection (remove irrelevant features).
  2. Dimensionality reduction (PCA, t-SNE, UMAP).
  3. Feature engineering (domain-driven feature creation).
  4. Regularization.

---

### Q: What is a confusion matrix? Explain TP, FP, TN, FN.

**A:** A confusion matrix is a table showing actual vs predicted classifications:
* **True Positive (TP)**: Correctly predicted positive.
* **False Positive (FP)**: Incorrectly predicted positive (Type I error).
* **True Negative (TN)**: Correctly predicted negative.
* **False Negative (FN)**: Incorrectly predicted negative (Type II error).
* **Derived metrics**:
  - Accuracy = (TP+TN)/(TP+TN+FP+FN)
  - Precision = TP/(TP+FP) — "Of predicted positives, how many are correct?"
  - Recall = TP/(TP+FN) — "Of actual positives, how many did we find?"
  - F1 = 2×(Precision×Recall)/(Precision+Recall)

---

### Q: Explain ROC curve and AUC. When is PR-AUC better?

**A:** * **ROC Curve**: Plots True Positive Rate (Recall) vs False Positive Rate at various classification thresholds.
* **AUC (Area Under ROC Curve)**: Summarizes ROC curve. AUC=1 is perfect, AUC=0.5 is random.
* **PR-AUC (Precision-Recall AUC)**: Plots Precision vs Recall. Better for imbalanced datasets because:
  - ROC-AUC can be misleadingly high when negatives dominate (high TN inflates FPR denominator).
  - PR-AUC focuses only on the positive class, giving a more honest performance picture.

---

### Q: What is RMSE vs MAE vs MAPE? When to use each?

**A:** * **MAE (Mean Absolute Error)**: Average of |actual - predicted|. Robust to outliers. Interpretable in original units.
* **RMSE (Root Mean Squared Error)**: √(mean of (actual - predicted)²). Penalizes large errors more heavily than MAE. Use when large errors are especially costly.
* **MAPE (Mean Absolute Percentage Error)**: Average of |actual-predicted|/|actual| × 100. Scale-independent (percentage). Bad when actual values are near zero.
* **R² (Coefficient of Determination)**: 1 - (SS_res/SS_tot). Proportion of variance explained. R²=1 is perfect, R²=0 is as good as predicting the mean.

---

### Q: What is the F1 Score? When would you prefer precision over recall?

**A:** * **F1 Score**: Harmonic mean of Precision and Recall. F1 = 2PR/(P+R). Ranges from 0 to 1.
* **Prefer Precision when**: False positives are costly (e.g., spam filter — marking important email as spam is bad).
* **Prefer Recall when**: False negatives are costly (e.g., cancer detection — missing a cancer patient is dangerous).
* **F-beta score**: Generalized version. β>1 weighs recall higher, β<1 weighs precision higher.

---

### Q: What is log loss (cross-entropy loss)? Why is it preferred for classification?

**A:** * **Log Loss** = -1/N × Σ[yᵢ·log(pᵢ) + (1-yᵢ)·log(1-pᵢ)]
* Measures how far predicted probabilities are from actual labels.
* **Why preferred**: Unlike accuracy (discrete), log loss penalizes confident wrong predictions heavily. A model predicting 0.99 for a negative class gets a much higher penalty than one predicting 0.51.
* **Perfect model**: Log loss = 0. Random guessing: Log loss = 0.693 (binary).

---

### Q: Explain the Central Limit Theorem (CLT).

**A:** The CLT states that the sampling distribution of the sample mean approaches a normal distribution as sample size (n) increases, regardless of the underlying population distribution.
* **Conditions**: Samples are independent, identically distributed (i.i.d.), and n ≥ 30 (rule of thumb).
* **Implication**: Mean of sample means = population mean (μ). Standard error = σ/√n.
* **Why it matters**: Enables hypothesis testing and confidence intervals even when population distribution is unknown.

---

### Q: What is the difference between Type I and Type II errors?

**A:** * **Type I Error (False Positive)**: Rejecting the null hypothesis when it is actually true. Probability = α (significance level, typically 0.05).
* **Type II Error (False Negative)**: Failing to reject the null hypothesis when it is actually false. Probability = β.
* **Power** = 1 - β = probability of correctly detecting a true effect.
* **Trade-off**: Reducing α increases β (and vice versa). Increasing sample size reduces both errors.
* **Example**: Medical test — Type I: healthy person diagnosed as sick. Type II: sick person diagnosed as healthy.

---

### Q: What is a p-value? How do you interpret it?

**A:** The p-value is the probability of observing data as extreme as (or more extreme than) the observed results, assuming the null hypothesis is true.
* **Interpretation**: Small p-value (< 0.05) = strong evidence against H₀ → reject H₀.
* **p-value is NOT**: The probability that H₀ is true. It's about the data, not the hypothesis.
* **Common thresholds**: p < 0.05 (significant), p < 0.01 (highly significant), p < 0.001 (very highly significant).
* **Caution**: Statistical significance ≠ practical significance. Large samples can make trivial effects "significant."

---

### Q: Explain correlation vs causation. What is the Pearson correlation coefficient?

**A:** * **Correlation**: Two variables move together (positive or negative relationship). Does NOT imply one causes the other.
* **Causation**: A change in one variable DIRECTLY causes a change in another. Requires controlled experiments (A/B tests, RCTs) to establish.
* **Pearson's r**: Measures LINEAR correlation between two variables. Range: [-1, 1].
  - r = 1: Perfect positive linear relationship.
  - r = 0: No linear relationship (can still have non-linear relationship!).
  - r = -1: Perfect negative linear relationship.
* **Spearman's ρ**: Measures monotonic relationship (rank-based). More robust to outliers.

---

### Q: What is a confidence interval? How do you interpret a 95% CI?

**A:** A confidence interval gives a range of plausible values for a population parameter.
* **95% CI interpretation**: If we repeated the experiment many times and computed a CI each time, 95% of those intervals would contain the true population parameter.
* **Formula** (for mean): x̄ ± z × (σ/√n), where z=1.96 for 95% CI.
* **Width depends on**: Sample size (larger n → narrower CI), confidence level (higher confidence → wider CI), variability (higher σ → wider CI).
* **Common misconception**: It does NOT mean there's a 95% probability the parameter is in THIS interval.

---

### Q: Design an A/B test. What are the key steps and pitfalls?

**A:** * **Steps**:
  1. **Define hypothesis**: H₀ (no difference), H₁ (difference exists).
  2. **Choose metric**: Primary (conversion rate) and guardrail metrics.
  3. **Sample size calculation**: Using baseline rate, MDE, α=0.05, power=0.80.
  4. **Randomize**: Randomly assign users to control (A) and treatment (B).
  5. **Run experiment**: For full duration (avoid peeking!).
  6. **Analyze**: Statistical test (Z-test, t-test, chi-squared).
  7. **Decision**: If p < 0.05 and effect is practically significant, deploy.
* **Pitfalls**: Peeking (inflates false positive rate), novelty effect, sample ratio mismatch, Simpson's paradox, network effects.

---

### Q: Describe the end-to-end Data Analysis Lifecycle.

**A:** 1. **Define Objectives**: Clarify the business question.
2. **Data Collection**: SQL queries, APIs, log files, web scraping.
3. **Data Cleaning / Wrangling**: Handle missing values, remove duplicates, fix data types, detect outliers, merge datasets.
4. **EDA (Exploratory Data Analysis)**: Descriptive statistics (mean, median, std), visualizations (histograms, box plots, scatter plots), correlations.
5. **Data Modeling**: Statistical tests (t-tests, chi-squared) or ML models.
6. **Visualization & Reporting**: Dashboards (Tableau, PowerBI), presentations.

---

### Q: How do you handle missing values? Strategies and trade-offs.

**A:** * **Detection**: df.isnull().sum(), df.info(), missing percentage per column.
* **Strategies**:
  1. **Deletion**: Drop rows (df.dropna()) if <5% missing and MCAR (Missing Completely At Random).
  2. **Mean/Median/Mode Imputation**: Simple, fast. Risk: reduces variance, distorts relationships.
  3. **Forward/Backward Fill**: For time-series data.
  4. **KNN Imputer**: Uses K nearest neighbors to estimate values. Better accuracy.
  5. **Iterative Imputer (MICE)**: Models each missing feature as function of others.
  6. **Indicator variable**: Add a binary column is_missing_X to capture missingness pattern.
* **Trade-offs**: Deletion loses data. Simple imputation biases distributions. Complex imputation is computationally expensive.

---

### Q: Explain Normalization vs Standardization.

**A:** * **Normalization (Min-Max Scaling)**: x_norm = (x - x_min) / (x_max - x_min). Scales to [0,1]. Use for algorithms that don't assume normal distribution (KNN, Neural Networks, image data).
* **Standardization (Z-score)**: x_std = (x - μ) / σ. Centers at mean=0, std=1. Unbounded. Use for algorithms assuming normal distribution (Linear Regression, PCA, SVM).
* **Key difference**: Standardization is less sensitive to outliers. Normalization is bounded.
* **RobustScaler**: Uses median and IQR instead of mean/std. Best when outliers are present.

---

### Q: How do you detect and handle outliers?

**A:** * **Detection methods**:
  1. **IQR method**: Outlier if value < Q1 - 1.5×IQR or > Q3 + 1.5×IQR.
  2. **Z-score**: Outlier if |z| > 3.
  3. **Visual**: Box plots, scatter plots, histograms.
  4. **Isolation Forest**: ML-based anomaly detection.
* **Handling**:
  1. **Trimming**: Remove outliers (if data errors).
  2. **Capping/Winsorization**: Cap at 1st/99th percentile.
  3. **Log transform**: Reduces skewness.
  4. **Robust methods**: Use median instead of mean, use algorithms robust to outliers (trees).
  5. **Keep them**: If they represent valid extreme cases (fraud detection).

---

### Q: What is EDA? What visualizations would you use?

**A:** EDA (Exploratory Data Analysis) explores datasets to summarize characteristics, find patterns, and detect anomalies.
* **Univariate**: Histograms (distribution), box plots (outliers), bar charts (categorical).
* **Bivariate**: Scatter plots (correlation), heatmaps (correlation matrix), grouped bar charts.
* **Multivariate**: Pair plots, parallel coordinates, dimensionality reduction plots (PCA, t-SNE).
* **Time-series**: Line plots, seasonal decomposition.
* **Key tools**: pandas.describe(), df.corr(), seaborn, matplotlib, plotly.

---

### Q: What is ETL vs ELT? When to use which?

**A:** * **ETL (Extract, Transform, Load)**: Data is transformed BEFORE loading into the warehouse. Traditional approach for structured data.
  - Use when: Data needs cleaning/conforming before storage. Limited warehouse compute.
* **ELT (Extract, Load, Transform)**: Data is loaded raw into the warehouse, then transformed using warehouse compute power. Modern approach.
  - Use when: Cloud data warehouses (Snowflake, BigQuery) with massive compute. Need flexibility to transform data differently for different use cases.
* **Tools**: ETL: Informatica, Talend. ELT: dbt, Snowflake, BigQuery.

---

### Q: When to use bar chart vs line chart vs scatter plot?

**A:** * **Bar Chart**: Compare categories or discrete groups. Show frequency, count, or aggregated values. Vertical for categories, horizontal for long labels.
* **Line Chart**: Show trends over time. Continuous data on x-axis (dates, time). Use for time-series, progress tracking.
* **Scatter Plot**: Show relationship between two continuous variables. Detect correlation, clusters, outliers.
* **Histogram**: Show distribution/frequency of a single continuous variable. Detect skewness, modality.
* **Box Plot**: Show distribution summary (median, quartiles, outliers). Compare distributions across groups.
* **Heatmap**: Show magnitude in 2D matrix (correlation, confusion matrix).

---

### Q: What is Tableau? Key features for data analysis.

**A:** Tableau is a business intelligence and data visualization tool.
* **Key features**:
  1. **Drag-and-drop interface**: No coding required for most visualizations.
  2. **Data connectors**: Connect to databases, Excel, CSV, cloud sources.
  3. **Calculated fields**: Custom metrics using built-in functions.
  4. **Dashboard creation**: Combine multiple visualizations into interactive dashboards.
  5. **LOD Expressions**: Level of Detail expressions for complex aggregations at different granularities.
  6. **Parameters**: Dynamic user inputs that control filters and calculations.
  7. **Tableau Server/Cloud**: Share dashboards with stakeholders.

---

### Q: Explain the four major machine learning paradigms and their typical business use cases.

**A:** 1. Supervised Learning:
   - What it is: The model is trained on labeled training data (inputs mapped to known output labels).
   - Use Cases: Classification (e.g., spam detection, customer churn prediction) and Regression (e.g., house price forecasting).
2. Unsupervised Learning:
   - What it is: The model finds hidden patterns or structures in unlabeled data.
   - Use Cases: Clustering (e.g., customer segmentation), Dimensionality Reduction (e.g., PCA for feature compression), and Association Rules (e.g., market basket analysis).
3. Semi-supervised Learning:
   - What it is: Combines a small amount of labeled data with a large amount of unlabeled data during training. Often used when labeling is expensive.
   - Use Cases: Image classification, voice recognition, and medical diagnostics.
4. Reinforcement Learning:
   - What it is: An agent learns to make decisions by taking actions in an environment to maximize cumulative rewards.
   - Use Cases: Robotics, game-playing AI (e.g., AlphaGo), and autonomous driving.

---

### Q: How do Decision Trees work, and how do ensemble methods like Random Forests and Gradient Boosting (XGBoost, LightGBM) improve prediction?

**A:** * Decision Trees: Split data recursively based on feature values that maximize information gain (e.g., minimizing Gini Impurity or Entropy for classification, or Mean Squared Error for regression). While intuitive, they easily overfit.
* Random Forests (Bagging):
  - Work by training many independent decision trees in parallel.
  - Use Bootstrap Aggregating (Bagging): Each tree is trained on a random sample of the data.
  - Use Feature Randomness: Each split in a tree only considers a random subset of features.
  - Improvement: Reduces variance by averaging the predictions of uncorrelated trees.
* Gradient Boosting Machines (XGBoost, LightGBM) (Boosting):
  - Work sequentially: Each tree is trained to predict the residual errors (mistakes) of the combined ensemble of previous trees.
  - Improvement: Reduces bias. XGBoost/LightGBM introduce advanced regularization (L1/L2) and optimized split algorithms to make training incredibly fast and resilient to overfitting.

---

### Q: What is the Bias-Variance Trade-off? Explain how L1 (Lasso) and L2 (Ridge) regularization help control overfitting.

**A:** * Bias-Variance Trade-off:
  - Bias: Error introduced by approximating a real-world problem with a simplified model (leads to underfitting).
  - Variance: Error introduced by a model that is too complex and sensitive to small fluctuations in the training set (leads to overfitting).
  - Goal: Find the sweet spot that minimizes total error (Bias^2 + Variance + Irreducible Error).
* Regularization: Adds a penalty term to the loss function to constrain model weights.
  - L1 Regularization (Lasso): Penalty is the absolute sum of weights: $\lambda \sum |w_i|$. It drives less important feature weights to exactly zero, performing feature selection and creating sparse models.
  - L2 Regularization (Ridge): Penalty is the squared sum of weights: $\lambda \sum w_i^2$. It shrinks weights close to zero (but never exactly zero), keeping all features while preventing any single feature from dominating.

---

### Q: What is the "Kernel Trick" in Support Vector Machines (SVM), and how does Principal Component Analysis (PCA) work?

**A:** * SVM and the Kernel Trick: Support Vector Machines find the optimal hyperplane that maximizes the margin between different classes. When data is not linearly separable in the current dimension, the Kernel Trick maps it into a higher-dimensional space where it becomes separable. Critically, it computes similarity in this higher space using mathematical functions (kernels) without actually calculating the high-dimensional coordinates of the data points, saving computation.
* Principal Component Analysis (PCA): An unsupervised dimensionality reduction technique. It projects high-dimensional data onto a lower-dimensional subspace by finding orthogonal axes (Principal Components) along which the variance of the data is maximized. This retains the maximum possible information while reducing feature count.

--------------------------------------------------------------------------------
[Interview Questions]
--------------------------------------------------------------------------------

---

### Q: You are dealing with a highly imbalanced dataset (e.g., fraud detection where 0.1% are positive). What evaluation metrics would you prioritize, and what techniques would you use to handle the imbalance?

**A:** * Metrics to Avoid: Accuracy (a model predicting "no fraud" always would get 99.9% accuracy, which is useless).
* Metrics to Prioritize:
  - Precision: Out of all predicted fraud cases, how many were actually fraud? (Minimizes false positives).
  - Recall (Sensitivity): Out of all actual fraud cases, how many did we detect? (Minimizes false negatives).
  - F1-Score: Harmonic mean of Precision and Recall.
  - Precision-Recall AUC (PR-AUC): Better than ROC-AUC when classes are highly imbalanced, focusing on the minority class.
* Handling Techniques:
  1. Resampling: SMOTE (Synthetic Minority Over-sampling Technique) to generate synthetic minority samples, or undersampling the majority class.
  2. Loss Function Adjustment: Class weights or focal loss to penalize errors on the minority class more severely.
  3. Model Selection: Use tree ensembles (like XGBoost) which handle class imbalance better than logistic regression.

---

### Q: Compare K-Means Clustering and K-Nearest Neighbors (KNN). What are their computational complexities, and how do you choose the optimal 'K'?

**A:** * Differences:
  - K-Means: Unsupervised clustering algorithm that groups unlabeled data points into K clusters by minimizing the distance between points and cluster centroids.
  - KNN: Supervised classification/regression algorithm. To predict a new point, it looks at the labels of its K closest training points and takes a majority vote.
* Choosing 'K':
  - K-Means: Use the Elbow Method (plotting the Sum of Squared Errors against K and finding the point where the curve bends) or Silhouette Analysis (measuring how similar points are to their own cluster vs. other clusters).
  - KNN: Use Cross-Validation. Test different values of K (e.g., odd numbers to avoid ties) on validation data and choose the one that yields the best accuracy/F1 score.
* Computational Complexity:
  - K-Means: $O(I \cdot K \cdot N \cdot D)$ where $I$ is iterations, $N$ is data points, and $D$ is dimensions.
  - KNN: Lazy learner (training is $O(1)$). Querying is slow: $O(N \cdot D)$ per test point because it must compute the distance to every single training point. Can be optimized using KD-Trees.

---

### Q: What is the difference between Data Normalization (Min-Max Scaling) and Data Standardization (Z-score Scaling)? When should you use which?

**A:** * Normalization (Min-Max Scaling):
  - Formula: $x_{norm} = \frac{x - x_{min}}{x_{max} - x_{min}}$
  - Result: Scales all data to a bounded range, typically $[0, 1]$.
  - When to use: When the algorithm does not assume normal distribution of features (e.g., KNN, Neural Networks, Image processing) and bounding values is critical.
* Standardization (Z-score Scaling):
  - Formula: $x_{std} = \frac{x - \mu}{\sigma}$
  - Result: Centers data around a mean of 0 with a standard deviation of 1. Values are unbounded.
  - When to use: When the algorithm assumes normal distribution of features (e.g., Linear Regression, PCA, SVM) and the data contains outliers (Standardization is less sensitive to extreme outliers than Min-Max scaling).

---

### Q: Explain the differences between SQL Joins (Inner, Left, Right, Full Outer) and the concept of Common Table Expressions (CTEs).

**A:** * SQL Joins:
  - INNER JOIN: Returns only the rows that have matching values in both tables.
  - LEFT JOIN: Returns all rows from the left table, and the matched rows from the right table. Unmatched right rows return `NULL`.
  - RIGHT JOIN: Returns all rows from the right table, and the matched rows from the left table. Unmatched left rows return `NULL`.
  - FULL OUTER JOIN: Returns all rows when there is a match in either left or right table. Unmatched values return `NULL`.
* Common Table Expressions (CTEs):
  - What they are: Temporary named result sets defined using the `WITH` clause. They exist only within the execution scope of a single query.
  - Why use them: They replace complex nested subqueries, making queries highly readable, modular, and easier to debug.

---

### Q: Explain the differences between ROW_NUMBER, RANK, and DENSE_RANK window functions.

**A:** All three assign a sequential integer to rows within a partition based on an order condition, but handle duplicate values (ties) differently:
* ROW_NUMBER(): Assigns a unique sequential number to every single row, regardless of ties. (e.g., 1, 2, 3, 4).
* RANK(): Assigns the same rank to identical values, but skips subsequent numbers. (e.g., 1, 2, 2, 4).
* DENSE_RANK(): Assigns the same rank to identical values, but does not skip any numbers. (e.g., 1, 2, 2, 3).

--------------------------------------------------------------------------------
[Interview Questions]
--------------------------------------------------------------------------------

---

### Q: How do you detect and handle missing values and outliers in a dataset prior to analysis? Walk me through your methodology in Python.

**A:** * Missing Value Handling:
  1. Detection: Use `df.isnull().sum()` in Pandas.
  2. Action:
     - Deletion: Drop rows/columns using `df.dropna()` if the missing ratio is very small (<5%) and missingness is completely random.
     - Imputation: Fill missing values using `df.fillna()`. Use median for skewed numerical data, mean for normally distributed numerical data, and mode for categorical data.
     - Modeling: Use iterative algorithms (like MICE or KNN Imputer) to predict missing values based on other features.
* Outlier Handling:
  1. Detection: Use the Interquartile Range (IQR) method. Any data point outside $Q1 - 1.5 \times IQR$ or $Q3 + 1.5 \times IQR$ is flagged. Alternatively, use Z-score (absolute value > 3).
  2. Action:
     - Trimming: Drop outliers if they are data entry errors.
     - Capping (Winsorization): Cap outliers at the 1st and 99th percentiles.
     - Transformation: Apply log transformations to reduce the skewness of outliers.

---

### Q: Design an A/B test for a new checkout button color. Explain how you would formulate the hypotheses, check statistical significance, and interpret the p-value.

**A:** * Hypothesis Formulation:
  - Null Hypothesis ($H_0$): The new checkout button color has no effect on conversion rates (Conversion Rate A = Conversion Rate B).
  - Alternative Hypothesis ($H_1$): The new checkout button color increases conversion rates (Conversion Rate B > Conversion Rate A).
* Sample Size & Duration: Determine the required sample size beforehand using power analysis based on:
  - Baseline conversion rate.
  - Minimum Detectable Effect (MDE).
  - Significance level ($\alpha = 0.05$).
  - Statistical power ($\beta = 0.80$).
  Run the test until the sample size is met (usually across full weekly cycles to avoid day-of-week bias).
* Checking Significance: Since Conversion Rate is a proportion (converted vs. not converted), run a two-sample Z-test for proportions or a Chi-Square test.
* Interpreting the p-value:
  - The p-value is the probability of observing a difference as large as (or larger than) the one observed, assuming the null hypothesis is true.
  - If $p < 0.05$, reject the Null Hypothesis. The conversion difference is statistically significant, and we should deploy the new button.
  - If $p \ge 0.05$, fail to reject the Null Hypothesis. The observed change could be due to random noise.

---

