-- =====================================================================
-- Query 1 — Salario por Departamento e Cargo
-- Base: FreeSQL  |  Esquema: Human Resources (HR)
-- ---------------------------------------------------------------------
-- Objetivo:
--   Extrair o salario de cada funcionario junto do seu departamento e
--   do seu cargo, para analisar a DISTRIBUICAO SALARIAL por departamento
--   e por cargo (media, mediana, minimo e maximo sao calculados no Python).
--
-- Tecnicas exigidas:
--   * LEFT JOIN  -> EMPLOYEES x DEPARTMENTS  (nome do departamento)
--   * LEFT JOIN  -> EMPLOYEES x JOBS         (titulo do cargo)
--   * WHERE simples -> mantem apenas funcionarios alocados a um
--                      departamento (DEPARTMENT_ID IS NOT NULL).
--
-- Observacao: o LEFT JOIN preserva todos os funcionarios mesmo que o
--   departamento ou o cargo nao tivessem correspondencia; o filtro WHERE
--   remove, de forma explicita, o unico funcionario sem departamento na
--   base (caso de qualidade de dado discutido no README).
-- =====================================================================
SELECT
    e.EMPLOYEE_ID,
    CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS EMPLOYEE_NAME,
    d.DEPARTMENT_NAME,
    j.JOB_TITLE,
    e.SALARY
FROM EMPLOYEES e
LEFT JOIN DEPARTMENTS d ON e.DEPARTMENT_ID = d.DEPARTMENT_ID
LEFT JOIN JOBS       j ON e.JOB_ID        = j.JOB_ID
WHERE e.DEPARTMENT_ID IS NOT NULL
ORDER BY d.DEPARTMENT_NAME, e.SALARY DESC;
