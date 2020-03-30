define MIGRATION_SCRIPT
CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temp DECIMAL(5,2),
    humidity TINYINT,
    moisture TINYINT,
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP
);
endef

export MIGRATION_SCRIPT
migrate:
	sqlite3 db.sqlite "$$MIGRATION_SCRIPT"

define SEED_SCRIPT
INSERT INTO data (temp, humidity, moisture, datetime) VALUES (22, 50, 75, '2018-01-01 02:00:00');
INSERT INTO data (temp, humidity, moisture, datetime) VALUES (25, 45, 72, '2018-01-01 02:15:00');
INSERT INTO data (temp, humidity, moisture, datetime) VALUES (23, 55, 68, '2018-01-01 02:30:00');
INSERT INTO data (temp, humidity, moisture, datetime) VALUES (20, 60, 64, '2018-01-01 02:45:00');
INSERT INTO data (temp, humidity, moisture, datetime) VALUES (18, 72, 60, '2018-01-01 03:00:00');
INSERT INTO data (temp, humidity, moisture, datetime) VALUES (17, 50, 60, '2018-01-01 03:15:00');
INSERT INTO data (temp, humidity, moisture, datetime) VALUES (22, 45, 58, '2018-01-01 03:30:00');
INSERT INTO data (temp, humidity, moisture, datetime) VALUES (25, 45, 59, '2018-01-01 03:45:00');
INSERT INTO data (temp, humidity, moisture, datetime) VALUES (26, 40, 59, '2018-01-01 04:00:00');
INSERT INTO data (temp, humidity, moisture, datetime) VALUES (25, 42, 58, '2018-01-01 04:15:00');
endef

export SEED_SCRIPT
seed:
	sqlite3 db.sqlite "$$SEED_SCRIPT"

remigrate:
	rm -f db.sqlite
	make migrate
	make seed

export FLASK_APP=server
export FLASK_DEBUG=1
export TEMPLATES_AUTO_RELOAD=1
local:
	cd app && flask run --host=0.0.0.0

pip:
	pip install -Ur deploy/requirements.txt

venv:
	deactivate | true
	rm -rf ../venv/
	virtualenv -p python3 --no-site-packages --prompt=apollo- ../venv
	. ../venv/bin/activate

check:
	black --line-length 89 --target-version py36 app/
	isort app/*.py
	flake8
