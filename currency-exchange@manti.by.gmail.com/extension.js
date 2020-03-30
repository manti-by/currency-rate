'use strict';

const St = imports.gi.St;
const Main = imports.ui.main;

let refreshButton, mainLayout, mainCurrencyText, iconBin;
let soupSession;

let lastCurrency = 0.00;


function refreshCurrency() {
    let requestMessage = Soup.Message.new('GET', 'https://www.mtbank.by/currxml.php?ver=2');

    soupSession.queue_message(requestMessage, function(session, message) {
        if (message.status_code !== 200) { return; }

        let body = JSON.parse(message.response_body.data);
        let value = body.rates.BRL;
        let arrow;
        if (lastCurrency !== 0) {
            if (value > lastCurrency) {
                arrow = 'arrow-up';
            } else if (value < lastCurrency) {
                arrow = 'arrow-down';
            }
            let arrowIcon = new St.Icon({
                icon_name: arrow,
                style_class: 'system-status-icon'
            });
            iconBin.set_child(arrowIcon);
        }

        lastCurrency = value;
        mainCurrencyText.set_text('BYN/USD ' + value.toString());
    });
}

function init(extensionMeta) {
    let theme = imports.gi.Gtk.IconTheme.get_default();
    theme.append_search_path(extensionMeta.path + "/icons");

    mainCurrencyText = new St.Label({ text: 'BYN/USD 0.00' });
    mainLayout = new St.BoxLayout();
    refreshButton = new St.Bin({
        style_class: 'panel-button',
        reactive: true,
        can_focus: true,
        x_fill: true,
        y_fill: false,
        track_hover: true
    });

    refreshButton.connect('button-press-event', refreshCurrency);
    iconBin = new St.Bin({
        style_class: 'panel-button',
        reactive: true,
        can_focus: true,
        x_fill: true,
        y_fill: false,
        track_hover: true
    });

    mainLayout.add(refreshButton, 0);
    mainLayout.add(mainCurrencyText, 1);
    mainLayout.add(iconBin, 2);

    refreshCurrency();
}

function enable() {
    Main.panel._centerBox.insert_child_at_index(mainLayout, 0);
}

function disable() {
    Main.panel._centerBox.remove_child(mainLayout);
}
