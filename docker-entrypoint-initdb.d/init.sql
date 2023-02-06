CREATE USER shortener_user;
ALTER USER shortener_user WITH encrypted password '123456';
CREATE DATABASE shortener;
ALTER DATABASE shortener OWNER TO shortener_user;