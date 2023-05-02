create
    definer = root@localhost procedure sp_activate_user(IN in_u_id bigint unsigned, IN in_ipv4 varchar(15),
                                                        IN in_by_user bigint unsigned)
begin
    UPDATE users SET u_status_p = 'A', u_last_ip = inet_aton(in_ipv4), u_date_update = current_timestamp, u_by_user = in_by_user WHERE u_id = in_u_id;
END;

create
    definer = root@localhost procedure sp_create_menu(IN in_m_title varchar(45), IN in_m_url varchar(300),
                                                      IN in_m_status enum ('A', 'D'))
begin
    INSERT INTO menus (m_title, m_url, m_status) VALUES (in_m_title, in_m_url,in_m_status);
END;

create
    definer = root@localhost procedure sp_create_patient(IN email_u varchar(45), IN name_u varchar(40),
                                                         IN last_name_u varchar(25), IN last_m_name_u varchar(25),
                                                         IN password_u varchar(60), IN phone_u varchar(10))
BEGIN
    INSERT INTO users(u_email, u_name, u_last_name, u_last_m_name, u_password, u_phone, u_r_id)
        VALUES (email_u, name_u, last_name_u, last_m_name_u, password_u, phone_u, 10000002);
END;

create
    definer = root@localhost procedure sp_create_user(IN ui_email varchar(45), IN ui_name varchar(40),
                                                      IN ui_last_name varchar(25), IN ui_last_m_name varchar(25),
                                                      IN ui_password varchar(60), IN ui_phone varchar(10),
                                                      IN ui_status_p enum ('A', 'D'), IN ui_s_id bigint unsigned,
                                                      IN ui_r_id bigint unsigned)
begin
    
    INSERT INTO users (u_email, u_name, u_last_name, u_last_m_name, u_password, u_phone, u_status_p , u_s_id, u_r_id) VALUES(ui_email, ui_name, ui_last_name, ui_last_m_name, ui_password, ui_phone, ui_status_p, ui_s_id, ui_r_id);
END;

create
    definer = root@localhost procedure sp_deactivate_user(IN in_u_id bigint unsigned, IN in_ipv4 varchar(15),
                                                          IN in_by_user bigint unsigned)
begin
    UPDATE users SET u_status_p = 'D', u_date_update = current_timestamp, u_last_ip = inet_aton(in_ipv4), u_by_user = in_by_user WHERE u_id = in_u_id;
END;

create
    definer = root@localhost procedure sp_delete_dicom(IN in_di_id bigint unsigned, IN in_ipv4 varchar(15),
                                                       IN in_by_user bigint unsigned)
begin
    update dicoms set d_status = 'D', d_date_update = current_timestamp, d_last_ip = inet_aton(in_ipv4), d_by_user = in_by_user where d_id = in_di_id;
end;

create
    definer = root@localhost procedure sp_delete_institute(IN in_mi_id bigint unsigned, IN in_ipv4 varchar(15),
                                                           IN in_by_user bigint unsigned)
begin
    update medical_institutions set mi_status = 'D', mi_date_update = current_timestamp, mi_last_ip = inet_aton(in_ipv4), mi_by_user = in_by_user where mi_id = in_mi_id;
end;

create
    definer = root@localhost procedure sp_delete_medic_study(IN in_ms_id bigint unsigned, IN in_ipv4 varchar(15),
                                                             IN in_by_user bigint unsigned)
begin
    update medical_appoiment set ma_status = 'D', ma_last_ip = inet_aton(in_ipv4), ma_by_user = in_by_user, ma_date_update = current_timestamp where ma_id = in_ms_id;
end;

create
    definer = root@localhost procedure sp_delete_menu(IN in_m_id bigint unsigned, IN in_ipv4 varchar(15),
                                                      IN in_by_user bigint unsigned)
begin
    update menus set m_status = 'D', m_last_ip = inet_aton(in_ipv4), m_by_user = in_by_user, m_date_update = current_timestamp where m_id = in_m_id;
end;

create
    definer = root@localhost procedure sp_delete_user(IN in_u_id bigint unsigned, IN in_ipv4 varchar(15),
                                                      IN in_by_user bigint unsigned)
begin
    update users set u_status = 'D', u_last_ip = inet_aton(in_ipv4), u_date_update = current_timestamp, u_by_user = in_by_user where u_id = in_u_id;
end;

create
    definer = root@localhost procedure sp_get_institute()
begin
    Select mi_institute, mi_address, mi_status FROM medical_institutions;
END;

create
    definer = root@localhost procedure sp_get_medic_study()
begin
    Select ma_date_study, ma_description, ma_status, ma_mi_id, ma_cs_id FROM medical_appoiment;
END;

create
    definer = root@localhost procedure sp_get_menus()
begin
    Select m_title, m_url, m_status FROM menus;
END;

create
    definer = root@localhost procedure sp_get_users()
begin
    
    select u_id `id`,
           u_email `email`,
           u_last_name `last_name`,
           u_last_m_name `last_m_name`,
           u_phone `phone`,
           u_status_p `isActive`,
           u_r_id `role_id`,
           r.r_name `role_name`,
           u_s_id `speciality_id`
           from users
           inner join roles r on users.u_r_id = r.r_id
           where u_status = 'A';
    
END;

create
    definer = root@localhost procedure sp_register_institute(IN in_name_institute varchar(50),
                                                             IN in_address_institute varchar(100))
begin
    INSERT INTO medical_institutions (mi_institute, mi_address) VALUES (in_name_institute, in_address_institute);
END;

create
    definer = root@localhost procedure sp_register_medic_study(IN ms_date_study date, IN ms_description tinytext,
                                                               IN ms_status enum ('A', 'D'),
                                                               IN ms_mi_id bigint unsigned, IN ms_cs_id bigint unsigned)
begin
    insert into medical_appoiment (ma_date_study, ma_description, ma_status, ma_mi_id, ma_cs_id) values(ms_date_study, ms_description, ms_status, ms_mi_id, ms_cs_id);
END;

create
    definer = root@localhost procedure sp_validate_user(IN email_u varchar(45))
BEGIN
    SELECT u_email as `email`,
    u_password as `password`,
    u_name as `name`,
    u_last_name,
    u_last_m_name,
    u_phone as `phone`,
    u_id as `id_user`
    FROM users
    WHERE u_email = email_u;
END;

create
    definer = root@localhost procedure sp_save_dicom(IN in_d_serie varchar(500), IN in_d_dicom mediumblob,
                                                     IN in_d_ma_id bigint unsigned)
begin
    insert into dicoms (d_serie, d_dicom, d_ma_id) values(in_d_serie, in_d_dicom, in_d_ma_id);
end;