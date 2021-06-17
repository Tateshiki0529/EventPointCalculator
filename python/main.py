import wx, math, sys, os, configparser, time, datetime, webbrowser
from distutils.version import LooseVersion
from requests import get

versusContPointList = [60, 52, 44, 37, 30]
APPVERSION = "2.1.0"
lastUpdated = 0
eventTypeList = {
	"challenge_live": "チャレンジライブイベント",
	"vs_live": "対バンライブイベント",
	"live_goals": "ライブトライ！イベント",
	"mission_live": "ミッションライブイベント"
}
eventTypeIndexList = {
	"challenge_live": 0,
	"vs_live": 1,
	"live_goals": 2,
	"mission_live": 3
}

def updateCheck(e):
	url = "https://raw.githubusercontent.com/Tateshiki0529/EventPointCalculator/main/AppVersion.json"
	versionData = get(url).json()
	if LooseVersion(APPVERSION) < LooseVersion(versionData["Version"]["WindowsApp"]):
		ret = wx.MessageBox(u"アプリのアップデートがあります。\n\n現在のアプリのバージョン: "+APPVERSION+"\n最新のバージョン: "+versionData["Version"]["AppVersion"]+"\n\nアップデートリリースページへアクセスしますか？", u"EventPointCalculator", wx.YES_NO)
		if ret == wx.YES:
			webbrowser.open(versionData["UpdateURL"]["WindowsApp"])
	else:
		if e is not None:
			wx.MessageBox(u"利用中のバージョン("+APPVERSION+")は最新です。", u"EventPointCalculator")

def reloadNowEventInfo():
	global lastUpdated
	url = "https://bandori.party/api/events/"
	eventData = get(url).json()
	lastUpdated = int(time.time())
	return eventData

def reloadNowEventInfoShow(e):
	global lastUpdated
	global eventTypeList
	global eventTypeIndexList
	if time.time() - lastUpdated > 300:
		eventData = reloadNowEventInfo()["results"][0]

		lastUpdated = int(time.time())
		eventStartDate = (datetime.datetime.strptime(eventData["start_date"], "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(hours=9)).strftime("%Y/%m/%d %H:%M:%S")
		eventEndDate = (datetime.datetime.strptime(eventData["end_date"], "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(hours=9)).strftime("%Y/%m/%d %H:%M:%S")
		labelEventTitle.SetLabel("イベントタイトル: "+eventData["japanese_name"])
		labelEventDuration.SetLabel("イベント期間: "+eventStartDate+" ～ "+eventEndDate)
		labelEventType.SetLabel("イベントタイプ: "+eventTypeList[eventData["i_type"]])
		labelEventDataLastUpdated.SetLabel("最終更新日時: "+datetime.datetime.fromtimestamp(lastUpdated).strftime("%Y/%m/%d %H:%M:%S"))
		calcPanelEventDataResultPanel.Layout()
		calcPanelEventTypeListbox.SetSelection(eventTypeIndexList[eventData["i_type"]])
		if eventData["i_type"] == "challenge_live":
			calcPanelLiveTypeListbox.SetSelection(0)
		selectEventType(calcPanelEventTypeListbox)
		if e is not None:
			wx.MessageBox(u"情報を更新しました。", u"EventPointCalculator")
	else:
		wx.MessageBox(u"更新は5分ごとしかできません。", u"EventPointCalculator", wx.ICON_EXCLAMATION)

def selectEventType(e):
	eventType = calcPanelEventTypeListbox.GetClientData(calcPanelEventTypeListbox.GetSelection())
	eventPanelVisibleToggle(eventType)
	if eventType == "challenge":
		calcPanelLiveTypeListbox.Clear()
		calcPanelLiveTypeListbox.Append("フリーライブ", "free")
		calcPanelLiveTypeListbox.Append("チャレンジライブ(Beta)", "challenge")
		calcPanelLiveTypeListbox.Enable()
	elif eventType == "versus":
		calcPanelLiveTypeListbox.Clear()
		calcPanelLiveTypeListbox.Append("⚠ 対応していません! ⚠", None)
		calcPanelLiveTypeListbox.Disable()
	elif eventType == "livetry":
		calcPanelLiveTypeListbox.Clear()
		calcPanelLiveTypeListbox.Append("⚠ 対応していません! ⚠", None)
		calcPanelLiveTypeListbox.Disable()
	elif eventType == "mission":
		calcPanelLiveTypeListbox.Clear()
		calcPanelLiveTypeListbox.Append("⚠ 対応していません! ⚠", None)
		calcPanelLiveTypeListbox.Disable()
	calcPanel.Layout()

def selectLiveType(e):
	obj = e.GetEventObject()
	eventType = obj.GetClientData(obj.GetSelection())
	calculate(None)

def calculate(e):
	eventType = calcPanelEventTypeListbox.GetClientData(calcPanelEventTypeListbox.GetSelection())
	itemEmpty = False

	if eventType == "challenge":
		try:
			liveType = calcPanelLiveTypeListbox.GetClientData(calcPanelLiveTypeListbox.GetSelection())
			eventPoint = calcPanelChallengeEventPointInput.GetValue()
			if liveType == "free":
				scoreMin = (eventPoint - 20) * 25000
				scoreMax = scoreMin + 24999
			elif liveType == "challenge":
				scoreMin = eventPoint - 1000
				scoreMin *= 300
				scoreMax = scoreMin + 24999
			resultPanelCalcOutput.SetValue("{:,}".format(scoreMin)+" ～ "+"{:,}".format(scoreMax))
		except wx._core.wxAssertionError:
			itemEmpty = True
			resultPanelCalcOutput.SetValue("入力が不足しています")
	elif eventType == "versus":
		try:
			eventPoint = calcPanelVersusEventPointInput.GetValue()
			contributePoint = calcPanelVersusContributePointOutput.GetValue()
			scoreMin = (eventPoint - contributePoint) * 5500
			scoreMax = scoreMin + 5499
			resultPanelCalcOutput.SetValue("{:,}".format(scoreMin)+" ～ "+"{:,}".format(scoreMax))
		except wx._core.wxAssertionError:
			itemEmpty = True
			resultPanelCalcOutput.SetValue("入力が不足しています")
	elif eventType == "livetry":
		try:
			eventPoint = calcPanelLiveTryEventPointInput.GetValue()
			scoreMin = (eventPoint - 40) * 13000
			scoreMax = scoreMin + 12999
			resultPanelCalcOutput.SetValue("{:,}".format(scoreMin)+" ～ "+"{:,}".format(scoreMax))
		except wx._core.wxAssertionError:
			itemEmpty = True
			resultPanelCalcOutput.SetValue("入力が不足しています")
	elif eventType == "mission":
		try:
			eventPoint = calcPanelMissionEventPointInput.GetValue()
			SBPower = calcPanelMissionSBPowerInput.GetValue()
			scoreMin = (eventPoint - 40 - math.floor(SBPower / 3000)) * 10000
			scoreMax = scoreMin + 9999
			resultPanelCalcOutput.SetValue("{:,}".format(scoreMin)+" ～ "+"{:,}".format(scoreMax))
		except wx._core.wxAssertionError:
			itemEmpty = True
			resultPanelCalcOutput.SetValue("入力が不足しています")
	if itemEmpty == False and scoreMax < 0:
		resultPanelCalcOutput.AppendText(" (調整不可)")
def eventPanelVisibleToggle(eventType):
	calcPanelChallengeEventPanel.Hide()
	calcPanelVersusEventPanel.Hide()
	calcPanelLiveTryEventPanel.Hide()
	calcPanelMissionEventPanel.Hide()
	if eventType == "challenge":
		calcPanelChallengeEventPanel.Show()
	elif eventType == "versus":
		calcPanelVersusEventPanel.Show()
	elif eventType == "livetry":
		calcPanelLiveTryEventPanel.Show()
	elif eventType == "mission":
		calcPanelMissionEventPanel.Show()
	calcPanel.Layout()

def changeCPParticipantsCount(e):
	participantsCount = calcPanelVersusContributePointParticipantsCount.GetClientData(calcPanelVersusContributePointParticipantsCount.GetSelection())
	if participantsCount == 2:
		calcPanelVersusContributePointRankListbox.Clear()
		calcPanelVersusContributePointRankListbox.Append("1位", 3)
		calcPanelVersusContributePointRankListbox.Append("2位", 4)
	elif participantsCount == 3:
		calcPanelVersusContributePointRankListbox.Clear()
		calcPanelVersusContributePointRankListbox.Append("1位", 2)
		calcPanelVersusContributePointRankListbox.Append("2位", 3)
		calcPanelVersusContributePointRankListbox.Append("3位", 4)
	elif participantsCount == 4:
		calcPanelVersusContributePointRankListbox.Clear()
		calcPanelVersusContributePointRankListbox.Append("1位", 1)
		calcPanelVersusContributePointRankListbox.Append("2位", 2)
		calcPanelVersusContributePointRankListbox.Append("3位", 3)
		calcPanelVersusContributePointRankListbox.Append("4位", 4)
	elif participantsCount == 5:
		calcPanelVersusContributePointRankListbox.Clear()
		calcPanelVersusContributePointRankListbox.Append("1位", 0)
		calcPanelVersusContributePointRankListbox.Append("2位", 1)
		calcPanelVersusContributePointRankListbox.Append("3位", 2)
		calcPanelVersusContributePointRankListbox.Append("4位", 3)
		calcPanelVersusContributePointRankListbox.Append("5位", 4)
	calcPanelVersusContributePointRankListbox.SetSelection(0)
	calcPanelVersusContributePointOutput.SetValue(versusContPointList[0])
	calcPanelVersusContributePointEventPanel.Layout()
	calcPanelVersusEventPanel.Layout()
	calculate(None)

def calculateCP(e):
	participantsCount = calcPanelVersusContributePointParticipantsCount.GetClientData(calcPanelVersusContributePointParticipantsCount.GetSelection())
	try:
		pointIndex = calcPanelVersusContributePointRankListbox.GetClientData(calcPanelVersusContributePointRankListbox.GetSelection())
	except wx._core.wxAssertionError:
		pointIndex = 0
	calcPanelVersusContributePointOutput.SetValue(versusContPointList[pointIndex])
	calcPanelVersusContributePointEventPanel.Layout()
	calcPanelVersusEventPanel.Layout()
	calculate(None)

def urlClick1(e):
	if e.LeftUp():
		webbrowser.open("https://twitter.com/@T_BanGDreamer")
	e.Skip()

def urlClick2(e):
	if e.LeftUp():
		webbrowser.open("https://gbp.epcalc.ml/")
	e.Skip()

def resourcePath(path):
	if hasattr(sys, '_MEIPASS'):
		return os.path.join(sys._MEIPASS, path)
	return os.path.join(os.path.abspath("."), path)

def loadConfig():
	if (os.path.isfile(".\\EventPointCalculator.ini")):
		config = configparser.ConfigParser()
		config.read("./EventPointCalculator.ini")
		return config
	else:
		wx.MessageBox(u"コンフィグファイルがありません。自動作成します。", u"EventPointCalculator")
		config = configparser.RawConfigParser()
		config.add_section("Settings")
		config.set("Settings", "EventAutoload", True)
		config.set("Settings", "AppUpdateCheck", False)

		with open(".\\EventPointCalculator.ini", "w") as f:
			config.write(f)

def saveConfig(e):
	config = configparser.RawConfigParser()
	config.add_section("Settings")
	config.set("Settings", "EventAutoload", settingPanelEventAutoloadCheckbox.GetValue())
	config.set("Settings", "AppUpdateCheck", settingPanelAppAutoUpdateCheckCheckbox.GetValue())

	with open(".\\EventPointCalculator.ini", "w") as f:
		config.write(f)
	
	wx.MessageBox(u"設定を保存しました。", u"EventPointCalculator")

if __name__ == "__main__":
	app = wx.App()
	config = loadConfig()
	frame = wx.Frame(None, wx.ID_ANY, "EventPointCalculator for Python", size=(532, 450), style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.MINIMIZE_BOX)
	frame.CreateStatusBar()
	frame.SetStatusText('EventPointCalculator Ready.')

	notebook = wx.Notebook(frame, wx.ID_ANY)

	# 計算ページ (ここから)
	
	# ページパネル (親: notebook)
	pagePanelCalc = wx.Panel(notebook, wx.ID_ANY)

	# 計算パラメータ等入力パネル (親: pagePanelCalc)
	calcPanel = wx.Panel(pagePanelCalc, wx.ID_ANY)
	calcPanel.SetBackgroundColour("#fff")
	
	# イベントタイプ選択用パネル (親: calcPanel)
	calcPanelEventTypePanel = wx.Panel(calcPanel, wx.ID_ANY)

	# イベントタイプ選択用リストボックス (親: calcPanelEventTypePanel)
	calcPanelEventTypeListbox = wx.ListBox(calcPanelEventTypePanel, wx.ID_ANY, style=wx.LB_SINGLE)
	calcPanelEventTypeListbox.Append("チャレンジライブイベント", "challenge")
	calcPanelEventTypeListbox.Append("対バンライブイベント", "versus")
	calcPanelEventTypeListbox.Append("ライブトライ！イベント", "livetry")
	calcPanelEventTypeListbox.Append("ミッションライブイベント", "mission")
	calcPanelEventTypeListbox.Bind(wx.EVT_LISTBOX, selectEventType)
	
	# ライブ種別選択用リストボックス (親: calcPanelEventTypePanel)
	calcPanelLiveTypeListbox = wx.ListBox(calcPanelEventTypePanel, wx.ID_ANY, style=wx.LB_SINGLE)
	calcPanelLiveTypeListbox.Append("⚠ イベントタイプを指定してください! ⚠", None)
	calcPanelLiveTypeListbox.Bind(wx.EVT_LISTBOX, selectLiveType)

	# イベントタイプ選択用パネル構成レイアウト (親: calcPanelEventTypePanel)
	calcPanelEventTypeLayout = wx.BoxSizer(wx.VERTICAL)
	calcPanelEventTypeLayout.Add(wx.StaticText(calcPanelEventTypePanel, wx.ID_ANY, "イベント種別"))
	calcPanelEventTypeLayout.Add(calcPanelEventTypeListbox, flag=wx.EXPAND | wx.ALL, border=3)
	calcPanelEventTypeLayout.Add(wx.StaticText(calcPanelEventTypePanel, wx.ID_ANY, "ライブ種別"))
	calcPanelEventTypeLayout.Add(calcPanelLiveTypeListbox, flag=wx.EXPAND | wx.ALL, border=3)

	calcPanelEventDataResultPanel = wx.Panel(calcPanelEventTypePanel, wx.ID_ANY)

	labelEventTitle = wx.StaticText(calcPanelEventDataResultPanel, wx.ID_ANY, "イベントタイトル: ------")
	labelEventDuration = wx.StaticText(calcPanelEventDataResultPanel, wx.ID_ANY, "イベント期間: ----/--/-- --:--:-- ～ ----/--/-- --:--:--")
	labelEventType = wx.StaticText(calcPanelEventDataResultPanel, wx.ID_ANY, "イベントタイプ: ------")
	labelEventDataLastUpdated = wx.StaticText(calcPanelEventDataResultPanel, wx.ID_ANY, "最終更新日時: ----/--/-- --:--:--")

	calcPanelEventDataResultLayout = wx.StaticBoxSizer(wx.StaticBox(calcPanelEventDataResultPanel, wx.ID_ANY, "イベント情報取得結果"), wx.VERTICAL)
	calcPanelEventDataResultLayout.Add(wx.StaticText(calcPanelEventDataResultPanel, wx.ID_ANY, "現在開催されているイベント: "))
	calcPanelEventDataResultLayout.Add(labelEventTitle)
	calcPanelEventDataResultLayout.Add(labelEventDuration)
	calcPanelEventDataResultLayout.Add(labelEventType)
	calcPanelEventDataResultLayout.Add(wx.StaticText(calcPanelEventDataResultPanel, wx.ID_ANY, ""))
	calcPanelEventDataResultLayout.Add(labelEventDataLastUpdated)
		
	calcPanelEventDataResultPanel.SetSizer(calcPanelEventDataResultLayout)

	calcPanelEventTypeLayout.Add(calcPanelEventDataResultPanel)

	calcPanelEventReloadButton = wx.Button(calcPanelEventTypePanel, wx.ID_ANY, "情報を更新する")
	calcPanelEventReloadButton.Bind(wx.EVT_BUTTON, reloadNowEventInfoShow)
	calcPanelEventTypeLayout.Add(calcPanelEventReloadButton, flag=wx.ALIGN_RIGHT | wx.ALL, border=5)

	calcPanelEventTypePanel.SetSizer(calcPanelEventTypeLayout)

	# ------------------------------

	# チャレンジライブイベント用パラメータ入力パネル (親: calcPanel)
	calcPanelChallengeEventPanel = wx.Panel(calcPanel, wx.ID_ANY)

	# チャレンジライブイベント用目標ポイント入力ボックス (親: calcPanelChallengeEventPanel)
	calcPanelChallengeEventPointInput = wx.SpinCtrl(calcPanelChallengeEventPanel, wx.ID_ANY)
	calcPanelChallengeEventPointInput.Bind(wx.EVT_SPINCTRL, calculate)
	calcPanelChallengeEventPointInput.SetMax(100000)
	calcPanelChallengeEventPointInput.SetMin(0)

	# チャレンジライブイベント用パラメータ入力パネル構成レイアウト (親: calcPanelChallengeEventPanel)
	calcPanelChallengeEventLayout = wx.BoxSizer(wx.VERTICAL)
	calcPanelChallengeEventLayout.Add(wx.StaticText(calcPanelChallengeEventPanel, wx.ID_ANY, "欲しいイベントポイント数"))
	calcPanelChallengeEventLayout.Add(calcPanelChallengeEventPointInput, flag=wx.EXPAND | wx.ALL, border=3)

	calcPanelChallengeEventPanel.SetSizer(calcPanelChallengeEventLayout)

	# -------------------------------------

	# 対バンライブイベント用パラメータ入力パネル (親: calcPanel)
	calcPanelVersusEventPanel = wx.Panel(calcPanel, wx.ID_ANY)

	# 対バンライブイベント用目標ポイント入力ボックス (親: calcPanelVersusEventPanel)
	calcPanelVersusEventPointInput = wx.SpinCtrl(calcPanelVersusEventPanel, wx.ID_ANY)
	calcPanelVersusEventPointInput.Bind(wx.EVT_SPINCTRL, calculate)
	calcPanelVersusEventPointInput.SetMax(100000)
	calcPanelVersusEventPointInput.SetMin(0)

	# ----------------

	# 対バンライブ貢献度ポイント計算パネル (親: calcPanelVersusEventPanel)
	calcPanelVersusContributePointEventPanel = wx.Panel(calcPanelVersusEventPanel, wx.ID_ANY)

	# 対バンライブ貢献ポイント計算用参加人数入力ボックス (親: calcPanelVersusContributePointEventPanel)
	calcPanelVersusContributePointParticipantsCount = wx.ListBox(calcPanelVersusContributePointEventPanel, wx.ID_ANY)
	calcPanelVersusContributePointParticipantsCount.Bind(wx.EVT_LISTBOX, changeCPParticipantsCount)
	calcPanelVersusContributePointParticipantsCount.Append("2人", 2)
	calcPanelVersusContributePointParticipantsCount.Append("3人", 3)
	calcPanelVersusContributePointParticipantsCount.Append("4人", 4)
	calcPanelVersusContributePointParticipantsCount.Append("5人", 5)
	calcPanelVersusContributePointParticipantsCount.SetSelection(3)

	# 対バンライブ貢献ポイント計算用貢献順位入力ボックス (親: calcPanelVersusContributePointEventPanel)
	calcPanelVersusContributePointRankListbox = wx.ListBox(calcPanelVersusContributePointEventPanel, wx.ID_ANY)
	calcPanelVersusContributePointRankListbox.Bind(wx.EVT_LISTBOX, calculateCP)
	calcPanelVersusContributePointRankListbox.Append("1位", 0)
	calcPanelVersusContributePointRankListbox.Append("2位", 1)
	calcPanelVersusContributePointRankListbox.Append("3位", 2)
	calcPanelVersusContributePointRankListbox.Append("4位", 3)
	calcPanelVersusContributePointRankListbox.Append("5位", 4)
	calcPanelVersusContributePointRankListbox.SetSelection(0)

	# 対バンライブ貢献ポイント表示ボックス (親: calcPanelVersusContributePointEventPanel)
	calcPanelVersusContributePointOutput = wx.SpinCtrl(calcPanelVersusContributePointEventPanel, wx.ID_ANY)
	calcPanelVersusContributePointOutput.Bind(wx.EVT_SPINCTRL, calculate)
	calcPanelVersusContributePointOutput.SetMin(30)
	calcPanelVersusContributePointOutput.SetMax(60)
	calcPanelVersusContributePointOutput.SetValue(60)
	calcPanelVersusContributePointOutput.Disable()

	# 対バンライブ貢献度ポイント計算パネル構成レイアウト (親: calcPanelVersusContributePointEventPanel)
	calcPanelVersusContributePointEventBox = wx.StaticBox(calcPanelVersusContributePointEventPanel, wx.ID_ANY, "貢献度ポイント関係")

	calcPanelVersusContributePointEventLayout = wx.StaticBoxSizer(calcPanelVersusContributePointEventBox, wx.VERTICAL)
	calcPanelVersusContributePointEventLayout.Add(wx.StaticText(calcPanelVersusContributePointEventPanel, wx.ID_ANY, "参加人数"))
	calcPanelVersusContributePointEventLayout.Add(calcPanelVersusContributePointParticipantsCount, flag=wx.EXPAND | wx.ALL, border=2)
	calcPanelVersusContributePointEventLayout.Add(wx.StaticText(calcPanelVersusContributePointEventPanel, wx.ID_ANY, "貢献度ランキング"))
	calcPanelVersusContributePointEventLayout.Add(calcPanelVersusContributePointRankListbox, flag=wx.EXPAND | wx.ALL, border=2)
	calcPanelVersusContributePointEventLayout.Add(wx.StaticText(calcPanelVersusContributePointEventPanel, wx.ID_ANY, "参加人数"))
	calcPanelVersusContributePointEventLayout.Add(wx.StaticLine(calcPanelVersusContributePointEventPanel), flag=wx.GROW)
	calcPanelVersusContributePointEventLayout.Add(wx.StaticText(calcPanelVersusContributePointEventPanel, wx.ID_ANY, "貢献度ポイント"))
	calcPanelVersusContributePointEventLayout.Add(calcPanelVersusContributePointOutput, flag=wx.EXPAND | wx.ALL, border=2)

	calcPanelVersusContributePointEventPanel.SetSizer(calcPanelVersusContributePointEventLayout)

	# ----------------

	# 対バンライブイベント用パラメータ入力パネル構成レイアウト (親: calcPanelVersusEventPanel)
	calcPanelVersusEventLayout = wx.BoxSizer(wx.VERTICAL)
	calcPanelVersusEventLayout.Add(wx.StaticText(calcPanelVersusEventPanel, wx.ID_ANY, "欲しいイベントポイント数"))
	calcPanelVersusEventLayout.Add(calcPanelVersusEventPointInput, flag=wx.EXPAND | wx.ALL, border=3)
	calcPanelVersusEventLayout.Add(calcPanelVersusContributePointEventPanel,  flag=wx.EXPAND | wx.ALL, border=3)

	calcPanelVersusEventPanel.SetSizer(calcPanelVersusEventLayout)

	# -------------------------------

	# ミッションライブイベント用パラメータ入力パネル (親: calcPanel)
	calcPanelMissionEventPanel = wx.Panel(calcPanel, wx.ID_ANY)

	# ミッションライブイベント用目標ポイント入力ボックス (親: calcPanelMissionEventPanel)
	calcPanelMissionEventPointInput = wx.SpinCtrl(calcPanelMissionEventPanel, wx.ID_ANY)
	calcPanelMissionEventPointInput.Bind(wx.EVT_SPINCTRL, calculate)
	calcPanelMissionEventPointInput.SetMax(100000)
	calcPanelMissionEventPointInput.SetMin(0)

	# ----------------

	# ミッションライブイベントSB総合力入力パネル (親: calcPanelMissionEventPanel)
	calcPanelMissionSBPowerInputPanel = wx.Panel(calcPanelMissionEventPanel, wx.ID_ANY)

	# ミッションライブイベントSB総合力入力ボックス (親: calcPanelMissionSBPowerInputPanel)
	calcPanelMissionSBPowerInput = wx.SpinCtrl(calcPanelMissionSBPowerInputPanel, wx.ID_ANY)
	calcPanelMissionSBPowerInput.Bind(wx.EVT_SPINCTRL, calculate)
	calcPanelMissionSBPowerInput.SetMin(0)
	calcPanelMissionSBPowerInput.SetMax(1000000)
	calcPanelMissionSBPowerInput.SetValue(150000)

	# ミッションライブイベントSB総合力入力パネル構成レイアウト (親: calcPanelMissionSBPowerInputPanel)
	calcPanelMissionSBPowerInputBox = wx.StaticBox(calcPanelMissionSBPowerInputPanel, wx.ID_ANY, "SB総合力")

	calcPanelMissionSBPowerInputLayout = wx.StaticBoxSizer(calcPanelMissionSBPowerInputBox, wx.VERTICAL)
	calcPanelMissionSBPowerInputLayout.Add(wx.StaticText(calcPanelMissionSBPowerInputPanel, wx.ID_ANY, "サポートバンドの総合力"))
	calcPanelMissionSBPowerInputLayout.Add(calcPanelMissionSBPowerInput, flag=wx.EXPAND | wx.ALL, border=2)

	calcPanelMissionSBPowerInputPanel.SetSizer(calcPanelMissionSBPowerInputLayout)

	# ----------------

	# ミッションライブイベント用パラメータ入力パネル構成レイアウト (親: calcPanelMissionEventPanel)
	calcPanelMissionEventLayout = wx.BoxSizer(wx.VERTICAL)
	calcPanelMissionEventLayout.Add(wx.StaticText(calcPanelMissionEventPanel, wx.ID_ANY, "欲しいイベントポイント数"))
	calcPanelMissionEventLayout.Add(calcPanelMissionEventPointInput, flag=wx.EXPAND | wx.ALL, border=5)
	calcPanelMissionEventLayout.Add(calcPanelMissionSBPowerInputPanel,  flag=wx.EXPAND | wx.ALL, border=3)

	calcPanelMissionEventPanel.SetSizer(calcPanelMissionEventLayout)

	# -------------------------------

	# ライブトライ！イベント用パラメータ入力パネル (親: calcPanel)
	calcPanelLiveTryEventPanel = wx.Panel(calcPanel, wx.ID_ANY)

	# ライブトライ！イベント用目標ポイント入力ボックス (親: calcPanelLiveTryEventPanel)
	calcPanelLiveTryEventPointInput = wx.SpinCtrl(calcPanelLiveTryEventPanel, wx.ID_ANY)
	calcPanelLiveTryEventPointInput.Bind(wx.EVT_SPINCTRL, calculate)
	calcPanelLiveTryEventPointInput.SetMax(100000)
	calcPanelLiveTryEventPointInput.SetMin(0)

	# ライブトライ！イベント用パラメータ入力パネル構成レイアウト (親: calcPanelLiveTryEventPanel)
	calcPanelLiveTryEventLayout = wx.BoxSizer(wx.VERTICAL)
	calcPanelLiveTryEventLayout.Add(wx.StaticText(calcPanelLiveTryEventPanel, wx.ID_ANY, "欲しいイベントポイント数"))
	calcPanelLiveTryEventLayout.Add(calcPanelLiveTryEventPointInput, flag=wx.EXPAND | wx.ALL, border=3)

	calcPanelLiveTryEventPanel.SetSizer(calcPanelLiveTryEventLayout)

	# -------------------------------

	# 計算パラメータ等入力パネル構成レイアウト (親: calcPanel)
	calcPanelBox = wx.StaticBox(calcPanel, wx.ID_ANY, "パラメータ")

	calcPanelLayout = wx.StaticBoxSizer(calcPanelBox, wx.HORIZONTAL)
	calcPanelLayout.Add(calcPanelEventTypePanel)
	calcPanelLayout.Add(calcPanelChallengeEventPanel)
	calcPanelLayout.Add(calcPanelVersusEventPanel)
	calcPanelLayout.Add(calcPanelLiveTryEventPanel)
	calcPanelLayout.Add(calcPanelMissionEventPanel)

	calcPanel.SetSizer(calcPanelLayout)

	# ライブ種別リストボックス無効化
	calcPanelLiveTypeListbox.Disable()

	# 全入力パネルを隠す
	calcPanelChallengeEventPanel.Hide()
	calcPanelVersusEventPanel.Hide()
	calcPanelLiveTryEventPanel.Hide()
	calcPanelMissionEventPanel.Hide()
	calcPanel.Layout()

	# 計算結果表示パネル (親: pagePanelCalc)
	resultPanel = wx.Panel(pagePanelCalc, wx.ID_ANY)
	resultPanel.SetBackgroundColour("#fff")

	# 計算結果テキスト表示ボックス (親: resultPanel)
	resultPanelCalcOutput = wx.TextCtrl(resultPanel, wx.ID_ANY, "入力待ち…", style=wx.TE_CENTER, size=(250, -1))

	# 計算結果表示パネル構成レイアウト (親: resultPanel)
	resultPanelBox = wx.StaticBox(resultPanel, wx.ID_ANY, "計算結果")
	resultPanelLayout = wx.StaticBoxSizer(resultPanelBox, wx.HORIZONTAL)
	resultPanelLayout.Add(wx.StaticText(resultPanel, wx.ID_ANY, "獲得すべきライブスコア: "), flag=wx.GROW | wx.EXPAND | wx.TOP | wx.LEFT, border=6)
	resultPanelLayout.Add(resultPanelCalcOutput, flag=wx.GROW | wx.EXPAND | wx.TOP | wx.BOTTOM, border=3)

	resultPanel.SetSizer(resultPanelLayout)

	# ページパネル構成レイアウト (親: pagePanelCalc)
	pagePanelCalcLayout = wx.FlexGridSizer(rows=2, cols=1, gap=(0, 0))
	pagePanelCalcLayout.Add(calcPanel, proportion=1, flag=wx.GROW | wx.EXPAND | wx.ALL, border=7)
	pagePanelCalcLayout.Add(resultPanel, proportion=1, flag=wx.GROW | wx.EXPAND | wx.ALL, border=7)
	pagePanelCalcLayout.AddGrowableRow(0)
	pagePanelCalcLayout.AddGrowableCol(0)

	pagePanelCalc.SetSizer(pagePanelCalcLayout)
	# 計算ページ (ここまで)

	# 概要ページ (ここから)
	pagePanelAbout = wx.Panel(notebook, wx.ID_ANY)

	pagePanelAboutLayout = wx.BoxSizer(wx.VERTICAL)
	aboutPanelUrlTextTwitter = wx.StaticText(pagePanelAbout, wx.ID_ANY, "by @T_BanGDreamer")
	aboutPanelUrlTextTwitter.Bind(wx.EVT_MOUSE_EVENTS, urlClick1)
	aboutPanelUrlTextTwitter.Bind(wx.EVT_MOTION, urlClick1)
	font = wx.Font(8, wx.DEFAULT, wx.ITALIC, wx.FONTWEIGHT_LIGHT, True)
	aboutPanelUrlTextTwitter.SetFont(font)
	aboutPanelUrlTextTwitter.SetForegroundColour('#0000ff')
	aboutPanelUrlTextWeb = wx.StaticText(pagePanelAbout, wx.ID_ANY, "https://gbp.epcalc.ml/")
	aboutPanelUrlTextWeb.Bind(wx.EVT_MOUSE_EVENTS, urlClick2)
	aboutPanelUrlTextWeb.Bind(wx.EVT_MOTION, urlClick2)
	font2 = wx.Font(8, wx.DEFAULT, wx.ITALIC, wx.FONTWEIGHT_LIGHT, True)
	aboutPanelUrlTextWeb.SetFont(font2)
	aboutPanelUrlTextWeb.SetForegroundColour('#0000ff')
	for i in range(0, 9):
		pagePanelAboutLayout.Add(wx.StaticText(pagePanelAbout, wx.ID_ANY, ""))
	pagePanelAboutLayout.Add(wx.StaticText(pagePanelAbout, wx.ID_ANY, "EventPointCalculator for Python v"+APPVERSION), flag=wx.ALIGN_CENTER, border=3)
	pagePanelAboutLayout.Add(aboutPanelUrlTextTwitter, flag=wx.ALIGN_CENTER, border=3)
	pagePanelAboutLayout.Add(wx.StaticText(pagePanelAbout, wx.ID_ANY, ""))
	pagePanelAboutLayout.Add(aboutPanelUrlTextWeb, flag=wx.ALIGN_CENTER, border=3)
	pagePanelAboutLayout.Add(wx.StaticText(pagePanelAbout, wx.ID_ANY, ""))

	aboutPanelUpdateCheckButton = wx.Button(pagePanelAbout, wx.ID_ANY, "更新を確認する")
	aboutPanelUpdateCheckButton.Bind(wx.EVT_BUTTON, updateCheck)
	pagePanelAboutLayout.Add(aboutPanelUpdateCheckButton, flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
	pagePanelAbout.SetSizer(pagePanelAboutLayout)

	# 概要ページ (ここまで)

	# 設定ページ (ここから)
	pagePanelSetting = wx.Panel(notebook, wx.ID_ANY)

	# イベント自動取得設定パネル (親: pagePanelSetting)
	settingPanelEventAutoloadPanel = wx.Panel(pagePanelSetting, wx.ID_ANY)

	# イベント自動取得設定チェックボックス (親: settingPanelEventAutoloadPanel)
	settingPanelEventAutoloadCheckbox = wx.CheckBox(settingPanelEventAutoloadPanel, wx.ID_ANY, " 起動時にイベント情報を自動で取得し反映する")

	# アプリ更新自動取得設定チェックボックス (親: settingPanelEventAutoloadPanel)
	settingPanelAppAutoUpdateCheckCheckbox = wx.CheckBox(settingPanelEventAutoloadPanel, wx.ID_ANY, " 起動時にアプリの更新を確認する")

	# イベント自動取得設定パネルレイアウト (親: settingPanelEventAutoloadPanel)
	settingPanelEventAutoloadBox = wx.StaticBox(settingPanelEventAutoloadPanel, wx.ID_ANY, "自動更新設定")
	settingPanelEventAutoloadLayout = wx.StaticBoxSizer(settingPanelEventAutoloadBox, wx.VERTICAL)
	settingPanelEventAutoloadLayout.Add(settingPanelEventAutoloadCheckbox, flag=wx.ALL, border=5)
	settingPanelEventAutoloadLayout.Add(settingPanelAppAutoUpdateCheckCheckbox, flag=wx.ALL, border=5)

	settingPanelEventAutoloadPanel.SetSizer(settingPanelEventAutoloadLayout)

	# 設定保存ボタン (親: pagePanelSetting)
	settingPanelSaveButton = wx.Button(pagePanelSetting, wx.ID_ANY, "設定を保存する")
	settingPanelSaveButton.Bind(wx.EVT_BUTTON, saveConfig)
	
	# 設定ページレイアウト (親: pagePanelSetting)
	settingPanelLayout = wx.BoxSizer(wx.VERTICAL)
	settingPanelLayout.Add(settingPanelEventAutoloadPanel, flag=wx.EXPAND | wx.ALL, border=10)
	settingPanelLayout.Add(settingPanelSaveButton, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=10)

	pagePanelSetting.SetSizer(settingPanelLayout)

	# 設定ページ (ここまで)

	# 設定項目自動読み込み
	if config["Settings"]["EventAutoload"].lower() == "true":
		settingPanelEventAutoloadCheckbox.SetValue(True)
	else:
		settingPanelEventAutoloadCheckbox.SetValue(False)
	if config["Settings"]["AppUpdateCheck"].lower() == "true":
		settingPanelAppAutoUpdateCheckCheckbox.SetValue(True)
	else:
		settingPanelAppAutoUpdateCheckCheckbox.SetValue(False)

	notebook.InsertPage(0, pagePanelCalc, "計算")
	notebook.InsertPage(1, pagePanelSetting, "設定")
	notebook.InsertPage(2, pagePanelAbout, "このアプリについて")

	icon = wx.Icon(resourcePath('logo.ico'), wx.BITMAP_TYPE_ICO)
	frame.SetIcon(icon)

	# イベント自動取得設定確認
	if config["Settings"]["EventAutoload"].lower() == "true":
		reloadNowEventInfoShow(None)
	if config["Settings"]["AppUpdateCheck"].lower() == "true":
		updateCheck(None)
	
	frame.Show()
	app.MainLoop()