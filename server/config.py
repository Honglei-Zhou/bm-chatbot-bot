username = 'hzhou'
password = 'cognitiveati'
host = 'blissmotors.cqh3eh5shl0r.us-east-2.rds.amazonaws.com'
port = 5432
test_db = 'bmcars_dev'

db_string = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(username, password, host, port, test_db)

project_id = 'newagent-c47af'
# project_id = 'telle-ai-dev-rdgebu'