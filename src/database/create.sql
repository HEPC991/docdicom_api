DROP DATABASE IF EXISTS dicom;
CREATE DATABASE IF NOT EXISTS dicom;

USE dicom;

DROP TABLE IF EXISTS menus;
CREATE TABLE IF NOT EXISTS menus(
    m_id BIGINT UNSIGNED NOT NULL  AUTO_INCREMENT
        COMMENT 'Identificador del menú',
    m_title VARCHAR(45) NOT NULL
        COMMENT 'Título o nombre del menú',
    m_url VARCHAR(300) NOT NULL
        COMMENT 'Enlace donde esta guardado el archivo que tiene relación con el menú',
    m_status ENUM('A', 'D') NOT NULL DEFAULT 'D'
        COMMENT 'Estado del menú donde: A = Activo (Active), D = Inactivo (Disable)',
    m_date_insert TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
        COMMENT 'Fecha de insercción',
    m_date_update TIMESTAMP
        COMMENT 'Última fecha de actualización',
    m_last_ip INT UNSIGNED
        COMMENT 'Últiama direccion IP que la modificó',
    m_by_user BIGINT UNSIGNED
        COMMENT 'Identificardor del usuario quien hizo la modificación',
    CONSTRAINT pk_m_id PRIMARY KEY (m_id)
)AUTO_INCREMENT = 10000000 ENGINE = InnoDB
COMMENT 'Tabla que guarda las opciones de menú';

DROP TABLE IF EXISTS specialities;
CREATE TABLE IF NOT EXISTS specialities(
    s_id BIGINT UNSIGNED NOT NULL  AUTO_INCREMENT
        COMMENT 'Identificador de la especialidad',
    s_name VARCHAR(45) NOT NULL
        COMMENT 'Nombre de la especialidad médica',
    s_status ENUM('A', 'D') NOT NULL DEFAULT 'D'
        COMMENT 'Estado de la especialidad donde: A = Activo (Active), D = Inactivo (Disable)',
    s_date_insert TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
        COMMENT 'Fecha de insercción',
    s_date_update TIMESTAMP
        COMMENT 'Última fecha de actualización',
    s_last_ip INT UNSIGNED
        COMMENT 'Últiama direccion IP que la modificó',
    s_by_user BIGINT UNSIGNED
        COMMENT 'Identificardor del usuario quien hizo la modificación',
    CONSTRAINT pk_s_id PRIMARY KEY (s_id)
)AUTO_INCREMENT = 10000000 ENGINE = InnoDB
COMMENT 'Tabla de especialidades de los médicos';

DROP TABLE IF EXISTS roles;
CREATE TABLE IF NOT EXISTS roles(
    r_id BIGINT UNSIGNED NOT NULL  AUTO_INCREMENT
        COMMENT 'Identificador del rol',
    r_name VARCHAR(50) NOT NULL
        COMMENT 'Nombre del rol',
    r_status ENUM('A', 'D') NOT NULL DEFAULT 'D'
        COMMENT 'Estado del rol donde: A = Activo (Active), D = Inactivo (Disable)',
    r_date_insert TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
        COMMENT 'Fecha de insercción',
    r_date_update TIMESTAMP
        COMMENT 'Última fecha de actualización',
    r_last_ip INT UNSIGNED
        COMMENT 'Últiama direccion IP que la modificó',
    r_by_user BIGINT UNSIGNED
        COMMENT 'Identificardor del usuario quien hizo la modificación',
    CONSTRAINT pk_r_id PRIMARY KEY (r_id)
)AUTO_INCREMENT = 10000000 ENGINE = InnoDB
COMMENT 'Tabla para asignar roles a los usuarios';

DROP TABLE IF EXISTS medical_institutions;
CREATE TABLE IF NOT EXISTS medical_institutions(
    mi_id BIGINT UNSIGNED NOT NULL  AUTO_INCREMENT
        COMMENT 'Identificador de la institución',
    mi_institute VARCHAR(50) NOT NULL
        COMMENT 'Nombre de la institución',
    mi_address VARCHAR(100) NOT NULL
        COMMENT 'Ubicación de la institución',
    mi_status ENUM('A', 'D') NOT NULL DEFAULT 'D'
        COMMENT 'Estado de la institución donde: A = Activo (Active), D = Inactivo (Disable)',
    mi_date_insert TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
        COMMENT 'Fecha de insercción',
    mi_date_update TIMESTAMP
        COMMENT 'Última fecha de actualización',
    mi_last_ip INT UNSIGNED
        COMMENT 'Últiama direccion IP que la modificó',
    mi_by_user BIGINT UNSIGNED
        COMMENT 'Identificardor del usuario quien hizo la modificación',
    CONSTRAINT pk_mi_id PRIMARY KEY (mi_id)
)AUTO_INCREMENT = 10000000 ENGINE = InnoDB
COMMENT 'Tabla de las instituciones médicas';

DROP TABLE IF EXISTS category_studies;
CREATE TABLE IF NOT EXISTS category_studies(
    cs_id BIGINT UNSIGNED NOT NULL  AUTO_INCREMENT
        COMMENT 'Identificador de la categoría',
    cs_name VARCHAR(45) NOT NULL
        COMMENT 'Nombre de la categoría',
    cs_status ENUM('A', 'D') NOT NULL DEFAULT 'D'
        COMMENT 'Estado de la categoría donde: A = Activo (Active), D = Inactivo (Disable)',
    cs_date_insert TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
        COMMENT 'Fecha de insercción',
    cs_date_update TIMESTAMP
        COMMENT 'Última fecha de actualización',
    cs_last_ip INT UNSIGNED
        COMMENT 'Últiama direccion IP que la modificó',
    cs_by_user BIGINT UNSIGNED
        COMMENT 'Identificardor del usuario quien hizo la modificación',
    CONSTRAINT pk_cs_id PRIMARY KEY (cs_id)
)AUTO_INCREMENT = 10000000 ENGINE = InnoDB
COMMENT 'Tabla que almacena el tipo de estudio que se realizó';

DROP TABLE IF EXISTS relations_m_r;
CREATE TABLE IF NOT EXISTS relations_m_r(
    rmr_m_id BIGINT UNSIGNED NOT NULL
        COMMENT 'Identificador del menú',
    rmr_r_id BIGINT UNSIGNED NOT NULL
        COMMENT 'Identificador del rol',
    rmr_status ENUM('A', 'D') NOT NULL DEFAULT 'D'
        COMMENT 'Estado de la relación menús-roles donde: A = Activo (Active), D = Inactivo (Disable)',
    rmr_date_insert TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
        COMMENT 'Fecha de insercción',
    rmr_date_update TIMESTAMP
        COMMENT 'Última fecha de actualización',
    rmr_last_ip INT UNSIGNED
        COMMENT 'Últiama direccion IP que la modificó',
    rmr_by_user BIGINT UNSIGNED
        COMMENT 'Identificardor del usuario quien hizo la modificación',
    CONSTRAINT pk_rmr_id PRIMARY KEY (rmr_r_id, rmr_m_id),
    CONSTRAINT fk_rmr_m FOREIGN KEY (rmr_m_id) REFERENCES menus(m_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_rmr_r FOREIGN KEY (rmr_r_id) REFERENCES roles(r_id)
            ON UPDATE CASCADE ON DELETE CASCADE
)ENGINE = InnoDB
COMMENT 'Relación entre la tabla "Roles" y "Menu"';

DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users(
    u_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT
        COMMENT 'Identificador del usuario',
    u_email VARCHAR(45) NOT NULL
        COMMENT 'Correo del usuario',
    u_name VARCHAR(40) NOT NULL
        COMMENT 'Nombre del usuario',
    u_last_name VARCHAR(25) NOT NULL
        COMMENT 'Apellido paterno del usuario',
    u_last_m_name VARCHAR(25)
        COMMENT 'Apellido materno del usuario',
    u_password VARCHAR(60) NOT NULL
        COMMENT 'Contraseña del usuario',
    u_phone VARCHAR(10)
            COMMENT 'Teléfono del usuario',
    u_status_p ENUM('A', 'D') NOT NULL DEFAULT 'D'
        COMMENT 'Estado del usuario en el sistema donde: A = Activo (Active), D = Inactivo (Disable)',
    u_status ENUM('A', 'D') NOT NULL DEFAULT 'A'
        COMMENT 'Estado del usuario en la DB donde: A = Activo (Active), D = Inactivo (Disable)',
    u_date_insert TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
        COMMENT 'Fecha de insercción',
    u_date_update TIMESTAMP
        COMMENT 'Última fecha de actualización',
    u_last_ip INT UNSIGNED
        COMMENT 'Últiama direccion IP que la modificó',
    u_by_user BIGINT UNSIGNED
        COMMENT 'Identificardor del usuario quien hizo la modificación',
    u_s_id BIGINT UNSIGNED DEFAULT NULL
        COMMENT 'Relaciona la tabla "Users" con "Specialties".
                Si es nula, significa que no es una médico sino un administrador o un paciente',
    u_r_id BIGINT UNSIGNED NOT NULL
        COMMENT 'Relaciona la tabla "Users" con "Roles"',
    CONSTRAINT uq_u_email UNIQUE (u_email),
    CONSTRAINT pk_u_id PRIMARY KEY (u_id),
    CONSTRAINT fk_u_s FOREIGN KEY (u_s_id) REFERENCES specialities(s_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_u_r FOREIGN KEY (u_r_id) REFERENCES roles(r_id)
                ON UPDATE CASCADE ON DELETE CASCADE
)AUTO_INCREMENT = 10000000 ENGINE = InnoDB
COMMENT 'Tabla de usuarios';

DROP TABLE IF EXISTS medical_appoiment;
CREATE TABLE IF NOT EXISTS medical_appoiment(
    ma_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT
        COMMENT 'Identificador de la cita médica',
    ma_date_study DATE
        COMMENT 'Fecha del estudio realizado',
    ma_description TINYTEXT NOT NULL
        COMMENT 'Pequeña descripción del estudio médico',
    ma_status ENUM('A', 'D') NOT NULL DEFAULT 'D'
        COMMENT 'Estado de la cita médica donde: A = Activo (Active), D = Inactivo (Disable)',
    ma_date_insert TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
        COMMENT 'Fecha de insercción',
    ma_date_update TIMESTAMP
        COMMENT 'Última fecha de actualización',
    ma_last_ip INT UNSIGNED
        COMMENT 'Últiama direccion IP que la modificó',
    ma_by_user BIGINT UNSIGNED
        COMMENT 'Identificardor del usuario quien hizo la modificación',
    ma_mi_id BIGINT UNSIGNED NOT NULL
        COMMENT 'Relacion entre la tabla "Medical_studies" y "Medical_institutions"',
    ma_cs_id BIGINT UNSIGNED NOT NULL
        COMMENT 'Relacion entre la tabla "Medical_studies" y "Category_studies"',
    CONSTRAINT pk_ma_id PRIMARY KEY (ma_id),
    CONSTRAINT fk_ma_mi FOREIGN KEY (ma_mi_id) REFERENCES medical_institutions(mi_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_ma_cs FOREIGN KEY (ma_cs_id) REFERENCES category_studies(cs_id)
                ON UPDATE CASCADE ON DELETE CASCADE
)AUTO_INCREMENT = 10000000 ENGINE = InnoDB
COMMENT 'Tabla de cita médicos';

DROP TABLE IF EXISTS history_medical;
CREATE TABLE IF NOT EXISTS history_medical(
    hm_u_id BIGINT UNSIGNED NOT NULL
        COMMENT 'Identificacor del usuario',
    hm_ma_id BIGINT UNSIGNED NOT NULL
        COMMENT 'identificador de la cita médica',
    hm_status ENUM('A', 'D') NOT NULL DEFAULT 'D'
        COMMENT 'Estado de la relación cita médica - usuarios donde: A = Activo (Active), D = Inactivo (Disable)',
    hm_date_insert TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
        COMMENT 'Fecha de insercción',
    hm_date_update TIMESTAMP
        COMMENT 'Última fecha de actualización',
    hm_last_ip INT UNSIGNED
        COMMENT 'Últiama direccion IP que la modificó',
    hm_by_user BIGINT UNSIGNED
        COMMENT 'Identificardor del usuario quien hizo la modificación',
    CONSTRAINT pk_hm_id PRIMARY KEY (hm_u_id, hm_ma_id),
    CONSTRAINT fk_hm_ma FOREIGN KEY (hm_ma_id) REFERENCES medical_appoiment(ma_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_hm_u FOREIGN KEY (hm_u_id) REFERENCES users(u_id)
                ON UPDATE CASCADE ON DELETE CASCADE
)ENGINE = InnoDB
COMMENT 'Relación entre "users" y "medical_appoiment"';

DROP TABLE IF EXISTS dicoms;
CREATE TABLE IF NOT EXISTS dicoms(
    d_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT
        COMMENT 'Identificador de un único archivo dicom',
    d_serie VARCHAR(20) NOT NULL
        COMMENT 'Serie a la que pertenece el dicom',
    d_dicom MEDIUMBLOB
        COMMENT 'Es el archivo dicom',
    d_status ENUM('A', 'D') NOT NULL DEFAULT 'D'
        COMMENT 'Estado del dicom donde: A = Activo (Active), D = Inactivo (Disable)',
    d_date_insert TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
        COMMENT 'Fecha de insercción',
    d_date_update TIMESTAMP
        COMMENT 'Última fecha de actualización',
    d_last_ip INT UNSIGNED
        COMMENT 'Últiama direccion IP que la modificó',
    d_by_user BIGINT UNSIGNED
        COMMENT 'Identificardor del usuario quien hizo la modificación',
    d_ma_id BIGINT UNSIGNED NOT NULL
        COMMENT 'Identificador del id de la tabla medical_appoiment',
    CONSTRAINT pk_d_id PRIMARY KEY (d_id, d_serie),
    CONSTRAINT fk_d_ma FOREIGN KEY (d_ma_id) REFERENCES medical_appoiment(ma_id)
                ON UPDATE CASCADE ON DELETE CASCADE
)AUTO_INCREMENT = 10000000 ENGINE = InnoDB
COMMENT 'Tabla de cita médicos';

DROP TABLE IF EXISTS images;
CREATE TABLE IF NOT EXISTS images(
    i_d_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT
        COMMENT 'Identificador de un único archivo dicom',
    i_d_serie VARCHAR(20) NOT NULL
        COMMENT 'Serie a la que pertenece el dicom',
    i_image MEDIUMBLOB
        COMMENT 'Es la imagen',
    i_status ENUM('A', 'D') NOT NULL DEFAULT 'D'
        COMMENT 'Estado de la imagen donde: A = Activo (Active), D = Inactivo (Disable)',
    i_date_insert TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
        COMMENT 'Fecha de insercción',
    i_date_update TIMESTAMP
        COMMENT 'Última fecha de actualización',
    i_last_ip INT UNSIGNED
        COMMENT 'Últiama direccion IP que la modificó',
    i_by_user BIGINT UNSIGNED
        COMMENT 'Identificardor del usuario quien hizo la modificación',
    CONSTRAINT pk_i_id PRIMARY KEY(i_d_id, i_d_serie),
    CONSTRAINT fk_i_d FOREIGN KEY (i_d_id, i_d_serie) REFERENCES dicoms(d_id, d_serie)
                ON UPDATE CASCADE ON DELETE CASCADE
)ENGINE = InnoDB
COMMENT 'Tabla donde se guardan las imagenes';