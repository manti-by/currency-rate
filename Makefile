EXT_UUID = currency-rate@manti.by.gmail.com
EXT_PATH = ~/.local/share/gnome-shell/extensions

install:
	mkdir -p $(EXT_PATH)/$(EXT_UUID)/
	cp data.py $(EXT_PATH)/$(EXT_UUID)/
	cp extension.js $(EXT_PATH)/$(EXT_UUID)/
	cp metadata.json $(EXT_PATH)/$(EXT_UUID)/
	cp stylesheet.css $(EXT_PATH)/$(EXT_UUID)/
	gnome-shell-extension-tool -e $(EXT_UUID)

update:
	cp data.py $(EXT_PATH)/$(EXT_UUID)/
	cp extension.js $(EXT_PATH)/$(EXT_UUID)/
	cp metadata.json $(EXT_PATH)/$(EXT_UUID)/
	cp stylesheet.css $(EXT_PATH)/$(EXT_UUID)/
	gnome-shell-extension-tool -r $(EXT_UUID)

remove:
	gnome-shell-extension-tool -d $(EXT_UUID)
	rm -rf $(EXT_PATH)/$(EXT_UUID)/
