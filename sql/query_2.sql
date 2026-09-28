-- =====================================================================
-- Query 2 — Funcionarios por Regiao (com localizacao)
-- Base: FreeSQL  |  Esquema: Human Resources (HR)
-- ---------------------------------------------------------------------
-- Objetivo:
--   Relacionar cada funcionario a sua localizacao geografica
--   (Cidade, Estado/Provincia, Pais e Regiao) e ao seu salario, para
--   analisar a DISTRIBUICAO GEOGRAFICA dos funcionarios e as diferencas
--   salariais entre regioes.
--
-- Tecnicas exigidas:
--   * LEFT JOIN encadeado ligando 5 tabelas da base HR:
--       EMPLOYEES -> DEPARTMENTS -> LOCATIONS -> COUNTRIES -> REGIONS
--   * WHERE simples -> mantem apenas registros com regiao identificada
--                      (REGION_NAME IS NOT NULL).
--
-- Observacao: o caminho geografico so existe atraves do departamento
--   (EMPLOYEES nao tem LOCATION_ID). Por isso o funcionario sem
--   departamento fica sem regiao e e removido pelo filtro WHERE.
-- =====================================================================
SELECT
    e.EMPLOYEE_ID,
    CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS EMPLOYEE_NAME,
    d.DEPARTMENT_NAME,
    l.CITY,
    l.STATE_PROVINCE,
    c.COUNTRY_NAME,
    r.REGION_NAME,
    e.SALARY
FROM EMPLOYEES e
LEFT JOIN DEPARTMENTS d ON e.DEPARTMENT_ID = d.DEPARTMENT_ID
LEFT JOIN LOCATIONS   l ON d.LOCATION_ID   = l.LOCATION_ID
LEFT JOIN COUNTRIES   c ON l.COUNTRY_ID    = c.COUNTRY_ID
LEFT JOIN REGIONS     r ON c.REGION_ID     = r.REGION_ID
WHERE r.REGION_NAME IS NOT NULL
ORDER BY r.REGION_NAME, c.COUNTRY_NAME, e.SALARY DESC;
