-- Compare both directions and report only exceptions.
WITH all_keys AS (
    SELECT company, period, employee_id, pay_code FROM expected
    UNION
    SELECT company, period, employee_id, pay_code FROM actual
)
SELECT k.company,
       k.period,
       k.employee_id,
       k.pay_code,
       e.cents AS expected_cents,
       a.cents AS actual_cents,
       COALESCE(a.cents, 0) - COALESCE(e.cents, 0) AS difference_cents,
       CASE
           WHEN e.cents IS NULL THEN 'unexpected_record'
           WHEN a.cents IS NULL THEN 'missing_record'
           ELSE 'amount_mismatch'
       END AS status
FROM all_keys AS k
LEFT JOIN expected AS e USING (company, period, employee_id, pay_code)
LEFT JOIN actual AS a USING (company, period, employee_id, pay_code)
WHERE e.cents IS NULL OR a.cents IS NULL OR e.cents <> a.cents
ORDER BY k.company, k.period, k.employee_id, k.pay_code;
