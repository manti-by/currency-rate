const Main = imports.ui.main;
const Mainloop = imports.mainloop;
const St = imports.gi.St;
const GLib = imports.gi.GLib;

const EXT_PATH = '/home/manti/.local/share/gnome-shell/extensions/'
const EXT_UUID = 'currency-rate@manti.by.gmail.com';

let layout, button, label;

function update() {
  let data = GLib.spawn_command_line_sync('/usr/bin/python3 ' + EXT_PATH + EXT_UUID + '/data.py')[1].toString(),
      rates = JSON.parse(data);

  label.set_text('$ ' + ((rates.usd_buy + rates.usd_sell) / 2).toFixed(2));
  Mainloop.timeout_add_seconds(60 * 60, update);
}

function init() {
  layout = new St.BoxLayout();
  label = new St.Label({
    text: '$ ---',
    style_class: 'currency-rate'
  });
  button = new St.Bin({
    style_class: 'panel-button',
    reactive: true,
    can_focus: true,
    x_fill: true,
    y_fill: false,
    track_hover: true
  });

  button.set_child(label);
  layout.add(button, 0);

  update();
}

function enable() {
  Main.panel._centerBox.insert_child_at_index(layout, 2);
}

function disable() {
  Main.panel._centerBox.remove_child(layout);
}