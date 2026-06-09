-- 允许 alice 连接数据库
GRANT CONNECT ON DATABASE mydb TO alice;

-- 允许 alice 使用 hr 模式
GRANT USAGE ON SCHEMA hr TO alice;

-- 允许 alice 在 hr 模式下创建自己的表
GRANT CREATE ON SCHEMA hr TO alice;

-- 允许 alice 查询 employees 表除 salary 外的列
GRANT SELECT (id, name, dept) ON hr.employees TO alice;




-- 回收 alice 在 hr 模式中创建表的权限
REVOKE CREATE ON SCHEMA hr FROM alice;

-- 回收 alice 对 employees 表的查询权限
REVOKE SELECT ON hr.employees FROM alice;








-- 创建用户并允许登录
CREATE USER manager WITH PASSWORD 'manager123';
CREATE USER emp_zhang WITH PASSWORD 'zhang123';
CREATE USER emp_wang WITH PASSWORD 'wang123';

-- 确保普通员工没有多余的权限（如默认对 public schema 的权限可回收）
REVOKE ALL ON SCHEMA public FROM emp_zhang, emp_wang;


-- 在 employees 表上启用行级安全
ALTER TABLE hr.employees ENABLE ROW LEVEL SECURITY;

-- 策略1：员工只能查看 name 等于自己用户名的行，且只能看到有限列（但 RLS 不控制列，列权限另行控制）
-- 注意：这里先允许员工看到自己的行（列权限后续收紧）
CREATE POLICY emp_self_policy ON hr.employees
    FOR SELECT
    USING (name = CURRENT_USER);

-- 策略2：manager 可以查看所有行
CREATE POLICY manager_all_policy ON hr.employees
    FOR SELECT
    USING (CURRENT_USER = 'manager');


-- 员工：只能看到 id, name, dept，不能看到 salary
GRANT SELECT (id, name, dept) ON hr.employees TO emp_zhang, emp_wang;

-- 经理：可以看到所有列
GRANT SELECT ON hr.employees TO manager;


GRANT CONNECT ON DATABASE mydb TO manager, emp_zhang, emp_wang;
GRANT USAGE ON SCHEMA hr TO manager, emp_zhang, emp_wang;



-- ✅ 允许
SELECT id, name, dept FROM hr.employees;

-- ❌ 无法查询 salary 列（权限不足）
SELECT * FROM hr.employees;

-- ❌ 看不到其他员工的行（RLS 拦截）
SELECT id, name, dept FROM hr.employees;   -- 只返回自己那行