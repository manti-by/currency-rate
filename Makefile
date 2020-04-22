EXT_UUID = currency-rate@manti.by.gmail.com
EXT_PATH = ~/.local/share/gnome-shell/extensions

install:
	mkdir -p $(EXT_PATH)/$(EXT_UUID)/
	cp -r * $(EXT_PATH)/$(EXT_UUID)/
	gnome-shell-extension-tool -e $(EXT_UUID)

update:
	cp -r * $(EXT_PATH)/$(EXT_UUID)/
	gnome-shell-extension-tool -r $(EXT_UUID)

remove:
	gnome-shell-extension-tool -d $(EXT_UUID)
	rm -rf $(EXT_PATH)/$(EXT_UUID)/

define MIGRATION_SCRIPT
CREATE TABLE IF NOT EXISTS exchange_rates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usd_buy DECIMAL(5,2),
    usd_sell DECIMAL(5,2),
    eur_buy DECIMAL(5,2),
    eur_sell DECIMAL(5,2),
    rur_buy DECIMAL(5,2),
    rur_sell DECIMAL(5,2),
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP
);
endef

export MIGRATION_SCRIPT
migrate:
	sqlite3 app/db.sqlite "$$MIGRATION_SCRIPT"