pkg load database

conn = pq_connect(setdbopts(...
'dbname','postgres',...
'host','localhost',...
'port','5432',...
'user','postgres',...
'password','mafer123'));

% INSERT
pq_exec_params(conn,"INSERT INTO redes VALUES ('Sofia Rodriguez',201854321);");

% SELECT
N = pq_exec_params(conn,"SELECT * FROM redes")

% UPDATE
pq_exec_params(conn,"UPDATE redes SET nombre='María Fernanda' WHERE carnet=201854321;");

% SELECT
N = pq_exec_params(conn,"SELECT * FROM redes")

% DELETE
pq_exec_params(conn,"DELETE FROM redes WHERE carnet=201854321;");

% SELECT
N = pq_exec_params(conn,"SELECT * FROM redes")
