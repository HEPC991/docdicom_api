USE dicom;

INSERT INTO menus (m_title,m_url,m_status)
VALUES ('Borland','http://reddit.com/one?k=0','A'),
  ('Microsoft','https://youtube.com/en-ca?q=test','D'),
  ('Yahoo','http://guardian.co.uk/user/110?q=11','A'),
  ('Sibelius','https://twitter.com/site?client=g','D'),
  ('Lavasoft','http://guardian.co.uk/settings?ab=441&aad=2','A'),
  ('Amazon','https://cnn.com/user/110?q=11','D'),
  ('Apple','http://youtube.com/en-us?k=0','A'),
  ('Borland','http://pinterest.com/fr?gi=100','D'),
  ('Google','http://facebook.com/site?search=1','A'),
  ('Borland','https://youtube.com/fr?p=8','D');

INSERT INTO specialities (s_name, s_status) VALUES ('Cardiología Clínica', 'A');
INSERT INTO specialities (s_name, s_status) VALUES ('Cirugía Pediátrica', 'D');
INSERT INTO specialities (s_name, s_status) VALUES ('Cirugía General', 'A');
INSERT INTO specialities (s_name, s_status) VALUES ('Gastroenterología', 'D');
INSERT INTO specialities (s_name, s_status) VALUES ('Hematología', 'A');
INSERT INTO specialities (s_name, s_status) VALUES ('Neumología', 'A');
INSERT INTO specialities (s_name, s_status) VALUES ('Ortopedia', 'A');
INSERT INTO specialities (s_name, s_status) VALUES ('Otorrinolaringología', 'D');
INSERT INTO specialities (s_name, s_status) VALUES ('Radiología e Imagen', 'A');
INSERT INTO specialities (s_name, s_status) VALUES ('Cirugía Oncológica', 'D');

INSERT INTO roles (r_name, r_status) VALUES ('Adiministrador', 'A');
INSERT INTO roles (r_name, r_status) VALUES ('Médico', 'A');
INSERT INTO roles (r_name, r_status) VALUES ('Paciente', 'A');

INSERT INTO medical_institutions (mi_institute, mi_address, mi_status) VALUES ('American Sales Company', '02 Talmadge Junction', 'D');
INSERT INTO medical_institutions (mi_institute, mi_address, mi_status) VALUES ('Lake Erie Medical DBA Quality Care Products LLC', '32487 Pleasure Avenue', 'D');
INSERT INTO medical_institutions (mi_institute, mi_address, mi_status) VALUES ('Procter & Gamble Manufacturing Co.', '10957 Old Shore Lane', 'D');
INSERT INTO medical_institutions (mi_institute, mi_address, mi_status) VALUES ('Cadila Healthcare Limited', '24532 Esker Lane', 'A');
INSERT INTO medical_institutions (mi_institute, mi_address, mi_status) VALUES ('AMOREPACIFIC', '42 Anhalt Place', 'D');
INSERT INTO medical_institutions (mi_institute, mi_address, mi_status) VALUES ('Contract Pharmacy Services-PA', '72 Monica Way', 'A');
INSERT INTO medical_institutions (mi_institute, mi_address, mi_status) VALUES ('Otsuka America Pharmaceutical, Inc.', '76334 Arkansas Hill', 'A');
INSERT INTO medical_institutions (mi_institute, mi_address, mi_status) VALUES ('STAT Rx USA LLC', '403 Linden Center', 'D');
INSERT INTO medical_institutions (mi_institute, mi_address, mi_status) VALUES ('Preferred Pharmaceuticals, Inc.', '6 Erie Lane', 'D');
INSERT INTO medical_institutions (mi_institute, mi_address, mi_status) VALUES ('Health-Love Co.', '74414 Becker Drive', 'D');

INSERT INTO category_studies (cs_name, cs_status) VALUES ('Pulmo Bryonia', 'D');
INSERT INTO category_studies (cs_name, cs_status) VALUES ('Glipizide', 'A');
INSERT INTO category_studies (cs_name, cs_status) VALUES ('TRICLOSAN', 'A');
INSERT INTO category_studies (cs_name, cs_status) VALUES ('Nicotine Polacrilex', 'A');
INSERT INTO category_studies (cs_name, cs_status) VALUES ('Isopropyl Alcohol', 'D');
INSERT INTO category_studies (cs_name, cs_status) VALUES ('Octinoxate, Octisalate and Avobenzone', 'D');
INSERT INTO category_studies (cs_name, cs_status) VALUES ('divalproex sodium', 'D');
INSERT INTO category_studies (cs_name, cs_status) VALUES ('Trihexyphenidyl Hydrochloride', 'A');
INSERT INTO category_studies (cs_name, cs_status) VALUES ('Metoprolol tartrate', 'A');
INSERT INTO category_studies (cs_name, cs_status) VALUES ('Bacitracin Zinc', 'D');

INSERT INTO relations_m_r (rmr_m_id, rmr_r_id, rmr_status) VALUES (10000000, 10000000, 'A');
INSERT INTO relations_m_r (rmr_m_id, rmr_r_id, rmr_status) VALUES (10000006, 10000002, 'A');
INSERT INTO relations_m_r (rmr_m_id, rmr_r_id, rmr_status) VALUES (10000000, 10000001, 'A');
INSERT INTO relations_m_r (rmr_m_id, rmr_r_id, rmr_status) VALUES (10000007, 10000000, 'D');
INSERT INTO relations_m_r (rmr_m_id, rmr_r_id, rmr_status) VALUES (10000000, 10000002, 'D');
INSERT INTO relations_m_r (rmr_m_id, rmr_r_id, rmr_status) VALUES (10000007, 10000001, 'A');
INSERT INTO relations_m_r (rmr_m_id, rmr_r_id, rmr_status) VALUES (10000009, 10000002, 'D');
INSERT INTO relations_m_r (rmr_m_id, rmr_r_id, rmr_status) VALUES (10000003, 10000000, 'D');
INSERT INTO relations_m_r (rmr_m_id, rmr_r_id, rmr_status) VALUES (10000009, 10000001, 'A');
INSERT INTO relations_m_r (rmr_m_id, rmr_r_id, rmr_status) VALUES (10000008, 10000000, 'A');

INSERT INTO users (u_email, u_name, u_last_name, u_last_m_name, u_password, u_phone, u_status_p, u_s_id, u_r_id)
VALUES ('gsimko0@jigsy.com', 'Gilly', 'Cracie', 'Simko', 'b6dc8bb6dbc97e8da9e743be3b6474e7cc5dad0f', '7730824071', 'D', NULL, 10000002);
INSERT INTO users (u_email, u_name, u_last_name, u_last_m_name, u_password, u_phone, u_status_p, u_s_id, u_r_id)
VALUES ('itarquinio1@auda.org.au', 'Inger', 'Carbert', 'Tarquinio', 'b6dc8bb6dbc97e8da9e743be3b6474e7cc5dad0f', '7737602095', 'A', NULL, 10000002);
INSERT INTO users (u_email, u_name, u_last_name, u_last_m_name, u_password, u_phone, u_status_p, u_s_id, u_r_id)
VALUES ('cwise2@github.com', 'Candice', 'Chaloner', 'Wise', 'b6dc8bb6dbc97e8da9e743be3b6474e7cc5dad0f', '7732904572', 'A', 10000008, 10000001);
INSERT INTO users (u_email, u_name, u_last_name, u_last_m_name, u_password, u_phone, u_status_p, u_s_id, u_r_id)
VALUES ('wmccarlie3@moonfruit.com', 'Wilma', 'Paffett', 'McCarlie', 'b6dc8bb6dbc97e8da9e743be3b6474e7cc5dad0f', '7738202505', 'D', 10000001, 10000001);
INSERT INTO users (u_email, u_name, u_last_name, u_last_m_name, u_password, u_phone, u_status_p, u_s_id, u_r_id)
VALUES ('cfrantzeni4@wix.com', 'Cherish', 'Rickword', 'Frantzeni', 'b6dc8bb6dbc97e8da9e743be3b6474e7cc5dad0f', '7736253482', 'D', NULL, 10000000);
INSERT INTO users (u_email, u_name, u_last_name, u_last_m_name, u_password, u_phone, u_status_p, u_s_id, u_r_id)
VALUES ('kbrodest5@google.com', 'Kathi', 'Childs', 'Brodest', 'b6dc8bb6dbc97e8da9e743be3b6474e7cc5dad0f', '7739949028', 'D', 10000008, 10000001);
INSERT INTO users (u_email, u_name, u_last_name, u_last_m_name, u_password, u_phone, u_status_p, u_s_id, u_r_id)
VALUES ('adahlberg6@xinhuanet.com', 'Alayne', 'Leavens', 'Dahlberg', 'b6dc8bb6dbc97e8da9e743be3b6474e7cc5dad0f', '7719714726', 'D', NULL, 10000002);
INSERT INTO users (u_email, u_name, u_last_name, u_last_m_name, u_password, u_phone, u_status_p, u_s_id, u_r_id)
VALUES ('teads7@stumbleupon.com', 'Thibaud', 'Balcers', 'Eads', 'b6dc8bb6dbc97e8da9e743be3b6474e7cc5dad0f', '7731073529', 'A', NULL, 10000002);
INSERT INTO users (u_email, u_name, u_last_name, u_last_m_name, u_password, u_phone, u_status_p, u_s_id, u_r_id)
VALUES ('nveeler8@1688.com', 'Nellie', 'Balaam', 'Veeler', 'b6dc8bb6dbc97e8da9e743be3b6474e7cc5dad0f', '7735572619', 'A', 10000008, 10000001);
INSERT INTO users (u_email, u_name, u_last_name, u_last_m_name, u_password, u_phone, u_status_p, u_s_id, u_r_id)
VALUES ('kbennough9@github.com', 'Kattie', 'Douglas', 'Bennough', 'b6dc8bb6dbc97e8da9e743be3b6474e7cc5dad0f', '7732159307', 'D', NULL, 10000002);

INSERT INTO medical_appoiment (ma_date_study, ma_description, ma_status, ma_mi_id, ma_cs_id)
VALUES ('2023-03-15', 'Curabitur gravida nisi at nibh. In hac habitasse platea dictumst. Aliquam augue quam, sollicitudin vitae, consectetuer eget, rutrum at, lorem.', 'D', 10000009, 10000008);
INSERT INTO medical_appoiment (ma_date_study, ma_description, ma_status, ma_mi_id, ma_cs_id)
VALUES ('2023-02-02', 'Proin eu mi. Nulla ac enim. In tempor, turpis nec euismod scelerisque, quam turpis adipiscing lorem, vitae mattis nibh ligula nec sem.', 'D', 10000003, 10000003);
INSERT INTO medical_appoiment (ma_date_study, ma_description, ma_status, ma_mi_id, ma_cs_id)
VALUES ('2023-02-17', 'Cras non velit nec nisi vulputate nonummy. Maecenas tincidunt lacus at velit. Vivamus vel nulla eget eros elementum pellentesque.', 'A', 10000004, 10000000);
INSERT INTO medical_appoiment (ma_date_study, ma_description, ma_status, ma_mi_id, ma_cs_id)
VALUES ('2023-03-03', 'Nulla ut erat id mauris vulputate elementum. Nullam varius. Nulla facilisi.', 'D', 10000006, 10000004);
INSERT INTO medical_appoiment (ma_date_study, ma_description, ma_status, ma_mi_id, ma_cs_id)
VALUES ('2023-02-17', 'Phasellus sit amet erat. Nulla tempus. Vivamus in felis eu sapien cursus vestibulum.', 'A', 10000002, 10000003);
INSERT INTO medical_appoiment (ma_date_study, ma_description, ma_status, ma_mi_id, ma_cs_id)
VALUES ('2023-02-25', 'Aenean fermentum. Donec ut mauris eget massa tempor convallis. Nulla neque libero, convallis eget, eleifend luctus, ultricies eu, nibh.', 'D', 10000007, 10000009);
INSERT INTO medical_appoiment (ma_date_study, ma_description, ma_status, ma_mi_id, ma_cs_id)
VALUES ('2023-02-24', 'Nullam porttitor lacus at turpis. Donec posuere metus vitae ipsum. Aliquam non mauris.', 'A', 10000009, 10000009);
INSERT INTO medical_appoiment (ma_date_study, ma_description, ma_status, ma_mi_id, ma_cs_id)
VALUES ('2023-02-07', 'Phasellus in felis. Donec semper sapien a libero. Nam dui.', 'D', 10000004, 10000005);
INSERT INTO medical_appoiment (ma_date_study, ma_description, ma_status, ma_mi_id, ma_cs_id)
VALUES ('2023-03-04', 'Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis.', 'D', 10000001, 10000007);
INSERT INTO medical_appoiment (ma_date_study, ma_description, ma_status, ma_mi_id, ma_cs_id)
VALUES ('2023-03-15', 'Nam ultrices, libero non mattis pulvinar, nulla pede ullamcorper augue, a suscipit nulla elit ac nulla. Sed vel enim sit amet nunc viverra dapibus. Nulla suscipit ligula in lacus.', 'A', 10000008, 10000009);

INSERT INTO history_medical (hm_u_id, hm_ma_id, hm_status) VALUES (10000007, 10000000, 'A');
INSERT INTO history_medical (hm_u_id, hm_ma_id, hm_status) VALUES (10000008, 10000007, 'A');
INSERT INTO history_medical (hm_u_id, hm_ma_id, hm_status) VALUES (10000008, 10000005, 'A');
INSERT INTO history_medical (hm_u_id, hm_ma_id, hm_status) VALUES (10000005, 10000008, 'A');
INSERT INTO history_medical (hm_u_id, hm_ma_id, hm_status) VALUES (10000006, 10000005, 'A');
INSERT INTO history_medical (hm_u_id, hm_ma_id, hm_status) VALUES (10000003, 10000001, 'D');
INSERT INTO history_medical (hm_u_id, hm_ma_id, hm_status) VALUES (10000004, 10000006, 'A');
INSERT INTO history_medical (hm_u_id, hm_ma_id, hm_status) VALUES (10000002, 10000003, 'A');
INSERT INTO history_medical (hm_u_id, hm_ma_id, hm_status) VALUES (10000009, 10000006, 'D');
INSERT INTO history_medical (hm_u_id, hm_ma_id, hm_status) VALUES (10000005, 10000000, 'D');
