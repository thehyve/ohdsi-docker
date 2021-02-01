INSERT INTO ohdsi.source (source_id, source_name, source_key, source_connection, source_dialect) VALUES (${ID}, '${NAME}', '${NAME}', 'jdbc:postgresql://postgresql:5432/ohdsi?user=postgres&password=${POSTGRESQL_PASSWORD}', 'postgresql');
INSERT INTO ohdsi.source_daimon (source_id, daimon_type, table_qualifier, priority) VALUES (${ID}, 0, '${CDM_SCHEMA}', 0);
INSERT INTO ohdsi.source_daimon (source_id, daimon_type, table_qualifier, priority) VALUES (${ID}, 1, 'vocab', 1);
INSERT INTO ohdsi.source_daimon (source_id, daimon_type, table_qualifier, priority) VALUES (${ID}, 2, '${RESULTS_SCHEMA}', 1);
INSERT INTO ohdsi.source_daimon (source_id, daimon_type, table_qualifier, priority) VALUES (${ID}, 3, 'ohdsi', 1);
INSERT INTO ohdsi.source_daimon (source_id, daimon_type, table_qualifier, priority) VALUES (${ID}, 5, 'temp', 0);
-- You might need to refresh the webapi sources http://localhost:8080/WebAPI/source/refresh