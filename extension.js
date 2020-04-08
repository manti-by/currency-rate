const GObject = imports.gi.GObject
const Main = imports.ui.main
const Mainloop = imports.mainloop
const St = imports.gi.St
const Soup = imports.gi.Soup

let layout, button, label, session, value = 2.00

function update() {
  let session = new Soup.SessionAsync()
  Soup.Session.prototype.add_feature.call(session, new Soup.ProxyResolverDefault())

  let request = Soup.Message.new('GET', 'https://www.mtbank.by/currxml.php?ver=2')
  session.queue_message(request, function(session, message) {
    if (message.status_code !== 200) {
      label.set_text('$ err')
      return
    }

    let data = new GObject.Value()
    Soup.xmlrpc_parse_method_response(
      message.response_body.data, message.response_body.data.length, data
    )

    for (const element of data.children) {
      if (element.id === '168,768,968,868') {
        for (const currency of element.children) {
          if (currency.children[0].textContent === 'BYN' &&
            currency.children[1].textContent === 'USD') {
            value = (currency.children[2].textContent + currency.children[3].textContent) / 2
            label.set_text('$ ' + value.toFixed(2))
            break
          }
        }
        break
      }
    }

    label.set_text('$ ---')
  });

  Mainloop.timeout_add_seconds(60 * 60, update)
}

function init() {
  layout = new St.BoxLayout()
  label = new St.Label({
    text: '$ ---',
    style_class: 'currency-rate'
  })
  button = new St.Bin({
    style_class: 'panel-button',
    reactive: true,
    can_focus: true,
    x_fill: true,
    y_fill: false,
    track_hover: true
  })

  button.set_child(label)
  layout.add(button, 0)

  update()
}

function enable() {
  Main.panel._centerBox.insert_child_at_index(layout, 2)
}

function disable() {
  Main.panel._centerBox.remove_child(layout)
}
