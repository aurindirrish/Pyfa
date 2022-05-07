# noinspection PyPackageRequirements
import wx

import config
import gui.mainFrame
from gui.bitmap_loader import BitmapLoader
from gui.preferenceView import PreferenceView
from service.esi import Esi
from service.settings import EsiSettings

# noinspection PyPackageRequirements
_t = wx.GetTranslation


class PFEsiPref(PreferenceView):

    def populatePanel(self, panel):
        self.title = _t("EVE SSO")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = EsiSettings.getInstance()
        self.dirtySettings = False
        dlgWidth = panel.GetParent().GetParent().ClientSize.width
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.stTitle = wx.StaticText(panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0)
        self.stTitle.Wrap(-1)
        self.stTitle.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))
        mainSizer.Add(self.stTitle, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticline1 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        self.stInfo = wx.StaticText(panel, wx.ID_ANY,
                                    _t("Please see the pyfa wiki on GitHub for information regarding these options."),
                                    wx.DefaultPosition, wx.DefaultSize, 0)
        self.stInfo.Wrap(dlgWidth - 50)
        mainSizer.Add(self.stInfo, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        rbSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.rbMode = wx.RadioBox(panel, -1, _t("Login Authentication Method"), wx.DefaultPosition, wx.DefaultSize,
                                  [_t('Local Server'), _t('Manual')], 1, wx.RA_SPECIFY_COLS)
        self.rbMode.SetItemToolTip(0, _t("This option starts a local webserver that EVE SSO Server will call back to"
                                         " with information about the character login."))
        self.rbMode.SetItemToolTip(1, _t("This option prompts users to copy and paste information to allow for"
                                         " character login. Use this if having issues with the local server."))

        self.rbMode.SetSelection(self.settings.get('loginMode'))

        rbSizer.Add(self.rbMode, 1, wx.TOP | wx.RIGHT, 5)

        self.rbMode.Bind(wx.EVT_RADIOBOX, self.OnModeChange)

        mainSizer.Add(rbSizer, 0, wx.ALL | wx.EXPAND, 0)

        esiSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.esiServer = wx.StaticText(panel, wx.ID_ANY, _t("Default SSO Server:"), wx.DefaultPosition,wx.DefaultSize, 0)

        self.esiServer.Wrap(-1)

        esiSizer.Add(self.esiServer, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.esiServer.SetToolTip(wx.ToolTip(_t('The source you choose will be used on connection.')))

        self.chESIserver = wx.Choice(panel, choices=list(self.settings.keys()))

        self.chESIserver.SetStringSelection(self.settings.get("server"))

        esiSizer.Add(self.chESIserver, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)

        mainSizer.Add(esiSizer, 0, wx.TOP | wx.RIGHT , 10)

        self.chESIserver.Bind(wx.EVT_CHOICE, self.OnServerChange)

        panel.SetSizer(mainSizer)

        panel.Layout()

    def OnTimeoutChange(self, event):
        self.settings.set('timeout', event.GetEventObject().GetValue())

    def OnModeChange(self, event):
        self.settings.set('loginMode', event.GetInt())

    def OnServerChange(self, event):
        source = self.chESIserver.GetString(self.chESIserver.GetSelection())
        esiService = Esi.getInstance()
        esiService.init(config.supported_servers[source])
        self.settings.set("server", source)

    def getImage(self):
        return BitmapLoader.getBitmap("eve", "gui")


PFEsiPref.register()