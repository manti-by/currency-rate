const Main = imports.ui.main;
const Mainloop = imports.mainloop;
const St = imports.gi.St;
const GLib = imports.gi.GLib;

const EXT_PATH = '/home/manti/.local/share/gnome-shell/extensions/currency-rate@manti.by.gmail.com/';

let layout, button, label;

function update() {
  let data = GLib.spawn_sync(EXT_PATH, ['/usr/bin/python3', '-m', 'app.worker'], null, 0, null)[1].toString(),
      rates = JSON.parse(data);

  let value = rates.usd.toFixed(2),
      trend = rates.usd_trend > 0 ? '↑' : '↓';

  label.set_text('$ ' + value + trend);
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